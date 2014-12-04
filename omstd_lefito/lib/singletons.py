# -*- coding: utf-8 -*-

__ALL__ = ["Displayer", "IntellCollector"]

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

    # ---------------------------------------------------------------------
    def gather(self, params):
        out = Displayer()
        if params.url is not None:
            self.target = params.url
        else:
            self.target = str(input("url: "))
        originalreq = dorequest(self.target, params)
        m = re.search(b"(charset=(?P<value>.*)\")", originalreq['body'])
        if m:
            self.charset = m.group('value').decode()
        self.originalreq_lines = [x.decode(self.charset) for x in originalreq['body'].splitlines()]
        self.originalhead = originalreq['head']
        out.display(originalreq['head'])
        self.originalsess = getsess(originalreq['head'])
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
