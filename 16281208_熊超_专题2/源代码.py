# -*- coding: utf-8 -*-  
import pysnooper
Vt={'(',')','+','-','*','/','i','='}
Vn={'A','V','E','T','F','M','e','t'}
G={'A':['V=E','+','-'],'E':['Te'],'e':['ATe','ε'],'T':['Ft'],'t':['MFt','ε'],'F':['(E)','i'],'M':['*','/'],'V':['i']}
XVn = {'e','t'}
firstset = dict().fromkeys(Vn,set())
followset = dict().fromkeys(Vn)
def init_firstset(P):
    if len(firstset[P]) is not 0:
        return firstset[P]
    result = set()
    for i in G[P]:
        if i[0] in Vt :
            result.add(i[0])
        elif i[0] in Vn:
            result=result.union(init_firstset(i[0]))
    firstset[P]= result
    flag = True
    for i in G[P]:
        for j in i:
            if j not in XVn:
                flag = False
                break
    if flag :
        firstset[P].add('ε')
    return firstset[P]

def get_firstset(P):
    if P in Vt:
        return {P}
    elif P in Vn:
        return firstset[P]
    else:
        result = set()
        for i in P:
            result |= get_firstset(i)
            if i not in XVn or i in Vt:
                break
        return result
def harmful(p):
    for i in p:
        if i not in XVn:
            return False
    return True
def get_followset():
    for i in Vn:
        followset[i]=set()
    followset['A'].add('$')
    sum = 0
    while True:
        tsum = 0
        for V in Vn:
            for i in Vn:
                for j in G[i]:
                    for t in range(len(j)):
                        if j[t]==V:
                            followset[V]=followset[V].union(get_firstset(j[t+1:]).difference({'ε'}))
                            if t == len(j)-1 or harmful(j[t+1:]):
                                followset[V] = followset[V].union(followset[i])
                               
            tsum +=len(followset[V])
        if tsum == sum:
            break
        sum = tsum
current=0
S = list()
def V():
    global S, current
    if S[current][0]=='i':
        current += 1
        return True
    return False
def M():
    global S, current
    if S[current][0] == '*' or S[current][0] == '/':
        current+=1
        return True
    return False
def F():
    global S, current
    if S[current][0] == '(' :
        current+=1
        if E() and S[current][0]==')':
            current+=1
            return True
    elif S[current][0] == 'i':
        current+=1
        return True
    return False
def t():
    global S, current
    if S[current][0] in get_firstset('MFt'):
        return M() and F() and t()
    elif S[current][0] in followset['t']:
        return True
    return False
def T():
    global S, current
    if S[current][0] in get_firstset('Ft'):
        return F() and t()
    return False
def E():
    global S, current
    if S[current][0] in get_firstset('Te'):
        if T() and e():
            return True
    return False
def A():
    global S, current
    if S[current][0] in get_firstset('V'):
        if V() and S[current][0] == '=' :
            current += 1
            return E()
    elif S[current][0] == '+' or S[current][0]=='-':
        current+=1
        return True
    return False
def e():
    global S, current
    if S[current][0] in get_firstset('ATe'):
        if A() and T():
            return e()    
    elif S[current][0] in followset['e']:
        return True
    return False
def init_firstAndFollowSet():
    for i in Vn:
        init_firstset(i)
    get_followset()


from lexical_analyzer import lexical_analyzer
with open('input.txt','r') as f:
    S_,table = lexical_analyzer(f.read())
init_firstAndFollowSet()
for i in S_:
    if i[1] == table['标识符']:
        S.append(('i',i[1]))
    else:
        S.append(i)
print(A())


