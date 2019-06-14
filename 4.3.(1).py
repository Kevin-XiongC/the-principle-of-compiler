def Y(S):
    if S[:2] is ';s' and Y(S[2:]) is True:
        return True
    else:
        return False
def X(S):
    if S[:2] is 'd;' and X(S[2:]) is True:
        return True
    elif S[0] is 's' and Y(S[1:]) is True:
        return True
    else:
        return False
def P(S):
    if S[:9] is 'begin d; ' and X(S[9:-4]) is True and X(S[-4:]) is ' end':
        return True
    else:
        return False

        
    