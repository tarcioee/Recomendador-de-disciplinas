from dataclasses import dataclass
from typing import List, Optional

@dataclass
class Disciplina:
    codigo: str
    nome: str
    obrigatoria: bool
    pre_requisitos: List[str]
    semestre: Optional[int] = None

    def tem_pre_requisitos_cumpridos(self, feitas):
        return all(pr in feitas for pr in self.pre_requisitos)

    def eh_obrigatoria(self):
        return self.obrigatoria
