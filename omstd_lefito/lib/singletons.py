# -*- coding: utf-8 -*-

__all__ = ["Displayer", "IntellCollector"]

import re
import difflib
from urllib.parse import urlparse
from .commonfuncts import dorequest, readpayloads, menupayloads, cleanhtml

# -------------------------------------------------------------------------
class Displayer:
    """Output system"""
    instance = None
    # ---------------------------------------------------------------------
    def __new__(cls, *args, **kwargs):
        if cls.instance is None:
            cls.instance = object.__new__(cls, *args, **kwargs)
            cls.__initialized = False
        return cls.instance

    # ---------------------------------------------------------------------
    def config(self, **kwargs):
        self.out_file = kwargs.get("out_file", None)
        self.out_screen = kwargs.get("out_screen", True)
        self.verbosity = kwargs.get("verbosity", 0)
        if self.out_file:
            self.out_file_handler = open(self.out_file, "w")

    # ---------------------------------------------------------------------
    def display(self, message):
        if self.verbosity > 0:
            self.__display(message)

    # ---------------------------------------------------------------------
    def display_verbosity(self, message):
        if self.verbosity > 1:
            self.__display(message)

    # ---------------------------------------------------------------------
    def display_more_verbosity(self, message):
        if self.verbosity > 2:
            self.__display(message)

    # ---------------------------------------------------------------------
    def __display(self, message):
        if self.out_screen:
            print(message)
        if self.out_file_handler:
            self.out_file_handler.write(message)

    # ---------------------------------------------------------------------
    def __init__(self):
        if not self.__initialized:
            self.__initialized = True
            self.out_file = None
            self.out_file_handler = None
            self.out_screen = True
            self.verbosity = 0

# -------------------------------------------------------------------------
class IntellCollector:
    """gathered data container"""
    instance = None

    # ---------------------------------------------------------------------
    def __new__(cls, *args, **kwargs):
        if cls.instance is None:
            cls.instance = object.__new__(cls, *args, **kwargs)
            cls.__initialized = False
        return cls.instance

    # ---------------------------------------------------------------------
    def config(self, **kwargs):
        self.target = kwargs.get("target", None)

    # --------------------------------------------------------------------------
    def getsess(self):
        out = Displayer()
        if 'set-cookie' in self.originalhead:
            out.display(self.originalhead['set-cookie'])
            m = re.search("(PHPSESSID=(?P<value>.*);)", self.originalhead['set-cookie'])
            if m:
                out.display(m.group('value'))
                self.originalsess = m.group('value')
            else:
                self.originalsess = ''
        else:
            self.originalsess = ''

    # ---------------------------------------------------------------------
    def gather(self, params):
        out = Displayer()
        if params.url is not None:
            self.target = params.url
        else:
            self.target = str(input("url: "))
        originalreq = dorequest(self.target, params)
        try:
            m = re.search("(charset=(?P<value>.*)\")", originalreq['body'])
        except TypeError:
            m = re.search(b"(charset=(?P<value>.*)\")", originalreq['body'])
        if m:
            self.charset = m.group('value').decode()
        try:
            self.originalreq_lines = [x.decode(self.charset) for x in originalreq['body'].splitlines()]
        except AttributeError:
            self.originalreq_lines = originalreq['body'].splitlines()
        self.originalhead = originalreq['head']
        out.display(originalreq['head'])
        self.getsess()
        self.parsedurl = urlparse(self.target)
        self.parametros = self.parsedurl.query.split('&')

    # ---------------------------------------------------------------------
    def show(self):
        out = Displayer()
        out.display("target: %s" % str(self.target))
        out.display("originalreq_lines: %s" % str(self.originalreq_lines))
        out.display("originalhead: %s" % str(self.originalhead))
        out.display("originalsess: %s" % str(self.originalsess))
        out.display("parsedurl: %s" % str(self.parsedurl))
        out.display("parametros: %s" % str(self.parametros))
        out.display("charset: %s" % str(self.charset))

    # ---------------------------------------------------------------------
    def startrecogn(self, params, results):
        if params.payloads is not None:
            pause = input("Pause? [y/n]")
            payloadslist = readpayloads(params.payloads)
            self.attack(payloadslist, pause, params, results)
        else:
            selectedpayloadlist = menupayloads('./payloads')
            while len(selectedpayloadlist) > 0:
                pause = input("Pause? [y/n]")
                payloadslist = []
                for item in selectedpayloadlist:
                    payloadslist += readpayloads(item)
                self.attack(payloadslist, pause, params, results)
                selectedpayloadlist = menupayloads('./payloads')

    # ---------------------------------------------------------------------
    def attack(self, payloadslist, pause, params, results):
        out = Displayer()
        for parametro in self.parametros:
            urls = self.genurls(payloadslist, parametro)
            for url in urls:
                out.display('-' * len(url))
                out.display(url)
                out.display('-' * len(url))
                results.diffs[url] = ""
                req = "%s://%s%s?%s" % (self.parsedurl.scheme,
                                        self.parsedurl.netloc,
                                        self.parsedurl.path,
                                        url)
                result = dorequest(req, params)
                try:
                    result_lines = [x.decode(self.charset) for x in result['body'].splitlines()]
                except AttributeError:
                    result_lines = result['body'].splitlines()
                difflib.Differ()
                diff = difflib.unified_diff(self.originalreq_lines, result_lines)
                for line in diff:
                    if line.startswith('+'):
                        line = line.strip("+ ")
                        line = cleanhtml(line)
                        if len(line) > 1:
                            out.display(line)
                            results.diffs[url] += "%s\n" % line
                if pause == 'y':
                    cont = input('press enter to continue (q+enter to quit)')
                    if cont == 'q':
                        break

    # --------------------------------------------------------------------------
    def genurls(self, payloadslist, parametro):
        valores = parametro.split('=')
        resultado = []
        for payload in payloadslist:
            cadena = payload.replace("[FOO]", valores[0])
            cadena = cadena.replace("[BAR]", valores[1])
            cadena = cadena.replace("[SESS]", self.originalsess)
            cadena = cadena.replace("[HOST]", self.parsedurl.netloc)
            cadena = cadena.replace("[STHOST]", self.parsedurl.netloc.replace("www.", ""))
            resultado.append(cadena)
        return resultado

    # ---------------------------------------------------------------------
    def __init__(self):
        if not self.__initialized:
            self.__initialized = True
            self.target = None
            self.originalreq_lines = []
            self.originalhead = None
            self.originalsess = None
            self.parsedurl = None
            self.parametros = []
            self.charset = 'utf-8'
