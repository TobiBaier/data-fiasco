def merge(a: dict, b: dict, path=None):
    if path is None:
        path = []

    for key in b:
        if key in a:
            if isinstance(a[key], dict) and isinstance(b[key], dict):
                merge(a[key], b[key], path + [str(key)])
            elif isinstance(a[key], list) or isinstance(b[key], list):
                if a[key] is None:
                    a[key] = b[key]
                elif b[key] is None:
                    a[key] = a[key]
            elif a[key] != b[key]:
                pass  # raise Exception('Conflict at ' + '.'.join(path + [str(key)]))
        else:
            a[key] = b[key]
    return a