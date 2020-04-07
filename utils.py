def str2bool(s):
    if isinstance(s,str):
        if s == 'True':
            return True
        elif s == 'False':
            return False
        else:
            return ValueError
    else:
        return s
