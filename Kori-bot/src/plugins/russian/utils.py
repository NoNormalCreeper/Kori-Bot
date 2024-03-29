try:
    import ujson as json
except ModuleNotFoundError:
    import json


def get_message_at(data: str) -> list:
    qq_list = []
    data = json.loads(data)
    try:
        qq_list.extend(
            int(msg['data']['qq'])
            for msg in data['message']
            if msg['type'] == 'at'
        )

        return qq_list
    except Exception:
        return []


def is_number(s) -> bool:
    try:
        float(s)
        return True
    except ValueError:
        pass
    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass
    return False