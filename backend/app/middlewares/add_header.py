from fastapi import Request


class AddHeader:
    def __init__(self):
        pass

    async def __call__(self, request: Request, call_next):
        response = await call_next(request)
        response.headers["Accept"] = "application/json, text/plain, */*"
        response.headers["Accept-Encoding"] = "gzip, deflate, br, zstd"
        response.headers["Accept-Language"] = "ja,en-US;q=0.9,en;q=0.8"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        return response
