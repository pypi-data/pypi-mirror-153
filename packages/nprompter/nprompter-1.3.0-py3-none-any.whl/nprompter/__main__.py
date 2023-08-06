import http.server
import logging
import os
import shutil
import socketserver
import webbrowser
from importlib.resources import path
from typing import Any, Union

import pkg_resources
import typer
from dotenv import load_dotenv

from nprompter import CONTENT_DIRECTORY
from nprompter.notion_client import NotionClient
from nprompter.notion_processor import NotionProcessor

load_dotenv()
app = typer.Typer(add_completion=False)

notion_api_key = os.environ["NOTION_API_KEY"]
notion_version = "2021-05-13"

notion_client = NotionClient(notion_api_key, notion_version)

logger = logging.getLogger("NotionScripting")


@app.command()
def download(
    database_id: str = typer.Argument("", envvar="DATABASE_ID"),
    section_name: str = "Written",
    content_root: Union[str, None] = None,
):
    notion_processor = NotionProcessor(notion_client, content_root=content_root)
    notion_processor.create_scripts(database_id, section_name)


def copy_assets(content_root: str):
    assets_folder = pkg_resources.resource_filename("nprompter", "web")
    src_files = os.listdir(assets_folder)
    for file_name in src_files:
        full_file_name = os.path.join(assets_folder, file_name)
        if os.path.isfile(full_file_name):
            shutil.copy(full_file_name, content_root)


@app.command()
def serve(port: int = 8889, content_root: Union[str, None] = None):
    content_root = content_root or CONTENT_DIRECTORY
    copy_assets(content_root)

    class CustomHandler(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=content_root, **kwargs)

        def log_message(self, format: str, *args: Any) -> None:
            pass

    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", port), CustomHandler) as httpd:
        location = f"http://localhost:{port}"
        print(f"Serving at http://localhost:{port}")
        webbrowser.open(location)
        httpd.serve_forever()


if __name__ == "__main__":
    app()
