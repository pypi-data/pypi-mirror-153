def parse_metadata(parameters: dict) -> dict:
    params = {}
    for idx, param in parameters.items():
        try:
            params[idx] = param["metadata"]
        except:
            continue
    return params
