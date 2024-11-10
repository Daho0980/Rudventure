from Chat import status as s


def clear_0() -> bool:
    s.history['chat'] = []
    return True