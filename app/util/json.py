import orjson


def orjson_dumps_str(obj):
    return orjson.dumps(obj).decode('utf-8')
