from sys import stdin, stdout, stderr

from sys import argv

vchars_start = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
vchars = '_abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'

definitions = ['DEF_STR_CONSTANTS', 'DEF_WARNING', 'DEF_TRUNC', 'DEF_RANDOM', 'DEF_LENGTH', 'DEF_INDEXOF', 'DEF_PUSH', 'DEF_POP', 'DEF_QUEUE', 'DEF_UNQUEUE', 'DEF_POKE', 'DEF_PICK', 'DEF_DELETE', 'DEF_STR', 'DEF_PARSE_INT', 'DEF_BYTE_TO_HEXSTR', 'DEF_MATH_PI', 'DEF_MATH_SQRT', 'DEF_MATH_COS', 'DEF_MATH_SIN', 'DEF_MATH_ATAN2', 'DEF_MATH_LOG10', 'DEF_NOT', 'DEF_ISNULL', 'DEF_STRIP', 'DEF_SPLIT', 'DEF_SUBSTRING', 'DEF_CHAR_CODE_AT', 'DEF_STARTSWITH', 'DEF_ENDSWITH', 'DEF_LOWERCASE', 'DEF_UPPERCASE', 'DEF_CONCAT', 'DEF_SIGNED_32BITS', 'DEF_UNSIGNED_32BITS', 'DEF_USHR', 'DEF_GET_TYPE', 'DEF_IS_TYPE_NUM', 'DEF_IS_TYPE_BOOL', 'DEF_IS_TYPE_STR', 'DEF_IS_TYPE_LIST', 'DEF_IS_TYPE_DICT', 'DEF_IS_TYPE_NULL', 'DEF_CHR_QUOTE', 'DEF_CHR_SQUOTE', 'DEF_CHR_LF', 'DEF_CHR_CR', 'DEF_CHR_TAB']

def is_valid_var(v):
    if len(v) < 1: return False
    if v[0] == '`':
        if len(v) < 2: return False
        startidx = 1
    else:
        startidx = 0
    for j in range(startidx, len(v)):
        if v[j] not in vchars: return False
    return True

def sorted_by_length(l):
    sl = []
    for e in l:
        i = len(sl)
        for j in range(len(sl)):
            if len(sl[j]) <= len(e):
                i = j
                break
        sl.insert(i, e)
    return sl

def get_insvars(s):
    ivs = []
    ss = s.split('THIS.')
    for j1 in range(1, len(ss)):
        e = len(ss[j1])
        if e == 0: continue
        if ss[j1][0] == '`':
            if e == 1: continue
            b = 1
        else:
            b = 0
        for j2 in range(b, len(ss[j1])):
            if ss[j1][j2] not in vchars:
                e = j2
                break
        iv = ss[j1][0:e]
        ivs.append(iv)
    return ivs

def get_vars(s):
    vs = []
    s1 = s.split('`')
    for j1 in range(1, len(s1)):
        e = len(s1[j1])
        for j2 in range(len(s1[j1])):
            if s1[j1][j2] not in vchars:
                e = j2
                break
        v = s1[j1][0:e]
        vs.append('`'+v)
    return vs

def get_dot_vars(s):
    vs = []
    s1 = s.split('.')
    for j1 in range(1, len(s1)):
        e = len(s1[j1])
        if e == 0: continue
        if s1[j1][0] not in vchars_start: continue
        for j2 in range(1, len(s1[j1])):
            if s1[j1][j2] not in vchars:
                e = j2
                break
        v = s1[j1][0:e]
        vs.append(v)
    return vs

def create_vmaps(lines):
    vmap = {}
    vmap['defs'] = {}
    vmap['topvars'] = []
    vmap['functions'] = {}
    vmap['classes'] = {}
    vmap['mainvars'] = []
    strconsts = {}
    globalvars = []
    dotvars = []
    istack_type = 'empty'
    istack = []
    for line in lines:
        if line.strip() == '':
            continue
        if line.lstrip().startswith('COMMENT '):
            continue
        vs = get_dot_vars(line)
        for v in vs:
            if dotvars.count(v) == 0:
                dotvars.append(v)
        strsplits = line.split('"')
        if len(strsplits) > 1:
            if len(strsplits) % 2 != 1:
                print('ERROR: INVALID STRING:', line, end='', file=stderr)
                exit(1)
            for j in range(1, len(strsplits), 2):
                if strsplits[j] not in strconsts:
                    strconsts[strsplits[j]] = 0
                strconsts[strsplits[j]] += 1
        if line.startswith('DEF_'):
            tokens = line.strip().split(' ')
            if len(tokens) != 2:
                print('ERROR: INVALID DEFINITION:', line, end='', file=stderr)
                exit(1)
            if istack_type != 'empty':
                print('ERROR: UNEXPECTED DEFINITION:', line, end='', file=stderr)
                exit(1)
            if tokens[0] not in definitions:
                print('ERROR: UNKNOWN DEFINITION:', line, end='', file=stderr)
                exit(1)
            if tokens[0] in vmap['defs']:
                print('ERROR: DUPLICATE DEFINITION:', line, end='', file=stderr)
                exit(1)
            if not is_valid_var(tokens[1]):
                print('ERROR: INVALID DEFINITION:', line, end='', file=stderr)
                exit(1)
            if tokens[1] in globalvars:
                print('ERROR: DUPLICATE NAME: '+f'{tokens[1]}'+':', line, end='', file=stderr)
                exit(1)
            globalvars.append(tokens[1])
            vmap['defs'][tokens[0]] = tokens[1]
            continue
        if line.startswith('FUNC '):
            tokens = line.lstrip().split('(')[0].split(' ')
            if len(tokens) != 2 or not is_valid_var(tokens[1]):
                print('ERROR: INVALID FUNC:', line, end='', file=stderr)
                exit(1)
            if istack_type != 'empty':
                print('ERROR: UNEXPECTED FUNC:', line, end='', file=stderr)
                exit(1)
            func_name = tokens[1]
            if func_name in vmap['functions']:
                print('ERROR: DUPLICATE FUNC:', line, end='', file=stderr)
                exit(1)
            if func_name in globalvars:
                print('ERROR: DUPLICATE NAME: '+f'{func_name}'+':', line, end='', file=stderr)
                exit(1)
            globalvars.append(func_name)
            vmap['functions'][func_name] = {}
            vmap['functions'][func_name]['params'] = []
            vmap['functions'][func_name]['vars'] = []
            tokens = line.split('(')[1].split(')')[0].split(' ')
            if len(tokens) > 1 or len(tokens[0]) > 0:
                for token in tokens:
                    if not is_valid_var(token):
                        print('ERROR: INVALID VAR: '+f'{token}'+':', line, end='', file=stderr)
                        exit(1)
                    vmap['functions'][func_name]['params'].append(token)
            istack_type = 'func'
            istack.append(func_name)
            continue
        if line.rstrip() == 'ENDFUNC':
            if istack_type != 'func':
                print('ERROR: UNEXPECTED ENDFUNC:', line, end='', file=stderr)
                exit(1)
            istack_type = 'empty'
            istack.pop()
            continue
        if line.startswith('CLASS '):
            token = line.strip().split(' ')[1]
            if not token.endswith(':'):
                print('ERROR: INVALID CLASS:', line, end='', file=stderr)
                exit(1)
            if istack_type != 'empty':
                print('ERROR: UNEXPECTED CLASS:', line, end='', file=stderr)
                exit(1)
            token = token[:-1]
            if not is_valid_var(token):
                print('ERROR: INVALID CLASS:', line, end='', file=stderr)
                exit(1)
            if token in vmap['classes']:
                print('ERROR: DUPLICATE CLASS:', line, end='', file=stderr)
                exit(1)
            if token in globalvars:
                print('ERROR: DUPLICATE NAME: '+f'{token}'+':', line, end='', file=stderr)
                exit(1)
            globalvars.append(token)
            vmap['classes'][token] = {}
            vmap['classes'][token]['methods'] = {}
            vmap['classes'][token]['insvars'] = []
            istack_type = 'class'
            istack.append(token)
            continue
        if line.rstrip() == 'ENDCLASS':
            if istack_type != 'method':
                print('ERROR: UNEXPECTED ENDCLASS:', line, end='', file=stderr)
                exit(1)
            istack_type = 'empty'
            istack.clear()
            continue
        if line.startswith('  METHOD_INIT('):
            if istack_type != 'class':
                print('ERROR: UNEXPECTED METHOD_INIT:', line, end='', file=stderr)
                exit(1)
            vmap['classes'][istack[0]]['methods']['INIT'] = {}
            vmap['classes'][istack[0]]['methods']['INIT']['params'] = []
            vmap['classes'][istack[0]]['methods']['INIT']['vars'] = []
            vmap['classes'][istack[0]]['methods']['INIT']['closures'] = {}
            tokens = line.split('(')[1].split(')')[0].split(' ')
            if len(tokens) > 1 or len(tokens[0]) > 0:
                for token in tokens:
                    if not is_valid_var(token):
                        print('ERROR: INVALID VAR: '+f'{token}'+':', line, end='', file=stderr)
                        exit(1)
                    vmap['classes'][istack[0]]['methods']['INIT']['params'].append(token)
            istack_type = 'method'
            istack.append('INIT')
            continue
        if line.startswith('  METHOD '):
            if istack_type != 'method':
                print('ERROR: UNEXPECTED METHOD:', line, end='', file=stderr)
                exit(1)
            tokens = line.lstrip().split('(')[0].split(' ')
            if len(tokens) != 2 or not is_valid_var(tokens[1]):
                print('ERROR: INVALID METHOD:', line, end='', file=stderr)
                exit(1)
            method_name = tokens[1]
            if method_name in vmap['classes'][istack[0]]['methods']:
                print('ERROR: DUPLICATE METHOD:', line, end='', file=stderr)
                exit(1)
            if method_name not in globalvars:
                globalvars.append(method_name)
            vmap['classes'][istack[0]]['methods'][method_name] = {}
            vmap['classes'][istack[0]]['methods'][method_name]['params'] = []
            vmap['classes'][istack[0]]['methods'][method_name]['vars'] = []
            vmap['classes'][istack[0]]['methods'][method_name]['closures'] = {}
            tokens = line.split('(')[1].split(')')[0].split(' ')
            if len(tokens) > 1 or len(tokens[0]) > 0:
                for token in tokens:
                    if not is_valid_var(token):
                        print('ERROR: INVALID VAR: '+f'{token}'+':', line, end='', file=stderr)
                        exit(1)
                    vmap['classes'][istack[0]]['methods'][method_name]['params'].append(token)
            istack[1] = method_name
            continue
        if line.startswith('    CLOSURE '):
            if istack_type != 'method':
                print('ERROR: UNEXPECTED CLOSURE:', line, end='', file=stderr)
                exit(1)
            tokens = line.lstrip().split('(')[0].split(' ')
            if len(tokens) != 2 or not is_valid_var(tokens[1]):
                print('ERROR: INVALID CLOSURE:', line, end='', file=stderr)
                exit(1)
            closure_name = tokens[1]
            if closure_name in vmap['classes'][istack[0]]['methods'][istack[1]]['closures']:
                print('ERROR: DUPLICATE CLOSURE:', line, end='', file=stderr)
                exit(1)
            vmap['classes'][istack[0]]['methods'][istack[1]]['closures'][closure_name] = {}
            vmap['classes'][istack[0]]['methods'][istack[1]]['closures'][closure_name]['params'] = []
            vmap['classes'][istack[0]]['methods'][istack[1]]['closures'][closure_name]['vars'] = []
            tokens = line.split('(')[1].split(')')[0].split(' ')
            if len(tokens) > 1 or len(tokens[0]) > 0:
                for token in tokens:
                    if not is_valid_var(token):
                        print('ERROR: INVALID VAR: '+f'{token}'+':', line, end='', file=stderr)
                        exit(1)
                    vmap['classes'][istack[0]]['methods'][istack[1]]['closures'][closure_name]['params'].append(token)
            istack_type = 'closure'
            istack.append(closure_name)
            continue
        if line.rstrip() == '    ENDCLOSURE':
            if istack_type != 'closure':
                print('ERROR: UNEXPECTED ENDCLOSURE:', line, end='', file=stderr)
                exit(1)
            istack_type = 'method'
            istack.pop()
            continue
        if line.startswith('MAIN:'):
            if istack_type == 'class':
                print('ERROR: UNEXPECTED MAIN:', line, end='', file=stderr)
                exit(1)
            if istack_type == 'main':
                print('ERROR: DUPLICATE MAIN:', line, end='', file=stderr)
                exit(1)
            istack_type = 'main'
            istack.clear()
            continue
        if line.startswith('EXPORT('):
            continue
        indent = 0
        while line[indent] == ' ': indent += 1
        if line.lstrip().startswith('VAR '):
            if istack_type == 'class':
                print('ERROR: UNEXPECTED INDENT:', line, end='', file=stderr)
                exit(1)
            tokens = line.strip().split(' ')
            if not is_valid_var(tokens[1]):
                print('ERROR: INVALID VAR: '+f'{tokens[1]}'+':', line, end='', file=stderr)
                exit(1)
            if len(tokens) > 2 and tokens[2] != '=':
                print('ERROR: INVALID VAR DEF:', line, end='', file=stderr)
                exit(1)
            if tokens[1] in globalvars:
                print('ERROR: DUPLICATE NAME: '+f'{tokens[1]}'+':', line, end='', file=stderr)
                exit(1)
            if indent == 0:
                if istack_type == 'main':
                    print('ERROR: UNEXPECTED INDENT:', line, end='', file=stderr)
                    exit(1)
                istack_type = 'empty'
            if istack_type == 'empty':
                if indent != 0:
                    print('ERROR: UNEXPECTED INDENT:', line, end='', file=stderr)
                    exit(1)
                if tokens[1] in vmap['topvars']:
                    print('ERROR: DUPLICATE VAR: '+f'{tokens[1]}'+':', line, end='', file=stderr)
                    exit(1)
                vmap['topvars'].append(tokens[1])
                globalvars.append(tokens[1])
                continue
            if istack_type == 'func':
                if indent != 2:
                    print('ERROR: UNEXPECTED INDENT:', line, end='', file=stderr)
                    exit(1)
                if tokens[1] in vmap['functions'][istack[0]]['vars']:
                    print('ERROR: DUPLICATE VAR: '+f'{tokens[1]}'+':', line, end='', file=stderr)
                    exit(1)
                vmap['functions'][istack[0]]['vars'].append(tokens[1])
                if tokens[1] in vmap['functions'][istack[0]]['params']:
                    print('ERROR: DUPLICATE NAME: '+f'{tokens[1]}'+':', line, end='', file=stderr)
                    exit(1)
                continue
            if istack_type == 'method':
                if indent != 4:
                    print('ERROR: UNEXPECTED INDENT:', line, end='', file=stderr)
                    exit(1)
                if tokens[1] in vmap['classes'][istack[0]]['methods'][istack[1]]['vars']:
                    print('ERROR: DUPLICATE VAR: '+f'{tokens[1]}'+':', line, end='', file=stderr)
                    exit(1)
                vmap['classes'][istack[0]]['methods'][istack[1]]['vars'].append(tokens[1])
                if tokens[1] in vmap['classes'][istack[0]]['methods'][istack[1]]['params']:
                    print('ERROR: DUPLICATE NAME: '+f'{tokens[1]}'+':', line, end='', file=stderr)
                    exit(1)
                continue
            if istack_type == 'closure':
                if indent != 6:
                    print('ERROR: UNEXPECTED INDENT:', line, end='', file=stderr)
                    exit(1)
                if tokens[1] in vmap['classes'][istack[0]]['methods'][istack[1]]['closures'][istack[2]]['vars']:
                    print('ERROR: DUPLICATE VAR: '+f'{tokens[1]}'+':', line, end='', file=stderr)
                    exit(1)
                vmap['classes'][istack[0]]['methods'][istack[1]]['closures'][istack[2]]['vars'].append(tokens[1])
                if tokens[1] in vmap['classes'][istack[0]]['methods'][istack[1]]['params']:
                    print('ERROR: DUPLICATE NAME: '+f'{tokens[1]}'+':', line, end='', file=stderr)
                    exit(1)
                if tokens[1] in vmap['classes'][istack[0]]['methods'][istack[1]]['vars']:
                    print('ERROR: DUPLICATE NAME: '+f'{tokens[1]}'+':', line, end='', file=stderr)
                    exit(1)
                if tokens[1] in vmap['classes'][istack[0]]['methods'][istack[1]]['closures'][istack[2]]['params']:
                    print('ERROR: DUPLICATE NAME: '+f'{tokens[1]}'+':', line, end='', file=stderr)
                    exit(1)
                continue
            if istack_type == 'main':
                if indent != 2:
                    print('ERROR: UNEXPECTED INDENT:', line, end='', file=stderr)
                    exit(1)
                if tokens[1] in vmap['mainvars']:
                    print('ERROR: DUPLICATE VAR: '+f'{tokens[1]}'+':', line, end='', file=stderr)
                    exit(1)
                vmap['mainvars'].append(tokens[1])
                continue
            continue
        if istack_type == 'empty':
            continue
        if istack_type == 'func':
            if indent < 2:
                print('ERROR: UNEXPECTED INDENT:', line, end='', file=stderr)
                exit(1)
            continue
        if istack_type == 'class':
            print('ERROR: UNEXPECTED INDENT:', line, end='', file=stderr)
            exit(1)
        if istack_type == 'method':
            if indent < 4:
                print('ERROR: UNEXPECTED INDENT:', line, end='', file=stderr)
                exit(1)
            for iv in get_insvars(line):
                if iv not in vmap['classes'][istack[0]]['insvars']:
                    vmap['classes'][istack[0]]['insvars'].append(iv)
            continue
        if istack_type == 'closure':
            if indent < 6:
                print('ERROR: UNEXPECTED INDENT:', line, end='', file=stderr)
                exit(1)
            continue
        if istack_type == 'main':
            if indent < 2:
                print('ERROR: UNEXPECTED INDENT:', line, end='', file=stderr)
                exit(1)
            continue
        print('ERROR: UNEXPECTED LINE:', line, end='', file=stderr)
        exit(1)
        break
    for class_name in vmap['classes']:
        for method_name in vmap['classes'][class_name]['methods'].keys():
            if method_name in vmap['classes'][class_name]['insvars']:
                vmap['classes'][class_name]['insvars'].remove(method_name)
            for param in vmap['classes'][class_name]['methods'][method_name]['params']:
                if param in globalvars:
                    print('ERROR: DUPLICATE NAME: '+f'{param}'+': CLASS '+f'{class_name}'+"."+f'{method_name}', end='', file=stderr)
                    exit(1)
            for v in vmap['classes'][class_name]['methods'][method_name]['vars']:
                if v in globalvars:
                    print('ERROR: DUPLICATE NAME: '+f'{v}'+': CLASS '+f'{class_name}'+"."+f'{method_name}', end='', file=stderr)
                    exit(1)
            for closure_name in vmap['classes'][class_name]['methods'][method_name]['closures'].keys():
                for param in vmap['classes'][class_name]['methods'][method_name]['closures'][closure_name]['params']:
                    if param in globalvars:
                        print('ERROR: DUPLICATE NAME: '+f'{param}'+': CLASS '+f'{class_name}'+"."+f'{method_name}'+"."+f'{closure_name}', end='', file=stderr)
                        exit(1)
                for v in vmap['classes'][class_name]['methods'][method_name]['closures'][closure_name]['vars']:
                    if v in globalvars:
                        print('ERROR: DUPLICATE NAME: '+f'{v}'+': CLASS '+f'{class_name}'+"."+f'{method_name}'+"."+f'{closure_name}', end='', file=stderr)
                        exit(1)
    cipsmap = {}
    globalmap = {}
    localmap = {}
    localmap['functions'] = {}
    localmap['classes'] = {}
    localmap['mainvars'] = {}
    for d in vmap['defs']:
        if vmap['defs'][d][0] != "`": continue
        globalmap[vmap['defs'][d]] = "`def___"+vmap['defs'][d][1:]+"___name"
    for v in vmap['topvars']:
        if v[0] != "`": continue
        globalmap[v] = "`topvar___"+v[1:]+"___name"
    for f in vmap['functions']:
        if f[0] == "`":
            globalmap[f] = "`func___"+f[1:]+"___name"
            sf = f[1:]
        else:
            sf = f
        localmap['functions'][f] = {}
        for p in vmap['functions'][f]['params']:
            if p[0] == "`":
                localmap['functions'][f][p] = "`func___"+sf+"___param___"+p[1:]+"___name"
        for v in vmap['functions'][f]['vars']:
            if v[0] == "`":
                localmap['functions'][f][v] = "`func___"+sf+"___var___"+v[1:]+"___name"
    for c in vmap['classes']:
        if c[0] == "`":
            globalmap[c] = "`class___"+c[1:]+"___name"
            sc = c[1:]
        else:
            sc = c
        cipsmap[c] = []
        localmap['classes'][c] = {}
        localmap['classes'][c]['methods'] = {}
        localmap['classes'][c]['insvars'] = {}
        for m in vmap['classes'][c]['methods']:
            if m not in globalmap:
                if m[0] == "`":
                    globalmap[m] = "`method___"+m[1:]+"___name"
            if m[0] == "`":
                sm = m[1:]
            else:
                sm = m
            localmap['classes'][c]['methods'][m] = {}
            for p in vmap['classes'][c]['methods'][m]['params']:
                if p[0] == "`":
                    localmap['classes'][c]['methods'][m][p] = "`class___"+sc+"___method___"+sm+"___param___"+p[1:]+"___name"
                if m == 'INIT':
                    cipsmap[c].append(localmap['classes'][c]['methods'][m][p] if p[0] == "`" else p)
            for v in vmap['classes'][c]['methods'][m]['vars']:
                if v[0] == "`":
                    localmap['classes'][c]['methods'][m][v] = "`class___"+sc+"___method___"+sm+"___var___"+v[1:]+"___name"
            for l in vmap['classes'][c]['methods'][m]['closures']:
                if l[0] == "`":
                    localmap['classes'][c]['methods'][m][l] = "`class___"+sc+"___method___"+sm+"___closure___"+l[1:]+"___name"
                    sl = l[1:]
                else:
                    sl = l
                for p in vmap['classes'][c]['methods'][m]['closures'][l]['params']:
                    if p[0] == "`":
                        localmap['classes'][c]['methods'][m][p] = "`class___"+sc+"___method___"+sm+"___closure___"+sl+"___param___"+p[1:]+"___name"
                for v in vmap['classes'][c]['methods'][m]['closures'][l]['vars']:
                    if v[0] == "`":
                        localmap['classes'][c]['methods'][m][v] = "`class___"+sc+"___method___"+sm+"___closure___"+sl+"___var___"+v[1:]+"___name"
        for v in vmap['classes'][c]['insvars']:
            if v[0] == "`":
                localmap['classes'][c]['insvars'][v] = "`class___"+sc+"___insvar___"+v[1:]+"___name"
    for v in vmap['mainvars']:
        if v[0] != "`": continue
        localmap['mainvars'][v] = "`mainvar___"+v[1:]+"___name"
    if 'DEF_STR_CONSTANTS' in vmap['defs']:
        strconsts = sorted(strconsts.keys(), key=(lambda x: (-strconsts[x], x)))
    else:
        strconsts = []
    return [cipsmap, globalmap, localmap, strconsts, dotvars]

def alpha_convert(lines, vmaps):
    cipsmap = vmaps[0]
    globalmap = vmaps[1]
    localmap = vmaps[2]
    strconsts = vmaps[3]
    strconsts_dict_name = None
    globalkeys = sorted_by_length(globalmap.keys())
    activemap = globalmap
    activekeys = globalkeys
    alines = []
    istack_type = 'empty'
    istack = []
    for line in lines:
        if line.strip() == '':
            alines.append(line)
            continue
        if line.lstrip().startswith('COMMENT '):
            continue
        if line.startswith('DEF_STR_CONSTANTS '):
            dict_name = line.rstrip().split(' ')[1]
            if dict_name in activemap:
                dict_name = activemap[dict_name]
            aline = 'VAR '+f'{dict_name}'+' = {}\n'
            alines.append(aline)
            for j in range(0, len(strconsts)):
                aline = f'{dict_name}'+'['+f'{j}'+'] = "'+f'{strconsts[j]}'+'"\n'
                alines.append(aline)
            strconsts_dict_name = dict_name
            continue
        strsplits = line.split('"')
        if len(strsplits) > 1:
            aline = ''
            for j in range(0, len(strsplits)):
                if j % 2 == 0:
                    aline += strsplits[j]
                elif strconsts_dict_name is None:
                    aline += '"'+strsplits[j]+'"'
                else:
                    aline += f'{strconsts_dict_name}'+'['+str(strconsts.index(strsplits[j]))+']'
            line = aline
        if line.startswith('FUNC '):
            func_name = line.lstrip().split('(')[0].split(' ')[1]
            istack_type = 'func'
            istack.append(func_name)
            activemap = globalmap.copy()
            activekeys = globalkeys.copy()
            localkeys = []
            for k in localmap['functions'][func_name]:
                activemap[k] = localmap['functions'][func_name][k]
                localkeys.append(k)
            herekeys = localkeys.copy()
            aline = line
            if func_name in activemap:
                herekeys.append(func_name)
            for k in sorted_by_length(herekeys):
                aline = aline.replace(k, activemap[k])
            activekeys = sorted_by_length(activekeys+localkeys)
            alines.append(aline)
            continue
        if line.rstrip() == 'ENDFUNC':
            istack_type = 'empty'
            istack.pop()
            alines.append(line)
            continue
        if line.startswith('CLASS '):
            class_name = line.strip().split(' ')[1][:-1]
            istack_type = 'class'
            istack.append(class_name)
            aline = line
            if class_name in globalmap:
                aline = aline.replace(class_name, globalmap[class_name])
            if len(cipsmap[class_name]) > 0:
                cips = "("
                for p in cipsmap[class_name]:
                    cips += p+" "
                cips = cips[:-1]+"):"
            else:
                cips = "():"
            aline = aline.replace(":", cips)
            alines.append(aline)
            continue
        if line.rstrip() == 'ENDCLASS':
            istack_type = 'empty'
            istack.clear()
            alines.append(line)
            continue
        if line.startswith('  METHOD_INIT('):
            istack_type = 'method'
            istack.append('INIT')
            class_name = istack[0]
            method_name = istack[1]
            activemap = globalmap.copy()
            activekeys = globalkeys.copy()
            for k in localmap['classes'][class_name]['insvars']:
                activemap[k] = localmap['classes'][class_name]['insvars'][k]
                activekeys.append(k)
            localkeys = []
            for k in localmap['classes'][class_name]['methods'][method_name]:
                activemap[k] = localmap['classes'][class_name]['methods'][method_name][k]
                localkeys.append(k)
            localkeys = sorted_by_length(localkeys)
            aline = line
            for k in localkeys:
                aline = aline.replace(k, activemap[k])
            activekeys = sorted_by_length(activekeys+localkeys)
            alines.append(aline)
            continue
        if line.startswith('  METHOD '):
            method_name = line.lstrip().split('(')[0].split(' ')[1]
            istack[1] = method_name
            class_name = istack[0]
            activemap = globalmap.copy()
            activekeys = globalkeys.copy()
            for k in localmap['classes'][class_name]['insvars']:
                activemap[k] = localmap['classes'][class_name]['insvars'][k]
                activekeys.append(k)
            localkeys = []
            for k in localmap['classes'][class_name]['methods'][method_name]:
                activemap[k] = localmap['classes'][class_name]['methods'][method_name][k]
                localkeys.append(k)
            herekeys = localkeys.copy()
            aline = line
            if method_name in activemap:
                herekeys.append(method_name)
            for k in sorted_by_length(herekeys):
                aline = aline.replace(k, activemap[k])
            activekeys = sorted_by_length(activekeys+localkeys)
            alines.append(aline)
            continue
        if line.startswith('MAIN:'):
            istack_type = 'main'
            istack.clear()
            activemap = globalmap.copy()
            activekeys = globalkeys.copy()
            for k in localmap['mainvars']:
                activemap[k] = localmap['mainvars'][k]
                activekeys.append(k)
            activekeys = sorted_by_length(activekeys)
            aline = line
            alines.append(aline)
            continue
        aline = line
        vs = get_vars(aline)
        for v in sorted_by_length(vs):
            if not (v in activekeys): continue
            aline = replace_keyword(aline, v, activemap[v])
        alines.append(aline)
        continue
    hvs = {}
    for aline in alines:
        vs = get_vars(aline)
        for v in vs:
            if v not in hvs:
                hvs[v] = 1
                continue
            hvs[v] += 1
            if not v.endswith('___name'):
                print('WARNING: NOT FOUND:', f'{v}', aline, end='', file=stderr)
    hkeys = sorted(hvs.keys(), key=(lambda x: (-hvs[x], x)))
    hlines = []
    for aline in alines:
        vs = get_vars(aline)
        if len(vs) == 0:
            hlines.append(aline)
            continue
        hline = aline
        for v in sorted_by_length(vs):
            hline = hline.replace(v, '_'+str(hkeys.index(v)))
        hlines.append(hline)
    return hlines

def replace_keyword(line, kwfrom, kwto):
    splits = line.split(kwfrom)
    rline = splits[0]
    for j in range(1, len(splits)):
        if len(splits[j]) == 0 and (j != len(splits)-1):
            print('ERROR: UNEXPECTED '+f'{kwfrom}'+':', line, end='', file=stderr)
            exit(1)
        if (len(splits[j-1]) > 0 and splits[j-1][-1] in vchars) or (len(splits[j]) > 0 and splits[j][0] in vchars):
            rline += kwfrom+splits[j]
        else:
            rline += kwto+splits[j]
    return rline

def generate_js_definition(def_type, def_name):
    if def_type == "DEF_WARNING":
        return ('var '+f'{def_name}'+' = function(__1, __2) {\n  console["log"](__1, __2);\n};\n')
    if def_type == "DEF_TRUNC":
        return ('var '+f'{def_name}'+' = function(__1) {\n  return ~~(__1);\n};\n')
    if def_type == "DEF_RANDOM":
        return ('var '+f'{def_name}'+' = function() {\n  return Math["random"]();\n};\n')
    if def_type == "DEF_LENGTH":
        return ('var '+f'{def_name}'+' = function(__1) {\n  return __1["length"];\n};\n')
    if def_type == "DEF_INDEXOF":
        return ('var '+f'{def_name}'+' = function(__1, __2) {\n  return __1["indexOf"](__2);\n};\n')
    if def_type == "DEF_PUSH":
        return ('var '+f'{def_name}'+' = function(__1, __2) {\n  __1["push"](__2);\n};\n')
    if def_type == "DEF_POP":
        return ('var '+f'{def_name}'+' = function(__1) {\n  return __1["pop"]();\n};\n')
    if def_type == "DEF_QUEUE":
        return ('var '+f'{def_name}'+' = function(__1, __2) {\n  __1["unshift"](__2);\n};\n')
    if def_type == "DEF_UNQUEUE":
        return ('var '+f'{def_name}'+' = function(__1) {\n  return __1["shift"]();\n};\n')
    if def_type == "DEF_POKE":
        return ('var '+f'{def_name}'+' = function(__1, __2, __3) {\n  __1["splice"](__2, 0, __3);\n};\n')
    if def_type == "DEF_PICK":
        return ('var '+f'{def_name}'+' = function(__1, __2) {\n  return __1["splice"](__2, 1)[0];\n};\n')
    if def_type == "DEF_DELETE":
        return ('var '+f'{def_name}'+' = function(__1, __2) {\n  delete __1[__2];\n};\n')
    if def_type == "DEF_STR":
        return ('var '+f'{def_name}'+' = function(__1) {\n  return ""+__1;\n};\n')
    if def_type == "DEF_PARSE_INT":
        return ('var '+f'{def_name}'+' = function(__1, __2) {\n  return parseInt(__1, __2);\n};\n')
    if def_type == "DEF_BYTE_TO_HEXSTR":
        return ('var '+f'{def_name}'+' = function(__1) {\n  var __2 = __1["toString"](16); return (__2["length"] != 1 ? __2 : "0"+__2);\n};\n')
    if def_type == "DEF_MATH_PI":
        return ('var '+f'{def_name}'+' = function() {\n  return self["Math"]["PI"];\n};\n')
    if def_type == "DEF_MATH_SQRT":
        return ('var '+f'{def_name}'+' = function(__1) {\n  return self["Math"]["sqrt"](__1);\n};\n')
    if def_type == "DEF_MATH_COS":
        return ('var '+f'{def_name}'+' = function(__1) {\n  return self["Math"]["cos"](__1);\n};\n')
    if def_type == "DEF_MATH_SIN":
        return ('var '+f'{def_name}'+' = function(__1) {\n  return self["Math"]["sin"](__1);\n};\n')
    if def_type == "DEF_MATH_ATAN2":
        return ('var '+f'{def_name}'+' = function(__1, __2) {\n  return self["Math"]["atan2"](__1, __2);\n};\n')
    if def_type == "DEF_MATH_LOG10":
        return ('var '+f'{def_name}'+' = function(__1) {\n  return self["Math"]["log10"](__1);\n};\n')
    if def_type == "DEF_NOT":
        return ('var '+f'{def_name}'+' = function(__1) {\n  return (! __1);\n};\n')
    if def_type == "DEF_ISNULL":
        return ('var '+f'{def_name}'+' = function(__1) {\n  return (__1 === null);\n};\n')
    if def_type == "DEF_STRIP":
        return ('var '+f'{def_name}'+' = function(__1) {\n  return __1["trim"]();\n};\n')
    if def_type == "DEF_SPLIT":
        return ('var '+f'{def_name}'+' = function(__1, __2) {\n  return __1["split"](__2);\n};\n')
    if def_type == "DEF_SUBSTRING":
        return ('var '+f'{def_name}'+' = function(__1, __2, __3) {\n  return __1["substring"](__2, __3);\n};\n')
    if def_type == "DEF_CHAR_CODE_AT":
        return ('var '+f'{def_name}'+' = function(__1, __2) {\n  return __1["charCodeAt"](__2);\n};\n')
    if def_type == "DEF_STARTSWITH":
        return ('var '+f'{def_name}'+' = function(__1, __2) {\n  return __1["startsWith"](__2);\n};\n')
    if def_type == "DEF_ENDSWITH":
        return ('var '+f'{def_name}'+' = function(__1, __2) {\n  return __1["endsWith"](__2);\n};\n')
    if def_type == "DEF_LOWERCASE":
        return ('var '+f'{def_name}'+' = function(__1) {\n  return __1["toLowerCase"]();\n};\n')
    if def_type == "DEF_UPPERCASE":
        return ('var '+f'{def_name}'+' = function(__1) {\n  return __1["toUpperCase"]();\n};\n')
    if def_type == "DEF_CONCAT":
        return ('var '+f'{def_name}'+' = function(__1, __2) {\n  return __1["concat"](__2);\n};\n')
    if def_type == "DEF_SIGNED_32BITS":
        return ('var '+f'{def_name}'+' = function(__1) {\n  return (__1 | 0);\n};\n')
    if def_type == "DEF_UNSIGNED_32BITS":
        return ('var '+f'{def_name}'+' = function(__1) {\n  __1 = (__1 | 0); return (__1 < 0 ? __1+0x100000000 : __1);\n};\n')
    if def_type == "DEF_USHR":
        return ('var '+f'{def_name}'+' = function(__1, __2) {\n  return (__1 >>> __2);\n};\n')
    if def_type == "DEF_GET_TYPE":
        return ('var '+f'{def_name}'+' = function(__1) {\n  return Object["prototype"]["toString"]["call"](__1);\n};\n')
    if def_type == "DEF_IS_TYPE_NUM":
        return ('var '+f'{def_name}'+' = function(__1) {\n  return (__1 == "[object Number]");\n};\n')
    if def_type == "DEF_IS_TYPE_BOOL":
        return ('var '+f'{def_name}'+' = function(__1) {\n  return (__1 == "[object Boolean]");\n};\n')
    if def_type == "DEF_IS_TYPE_STR":
        return ('var '+f'{def_name}'+' = function(__1) {\n  return (__1 == "[object String]");\n};\n')
    if def_type == "DEF_IS_TYPE_LIST":
        return ('var '+f'{def_name}'+' = function(__1) {\n  return (__1 == "[object Array]");\n};\n')
    if def_type == "DEF_IS_TYPE_DICT":
        return ('var '+f'{def_name}'+' = function(__1) {\n  return (__1 == "[object Object]");\n};\n')
    if def_type == "DEF_IS_TYPE_NULL":
        return ('var '+f'{def_name}'+' = function(__1) {\n  return (__1 == "[object Null]");\n};\n')
    if def_type == "DEF_CHR_QUOTE":
        return (f'{def_name}'+' = String["fromCharCode"](34);\n')
    if def_type == "DEF_CHR_SQUOTE":
        return (f'{def_name}'+' = String["fromCharCode"](39);\n')
    if def_type == "DEF_CHR_LF":
        return (f'{def_name}'+' = String["fromCharCode"](10);\n')
    if def_type == "DEF_CHR_CR":
        return (f'{def_name}'+' = String["fromCharCode"](13);\n')
    if def_type == "DEF_CHR_TAB":
        return (f'{def_name}'+' = String["fromCharCode"](9);\n')
    print('ERROR: DEFINITION NOT IMPLEMENTED: '+f'{def_type}'+':', file=stderr)
    exit(1)

def replace_js_keywords(line):
    if len(line.split('THIS')) > 1:
        line = replace_keyword(line, 'THIS', 'this')
    if len(line.split('NULL')) > 1:
        line = replace_keyword(line, 'NULL', 'null')
    if len(line.split('TRUE')) > 1:
        line = replace_keyword(line, 'TRUE', 'true')
    if len(line.split('FALSE')) > 1:
        line = replace_keyword(line, 'FALSE', 'false')
    if len(line.split('AND')) > 1:
        line = replace_keyword(line, 'AND', '&&')
    if len(line.split('OR')) > 1:
        line = replace_keyword(line, 'OR', '||')
    splits = line.split('TERNARY{')
    if len(splits) > 1:
        sline = splits[0]
        for j in range(1, len(splits)):
            if len(splits[j-1]) > 0 and (splits[j-1][-1] in vchars):
                sline += 'TERNARY{'+splits[j]
                continue
            ssplits = splits[j].split('}')
            if len(ssplits) < 4 or len(ssplits[0]) <= 0 or len(ssplits[1]) <= 1 or len(ssplits[2]) <= 1 or ssplits[1][0] != '{' or ssplits[2][0] != '{':
                print('WARNING: INVALID TERNARY?:', line, end='', file=stderr)
                sline += 'TERNARY{'+splits[j]
                continue
            sline += '('+ssplits[0]+' ? '+ssplits[1][1:]+' : '+ssplits[2][1:]+')'+ssplits[3]
            for j2 in range(4, len(ssplits)):
                sline += '}'+ssplits[j2]
        line = sline
    return line

def generate_js_dotvars(lines, dotvars):
    if len(dotvars) == 0:
        return lines
    total = 0
    alines = []
    for line in lines:
        vs = get_dot_vars(line)
        if len(vs) == 0:
            alines.append(line)
            continue
        uvs = []
        for v in sorted(vs, reverse=True):
            if uvs.count(v) == 0:
                uvs.append(v)
        aline = line
        for v in uvs:
            total += 1
            splits = aline.split('.'+f'{v}')
            sline = splits[0]
            for j in range(1, len(splits)):
                sline += '["'+f'{v}'+'"]'+splits[j]
            aline = sline
        alines.append(aline)
    return alines

def generate_js(lines, mapped_str_constants):
    jlines = []
    jlines.append('(function() {\n')
    istack_type = 'empty'
    istack = []
    for line in lines:
        if line.strip() == '':
            jlines.append(line)
            continue
        if len(line.split('"')) > 1 and mapped_str_constants:
            jlines.append(line)
            continue
        if line.startswith('DEF_'):
            tokens = line.strip().split(' ')
            jlines.append(generate_js_definition(tokens[0], tokens[1]))
            continue
        if line.startswith('FUNC '):
            func_name = line.lstrip().split('(')[0].split(' ')[1]
            istack_type = 'func'
            istack.append(func_name)
            jline = 'var '+f'{func_name}'+' = function('
            params = line.split('(')[1].split(')')[0].split(' ')
            if len(params) > 1 or len(params[0]) > 0:
                jline += params.pop(0)
                for p in params:
                    jline += ', '+p
            jline += ') {\n'
            jlines.append(jline)
            continue
        if line.rstrip() == 'ENDFUNC':
            istack_type = 'empty'
            istack.pop()
            jline = '};\n'
            jlines.append(jline)
            continue
        if line.startswith('CLASS '):
            class_name = line.lstrip().split('(')[0].split(' ')[1]
            istack_type = 'class'
            istack.append(class_name)
            jline = 'var '+f'{class_name}'+' = function('
            params = line.split('(')[1].split(')')[0].split(' ')
            if len(params) > 1 or len(params[0]) > 0:
                jline += params.pop(0)
                for p in params:
                    jline += ', '+p
            jline += ') {\n'
            jlines.append(jline)
            continue
        if line.rstrip() == 'ENDCLASS':
            istack_type = 'empty'
            istack.clear()
            jline = '};\n'
            jlines.append(jline)
            continue
        if line.startswith('  METHOD_INIT('):
            istack_type = 'method'
            istack.append('INIT')
            continue
        if line.startswith('  METHOD '):
            if istack[1] == 'INIT':
                jline = '    return this;\n'
                jlines.append(jline)
            jline = '};\n'
            jlines.append(jline)
            class_name = istack[0]
            method_name = line.lstrip().split('(')[0].split(' ')[1]
            params = line.split('(')[1].split(')')[0].split(' ')
            istack[1] = method_name
            if method_name[0] == '_' and method_name[1:].isdigit():
                jline = f'{class_name}'+'["prototype"].'+f'{method_name}'+' = function('
            else:
                jline = f'{class_name}'+'["prototype"]["'+f'{method_name}'+'"] = function('
            if len(params) > 1 or len(params[0]) > 0:
                jline += params.pop(0)
                for p in params:
                    jline += ', '+p
            jline += ') {\n'
            jlines.append(jline)
            continue
        if line.startswith('    CLOSURE '):
            closure_name = line.lstrip().split('(')[0].split(' ')[1]
            params = line.split('(')[1].split(')')[0].split(' ')
            istack_type = 'closure'
            istack.append(closure_name)
            jline = '    var '+f'{closure_name}'+' = function('
            if len(params) > 1 or len(params[0]) > 0:
                jline += params.pop(0)
                for p in params:
                    jline += ', '+p
            jline += ') {\n'
            jlines.append(jline)
            continue
        if line.rstrip() == '    ENDCLOSURE':
            istack_type = 'method'
            istack.pop()
            jline = '    };\n'
            jlines.append(jline)
            continue
        if line.startswith('MAIN:'):
            if istack_type == 'func' or istack_type == 'method':
                jline = '};\n'
                jlines.append(jline)
            istack_type = 'main'
            istack.clear()
            continue
        if line.startswith('EXPORT('):
            params = '('.join(line.split('(')[1:]).split(')')[0].split(' ')
            jline = 'return ['
            if len(params) > 1 or len(params[0]) > 0:
                jline += params.pop(0)
                for p in params:
                    jline += ', '+p
            jline += '];\n'
            jlines.append(jline)
            continue
        if istack_type == 'main':
            continue
        if line.strip() == 'ENDIF':
            indent = 0
            while line[indent] == ' ': indent += 1
            jline = line[0:indent]+'}\n'
            jlines.append(jline)
            continue
        if line.strip() == 'ENDFOR':
            indent = 0
            while line[indent] == ' ': indent += 1
            jline = line[0:indent]+'}\n'
            jlines.append(jline)
            continue
        if line.strip() == 'ENDWHILE':
            indent = 0
            while line[indent] == ' ': indent += 1
            jline = line[0:indent]+'}\n'
            jlines.append(jline)
            continue
        if line.strip() == 'ELSE:':
            indent = 0
            while line[indent] == ' ': indent += 1
            jline = line[0:indent]+'}\n'+line[0:indent]+'else {\n'
            jlines.append(jline)
            continue
        if line.lstrip().startswith('VAR '):
            indent = 0
            while line[indent] == ' ': indent += 1
            line = line[0:indent]+'var '+line[indent+len('VAR '):]
        if len(line.split(' NEW ')) == 2:
            splits = line.split(' NEW ')
            line = splits[0]+' new '+splits[1]
        line = replace_js_keywords(line)
        if line.lstrip().startswith('IF ') and line.rstrip().endswith(':'):
            indent = 0
            while line[indent] == ' ': indent += 1
            line = line[0:indent]+'if ('+line[indent+len('IF '):].rstrip()[:-1]+') {\n'
        if line.lstrip().startswith('ELSIF ') and line.rstrip().endswith(':'):
            indent = 0
            while line[indent] == ' ': indent += 1
            line = line[0:indent]+'}\n'+line[0:indent]+'else if ('+line[indent+len('ELSIF '):].rstrip()[:-1]+') {\n'
        if line.lstrip().startswith('FORINCR ') and line.rstrip().endswith('):'):
            indent = 0
            while line[indent] == ' ': indent += 1
            tokens = line.lstrip().split('(')[0].split(' ')
            if len(tokens) != 2:
                print('ERROR: INVALID FORINCR:', line, end='', file=stderr)
                exit(1)
            for_var = tokens[1]
            tokens = '('.join(line.split('(')[1:]).rstrip()[:-2].split(' ')
            if len(tokens) != 2:
                print('ERROR: INVALID FORINCR:', line, end='', file=stderr)
                exit(1)
            line = line[0:indent]+'for ('+f'{for_var}'+' = '+f'{tokens[0]}'+'; '+f'{for_var}'+' < '+f'{tokens[1]}'+'; ++'+f'{for_var}'+') {\n'
        if line.lstrip().startswith('FORDECR ') and line.rstrip().endswith('):'):
            indent = 0
            while line[indent] == ' ': indent += 1
            tokens = line.lstrip().split('(')[0].split(' ')
            if len(tokens) != 2:
                print('ERROR: INVALID FORDECR:', line, end='', file=stderr)
                exit(1)
            for_var = tokens[1]
            tokens = '('.join(line.split('(')[1:]).rstrip()[:-2].split(' ')
            if len(tokens) != 2:
                print('ERROR: INVALID FORDECR:', line, end='', file=stderr)
                exit(1)
            line = line[0:indent]+'for ('+f'{for_var}'+' = '+f'{tokens[0]}'+'; '+f'{for_var}'+' >= '+f'{tokens[1]}'+'; --'+f'{for_var}'+') {\n'
        if line.lstrip().startswith('FOREACH ') and line.rstrip().endswith('):'):
            indent = 0
            while line[indent] == ' ': indent += 1
            tokens = line.lstrip().split('(')[0].split(' ')
            if len(tokens) != 2:
                print('ERROR: INVALID FOREACH:', line, end='', file=stderr)
                exit(1)
            for_var = tokens[1]
            for_dict = '('.join(line.split('(')[1:]).rstrip()[:-2]
            line = line[0:indent]+'for ('+f'{for_var}'+' in '+f'{for_dict}'+') {\n'
        if line.lstrip().startswith('WHILE ') and line.rstrip().endswith(':'):
            indent = 0
            while line[indent] == ' ': indent += 1
            line = line[0:indent]+'while ('+line[indent+len('WHILE '):].rstrip()[:-1]+') {\n'
        if not line.endswith(';\n'):
            if line.strip() != '}' and not line.endswith('{\n'):
                line = line.rstrip()+';\n'
        jlines.append(line)
    jlines.append('})();\n')
    return jlines

def generate_py_definition(def_type, def_name):
    if def_type == "DEF_WARNING":
        return ('from sys import stderr\ndef '+f'{def_name}'+'(__1, __2): print(__1, __2, file=stderr)\n')
    if def_type == "DEF_TRUNC":
        return ('from math import trunc as '+f'{def_name}'+'\n')
    if def_type == "DEF_RANDOM":
        return ('from random import random as '+f'{def_name}'+'\n')
    if def_type == "DEF_LENGTH":
        return ('def '+f'{def_name}'+'(__1): return len(__1)\n')
    if def_type == "DEF_INDEXOF":
        return ('def '+f'{def_name}'+'(__1, __2):\n  try:\n    __3 = __1.index(__2)\n  except ValueError:\n    __3 = -1\n  return __3\n')
    if def_type == "DEF_PUSH":
        return ('def '+f'{def_name}'+'(__1, __2): __1.append(__2)\n')
    if def_type == "DEF_POP":
        return ('def '+f'{def_name}'+'(__1): return __1.pop()\n')
    if def_type == "DEF_QUEUE":
        return ('def '+f'{def_name}'+'(__1, __2): __1.insert(0, __2)\n')
    if def_type == "DEF_UNQUEUE":
        return ('def '+f'{def_name}'+'(__1): return __1.pop(0)\n')
    if def_type == "DEF_POKE":
        return ('def '+f'{def_name}'+'(__1, __2, __3): __1.insert(__2, __3)\n')
    if def_type == "DEF_PICK":
        return ('def '+f'{def_name}'+'(__1, __2): return __1.pop(__2)\n')
    if def_type == "DEF_DELETE":
        return ('def '+f'{def_name}'+'(__1, __2): __1.pop(__2)\n')
    if def_type == "DEF_STR":
        return ('def '+f'{def_name}'+'(__1): return str(__1)\n')
    if def_type == "DEF_PARSE_INT":
        return ('def '+f'{def_name}'+'(__1, __2): return int(__1, __2)\n')
    if def_type == "DEF_BYTE_TO_HEXSTR":
        return ('def '+f'{def_name}'+'(__1): return ("%02x" % __1)\n')
    if def_type == "DEF_MATH_PI":
        return ('def '+f'{def_name}'+'():\n  from math import pi as _pi\n  return _pi\n')
    if def_type == "DEF_MATH_SQRT":
        return ('from math import sqrt as '+f'{def_name}'+'\n')
    if def_type == "DEF_MATH_COS":
        return ('from math import cos as '+f'{def_name}'+'\n')
    if def_type == "DEF_MATH_SIN":
        return ('from math import sin as '+f'{def_name}'+'\n')
    if def_type == "DEF_MATH_ATAN2":
        return ('from math import atan2 as '+f'{def_name}'+'\n')
    if def_type == "DEF_MATH_LOG10":
        return ('from math import log10 as '+f'{def_name}'+'\n')
    if def_type == "DEF_NOT":
        return ('def '+f'{def_name}'+'(__1): return (not __1)\n')
    if def_type == "DEF_ISNULL":
        return ('def '+f'{def_name}'+'(__1): return (__1 is None)\n')
    if def_type == "DEF_STRIP":
        return ('def '+f'{def_name}'+'(__1): return __1.strip()\n')
    if def_type == "DEF_SPLIT":
        return ('def '+f'{def_name}'+'(__1, __2): return __1.split(__2)\n')
    if def_type == "DEF_SUBSTRING":
        return ('def '+f'{def_name}'+'(__1, __2, __3): return __1[__2:__3]\n')
    if def_type == "DEF_CHAR_CODE_AT":
        return ('def '+f'{def_name}'+'(__1, __2): return ord(__1[__2])\n')
    if def_type == "DEF_STARTSWITH":
        return ('def '+f'{def_name}'+'(__1, __2): return __1.startswith(__2)\n')
    if def_type == "DEF_ENDSWITH":
        return ('def '+f'{def_name}'+'(__1, __2): return __1.endswith(__2)\n')
    if def_type == "DEF_LOWERCASE":
        return ('def '+f'{def_name}'+'(__1): return __1.lower()\n')
    if def_type == "DEF_UPPERCASE":
        return ('def '+f'{def_name}'+'(__1): return __1.upper()\n')
    if def_type == "DEF_CONCAT":
        return ('def '+f'{def_name}'+'(__1, __2): return (__1+__2)\n')
    if def_type == "DEF_SIGNED_32BITS":
        return ('def '+f'{def_name}'+'(__1): __1 = __1 & 0xffffffff; return (__1-0x100000000 if __1 > 0x7fffffff else __1)\n')
    if def_type == "DEF_UNSIGNED_32BITS":
        return ('def '+f'{def_name}'+'(__1): __1 = __1 & 0xffffffff; return (__1+0x100000000 if __1 < 0 else __1)\n')
    if def_type == "DEF_USHR":
        return ('def '+f'{def_name}'+'(__1, __2): return (__1 >> __2)\n')
    if def_type == "DEF_GET_TYPE":
        return ('def '+f'{def_name}'+'(__1): return type(__1)\n')
    if def_type == "DEF_IS_TYPE_NUM":
        return ('def '+f'{def_name}'+'(__1): return __1 is type(1) or __1 is type(1.0)\n')
    if def_type == "DEF_IS_TYPE_BOOL":
        return ('def '+f'{def_name}'+'(__1): return __1 is type(True)\n')
    if def_type == "DEF_IS_TYPE_STR":
        return ('def '+f'{def_name}'+'(__1): return __1 is type("")\n')
    if def_type == "DEF_IS_TYPE_LIST":
        return ('def '+f'{def_name}'+'(__1): return __1 is type([])\n')
    if def_type == "DEF_IS_TYPE_DICT":
        return ('def '+f'{def_name}'+'(__1): return __1 is type({})\n')
    if def_type == "DEF_IS_TYPE_NULL":
        return ('def '+f'{def_name}'+'(__1): return __1 is type(None)\n')
    if def_type == "DEF_CHR_QUOTE":
        return (f'{def_name}'+' = chr(34)\n')
    if def_type == "DEF_CHR_SQUOTE":
        return (f'{def_name}'+' = chr(39)\n')
    if def_type == "DEF_CHR_LF":
        return (f'{def_name}'+' = chr(10)\n')
    if def_type == "DEF_CHR_CR":
        return (f'{def_name}'+' = chr(13)\n')
    if def_type == "DEF_CHR_TAB":
        return (f'{def_name}'+' = chr(9)\n')
    print('ERROR: DEFINITION NOT IMPLEMENTED: '+f'{def_type}'+':', file=stderr)
    exit(1)

def replace_py_keywords(line):
    if len(line.split('THIS')) > 1:
        line = replace_keyword(line, 'THIS', 'self')
    if len(line.split('NULL')) > 1:
        line = replace_keyword(line, 'NULL', 'None')
    if len(line.split('TRUE')) > 1:
        line = replace_keyword(line, 'TRUE', 'True')
    if len(line.split('FALSE')) > 1:
        line = replace_keyword(line, 'FALSE', 'False')
    if len(line.split('AND')) > 1:
        line = replace_keyword(line, 'AND', 'and')
    if len(line.split('OR')) > 1:
        line = replace_keyword(line, 'OR', 'or')
    splits = line.split('TERNARY{')
    if len(splits) > 1:
        sline = splits[0]
        for j in range(1, len(splits)):
            if len(splits[j-1]) > 0 and (splits[j-1][-1] in vchars):
                sline += 'TERNARY{'+splits[j]
                continue
            ssplits = splits[j].split('}')
            if len(ssplits) < 4 or len(ssplits[0]) <= 0 or len(ssplits[1]) <= 1 or len(ssplits[2]) <= 1 or ssplits[1][0] != '{' or ssplits[2][0] != '{':
                print('WARNING: INVALID TERNARY?:', line, end='', file=stderr)
                sline += 'TERNARY{'+splits[j]
                continue
            sline += '('+ssplits[1][1:]+' if '+ssplits[0]+' else '+ssplits[2][1:]+')'+ssplits[3]
            for j2 in range(4, len(ssplits)):
                sline += '}'+ssplits[j2]
        line = sline
    return line

def generate_py(lines, mapped_str_constants):
    plines = []
    istack_type = 'empty'
    istack = []
    for line in lines:
        if line.strip() == '':
            plines.append(line)
            continue
        if len(line.split('"')) > 1 and mapped_str_constants:
            plines.append(line)
            continue
        if line.startswith('DEF_'):
            tokens = line.strip().split(' ')
            plines.append(generate_py_definition(tokens[0], tokens[1]))
            continue
        if line.startswith('FUNC '):
            func_name = line.lstrip().split('(')[0].split(' ')[1]
            istack_type = 'func'
            istack.append(func_name)
            pline = 'def '+f'{func_name}'+'('
            params = line.split('(')[1].split(')')[0].split(' ')
            if len(params) > 1 or len(params[0]) > 0:
                pline += params.pop(0)
                for p in params:
                    pline += ', '+p
            pline += '):\n'
            plines.append(pline)
            continue
        if line.rstrip() == 'ENDFUNC':
            istack_type = 'empty'
            istack.pop()
            continue
        if line.startswith('CLASS '):
            class_name = line.lstrip().split('(')[0].split(' ')[1]
            istack_type = 'class'
            istack.append(class_name)
            plines.append('class '+f'{class_name}'+'(object):\n')
            continue
        if line.rstrip() == 'ENDCLASS':
            istack_type = 'empty'
            istack.clear()
            continue
        if line.startswith('  METHOD_INIT('):
            params = line.split('(')[1].split(')')[0].split(' ')
            istack_type = 'method'
            istack.append('INIT')
            pline = '  def __init__(self'
            if len(params) > 1 or len(params[0]) > 0:
                for p in params:
                    pline += ', '+p
            pline += '):\n'
            plines.append(pline)
            continue
        if line.startswith('  METHOD '):
            method_name = line.lstrip().split('(')[0].split(' ')[1]
            params = line.split('(')[1].split(')')[0].split(' ')
            istack[1] = method_name
            pline = '  def '+f'{method_name}'+'(self'
            if len(params) > 1 or len(params[0]) > 0:
                for p in params:
                    pline += ', '+p
            pline += '):\n'
            plines.append(pline)
            continue
        if line.startswith('    CLOSURE '):
            closure_name = line.lstrip().split('(')[0].split(' ')[1]
            params = line.split('(')[1].split(')')[0].split(' ')
            istack_type = 'closure'
            istack.append(closure_name)
            pline = '    def '+f'{closure_name}'+'('
            if len(params) == 1 and len(params[0]) > 0:
                pline += params[0]
            if len(params) > 1:
                pline += params[0]
                for j in range(1, len(params)):
                    pline += ', '+params[j]
            pline += '):\n'
            plines.append(pline)
            continue
        if line.rstrip() == '    ENDCLOSURE':
            istack_type = 'method'
            istack.pop()
            continue
        if line.startswith('MAIN:'):
            istack_type = 'main'
            istack.clear()
            plines.append('if __name__ == "__main__":\n')
            continue
        if line.startswith('EXPORT('):
            continue
        if line.strip() == 'ENDIF':
            continue
        if line.strip() == 'ENDFOR':
            continue
        if line.strip() == 'ENDWHILE':
            continue
        if line.strip() == 'ELSE:':
            indent = 0
            while line[indent] == ' ': indent += 1
            pline = line[0:indent]+'else:\n'
            plines.append(pline)
            continue
        if line.lstrip().startswith('VAR '):
            if len(line.strip().split(' ')) == 2:
                continue
            indent = 0
            while line[indent] == ' ': indent += 1
            line = line[0:indent]+line[indent+len('VAR '):]
        if len(line.split(' NEW ')) == 2:
            splits = line.split(' NEW ')
            line = splits[0]+' '+splits[1]
        line = replace_py_keywords(line)
        if line.lstrip().startswith('IF ') and line.rstrip().endswith(':'):
            indent = 0
            while line[indent] == ' ': indent += 1
            line = line[0:indent]+'if '+line[indent+len('IF '):]
        if line.lstrip().startswith('ELSIF ') and line.rstrip().endswith(':'):
            indent = 0
            while line[indent] == ' ': indent += 1
            line = line[0:indent]+'elif '+line[indent+len('ELSIF '):]
        if line.lstrip().startswith('FORINCR ') and line.rstrip().endswith('):'):
            indent = 0
            while line[indent] == ' ': indent += 1
            tokens = line.lstrip().split('(')[0].split(' ')
            if len(tokens) != 2:
                print('ERROR: INVALID FORINCR:', line, end='', file=stderr)
                exit(1)
            for_var = tokens[1]
            tokens = '('.join(line.split('(')[1:]).rstrip()[:-2].split(' ')
            if len(tokens) != 2:
                print('ERROR: INVALID FORINCR:', line, end='', file=stderr)
                exit(1)
            line = line[0:indent]+'for '+f'{for_var}'+' in range('+f'{tokens[0]}'+', '+f'{tokens[1]}'+'):\n'
        if line.lstrip().startswith('FORDECR ') and line.rstrip().endswith('):'):
            indent = 0
            while line[indent] == ' ': indent += 1
            tokens = line.lstrip().split('(')[0].split(' ')
            if len(tokens) != 2:
                print('ERROR: INVALID FORDECR:', line, end='', file=stderr)
                exit(1)
            for_var = tokens[1]
            tokens = '('.join(line.split('(')[1:]).rstrip()[:-2].split(' ')
            if len(tokens) != 2:
                print('ERROR: INVALID FORDECR:', line, end='', file=stderr)
                exit(1)
            line = line[0:indent]+'for '+f'{for_var}'+' in range('+f'{tokens[0]}'+', '+f'{tokens[1]}'+'-1, -1):\n'
        if line.lstrip().startswith('FOREACH ') and line.rstrip().endswith('):'):
            indent = 0
            while line[indent] == ' ': indent += 1
            tokens = line.lstrip().split('(')[0].split(' ')
            if len(tokens) != 2:
                print('ERROR: INVALID FOREACH:', line, end='', file=stderr)
                exit(1)
            for_var = tokens[1]
            for_dict = '('.join(line.split('(')[1:]).rstrip()[:-2]
            line = line[0:indent]+'for '+f'{for_var}'+' in '+f'{for_dict}'+':\n'
        if line.lstrip().startswith('WHILE ') and line.rstrip().endswith(':'):
            indent = 0
            while line[indent] == ' ': indent += 1
            line = line[0:indent]+'while '+line[indent+len('WHILE '):]
        plines.append(line)
    return plines

def print_usage(argv0):
    print("Usage: python3.9 "+f'{argv0}'+" { --js | --py } < source.urc", file=stderr)

if __name__ == '__main__':
    if len(argv) != 2 or argv[1] not in ["--js", "--py"]:
        print_usage(argv[0])
        exit(1)
    lang = argv[1][2:]
    lines = []
    line = stdin.readline()
    while len(line) > 0:
        lines.append(line)
        line = stdin.readline()
    vmaps = create_vmaps(lines)
    lines = alpha_convert(lines, vmaps)
    mapped_str_constants = (len(vmaps[3]) > 0)
    if lang == "js":
        lines = generate_js(lines, mapped_str_constants)
        lines = generate_js_dotvars(lines, vmaps[4])
    else:
        lines = generate_py(lines, mapped_str_constants)
    for line in lines:
        print(line, end='', file=stdout)
