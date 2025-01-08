from fastapi import status, HTTPException, Request
from datetime import timedelta, datetime, timezone
import os
import re
import time
import binascii
import base64
import hashlib
import jwt
import jwt.algorithms
from passlib.context import CryptContext
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization

from .crud_util import Session
from .logger_util import logger
from exceptions import DigestAuthError
from database import User
from config import settings
from custom_types import CurrentUser


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXP = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)


# region rsa encrypt
with open(f"{settings.SETTING.APP_FOLDER}/resources/{settings.SETTING.BUILD_ENV}/public_key.pem", "r", encoding="utf-8") as fp:
    RSA_PUBLIC_KEY = fp.read()


with open(f"{settings.SETTING.APP_FOLDER}/resources/{settings.SETTING.BUILD_ENV}/private_key.pem", "rb") as fp:
    RSA_PRIVATE_KEY = serialization.load_pem_private_key(
        fp.read(),
        password=None
    )


def decrypt_password(encrypted_password: bytes) -> str:
    decrypted = RSA_PRIVATE_KEY.decrypt(
        encrypted_password,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return decrypted.decode()
# endregion


# region login auth
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    to_encode.update({"exp": datetime.now(timezone.utc) + ACCESS_TOKEN_EXP})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def authenticate_user(username: str, encrypted_password: str) -> User | None:
    async with Session() as db:
        user = await db.get_user_by_user_name(username)
    if user is None:
        return None

    # password = decrypt_password(encrypted_password.encode())
    password = encrypted_password
    if not verify_password(password, user.hashed_password):
        return None
    return user
# endregion


# region digest auth
digest_credentials = {'admin': settings.HTTP_DIGEST_AUTH_PASSWORD}


async def authenticate_digest(request: Request):
    logger.info(
        {"step": "authenticate_digest_start", "request_app": request.client.host}, extra={"api_call": "digest_auth"})
    if not await DigestAuth(request).get_authenticated_user(check_credentials_func=digest_credentials.get, realm='Protected'):
        logger.info({"step": "authenticate_digest_end", "request_app": request.client.host, "status": "FAILED"},
                    extra={"api_call": "digest_auth"})
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Invalid authentication credentials",
                            headers={"WWW-Authenticate": "Digest"})
    logger.info({"step": "authenticate_digest_end", "request_app": request.client.host, "status": "passed"},
                extra={"api_call": "digest_auth"})


class DigestAuth(object):
    DIGEST_PRIVATE_KEY = b'secret-random'
    DIGEST_CHALLENGE_TIMEOUT_SECONDS = 60

    class SendChallenge(Exception):
        pass

    re_auth_hdr_parts = re.compile(
        '([^= ]+)'  # The key
        '='  # Conventional key/value separator (literal)
        '(?:'  # Group together a couple options
        '"([^"]*)"'  # A quoted string of length 0 or more
        '|'  # The other option in the group is coming
        '([^,]+)'  # An unquoted string of length 1 or more, up to a comma
        ')'  # That non-matching group ends
        ',?')  # There might be a comma at the end (none on last pair)

    def __init__(self, request):
        self.request = request

    async def get_authenticated_user(self, check_credentials_func, realm):
        try:
            return await self.authenticate_user(check_credentials_func)
        except self.SendChallenge:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="Invalid authentication credentials",
                                headers={'www-authenticate': self.create_auth_challenge(realm, self.request.client.host,
                                                                                        self.get_time())})

    async def authenticate_user(self, check_credentials_func):
        auth_header = self.request.headers.get("Authorization")
        if auth_header is None or not auth_header.startswith('Digest '):
            raise self.SendChallenge()

        params = self.parse_auth_header(auth_header)
        try:
            self.verify_params(params)
            self.verify_opaque(params['opaque'], params['nonce'], self.request.client.host)
        except DigestAuthError:
            raise self.SendChallenge()
        challenge = check_credentials_func(params['username'])
        if not challenge:
            raise self.SendChallenge()

        received_response = params['response']
        expected_response = await self.calculate_expected_response(challenge, params)

        if expected_response and received_response:
            if expected_response == received_response:
                logger.info({'current_user': params['username']}, extra={"api_call": "digest_auth"})
                return True
            else:
                raise self.SendChallenge()

        return False

    def parse_auth_header(self, hdr):
        items = self.re_auth_hdr_parts.findall(hdr)
        params = {}
        for key, bare, quoted in items:
            params[key.strip()] = (quoted or bare).strip()

        return params

    def create_auth_challenge(self, realm, clientip, time_):
        nonce = binascii.hexlify(os.urandom(12))
        opaque = self.create_opaque(nonce, clientip, time_)
        realm = realm.replace('\\', '\\\\').replace('"', '\\"')

        hdr = 'Digest algorithm="MD5", realm="%s", qop="auth", nonce="%s", opaque="%s"'
        return hdr % (realm, nonce.decode('ascii'), opaque.decode('ascii'))

    def create_opaque(self, nonce, clientip, now):
        key = (nonce, clientip.encode('ascii'), self.int_to_bytes(now))
        key = b','.join(key)

        ekey = base64.b64encode(key).replace(b'\n', b'')
        digest = self.hexdigest_bytes(key + self.DIGEST_PRIVATE_KEY)
        return b'-'.join((digest, ekey))

    @staticmethod
    def hexdigest_bytes(data):
        return binascii.hexlify(hashlib.md5(data).digest())

    @staticmethod
    def hexdigest_str(data):
        return hashlib.md5(data).hexdigest()

    @staticmethod
    def int_to_bytes(i):
        return ('%d' % i).encode('ascii')

    @staticmethod
    def get_time():
        return time.time()

    @staticmethod
    def verify_params(params):
        if not params.get('username'):
            raise DigestAuthError('Invalid response, no username given')

        if 'opaque' not in params:
            raise DigestAuthError('Invalid response, no opaque given')

        if 'nonce' not in params:
            raise DigestAuthError('Invalid response, no nonce given')

    def verify_opaque(self, opaque, nonce, clientip):
        try:
            received_digest, received_ekey = opaque.split('-')
        except ValueError:
            raise DigestAuthError('Invalid response, invalid opaque value')

        try:
            received_key = base64.b64decode(received_ekey).decode('ascii')
            received_nonce, received_clientip, received_time = received_key.split(',')
        except ValueError:
            raise DigestAuthError('Invalid response, invalid opaque value')

        if received_nonce != nonce:
            raise DigestAuthError('Invalid response, incompatible opaque/nonce values')

        if received_clientip != clientip:
            raise DigestAuthError('Invalid response, incompatible opaque/client values')

        try:
            received_time = int(received_time)
        except ValueError:
            raise DigestAuthError('Invalid response, invalid opaque/time values')

        expired = (time.time() - received_time) > self.DIGEST_CHALLENGE_TIMEOUT_SECONDS
        if expired:
            raise DigestAuthError('Invalid response, incompatible opaque/nonce too old')

        digest = self.hexdigest_str(received_key.encode('ascii') + self.DIGEST_PRIVATE_KEY)
        if received_digest != digest:
            raise DigestAuthError('Invalid response, invalid opaque value')

        return True

    async def calculate_expected_response(self, challenge, params):
        algo = params.get('algorithm', 'md5').lower()
        qop = params.get('qop', 'auth')
        user = params['username']
        realm = params['realm']
        nonce = params['nonce']
        nc = params['nc']
        cnonce = params['cnonce']

        print(user, challenge)
        ha1 = self.HA1(algo, user, realm, challenge, nonce, cnonce)
        request_body = await self.request.body()
        ha2 = self.HA2(self.request.method, self.request.url.path, qop, request_body.decode())

        data = (ha1, nonce, nc, cnonce, qop, ha2)
        return self.hexdigest_str(':'.join(data).encode('ascii'))

    def HA1(self, algorithm, username, realm, password, nonce, cnonce):
        data = ':'.join((username, realm, password))
        ha1 = self.hexdigest_str(data.encode('ascii'))

        if algorithm == 'md5-sess':
            data = ':'.join((ha1, nonce, cnonce))
            ha1 = self.hexdigest_str(data.encode('ascii'))

        return ha1

    def HA2(self, method, digest_uri, qop, body):
        data = [method, digest_uri]
        if qop and qop == 'auth-int':
            data.append(self.hexdigest_str(body))

        return self.hexdigest_str(':'.join(data).encode('ascii'))


def is_internal_user(user: CurrentUser) -> bool:
    return user.authority_code < 4


def is_external_user(user: CurrentUser) -> bool:
    return user.authority_code == 4


def is_admin(user: CurrentUser) -> bool:
    return user.authority_code == 0


def is_inactive(user: CurrentUser) -> bool:
    return user.authority_code == 99
# endregion
