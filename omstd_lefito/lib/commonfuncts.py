# -*- coding: utf-8 -*-
import socks
import urllib.request
import re
import os

# --------------------------------------------------------------------------
def dorequest(url, params):
    req = urllib.request.Request(url)
    if params.agent is not None:
        req.add_header("User-agent", params.agent)
    else:
        req.add_header("User-agent", "Soy el lefito.")
    result = {}
    try:
        respuesta = urllib.request.urlopen(req)
        result['body'] = respuesta.read()
        result['head'] = respuesta.info()
    except:
        result = {
            'body': 'error',
            'head': 'error',
        }
    return result

# --------------------------------------------------------------------------
def create_connection(address, timeout=None, source_address=None):
    sock = socks.socksocket()
    sock.connect(address)
    return sock

# --------------------------------------------------------------------------
def cleanhtml(raw_html):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    return cleantext

# --------------------------------------------------------------------------
def showmenuppal():
    print("[0] Init Intelligence")
    print("[1] Show Intelligence")
    print("[2] Start Recogn")
    print("[q] Quit")
    choice = str(input("Select:"))
    return choice

# --------------------------------------------------------------------------
def readpayloads(fname):
    with open(fname) as f:
        content = f.readlines()
        content = [x.strip('\n') for x in content]
    return content

# --------------------------------------------------------------------------
def menupayloads(dirname):
    listapayloads = os.listdir(dirname)
    n = 0
    listapayloads.sort()
    for payload in listapayloads:
        print("[%i] %s" % (n, payload))
        n += 1
    print("[q] Salir")
    try:
        select = int(input("elige: "))
        payloadseleccionado = listapayloads[select]
        return dirname + '/' + payloadseleccionado
    except:
        return 'q'
