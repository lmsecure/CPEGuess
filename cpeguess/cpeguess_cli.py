import sys
sys.path[0] = ''

from cpeguess.cpeguess import CPEGuess
import uvicorn
from fastapi import FastAPI
from cpeguess.routers import cpe
import json
from cpeguess.tools.downloader import CPEDownloader
from cpeguess.database import Base, engine
from cpeguess.database import get_db
from cpeguess.tools.importer import Importer
import os
import click


@click.group()
def manager():
    pass


@manager.command()
@click.option('-n', '--name', required=True, type=str, show_default=True, help='Product to find')
@click.option('-v', '--version', required=True, type=str, show_default=True, help='Version to find')
def search(name: str, version: int):
    """This command searches cpe by name and version"""
    result = CPEGuess.search(name=name, version=version, format="dict")
    print(json.dumps(result, indent=4))


@manager.command
@click.option('-p', '--port', default=8000, type=int, show_default=True, help='WebServer port')
def runserver(port: int):
    """This command starts webserver via uvicorn"""
    app = FastAPI(title="CPE")
    app.include_router(cpe.router)
    uvicorn.run(app=app, port=port)


@manager.command()
def refresh():
    """This command drops database and downloads it from remote"""
    if click.confirm('Do you want to drop database and refill it?', abort=True):
        pass

    cpe_source = "https://nvd.nist.gov/feeds/xml/cpe/dictionary/official-cpe-dictionary_v2.3.xml.gz"
    filename = 'official-cpe-dictionary_v2.3.xml'
    full_path = os.path.join(os.path.dirname(__file__), filename)
    CPEDownloader.download(filename=full_path, url=cpe_source)

    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    importer = Importer(path=full_path, db=next(get_db()))
    importer.parse_and_fill()
    os.remove(full_path)


if __name__ == '__main__':
    manager()
