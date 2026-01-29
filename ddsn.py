#!/usr/bin/python3
import requests
import json
import os
import logging

logging.basicConfig(
    filename="/var/log/ddns.log",
    encoding="utf-8",
    filemode="a",
    format="{asctime} - {levelname} - {message}",
    style="{",
    datefmt="%Y-%m-%d %H:%M",
    level=logging.INFO,
)

DOMAIN = "YOURDOMAN.tld"
RECORD_NAME = "@"
IP_FILE = "/root/last_ip.txt"
API_KEY = "API_KEY"
API_URL = "https://developers.hostinger.com/api/dns/v1/zones/YOURDOMAIN.tld"

def get_public_ip():
    return requests.get("https://api.ipify.org").text.strip()

def get_last_ip():
    if not os.path.exists(IP_FILE):
        return None
    return open(IP_FILE).read().strip()

def save_ip(ip):
    with open(IP_FILE, "w") as f:
        f.write(ip)

def update_dns(ip):
    payload = {
    "overwrite": True,
    "zone": [{"name": RECORD_NAME,
    "records": [{"content": ip}],
    "ttl": 300,
    "type": "A"}]}
    headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
    try:
        r = requests.put(API_URL, headers=headers, data=json.dumps(payload))
        logging.info("Status Code: %s", r.status_code)
        logging.info("Response Content: %s", r.text)
        r.raise_for_status()
    except requests.exceptions.HTTPError as e:
        logging.error("HTTP error occurred:", e)
    except requests.exceptions.RequestException as e:
        logging.error("A request error occurred:", e)

def main():
    logging.info("ddns excuting!")
    current_ip = get_public_ip()
    last_ip = get_last_ip()
    if current_ip != last_ip:
        logging.info("IP changed: %s", current_ip)
        update_dns(current_ip)
        save_ip(current_ip)

if __name__ == "__main__":
    main()
