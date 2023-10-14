import os
import random

from bs4 import BeautifulSoup
import requests
from slack_sdk import WebClient


# Function to send a message to Slack
def send_slack_message(token, channel, text):
    slack_api_url = "https://slack.com/api/chat.postMessage"
    payload = {
        "channel": channel,
        "text": text,
    }
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    response = requests.post(slack_api_url, json=payload, headers=headers)
    return response


base_url = "https://xkcd.com"
SLACK_BOT_TOKEN = "##SLACK_BOT_API_TOKEN##"
CHANNEL = "##CHANNEL##"
slack_client = WebClient(token=SLACK_BOT_TOKEN)

random_number = random.randint(1, 1000)
fetch_url = f"{base_url}/{random_number}"

response = requests.get(fetch_url)

if response.status_code == 200:
    content_type = response.headers.get("Content-Type", "")
    if "text/html" in content_type:
        html_data = response.text
        soup = BeautifulSoup(html_data, "html.parser")
        comic_div = soup.find("div", id="comic")
        ctitle_div = soup.find("div", id="ctitle")
        if comic_div:
            comic_img_tag = comic_div.find("img")
            if comic_img_tag:
                img_url = "https:" + comic_img_tag["src"]

                # Send the image URL to the Slack channel
                result = f"Image URL: <{img_url}|{ctitle_div.text}>"
                # <{url}|here
                slack_client.chat_postMessage(channel=CHANNEL, text=result)
                print(fetch_url)
                print(img_url)
            else:
                print("No IMG Tag")
        else:
            print("No Comic DIV")
    else:
        print("Not HTML")
else:
    print("Not 200")

print("END")
