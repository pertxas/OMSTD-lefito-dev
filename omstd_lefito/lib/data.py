# -*- coding: utf-8 -*-

# --------------------------------------------------------------------------
class Results:
    """Program results"""

    # ----------------------------------------------------------------------
    def __init__(self, **kwargs):
        self.diffs = kwargs.get("diffs", {})


# --------------------------------------------------------------------------
class Parameters:
    """Program parameters"""
    # ----------------------------------------------------------------------
    def __init__(self, **kwargs):
        self.url = kwargs.get("url")
        self.payloads = kwargs.get("payloads")
        self.tor = kwargs.get("tor")
        self.checkip = kwargs.get("checkip")
        self.autorun = kwargs.get("autorun")
        self.agent = kwargs.get("agent")
        self.outfile = kwargs.get("outfile")

__all__ = ["Results", "Parameters"]


