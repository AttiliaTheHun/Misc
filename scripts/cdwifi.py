# By default, the wifi in the trains of Ceske Drahy asks you to authenticate, which reditects you to http://cdwifi.cz/captive where you are shown a 30 second
# long ad video and then you agree to the terms of service to be admitted to use internet connection. As a linux user, I find the waiting and the advertisement unacceptable, so
# I looked a little closer as how the portal knows you have watched the ad and I am still not sure. This script is a base that I intented to improve upon once I get more understanding of
# the requests sent and state kept, but as it appears to be working like this, I have no motivation to work on this further. Enjoy I guess.
# New version rehauled by DeepSeek
import socket
from http.client import HTTPConnection

FLAVORS = [
    {   # regional CD trains
        "name": "regional",
        "hosts": ["172.16.2.2", "10.200.0.60", "10.200.0.12"],
        "port": 80,
        "method": "GET",
        "path": ("/portal/api/vehicle/gateway/user/authenticate"
                 "?category=internet"
                 "&url=http%3A%2F%2Fcdwifi.cz%2Fportal%2Fapi%2Fvehicle%2Fgateway%2Fuser%2Fsuccess"
                 "&onerror=http%3A%2F%2Fcdwifi.cz%2Fportal%2Fapi%2Fvehicle%2Fgateway%2Fuser%2Ferror"),
        "body": "",
        "host_header": "cdwifi.cz",
        "referer": "http://cdwifi.cz/captive",
        "success_statuses": {307},
    },
    {   # urban Prague trains
        "name": "urban",
        "hosts": ["10.200.0.11", "10.200.0.60"],
        "port": 80,
        "method": "POST",
        "path": "/accept",
        "body": "secret=69ef940c4a370&eula=on",
        "host_header": "virtual-gw.cdwifi.cz",
        "origin": "http://virtual-gw.cdwifi.cz",
        "referer": "http://virtual-gw.cdwifi.cz/",
        "success_statuses": {302},
    },
]


def base_headers(flavor):
    h = {
        "Host": flavor["host_header"],
        "Accept": "application/json",
        "Referer": flavor["referer"],
        "Connection": "close",   # simpler than keep-alive for one-shot
    }
    if "origin" in flavor:
        h["Origin"] = flavor["origin"]
    return h


def try_flavor(flavor, host, timeout=3):
    try:
        conn = HTTPConnection(host, flavor["port"], timeout=timeout)
        conn.request(flavor["method"], flavor["path"],
                     flavor["body"], base_headers(flavor))
        resp = conn.getresponse()
        ok = resp.status in flavor["success_statuses"]
        if not ok:
            snippet = resp.read(512).decode("utf-8", "replace")
           # print(f"  {host}: {resp.status} {resp.reason} — {snippet!r}")
        conn.close()
        return ok
    except (socket.timeout) as e:
        return False
    except (OSError) as e:
        print(f"  {host}: {type(e).__name__}: {e}")
    return False


def main():
    for flavor in FLAVORS:
        # print(f"Trying {flavor['name']}…")
        for host in flavor["hosts"]:
            if try_flavor(flavor, host):
                print(f"success") 
                return 0
    print("captive portal not found")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
