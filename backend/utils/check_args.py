def are_all_args_present(*args):
    for a in args:
        if a is None:
            return False
        if isinstance(a, set):
            if len(a) == 0:
                return None
    return True