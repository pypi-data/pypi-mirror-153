def numero_multiplos(a,b,c):
    lista = []
    for i in range(a,b+1):
        if i%c == 0:
            lista.append(i)
    max = max(lista)
    min = min(lista)
    numero = ((max - min)/c) + 1 
    return numero

