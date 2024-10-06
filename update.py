import os

import requests
from dotenv import load_dotenv

load_dotenv()

CF_ZONE_ID = os.getenv("CF_ZONE_ID")
CF_API_TOKEN = os.getenv("CF_API_TOKEN")
CF_EMAIL = os.getenv("CF_EMAIL")


def update_cloudflare_dns(dns_record_id, ip_address):
    url = f"https://api.cloudflare.com/client/v4/zones/{CF_ZONE_ID}/dns_records/{dns_record_id}"

    payload = {
        "content": ip_address,
        "name": "edge",
        "proxied": False,
        "type": "A",
        "ttl": 1,
    }
    headers = {
        "Content-Type": "application/json",
        "X-Auth-Email": CF_EMAIL,
        "X-Auth-Key": CF_API_TOKEN,
    }

    response = requests.request("PATCH", url, json=payload, headers=headers)
    success = response.json()["success"]
    print(f"Cloudflare DNS Record Update Success: {success}")


def get_dns_record_id():
    import requests

    url = f"https://api.cloudflare.com/client/v4/zones/{CF_ZONE_ID}/dns_records"

    headers = {
        "Content-Type": "application/json",
        "X-Auth-Email": CF_EMAIL,
        "X-Auth-Key": CF_API_TOKEN,
    }

    response = requests.request("GET", url, headers=headers)

    result = response.json()
    for record in result["result"]:
        if record["name"] == "edge.otwako.xyz":
            id = record["id"]
            print(f"DNS Record ID: {id}")
            return id


def get_best_ip():
    response = requests.get("https://ip.164746.xyz/ipTop.html")
    ips = response.text.split(",")
    return ips


if __name__ == "__main__":
    fast_ip_addresses = get_best_ip()
    dns_record_id = get_dns_record_id()
    update_cloudflare_dns(dns_record_id, fast_ip_addresses[0])
