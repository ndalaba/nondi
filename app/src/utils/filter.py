def datetimeformat(value, format='%d/%m/%Y %H:%M'):
    if value is None:
        return ''
    return value.strftime(format)


def startswith(text, starts):
    if isinstance(text, str):
        return text.startswith(starts)
    return False
