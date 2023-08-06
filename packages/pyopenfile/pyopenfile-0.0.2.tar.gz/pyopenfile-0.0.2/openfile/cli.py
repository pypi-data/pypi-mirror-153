import click
import uvicorn
import logging

from openfile import __version__
from openfile.config import settings
from openfile.main import app

logger = logging.getLogger(__name__)


@click.group()
def cli():
    pass


@cli.command()
def version():
    print(__version__)


@cli.command()
def run():
    logger.info(f"run in {settings.host}:{settings.port}")
    uvicorn.run(app, host=settings.host, port=settings.port)
