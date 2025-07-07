from core.utils.horario import tem_conflito

class Turma:
    def __init__(self, codigo_disciplina, nome_disciplina, professores, horarios):
        self.codigo_disciplina = codigo_disciplina
        self.nome_disciplina = nome_disciplina
        self.professores = professores
        self.horarios = horarios

    def tem_conflito_horario(self, outra_turma):
        return tem_conflito(self.horarios, outra_turma.horarios)