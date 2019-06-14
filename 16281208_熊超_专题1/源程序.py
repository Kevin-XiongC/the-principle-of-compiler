def lexical_analyzer(source):
    import re
    max_length = 32
    reserve_word = { 'auto', 'break', 'case', 'char', 'const', 'continue',
        'default', 'do', 'double', 'else', 'enum', 'extern',
        'float', 'for', 'goto', 'if', 'int', 'long',
        'register', 'return', 'short', 'signed', 'sizeof', 'static',
        'struct', 'switch', 'typedef', 'union', 'unsigned', 'void',
        'volatile', 'while'}
    operatorORdelimiter = {"+","-","*","/","<","<=",">",">=","=","==","+=","-=","/=",
    "!=",";","(",")","^",",","\"","\'","#","&",
    "&&","|","||","%","~","<<",">>","[","]","{","}","\\",".","?",":","!",'++','--','*=','$'}
    other = {'常数','标识符'}
    all_signs = reserve_word.union(operatorORdelimiter).union(other)
    table = dict.fromkeys(all_signs)
    for i,value in enumerate(all_signs):
        table[value] = i+1
    #fliter the notes
    source = re.sub('//.*','',source)
    source = re.sub('/\*.*\*/','',source)
    #fliter /n and /f
    source = re.sub(r'\n|\f','',source) + '$'
    #scanner begin
    t=''
    i=0
    output = list()
    while source[i] != '$':
        if source[i].isspace():
            i = i + 1
            pass
        elif source[i].isalpha():
            while source[i].isalnum():
                t = t + source[i]
                i = i + 1
            if len(t)>max_length:
                print('标识符过长')
                break
            if t in reserve_word:
                output.append((t,table[t]))
            else:
                output.append((t,table['标识符']))
            t = ''
        elif source[i].isdigit():
            while source[i].isdigit():
                t = t + source[i]
                i = i + 1
            output.append((t,table['常数']))
            t = ''
        else:
            if source[i] == '<':
                if source[i+1] =='=':
                    output.append(('<'+'=',table['<=']))
                    i = i + 2
                elif source[i+1] == '<':
                    output.append(('<'+'<',table['<<']))
                    i = i + 2
                else:
                    output.append(('<',table['<']))
                    i = i + 1
            elif source[i] == '=':
                if source[i+1] =='=':
                    output.append(('='+'=',table['==']))
                    i = i + 2
                else:
                    output.append(('=',table['=']))
                    i = i + 1
            elif source[i] == '<':
                if source[i+1] =='=':
                    output.append(('>'+'=',table['>=']))
                    i = i + 2
                elif source[i+1] == '>':
                    output.append(('>'+'>',table['>>']))
                    i = i + 2
                else:
                    output.append(('<',table['<']))
                    i = i + 1
            elif source[i] == '/':
                if source[i+1] == '=':
                    output.append(('/'+'=',table['/=']))
                    i = i + 2
                else:
                    output.append(('/',table['/']))
                    i = i + 1
            elif source[i] == '+':
                if source[i+1] =='=':
                    output.append(('+'+'=',table['+=']))
                    i = i + 2
                elif source[i+1] == '+':
                    output.append(('+'+'+',table['++']))
                    i = i + 2
                else:
                    output.append(('+',table['+']))
                    i = i + 1
            elif source[i] == '-':
                if source[i+1] =='=':
                    output.append(('-'+'=',table['-=']))
                    i = i + 2
                elif source[i+1] == '-':
                    output.append(('-'+'-',table['--']))
                    i = i + 2
                else:
                    output.append(('-',table['-']))
                    i = i + 1
            elif source[i] == '*':
                if source[i+1] =='=':
                    output.append(('*'+'=',table['*=']))
                    i = i + 2
                else:
                    output.append(('*',table['*']))
                    i = i + 1
            elif source[i] == '/':
                if source[i+1] =='=':
                    output.append(('/'+'=',table['/=']))
                    i = i + 2
                else:
                    output.append(('/',table['/']))
                    i = i + 1
            elif source[i] == '!':
                if source[i+1] =='=':
                    output.append(('!'+'=',table['!=']))
                    i = i + 2
                else:
                    output.append(('!',table['!']))
            elif source[i] == '&':
                if source[i+1] =='&':
                    output.append(('&'+'&',table['&&']))
                    i = i + 2
                else:
                    output.append(('&',table['&']))
                    i = i + 1
            elif source[i] == '|':
                if source[i+1] =='|':
                    output.append(('|'+'|',table['||']))
                    i = i + 2
                else:
                    output.append(('|',table['|']))
                    i = i + 1
            elif source[i] in operatorORdelimiter:
                output.append((source[i],table[source[i]]))
                i = i + 1
            else:
                print('不认识',source[i])
                i+=1

    if source[i] == '$':
        with open('output.txt','w+') as f:
            for i in output:
                f.write('%s %d\n'%(i[0],i[1]))
        output.append(('$', table['$']))
        print('词法分析成功')
    return output,table

with open('input.txt','r') as f:
    lexical_analyzer(f.read())            
            

                



        
                    

