import aioboto3
from botocore.exceptions import ClientError
from io import BytesIO
from typing import LiteralString, Any
import orjson
from functools import lru_cache

from config import settings
from exceptions import NotFoundError, InternalServerError
from .logger_util import logger


class S3KeyCacheMixin:
    @lru_cache()
    def get_rps_conf_key(self, rps_conf_id, version) -> str:
        return f"RPS_CONF/{rps_conf_id}/rps_conf_{rps_conf_id}_{version}.json"

    @lru_cache()
    def get_gen_conf_key(self, gen_conf_id, version) -> str:
        return f"GEN_CONF/{gen_conf_id}/gen_conf_{gen_conf_id}_{version}.json"

    @lru_cache()
    def get_gen_app_folder_key(self, gen_conf_id) -> str:
        return f"GEN_CONF/{gen_conf_id}/APPS/"

    @lru_cache()
    def get_job_app_folder_key(self, job_id) -> str:
        return f"JOB/{job_id}/APPS/"

    @lru_cache()
    def get_gen_app_key(self, gen_conf_id, filename) -> str:
        return f"GEN_CONF/{gen_conf_id}/APPS/{filename}"

    @lru_cache()
    def get_job_app_key(self, job_id, filename) -> str:
        return f"JOB/{job_id}/APPS/{filename}"

    @lru_cache()
    def get_job_json_key(self, job_id) -> str:
        return f"JOB/{job_id}/work.json"

    @lru_cache()
    def get_media_key(self, job_id, file_name) -> str:
        return f"JOB/{job_id}/DATA/{file_name}"

    @lru_cache()
    def get_media_folder_key(self, job_id) -> str:
        return f"JOB/{job_id}/DATA/"


class S3Client(S3KeyCacheMixin):
    UPLOAD_MAX_TRY_COUNT = 3

    def __init__(self):
        self.bucket = settings.S3_BUCKET
        self.s3_client = None
        self.operations_no_need_to_check_result = ["download_fileobj", "list_objects_v2"]
        self.operation_check_result_mapping = {"put_object": True, "delete_object": False}

    async def __aenter__(self):
        session = aioboto3.Session()
        self.s3_client = await session.client(
            's3',
            region_name=settings.S3_REGION
        ).__aenter__()
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        await self.s3_client.__aexit__(exc_type, exc_value, traceback)

    async def list_objects_in_s3(self, prefix: str) -> list[dict] | list[str]:
        response = await self._do_operation("list_objects_v2", prefix, Bucket=self.bucket, Prefix=prefix)
        return response

    async def put_job_content_to_s3(self, file: dict, key: str) -> None:
        try:
            file["key"] = key
            await self.put_object_to_s3(file["content"], key=key)
            file["upload_status"] = "y"
        except InternalServerError as e:  # put_object_to_s3 raises InternalServerError when failed in upload operation
            logger.error({"key": key, "error_detail": str(e)}, extra="put_job_content_to_s3")

    async def put_object_to_s3(self, bytes_io: bytes | dict | list, *, key: str = "") -> None:
        if not isinstance(bytes_io, bytes):
            bytes_io = orjson.dumps(bytes_io)

        await self._do_operation("put_object", key, Bucket=self.bucket, Key=key, Body=bytes_io)

    async def delete_object_from_s3(self, *, key: str = "") -> None:
        if not await self.check_file_exists(key):
            raise NotFoundError(f"file {key} not found in s3")

        await self._do_operation("delete_object", key, Bucket=self.bucket, Key=key)

    async def get_object_from_s3(self, key: str) -> BytesIO:
        if not await self.check_file_exists(key):
            raise NotFoundError(f"file {key} not found in s3")

        file_stream = BytesIO()
        await self._do_operation("download_fileobj", key, Bucket=self.bucket, Key=key, Fileobj=file_stream)

        file_stream.seek(0)  # reset pointer
        return file_stream

    async def get_object_contain_kw_from_s3(self, folder: str, kw: str) -> tuple[str, BytesIO]:
        files: list[str] = await self.list_objects_in_s3(folder)
        for file_name in files:
            if kw in file_name:
                return file_name, await self.get_object_from_s3(folder + file_name)
        else:
            raise NotFoundError("media file not found")

    async def _do_operation(self, func: LiteralString, key: str, *args, **kwargs) -> Any:
        logger.info({"key": key, "func": func}, extra="do_operation")

        # initiate operation result checking condition
        if func in self.operations_no_need_to_check_result:
            _check_answer = None
        else:
            _check_answer = self.operation_check_result_mapping[func]

        # loop to do operation
        for i in range(self.UPLOAD_MAX_TRY_COUNT):
            try:
                # do operation
                _operation = getattr(self.s3_client, func)
                res = await _operation(*args, **kwargs)

                # check the operation result and retry when failed
                if await self.check_operation_done(key, _check_answer):
                    logger.info({"status": "success", "s3_key": key, "try_count": i + 1}, extra=func)
                    return res
                else:
                    raise ClientError("check operation failed", func)

            except ClientError as e:
                logger.error({"status": "failed", "s3_key": key, "error_detail": str(e), "try_count": i + 1},
                             extra=func)

        # when max loop, return error
        else:
            raise InternalServerError(f"s3 operation {func} failed")

    async def check_operation_done(self, file_key: str, answer: bool | None) -> bool:
        # no need to check
        if answer is None:
            return True

        # check if the file's status after perform push/delete
        done = await self.check_file_exists(file_key) is answer
        logger.info({"key": file_key, "check_result": done}, extra="check_operation_done")
        return done

    async def check_file_exists(self, file_key: str) -> bool:
        try:
            meta_data = await self.s3_client.head_object(Bucket=settings.S3_BUCKET, Key=file_key)
            print(meta_data)
            logger.info({"status": "success", "s3_key": file_key}, extra="check_file_exists")
            return True
        except ClientError as e:
            if e.response['Error']['Code'] == '404':
                return False
            else:
                raise InternalServerError(str(e))
