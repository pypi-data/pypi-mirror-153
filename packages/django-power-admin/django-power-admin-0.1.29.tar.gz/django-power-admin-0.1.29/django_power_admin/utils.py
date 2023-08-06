import urllib



def get_url_query(url, name, default=None):
    parameters = urllib.parse.parse_qs(urllib.parse.urlparse(url).query)
    return parameters.get(name, [default])[0]

def update_url_query(url, name, value):
    parameters = urllib.parse.parse_qs(urllib.parse.urlparse(url).query)
    parameters[name] = [value]
    params = []
    for key, value in parameters.items():
        params += [(key,v) for v in value]
    components = list(urllib.parse.urlparse(url))
    components[4] = urllib.parse.urlencode(params)
    return urllib.parse.urlunparse(components)
