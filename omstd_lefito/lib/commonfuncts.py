# -*- coding: utf-8 -*-

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
