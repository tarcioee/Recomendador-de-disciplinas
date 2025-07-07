from core.servicos.filtrador import FiltradorDeDisciplinas
from core.servicos.montador import MontadorDeGrade

class Recomendador:
    def __init__(self, ementario, guia_matricula, semestres_concluidos):
        self.ementario = ementario
        self.guia = guia_matricula
        self.semestres_concluidos = semestres_concluidos

    def recomendar(self, codigos_disciplinas_feitas, turnos_livres, professores_excluidos, limite):
        filtrador = FiltradorDeDisciplinas(
            self.ementario, self.guia, self.semestres_concluidos
        )
        candidatas = filtrador.filtrar(
            codigos_disciplinas_feitas, turnos_livres, professores_excluidos
        )

        montador = MontadorDeGrade(self.ementario, codigos_disciplinas_feitas, self.semestres_concluidos)
        selecionadas = montador.selecionar_disciplinas(candidatas, limite)

        return selecionadas
