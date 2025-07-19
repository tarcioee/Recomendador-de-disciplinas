from collections import Counter, defaultdict
from datetime import timedelta, datetime, date
from core.utils.horario import parse_horario, faixa_turno


def teste_exibir_recomendacoes_personalizadas(perfil, recomendador, ementario, disciplinas_feitas):
    linhas = []

    linhas.append("Você foi encaixado nos grupos: " + ', '.join(perfil.grupos))
    linhas.append("Com base nos seus dados, recomendamos as seguintes grades, nessa ordem:")

    ordem = determinar_ordem_grade_fuzzy(perfil)

    ajuste_limite = {
        "recomendada": 0,
        "mais fácil": -1,
        "desafiadora": 1,
    }

    for i, tipo in enumerate(ordem, start=1):
        limite = max(1, perfil.limite_disciplinas + ajuste_limite[tipo])
        linhas.append(f"\n{i}: Grade '{tipo}':")
        
        recomendadas = recomendador.recomendar(
            perfil.codigos_disciplinas_feitas,
            perfil.turnos_livres,
            perfil.professores_excluidos,
            limite
        )
        
        # Em vez de imprimir, criamos uma versão que retorna linhas para o resumo
        linhas.extend(grade_com_resumo_para_linhas(recomendadas, ementario, disciplinas_feitas))

    return "\n".join(linhas)

# core/utils/saida.py

def grade_com_resumo_para_linhas(grade, ementario, disciplinas_feitas):
    linhas = []

    # Se a grade estiver vazia, retorna uma mensagem
    if not grade:
        linhas.append("- Nenhuma disciplina pôde ser recomendada com os filtros atuais.")
        return linhas

    obrigatorias = 0
    optativas = 0
    dias_usados = set()
    turnos = Counter()
    total_blocos = 0
    dia_para_horas = {}

    for d, turma in grade:
        if d.obrigatoria:
            obrigatorias += 1
        else:
            optativas += 1

        for h in turma.horarios:
            parsed = parse_horario(h)
            if not parsed:
                continue
            dia, ini, fim = parsed
            dias_usados.add(dia)
            for nome_turno in ["matutino", "vespertino", "noturno"]:
                ini_t, fim_t = faixa_turno(nome_turno)
                if ini >= ini_t and fim <= fim_t:
                    turnos[nome_turno] += 1
                    total_blocos += 1
                    break
            if dia not in dia_para_horas:
                dia_para_horas[dia] = [ini, fim]
            else:
                dia_para_horas[dia][0] = min(dia_para_horas[dia][0], ini)
                dia_para_horas[dia][1] = max(dia_para_horas[dia][1], fim)

    #linhas.append(f"- Dias com aulas na semana: {len(dias_usados)}")
    
    total_horas_semana = 0
    for ini, fim in dia_para_horas.values():
        duracao = timedelta(hours=fim.hour, minutes=fim.minute) - timedelta(hours=ini.hour, minutes=ini.minute)
        total_horas_semana += duracao.total_seconds() / 3600
    #linhas.append(f"- Carga horária semanal no campus: {total_horas_semana:.2f} horas")


    if total_blocos > 0:
        dist_turnos = []
        for turno in ["matutino", "vespertino", "noturno"]:
            if turnos[turno] > 0:
                perc = (turnos[turno] / total_blocos) * 100
                dist_turnos.append(f" \n {turno.capitalize()}: {perc:.1f}%")
        if dist_turnos:
             linhas.append(f"- Distribuição por turno: " + ", ".join(dist_turnos))


    contagem_semestre = defaultdict(int)
    for d, _ in grade:
        if d.semestre is not None:
            contagem_semestre[d.semestre] += 1
    
    dist_semestres = []
    for s in sorted(contagem_semestre):
        dist_semestres.append(f"Semestre {s}: {contagem_semestre[s]}")
    if dist_semestres:
        linhas.append("- Semestre das disciplinas: " + ", ".join(dist_semestres))
    
    linhas.append(f"- Disciplinas optativas: {optativas}")

    feitas = set(disciplinas_feitas)
    # 'selecionadas' é o conjunto com os códigos das disciplinas da grade recomendada
    # 'feitas' é o conjunto com os códigos das disciplinas que o aluno já cursou
    selecionadas = {d.codigo for d, _ in grade}

    # Lista para guardar os nomes das disciplinas que foram totalmente desbloqueadas
    disciplinas_desbloqueadas = []

    # 1. Itera sobre todas as disciplinas do curso para encontrar as futuras
    for outra in ementario.disciplinas.values():

        # 2. Filtra apenas as que são obrigatórias e que o aluno ainda não fez (nem na grade atual)
        if not outra.obrigatoria or outra.codigo in feitas or outra.codigo in selecionadas:
            continue

        # 3. Garante que a disciplina futura tenha pré-requisitos a serem checados
        if not outra.pre_requisitos:
            continue

        # 4. Converte a lista de pré-requisitos da disciplina futura para um conjunto
        pre_requisitos_set = set(outra.pre_requisitos)

        # 5. AQUI ESTÁ A LÓGICA PRINCIPAL:
        #    Verifica se o conjunto de pré-requisitos é um subconjunto
        #    do conjunto de disciplinas selecionadas na grade.
        if pre_requisitos_set.issubset(selecionadas):
            disciplinas_desbloqueadas.append(outra.nome)

    # Por fim, formata a linha de impacto se alguma disciplina tiver sido desbloqueada.
    # Esta parte do código ficaria fora do loop.
    if disciplinas_desbloqueadas:
        # A variável 'impacto' é usada no seu código original para a saída
        impacto = []
        nomes_formatados = ", ".join(f"{nome}" for nome in disciplinas_desbloqueadas)
        impacto.append(f"- Destrava as seguintes obrigatórias: {nomes_formatados}")
        
        if impacto:
            linhas.append(f"".join(impacto))
        
    return linhas



def exibir_recomendacoes_personalizadas(perfil, recomendador, ementario, disciplinas_feitas):
    print("Você foi encaixado nos grupos:", ', '.join(perfil.grupos))
    print("Com base nos seus dados, recomendamos as seguintes grades, nessa ordem:")

    ordem = determinar_ordem_grade_fuzzy(perfil)

    # Mapear rótulos para ajuste do limite
    ajuste_limite = {
        "recomendada": 0,
        "mais fácil": -1,
        "desafiadora": 1,
    }
    i =0
    for tipo in ordem:
        i += 1
        limite = max(1,perfil.limite_disciplinas + ajuste_limite[tipo])
        print("limite", limite)
        print(f"\n{i}: Grade '{tipo}':")
        recomendadas = recomendador.recomendar(
            perfil.codigos_disciplinas_feitas,
            perfil.turnos_livres,
            perfil.professores_excluidos,
            limite
        )
        exibir_grade_com_resumo(recomendadas, ementario, disciplinas_feitas)


def determinar_ordem_grade_fuzzy(perfil):
    centroides = {
        "tempo_estudo": [8.75, 22.38, 33.75],
        "tempo_trabalho": [1.5, 27.7, 42.1],
        "tempo_transporte": [3.2, 9.7, 16.0],
    }

    pesos = {
        "tempo_estudo": 0.5,
        "tempo_trabalho": 0.3,
        "tempo_transporte": 0.2,
    }

    sobrecarga = 0.0

    for var, centros in centroides.items():
        valor = getattr(perfil, var)
        centro_leve = centros[0]
        centro_pesado = centros[-1]

        if var == "tempo_estudo":
            grau = (centro_leve - valor) / (centro_leve - centro_pesado)
        else:
            grau = (valor - centro_leve) / (centro_pesado - centro_leve)

        grau = min(max(grau, 0), 1)  # clamp
        sobrecarga += grau * pesos[var]

    if sobrecarga >= 0.5:
        return ["recomendada", "mais fácil", "desafiadora"]
    else:
        return ["recomendada", "desafiadora", "mais fácil"]


def exibir_grade(recomendadas):
    for disciplina, turma in recomendadas:
        professores = ', '.join(turma.professores)
        horarios = ', '.join(turma.horarios)
        print(f"{disciplina.nome} ({disciplina.codigo}) com {professores} no horário {horarios}")


def exibir_grade_com_resumo(grade, ementario, disciplinas_feitas):
    for i, (disciplina, turma) in enumerate(grade, 1):
        professores = ', '.join(turma.professores)
        horarios = ', '.join(turma.horarios)
        print(f"-{disciplina.nome} ({disciplina.codigo}) com {professores} no horário {horarios}")

    # 1. Contagem obrigatórias/optativas e dias usados
    obrigatorias = 0
    optativas = 0
    dias_usados = set()
    turnos = Counter()
    total_blocos = 0
    dia_para_horas = {}

    for d, turma in grade:
        if d.obrigatoria:
            obrigatorias += 1
        else:
            optativas += 1

        for h in turma.horarios:
            parsed = parse_horario(h)
            if not parsed:
                continue
            dia, ini, fim = parsed
            dias_usados.add(dia)
            for nome_turno in ["matutino", "vespertino", "noturno"]:
                ini_t, fim_t = faixa_turno(nome_turno)
                if ini >= ini_t and fim <= fim_t:
                    turnos[nome_turno] += 1
                    total_blocos += 1
                    break
            if dia not in dia_para_horas:
                dia_para_horas[dia] = [ini, fim]
            else:
                dia_para_horas[dia][0] = min(dia_para_horas[dia][0], ini)
                dia_para_horas[dia][1] = max(dia_para_horas[dia][1], fim)

    print("\n📊 Resumo:")
    print(f"- Dias da semana com aulas: {len(dias_usados)}")

    if total_blocos > 0:
        print("- Distribuição por turno:")
        for turno in ["matutino", "vespertino", "noturno"]:
            if turnos[turno] > 0:
                perc = (turnos[turno] / total_blocos) * 100
                print(f"  • {turno.capitalize()}: {perc:.1f}%")
    else:
        print("- Nenhum turno identificado nos horários.")

    total_horas_semana = 0
    for ini, fim in dia_para_horas.values():
        duracao = timedelta(hours=fim.hour, minutes=fim.minute) - timedelta(hours=ini.hour, minutes=ini.minute)
        total_horas_semana += duracao.total_seconds() / 3600
    print(f"- Carga horária semanal (presença no campus se nao voltar pra casa no meio): {total_horas_semana:.2f} horas")

    # 2. Disciplinas por semestre
    contagem_semestre = defaultdict(int)
    for d, _ in grade:
        if d.semestre is not None:
            contagem_semestre[d.semestre] += 1
    print("- Disciplinas por semestre:")
    for s in sorted(contagem_semestre):
        print(f"  • Semestre {s}: {contagem_semestre[s]} disciplina(s)")
    print(f"- Disciplinas optativas: {optativas}")

    # 3. Disciplinas com impacto futuro
    feitas = set(disciplinas_feitas)
    selecionadas = {d.codigo for d, _ in grade}
    impacto = []
    for cod in selecionadas:
        for outra in ementario.disciplinas.values():
            if not outra.obrigatoria or outra.codigo in feitas:
                continue
            if cod in outra.pre_requisitos:
                impacto.append(cod)
                break

    if impacto:
        print("- Disciplinas com impacto futuro (pré-requisito de obrigatórias ainda não feitas):")
        for cod in impacto:
            nome = ementario.disciplinas[cod].nome
            count = sum(
                1 for outra in ementario.disciplinas.values()
                if outra.obrigatoria and outra.codigo not in feitas and cod in outra.pre_requisitos
            )
            print(f"  • {nome} ({cod}) – pré de {count} obrigatória(s)")

    else:
        print("- Nenhuma disciplina da grade é pré-requisito de obrigatórias futuras.")
