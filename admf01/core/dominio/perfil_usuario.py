from dataclasses import dataclass
from typing import List

@dataclass
class PerfilDoUsuario:
    turnos_livres: List[str]
    professores_excluidos: List[str]
    codigos_disciplinas_feitas: List[str]
    semestres_concluidos: List[int]
    limite_disciplinas: int
    tempo_estudo: int  # em horas semanais
    tempo_transporte: int  # em horas semanais
    tempo_trabalho: int  # em horas semanais
    grupos: List[str] = None

    def inferir_disciplinas_concluidas(self, ementario):
        novas = set(self.codigos_disciplinas_feitas)
        for d in ementario.disciplinas.values():
            if d.semestre is not None and d.semestre in self.semestres_concluidos:
                novas.add(d.codigo)
        return list(novas)