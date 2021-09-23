class Except(Exception):
    def __init__(*args, **kwargs):
        Exception.__init__(*args, **kwargs)


def CheckExceptions(data):
    raise Except(data)
