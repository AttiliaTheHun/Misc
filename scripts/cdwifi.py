# By default, the wifi in the trains of Ceske Drahy asks you to authenticate, which reditects you to http://cdwifi.cz/captive where you are shown a 30 second
# long ad video and then you agree to the terms of service to be admitted to use internet connection. As a linux user, I find the waiting and the advertisement unacceptable, so
# I looked a little closer as how the portal knows you have watched the ad and I am still not sure. This script is a base that I intented to improve upon once I get more understanding of
# the requests sent and state kept, but as it appears to be working like this, I have no motivation to work on this further. Enjoy I guess.

from http.client import HTTPConnection
from http import HTTPStatus
import json
import sys

def send_request_urban():
    """
    This function handles the connection for urban trains within the Prague city. They do not usually show ads but still require you to check a box and click a button
    to gain internet access. A simple POST request can save you the trouble, not to mention lets you keep your current DNS settings.
    """
    host = "10.200.0.11" # the host is virtual-gw.cdwifi.cz but is only accessible if we use the router DNS. I want to avoid switching DNS
    port = 80
    conn = HTTPConnection(host, port)
    method = "POST"
    path = "/accept"

    body = "secret=69ef940c4a370&eula=on"
    headers = {
 		'Host': 'virtual-gw.cdwifi.cz',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept': 'application/json',
        'Origin': "http://virtual-gw.cdwifi.cz",
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36',
        'Referer': 'http://virtual-gw.cdwifi.cz/',
        'Accept-Encoding': 'gzip, deflate, br',
        'Cookie': '_ga=GA1.1.266849468.1774202642; _ga_EQ3JY0LPG6=GS2.1.s1774545056$o2$g1$t1774545107$j9$l0$h0',
        'Connection': 'keep-alive'
    }
    conn.request(method, path, body, headers)

    response = conn.getresponse()
    if response.status == HTTPStatus.FOUND:
        print("success")
        return
    content_length = int(response.getheader('Content-Length'))
    print(f"{response.status} failed:\n" + response.read(content_length))

def send_request_regional():   
    """
    This function handles the standard Ceske Drahy trains that travel between cities. It lets you skip the advertisment along with accepting the ToS while preserving your DNS settings.
    """ 
    host = "172.16.2.2" # the host is cdwifi.cz but is only accessible if we use the router DNS. I want to avoid switching DNS
    port = 80
    conn = HTTPConnection(host, port)
    method = "GET"
    path = "/portal/api/vehicle/gateway/user/authenticate?category=internet&url=http%3A%2F%2Fcdwifi.cz%2Fportal%2Fapi%2Fvehicle%2Fgateway%2Fuser%2Fsuccess&onerror=http%3A%2F%2Fcdwifi.cz%2Fportal%2Fapi%2Fvehicle%2Fgateway%2Fuser%2Ferror"

    body = ""
    headers = {
 		'Host': 'cdwifi.cz',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept': 'application/json',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36',
        'Referer': 'http://cdwifi.cz/captive',
        'Accept-Encoding': 'gzip, deflate, br',
        'Cookie': '_ga=GA1.1.266849468.1774202642; _ga_EQ3JY0LPG6=GS2.1.s1774545056$o2$g1$t1774545107$j9$l0$h0',
        'Connection': 'keep-alive'
    }
    conn.request(method, path, body, headers)

    response = conn.getresponse()
    if response.status == HTTPStatus.TEMPORARY_REDIRECT:
        print("success")
        return
    content_length = int(response.getheader('Content-Length'))
    print(f"{response.status} failed:\n" + response.read(content_length))


if __name__ == "__main__":
    if len(sys.argv) > 1:
        send_request_urban()
    else:
        send_request_regional()
    
