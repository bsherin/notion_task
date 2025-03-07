import sys
import re
import webbrowser
import subprocess
from notion_client import Client

print('starting')
print(sys.version)


def read_from_clipboard():
    return subprocess.check_output(
        'pbpaste', env={'LANG': 'en_US.UTF-8'}).decode('utf-8')


def is_valid_url(url):
    pattern = re.compile(
        r'^(https?|ftp)://'  # HTTP, HTTPS, or FTP
        r'([A-Za-z0-9.-]+)'  # Domain
        r'(:\d+)?'  # Optional port
        r'(/.*)?$',  # Optional path
        re.IGNORECASE
    )
    return re.match(pattern, url) is not None

import os
import sys

def get_secret_file_path():
    if getattr(sys, 'frozen', False):  # Running from a bundled PyInstaller app
        base_path = sys._MEIPASS  # Temporary folder for bundled files
    else:
        base_path = os.path.dirname(__file__)  # Running as a normal script

    return os.path.join(base_path, "notion_secret.txt")

f = open(get_secret_file_path())
token = f.read().strip()

def not_all_spaces(lin):
    return not len(re.sub(" ", "", lin)) == 0


project_db_id = "e22bc1f728bb48a794e162a209ebe024"


def build_notion_page(project, subject, start_date, due_date):
    notion = Client(auth=token)
    the_json = {
        "database_id": project_db_id,
        "filter": {
            "property": "title",
            "rich_text": {
                "contains": project,
            },
        },
    }
    print("got json")
    my_page = notion.databases.query(**the_json)
    print("got project database page")

    relation_id = my_page["results"][0]["id"]
    icon = my_page["results"][0]["icon"]
    icon_url = icon["external"]["url"]
    icon_url = re.sub("^notion", "https", icon_url)
    icon["external"]["url"] = icon_url

    print("got icon")


    the_json = {"parent": {"database_id": "0eb71fcd9edb42e3aec60bdc739dbfb9"},
                "properties": {"Name": {"title": [{"text": {"content": subject}}]},
                               "Project": {"relation": [{"id": relation_id}], "has_more": False}
                               },
                "children": [],
                "icon": icon
    }
    email_url = read_from_clipboard()
    if email_url is not None and is_valid_url(email_url):
        the_json["properties"]["email"] = {"url": email_url}

    if not start_date == "":
        the_json["properties"]["Start On"] = {"date": {
            "start": start_date
            }
        }

    if not due_date == "":
        the_json["properties"]["Due Date"] = {"date": {
            "start": due_date
            }
        }

    print("about to post")
    result = notion.pages.create(**the_json)

    page_id_raw = result["id"]
    page_id = re.sub("\-", "", page_id_raw)
    url = "notion://www.notion.so/{}".format(page_id)
    webbrowser.open(url)
