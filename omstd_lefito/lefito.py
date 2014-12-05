# -*- coding: utf-8 -*-

import argparse

def main():
    from .api import Parameters, Results, Displayer, IntellCollector, connect_tor, testip, menuppal

    parser = argparse.ArgumentParser(description="lefito hace cositas de lfi")
    parser.add_argument("-u", dest="url", help="target url")
    parser.add_argument("-p", dest="payloads", help="payloads file (or 'all')")
    parser.add_argument("-t", dest="tor", help="use tor", action="store_true")
    parser.add_argument("-c", dest="checkip", help="check ip", action="store_true")
    parser.add_argument("-r", dest="autorun", help="performs auto recogn an attack (needs url and payloads)", action="store_true")
    parser.add_argument("-a", dest="agent", help="custom user agent")
    parser.add_argument("-o", dest="outfile", help="output file")
    params = parser.parse_args()

    try:
        input_parameters = Parameters(url=params.url,
                                      payloads=params.payloads,
                                      tor=params.tor,
                                      checkip=params.checkip,
                                      autorun=params.autorun,
                                      outfile=params.outfile,
                                      agent=params.agent, )
        results = Results()
        d = Displayer()
        d.config(out_screen=True,
                 out_file=params.outfile,
                 verbosity=1)
        intell = IntellCollector()
    except ValueError as e:
        print(e)
        exit()

    if params.tor is not None:
        connect_tor()
    if params.checkip is not None:
        testip(input_parameters)
    if params.autorun is not None:
        intell.gather(input_parameters)
        intell.show()
        intell.startrecogn(params, results)
    else:
        menuppal(input_parameters, results)
    print("RESULTS %s" % results.diffs)


if __name__ == "__main__" and __package__ is None:
    import sys
    import os

    parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.insert(1, parent_dir)
    import omstd_lefito

    __package__ = str("omstd_lefito")
    del sys, os

    main()