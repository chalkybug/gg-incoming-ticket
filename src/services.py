# external import
from datetime import date, timedelta, datetime
from openpyxl import Workbook
from httplib2 import Http
import configparser as _config
import json
import dateparser
import os
import pytz
import requests
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv
import urllib.parse

from models import JiraBatchModel, JiraViewModel

# Load environment variables from .env file
load_dotenv()
global JIRA_EMAIL, JIRA_API_TOKEN, REMINDER_BOT_URL, GG_TITLE, GG_MESSAGE, GG_SUB_TITLE, MISS_FTC
JIRA_EMAIL = os.getenv("JIRA_EMAIL")
JIRA_API_TOKEN = os.getenv("JIRA_API_TOKEN")

REMINDER_BOT_URL = os.getenv("REMINDER_BOT_URL")
GG_TITLE = os.getenv("GG_TITLE")
GG_MESSAGE = os.getenv("GG_MESSAGE")
GG_SUB_TITLE = os.getenv("GG_SUB_TITLE")

# query
MISS_FTC = os.getenv("MISS_FTC")


# *****************************************
# gChat Transaction to CRM
# *****************************************
def GChat_Message(incoming_tickets: list):

    # Tạo nội dung thông báo chỉ với các loại ticket count > 0
    message_lines = [f"📊 **Có {len(incoming_tickets)} vị khách **\n"]
    for ticket in incoming_tickets:
        message_lines.append(f"🎫 {ticket}")

    message_lines.append(f"\n{GG_MESSAGE}\n")
    message_content = "\n".join(message_lines)

    FiveDayForecastSection = [
        {
            "collapsible": "false",
            "widgets": [
                {
                    "textParagraph": {
                        "text": message_content,
                    },
                },
            ],
        },
    ]

    bot_message = {
        "cardsV2": [
            {
                "cardId": "unique-card-id",
                "card": {
                    "header": {
                        "title": f"{GG_TITLE} - {GG_SUB_TITLE}",
                    },
                    "sections": FiveDayForecastSection,
                },
            }
        ],
    }
    message_headers = {"Content-Type": "application/json; charset=UTF-8"}
    http_obj = Http()
    response = http_obj.request(
        uri=REMINDER_BOT_URL,
        method="POST",
        headers=message_headers,
        body=json.dumps(bot_message),
    )


# *****************************************
# Get Pending Ticket
# *****************************************
def get_ticket(jql_query: str):

    url = "https://e-courier.atlassian.net/rest/api/2/search/jql"

    auth = HTTPBasicAuth(
        JIRA_EMAIL,
        JIRA_API_TOKEN,
    )

    headers = {"Accept": "application/json"}

    query = {
        "jql": jql_query,
        "fields": ["key", "summary"],
    }

    response = requests.request("GET", url, headers=headers, params=query, auth=auth)

    # print(json.dumps(json.loads(response.text), sort_keys=True, indent=4, separators=(",", ": ")))
    data = json.loads(response.text)
    return data.get("issues")


# *****************************************
# handle ticket main function
# *****************************************
def forecast():
    tickets = get_ticket(MISS_FTC)
    incoming_tickets = []
    for ticket in tickets:
        key = ticket.get("key")
        summary = ticket.get("fields", {}).get("summary")
        print(f"{key}-{summary}")
        incoming_tickets.append(f"{key} - {summary}")
    if len(incoming_tickets) > 0:
        GChat_Message(incoming_tickets)
