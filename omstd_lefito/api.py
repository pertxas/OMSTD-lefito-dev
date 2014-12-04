# -*- coding: utf-8 -*-
__author__ = 'pertxas - partxas<-at->gmail.com (@pertxas)'

__all__ = ["connect_tor", "testip", "menuppal"]

import socks
import socket
from .lib.data import Parameters, Results
from .lib.singletons import Displayer, IntellCollector
from .lib.commonfuncts import dorequest, create_connection, cleanhtml, showmenuppal

# --------------------------------------------------------------------------
def connect_tor():
    socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, "127.0.0.1", 9050, True)
    # patch the socket module
    socket.socket = socks.socksocket
    socket.create_connection = create_connection

# --------------------------------------------------------------------------
def testip(params):
    url = 'http://www.leaky.org/ip_tester.pl'
    #url = 'http://echoip.com'
    req = dorequest(url, params)
    out = Displayer()
    for line in req['body'].splitlines():
        line = line.decode('utf-8')
        out.display_verbosity(line)
        if line.startswith('<p>Your') or line.startswith('The conn'):
            out.display(cleanhtml(line))

# --------------------------------------------------------------------------
def menuppal(params, results):
    intell = IntellCollector()
    choice = showmenuppal()
    while choice != "q":
        if choice == "0":
            intell.gather(params)
        elif choice == "1":
            intell.show()
        elif choice == "2":
            intell.startrecogn(params, results)
        choice = showmenuppal()
    return True
