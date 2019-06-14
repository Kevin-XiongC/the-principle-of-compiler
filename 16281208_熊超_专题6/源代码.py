from lexical_analyzer import lexical_analyzer
G={'E':['T','E+T','E-T'],'T':['F','T*F','T/F'],'F':['(E)','i'],'A':['V=E'],'V':['i']}
Vt={'+','-','/','i','*','(',')','=','$'}
Vn={'E','T','F','V','A'}
XVn=set()
I=list()
EVn=Vn.copy()
EVn.add('H')
EG=dict().fromkeys(EVn)
firstset = dict().fromkeys(Vn)
followset = dict().fromkeys(Vn)
def init_firstset(P):
    if len(firstset[P]):
        return firstset[P]
    for i in G[P]:
        if i[0] in Vt :
            firstset[P].add(i[0])
        elif i[0] in Vn:
            firstset[P]|=init_firstset(i[0])
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
    sum= 0
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
        firstset[i]=set()
    for i in Vn:
        init_firstset(i)
    get_followset()
def init_project():
    init_firstAndFollowSet()
    for i in EVn:
        EG[i]=list()
    EG['H'].extend(['·A','A·'])
    for i in Vn:
        for j in G[i]:
            EG[i].append('·'+j)
def get_closure(r,C):
    j= C[1].find('·')
    if j!=len(C[1])-1 and C[1][j+1] in Vn :
        for i in EG[C[1][j+1]]:
            r.add((C[1][j+1],i))
        for i in G[C[1][j+1]]:
            if (C[1][j+1],'·'+i) not in r:
                get_closure(r,(C[1][j+1],'·'+i))
    r.add(C)
def closure(C):
    while True:
        t = C.copy()
        for i in t:
            get_closure(C,i)
        if len(t) == len(C):
            break 
def Go(C,x):
    r = set()
    for i in C:
        j=i[1].find('·')
        if j!=len(i[1])-1 and i[1][j+1]==x:
            r.add((i[0],i[1][:j]+x+'·'+i[1][j+2:]))
    return r
GOTO=list()
ACTION=list()
def get_I():
    init_project()
    I.append(set())
    I[0].add(('H','·A'))
    closure(I[0])
    V = Vn|Vt
    GOTO.append(dict().fromkeys(V))
    ACTION.append(dict().fromkeys(Vt))
    i=0
    while True:
        for j in V:
            t = Go(I[i],j)
            if t :
                closure(t)
                if t not in I:
                    I.append(t)
                for k in range(len(I)-1,-1,-1):
                    if I[k] == t:
                        GOTO[i][j]=k
        i+=1
        if i ==len(I):
            break
        GOTO.append(dict().fromkeys(V))
        ACTION.append(dict().fromkeys(Vt))
    for i in range(len(GOTO)):
        for j in GOTO[i]:
            if j in Vt and GOTO[i][j] is not None:
                ACTION[i][j]=('s',GOTO[i][j])
    for i in range(len(I)):
        for j in I[i]:
            if j[1].find('·')==len(j[1])-1 and j[0] in Vn:
                for k in followset[j[0]]:
                    ACTION[i][k]=('r',(j[0],j[1][:-1]))
    for i in range(len(I)):
        if ('H','A·') in I[i]:
            ACTION[i]['$']='acc'
            break

with open('input.txt','r') as f:
    S,table = lexical_analyzer(f.read())
a = list()
for i in S:
    if i[1] == table['标识符']:
        a.append('i')
    else:
        a.append(i[0])
get_I()
status_s=list()
x=list()
x.append('$')
status_s.append(0)
syntax_value = list()
syntax_value.append(0)
i = m = t=0
result=list()
while True:
    if ACTION[status_s[m]][a[i]] is None:
        print('error')
        break
    elif ACTION[status_s[m]][a[i]][0]=='s':
        x.append(a[i])
        syntax_value.append(0)
        status_s.append(GOTO[status_s[m]][a[i]])
        m+=1
        i+=1
    elif ACTION[status_s[m]][a[i]][0]=='r':
        P = ACTION[status_s[m]][a[i]][1][1]
        A = ACTION[status_s[m]][a[i]][1][0]#A->P
        if P == 'i':
            syntax_value[m]=S[i-1][0]
        elif P == 'E+T' or P == 'E-T' or P=='T/F' or P=='T*F'  :
            result.append((P[1],syntax_value[m-2],syntax_value[m],'t'+str(t)))
            syntax_value[m-2]='t'+str(t)
            t+=1
        elif P== '(E)':
            syntax_value[m-2]=syntax_value[m-1]
        elif P == 'V=E':
            result.append((P[1],syntax_value[m],0,syntax_value[m-2]))
        for k in range(len(P)-1):
            x.pop()
            status_s.pop()
            syntax_value.pop()
            m-=1
        x.pop()
        status_s.pop()
        m-=1
        x.append(A)
        syntax_value.append(0)
        status_s.append(GOTO[status_s[m]][A])
        m+=1

    elif ACTION[status_s[m]][a[i]]=='acc':
        print('acc')
        for i in result:
            print(i)
        break




         
    









        


         
    






