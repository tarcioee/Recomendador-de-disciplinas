def agrupar_usuario(tempo_transporte, tempo_trabalho, tempo_estudo):
    # centroides fixos
    grupos_transporte = {
        "próximos da ufba": 3.2,
        "longinhos da ufba": 9.7,
        "morador de cajazeiras 20": 16.0
    }

    grupos_trabalho = {
        "desempregados": 1.5,
        "trabalhadores": 27.7,
        "escala 7x0": 42.1
    }

    grupos_estudo = {
        "atarefados": 8.75,
        "estudiosos": 22.38,
        "cdfs": 33.75
    }

    def mais_proximo(valor, centroides):
        return min(centroides.items(), key=lambda x: abs(valor - x[1]))[0]

    grupo_transporte = mais_proximo(tempo_transporte, grupos_transporte)
    grupo_trabalho = mais_proximo(tempo_trabalho, grupos_trabalho)
    grupo_estudo = mais_proximo(tempo_estudo, grupos_estudo)

    return grupo_transporte, grupo_trabalho, grupo_estudo
