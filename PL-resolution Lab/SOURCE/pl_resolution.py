import re
def parse_PL_sentences(sentence):
    # split all the blank space
    res = re.split(' +', sentence)
    res = [literal for literal in res if literal != 'OR' and literal != '']
    return res

def read_input(path):
    lst_queries = []
    KB = []
    file = open(path, 'rt')
    num_queries = int(file.readline().splitlines()[0])
    for i in range(num_queries):
        query = file.readline().splitlines()[0]
        query = parse_PL_sentences(query)
        lst_queries.append(query)

    num_axiom = int(file.readline().splitlines()[0])
    for i in range(num_axiom):
        axiom = file.readline().splitlines()[0]
        axiom = parse_PL_sentences(axiom)
        KB.append(axiom)
    return KB, lst_queries

def find_contrast(lst_literal_01, lst_literal_02):
    lst_contrast = []
    for literal in lst_literal_01:
        if literal[0] == '-':
            contrast = literal[-1]
        else:
            contrast = f'-{literal}'
        if contrast in lst_literal_02:
            lst_contrast.append(literal)
            lst_contrast.append(contrast)
    return lst_contrast

def resolve(literals_01, literals_02):
    #literals_01 = parse_PL_sentences(sentence_01)
    #literals_02 = parse_PL_sentences(sentence_02)

    literals = literals_01 + literals_02
    literals = list(dict.fromkeys(literals))
    lst_constrast = find_contrast(literals_01, literals_02)
    if not lst_constrast or len(lst_constrast) > 2:
        return []
    resol = [literal for literal in literals if literal not in lst_constrast]
    if not resol:
        resol.append('{}')
    return resol

def negative_queries(queries):
    queries = [item for sub in queries for item in sub]
    for i in range(len(queries)):
        if queries[i][0] == '-':
            queries[i] = [queries[i][1]]
        else:
            queries[i] = [f'-{queries[i]}']
    return queries

def PL_Resolution(KB, queries):
    clauses = KB + negative_queries(queries)
    clauses = [tuple(clauses[i]) for i in range(len(clauses))]
    new = set()
    lst_res = []
    while True:
        n = len(clauses)
        pairs = [(clauses[i], clauses[j])
            for i in range(n) for j in range(i+1, n)]
        res = []
        for (ci, cj) in pairs:
            ci, cj = list(ci), list(cj)
            resol = resolve(ci, cj)
            if resol == ['{}']:
                res.append('{}')
                lst_res.append(res)
                return True, lst_res
        if resol != [] and resol != ['{}']:
            if resol not in res and tuple(resol) not in clauses:
                res.append(resol)
            new = new.union([tuple(resol)])

    lst_res.append(res)
    if new.issubset(set(clauses)):
        return False, lst_res
    for c in new:
        if c not in clauses:
            clauses.append(c)

def combination(lst_literals):
    if lst_literals == '{}':
        return '{}'
    sentence = f'{lst_literals[0]}'
    for i in range(1, len(lst_literals)):
        sentence += f' OR {lst_literals[i]}'
    return sentence

def write_output(input_path, output_path):
    KB, lst_queries = read_input(input_path)
    res, lst_res = PL_Resolution(KB, lst_queries)
    file = open(output_path, 'w')
    n = len(lst_res)
    for i in range(n):
        m = len(lst_res[i])
        file.write(f'{m}\n')
        for j in range(m):
            sentence = combination(lst_res[i][j])
            file.write(f'{sentence}\n')
  
    if res == True:
        file.write('YES')
    if res == False:
        file.write('NO')

write_output('testcase01.txt', 'resultcase01.txt')
write_output('testcase02.txt', 'resultcase02.txt')
write_output('testcase03.txt', 'resultcase03.txt')
write_output('testcase04.txt', 'resultcase04.txt')
write_output('testcase05.txt', 'resultcase05.txt')