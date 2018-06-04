import random

def converterQBIT_Maximize_Func(cromossomo):
    cromossomoClassico = []
    for qbit in cromossomo:
        rand = random.random()
        if rand > qbit[0] ** 2: # Minimiza funcao. > Maximiza funcao
            cromossomoClassico.append(1)
        else:
            cromossomoClassico.append(0)

    return cromossomoClassico

def converterQBIT_Minimize_Func(cromossomo):
    cromossomoClassico = []
    for qbit in cromossomo:
        rand = random.random()
        if rand < qbit[0] ** 2: # Minimiza funcao. > Maximiza funcao
            cromossomoClassico.append(1)
        else:
            cromossomoClassico.append(0)

    return cromossomoClassico




setFunction = {
    'min': converterQBIT_Minimize_Func,
    'max': converterQBIT_Maximize_Func
}