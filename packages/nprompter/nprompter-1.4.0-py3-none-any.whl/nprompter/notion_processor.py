import logging
import shutil
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Union

from jinja2 import Environment, PackageLoader, select_autoescape
from slugify import slugify

from nprompter import CONTENT_DIRECTORY
from nprompter.notion_client import NotionClient

logger = logging.getLogger("NotionScripting")

env = Environment(loader=PackageLoader("nprompter"), autoescape=select_autoescape())
script_template = env.get_template("script.html")
index_template = env.get_template("index.html")


@dataclass
class Link:
    link: str
    name: str


class NotionProcessor:
    def __init__(self, notion_client: NotionClient, content_root: Union[str, None] = None):
        self.notion_client = notion_client
        self.links = []
        self.database_name = None
        self.folder = None
        self.content_root = content_root or CONTENT_DIRECTORY

    def create_scripts(self, database_id: str, section_name: str):
        database = self.notion_client.query_database(database_id)
        database_title = database["title"][0]["text"]["content"]

        self.start(database_title)

        pages = self.notion_client.get_pages(section_name, database_id)
        for page in pages:
            page_id = page["id"]
            blocks = self.notion_client.get_blocks(page_id)
            self.add_page(page_title=page["properties"]["Name"]["title"][0]["text"]["content"], blocks=blocks)
        self.finish(database_title)

    def start(self, database_name):
        self.folder = Path(self.content_root, slugify(database_name))
        try:
            shutil.rmtree(self.folder)
        except FileNotFoundError:
            pass
        except NotADirectoryError:
            print(f"The path {self.folder} exists but it is not a directory", file=sys.stderr)
            raise
        self.folder.mkdir(parents=True, exist_ok=True)

    def finish(self, database_title):
        index = index_template.render(elements=self.links, title=database_title)
        with open(Path(self.content_root, "index.html"), "w", encoding="utf8") as writable:
            writable.write(index)

    def process_paragraph_blog(self, block):
        return self.process_text_block_blog(block, "paragraph")

    def process_bulleted_list(self, block):
        return self.process_text_block_blog(block, "bulleted_list_item")

    def process_text_block_blog(self, block, node, make_paragraph=True):
        block_content = []
        for content in block[node]["text"]:
            if text_content := content.get("text"):
                text = text_content["content"]
                if content["annotations"].get("bold"):
                    text = f"<b>{text}</b>"
                if content["annotations"].get("italic"):
                    text = f"<i>{text}</i>"
                text = f"<span>{text}</span>"
            elif equation := content.get("equation"):
                text = f"\\({equation['expression']}\\)"
            else:
                text = None
                logger.warning(f"No action for {content['type']}")
            if text is not None:
                block_content.append(text)
        if make_paragraph:
            result = "<p>" + ("".join(block_content)) + "</p>"
        else:
            result = "".join(block_content)
        return result

    def add_page(self, page_title: str, blocks: List[Dict]) -> str:
        elements = []
        for block in blocks:
            block_type = block["type"]

            if block_type == "paragraph":
                result = self.process_paragraph_blog(block)
            elif block_type == "image":
                if "external" not in block["image"]:
                    image_url = block["image"]["file"]["url"]
                else:
                    image_url = block["image"]["external"]["url"]
                result = f'<img src="{image_url}" />'
            elif block_type == "bulleted_list_item":
                result = self.process_bulleted_list(block)
            elif block_type.startswith("heading_"):
                h_size = int(block_type[-1])
                content = self.process_text_block_blog(block, block_type, make_paragraph=False)
                result = f"<h{h_size}>{content}</h{h_size}>"
            elif block_type == "equation":
                result = f"$${block['equation']['expression']}$$"
            else:
                result = None
                logger.error(f"No action for block of type {block_type}")
            if result is not None:
                elements.append(result)

        content = script_template.render(elements=elements, title=page_title)

        file_name = Path(self.folder, Path(slugify(page_title) + ".html"))
        with open(file_name, "w", encoding="utf8") as writeable:
            writeable.write(content)

        parent_directory = str(file_name)[len(self.content_root) :]  # noqa

        self.links.append(Link(parent_directory, name=page_title))
        return content
