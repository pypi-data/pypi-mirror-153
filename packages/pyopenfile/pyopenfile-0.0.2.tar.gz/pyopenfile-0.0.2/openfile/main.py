import os
import logging
import hashlib
import uuid
import asyncio

import aiofiles
from aiofiles import os as aios
from fastapi import FastAPI, Request, Header
from fastapi.responses import StreamingResponse

from openfile.config import settings

logger = logging.getLogger(__name__)


app = FastAPI()


def _gen_hash(digest):
    _, hash = digest.split("=")
    return hash


def _gen_uuid():
    return str(uuid.uuid4())


@app.get("/ping")
def ping():
    return {"result": "pong"}


@app.put("/objects/{filename}")
async def upload_file(request: Request, filename: str, digest: str = Header()):
    loop = asyncio.get_running_loop()
    logger.info(f"put object {filename}, digest is {digest}")

    uid = await loop.run_in_executor(None, _gen_uuid)
    filepath = os.path.join(settings.data_path, uid)

    logger.debug(f"writing stream to file {filepath}")

    m = hashlib.sha256()
    async with aiofiles.open(filepath, mode="wb") as f:
        async for chunk in request.stream():
            await f.write(chunk)
            m.update(chunk)

        hash = m.hexdigest()

    if hash != _gen_hash(digest):
        logger.error(
            f"write file error. filename: {filename}, hash: {hash}, digest: {digest}"
        )
        await aios.remove(filepath)
        return {"filename": filename, "sha256": ""}

    dest_path = os.path.join(settings.data_path, hash)

    logger.debug(f"rename file to {dest_path}")
    await aios.rename(filepath, dest_path)

    return {"filename": filename, "sha256": hash}


@app.get("/objects/{filename}")
async def download_file(filename: str):
    filepath = os.path.join(settings.data_path, filename)

    logger.info(f"download file {filepath}")

    def iterfile():
        with open(filepath, mode="r") as f:
            yield from f.read()

    return StreamingResponse(iterfile())
