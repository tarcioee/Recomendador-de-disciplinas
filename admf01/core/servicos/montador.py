class MontadorDeGrade:

    def __init__(self, ementario, codigos_disciplinas_feitas, semestre):
        self.ementario = ementario
        self.codigos_disciplinas_feitas = set(codigos_disciplinas_feitas)
        self.contador_pre_requisitos = self._contar_pre_requisitos_obrigatorios_pendentes()

    def _contar_pre_requisitos_obrigatorios_pendentes(self):
        contador = {}
        for d in self.ementario.disciplinas.values():
            if not d.obrigatoria or d.codigo in self.codigos_disciplinas_feitas:
                continue
            for pre in d.pre_requisitos:
                if pre not in self.codigos_disciplinas_feitas:
                    contador[pre] = contador.get(pre, 0) + 1
        return contador

    def _tem_conflito_com_selecionadas(self, nova_turma, selecionadas):
        return any(nova_turma.tem_conflito_horario(t) for _, t in selecionadas)

    def _peso_prioridade(self, disciplina, semestre):
        obrigatoria = disciplina.obrigatoria
        impacto = self.contador_pre_requisitos.get(disciplina.codigo, 0)
        semestre = disciplina.semestre or 99
        return (not obrigatoria, -impacto, semestre)  # menor é melhor

    def selecionar_disciplinas(self, candidatas, limite):
        selecionadas = []  # lista final com disciplinas e turmas escolhidas
        disciplinas_adicionadas = set()  # guarda os códigos de disciplinas já adicionadas (evita duplicatas)

        # ordena as candidatas por prioridade: obrigatórias antes, maior impacto antes, menor semestre antes
        ordenadas = sorted(
            candidatas,
            key=lambda x: self._peso_prioridade(x[0], x[0].semestre or 99)
        )
        for disciplina, turma in ordenadas:
            if disciplina.codigo in disciplinas_adicionadas:
                continue  # já escolheu uma turma para essa disciplina → pula

            if self._tem_conflito_com_selecionadas(turma, selecionadas):
                continue  # essa turma conflita com alguma já escolhida → pula
            
            selecionadas.append((disciplina, turma))  # adiciona a disciplina e a turma selecionada
            disciplinas_adicionadas.add(disciplina.codigo)  # marca o código como já adicionado
            if len(selecionadas) == limite:
                break  # chegou ao número máximo permitido de disciplinas → para o laço
        
        return selecionadas  # retorna a lista final de (disciplina, turma) selecionadas
