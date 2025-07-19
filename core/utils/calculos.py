def calcular_limite_disciplinas(tempo_estudo, tempo_transporte, tempo_trabalho):
    base = 1.484064917 - (0.007378694056 * tempo_transporte) + (-0.02520904723 *tempo_trabalho) + 0.092882049 * (tempo_estudo)
    minimo_em_sala = tempo_estudo/ 3.66
    if base > minimo_em_sala:
        base = minimo_em_sala
    return min(8,max(1, int(base//1)))
