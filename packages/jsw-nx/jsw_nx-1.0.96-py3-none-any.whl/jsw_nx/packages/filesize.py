import os


def filesize(filename):
    size = os.stat(filename).st_size

    # Convert to familiar units
    kb = size / 1024
    mb = size / 1024 / 1024

    kb_2 = round(kb, 2)
    mb_2 = round(mb, 2)

    return kb_2, mb_2
