from lexical_analyzer import lexical_analyzer
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
    sum,count = 0,0
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

def init_firstAndFollowSet():
    for i in Vn:
        init_firstset(i)
    get_followset()
def addtodict(thedict, key_a, key_b, val): 
    if key_a in thedict:
        thedict[key_a].update({key_b: val})
    else:
        thedict.update({key_a:{key_b: val}})
def build_LLtalble():
    init_firstAndFollowSet()
    M=dict()
    for i in Vn:
        for p in G[i]:
            if p !='ε':
                for j in get_firstset(p).difference({'ε'}):
                    addtodict(M,i,j,p)
    for i in XVn:
        for j in followset[i]:
            addtodict(M,i,j,'ε')
    return M

M = build_LLtalble()
with open('input.txt','r') as f:
    S_,table = lexical_analyzer(f.read())
S=list()
for i in S_:
    if i[1] == table['标识符']:
        S.append(('i',i[1]))
    else:
        S.append(i)
AS = list()
AS.append('$')
AS.append('A')
i=0
while True:
    if AS[-1] in Vn:
        if S[i][0] in M[AS[-1]]:
            t = M[AS.pop()][S[i][0]]
            if t != 'ε':
                for j in range(len(t)-1,-1,-1):
                    AS.append(t[j])
        else:
            print('error')
            break
    elif AS[-1] in Vt:
        if AS[-1] == S[i][0]:
            if S[i][0]!='$':
                AS.pop()
                i+=1
        else: 
            print('error')
            break
    elif AS[-1] == '$':
        if AS[-1] == S[i][0]:
            if S[i][0]=='$':
                print('acc')
                break
        else:
            print('error')
            break







