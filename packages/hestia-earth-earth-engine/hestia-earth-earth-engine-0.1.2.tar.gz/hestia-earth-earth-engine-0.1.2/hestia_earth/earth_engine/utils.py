from hestia_earth.utils.tools import non_empty_list


def get_param(params: dict, key: str, default=None):
    value = params.get(key, default)
    return default if value is None else value


def get_required_param(params, key: str):
    if key not in params:
        raise KeyError(f"Missing required '{key}'")
    return params[key]


def parse_request_params(request):
    data = request.get_json(silent=True)
    return data if data is not None and len(data.keys()) > 0 else request.args


def get_fields_from_params(params: dict): return non_empty_list(get_param(params, 'fields', '').split(','))


def resolve(parts: list): return '/'.join(list(filter(lambda x: x is not None and len(x) > 0, parts)))


def float_precision(value): return float("{:.5f}".format(float(value) if type(value) == str else value))
