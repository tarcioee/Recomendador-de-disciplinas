from core.utils.horario import parse_horario, faixa_turno

class FiltradorDeDisciplinas:
    def __init__(self, ementario, guia_matricula, semestres_concluidos):
        self.ementario = ementario
        self.guia = guia_matricula
        self.semestres_concluidos = semestres_concluidos

    def filtrar(self, codigos_disciplinas_feitas, turnos_livres, professores_excluidos):
        candidatas = []
        for turma in self.guia.get_turmas_disponiveis():
            if self._tem_prof_excluido(turma, professores_excluidos):
                continue
            if not self._horario_em_turno(turma.horarios, turnos_livres):
                continue

            disciplina = self.ementario.get_disciplina(turma.codigo_disciplina)
            if not disciplina:
                continue
            if not disciplina.tem_pre_requisitos_cumpridos(codigos_disciplinas_feitas):
                continue
            if disciplina.semestre is not None and disciplina.semestre in self.semestres_concluidos:
                continue
            if disciplina.codigo in codigos_disciplinas_feitas:
                 continue
            candidatas.append((disciplina, turma))
        return candidatas

    def _tem_prof_excluido(self, turma, lista):
        return any(p in lista for p in turma.professores)

    def _horario_em_turno(self, horarios, turnos_livres):
        for h in horarios:
            parsed = parse_horario(h)
            if not parsed:
                continue
            _, ini, fim = parsed
            if any(ini >= faixa_turno(turno)[0] and fim <= faixa_turno(turno)[1] for turno in turnos_livres):
                continue
            else:
                return False
        return True