from puft.core.error.error import Error


def handle_wildcard_error(err: Error):
    return err.expose(), err.status_code


def handle_wildcard_builtin_error(err: Exception):
    return handle_wildcard_error(Error(' ; '.join(err.args), 400))
