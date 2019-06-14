G={'E':['E+T','E-T','T'],'T':['T*F','T/F','F'],'F':['(E)','i'],'H':['$E$']}
Vt={'+','-','/','i','*','$','(',')'}
Vn={'E','T','F','H'}
firstvt=dict().fromkeys(Vn)
lastvt=dict().fromkeys(Vn)
def get_firstvt(P):
    if len(firstvt[P]):
        return firstvt[P]
    for i in G[P]:
        if i[0] in Vt:
            firstvt[P].add(i[0])
        if len(i)>=2 and i[0] in Vn and i[1] in Vt:
            firstvt[P].add(i[1])
        if i[0] in Vn:
            firstvt[P]|=get_firstvt(i[0])
    return firstvt[P]
def get_lastvt(P):
    if len(lastvt[P]):
        return lastvt[P]
    for i in G[P]:
        if i[-1] in Vt:
            lastvt[P].add(i[-1])
        if len(i)>=2 and i[-1] in Vn and i[-2] in Vt:
            lastvt[P].add(i[-2])
        if i[-1] in Vn:
            lastvt[P]|=get_lastvt(i[-1])
    return lastvt[P]
def init_lastvt_firstvt():
    for i in Vn:
        firstvt[i]=set()
        lastvt[i]=set()
    for i in Vn:
        get_firstvt(i)
        get_lastvt(i)
def build_firstTalbe():
    init_lastvt_firstvt()
    table=dict().fromkeys(Vt)
    for i in Vt:
        table[i]=dict().fromkeys(Vt)
    for i in Vn:
        for j in G[i]:
            for k in range(0,len(j)-1):
                if j[k] in Vt and j[k+1] in Vt:
                    table[j[k]][j[k+1]]='='
                if k<len(j)-2 and j[k] in Vt and j[k+2] in Vt:
                    table[j[k]][j[k+2]]='='
                if j[k] in Vt and j[k+1] in Vn:
                    for x in firstvt[j[k+1]]:
                        table[j[k]][x]='<'
                if j[k] in Vn and j[k+1] in Vt:
                    for x in lastvt[j[k]]:
                        table[x][j[k+1]]='>'
    return table
table = build_firstTalbe()

G.update({'N':set()})
for i in Vn:
    t = G[i].copy()
    P = ''
    del G[i]
    for j in range(len(t)):
        P=list(t[j])
        for k in range(len(P)):
            if P[k] in Vn:
                P[k]='N'
        P = ''.join(P)
        for p in t:
            G['N'].add(P)
Vn={'N'}
S = list()
S.append('$')
i,j,k = 0,len(S)-1,len(S)-1
X = 'i+i*i$'
while True:
    if S[k] in Vn:
        j = k - 1
    else:
        j = k
    if table[S[j]][X[i]] == '<':
        S.append(X[i])
        i+=1
    elif table[S[j]][X[i]] == '=' or table[S[j]][X[i]] == '>':
        t = ''
        while S[j-1] in Vn:
            j-=1
        for p in Vn:
            for q in G[p]:
                if q ==''.join(S[j:k+1]):
                    t = (p,q)
                    break
            if t:
                break
        if t :
            for p in t[1]:
                S.pop()
            S.append(t[0])
        else:
            print('error')
            break
    k=len(S)-1
    if k == 1 and X[i]=='$':
        print('acc')
        break




