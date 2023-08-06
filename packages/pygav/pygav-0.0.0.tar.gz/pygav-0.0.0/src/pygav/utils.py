def rolling_window(iterable, length, stride=1):
    offset = 0
    while offset < len(iterable):
        yield iterable[offset:offset+length]
        offset += stride
