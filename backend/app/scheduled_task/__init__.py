from httpx import AsyncClient

from utils import logger


async def retry_job():
    logger.info("executing scheduled job: retry_job", extra="retry_job")

    async with AsyncClient() as client:
        try:
            response = await client.post("http://localhost:8080/api/1/front/login", data={"username": "", "password": ""})
            id_token = response.json()["id_token"]
            logger.info("logged in to the cognito...", extra="retry_job")

            await client.post("http://localhost:8080/transfer/retry", headers={"Authorization": f"Bearer {id_token}"})

            logger.info("retry job succeeded", extra="retry_job")
        except Exception as e:
            logger.info(f"terminating as error happened. error_detail: {e}", extra="retry_job")


scheduled_tasks = []
