import json
from core.dominio.turma import Turma
from core.utils.texto import normalizar

class GuiaMatricula:
    def __init__(self, path):
        self.turmas_disponiveis = self._carregar_turmas_guia(path)

    def _carregar_turmas_guia(self, path):
        with open(path, 'r', encoding='utf-8') as f:
            dados = json.load(f)

        turmas = []
        for entrada in dados:
            codigo = normalizar(entrada.get("Código"))
            nome = normalizar(entrada.get("Nome"))
            for turma in entrada.get("Turmas", []):
                professores = [normalizar(p) for p in turma.get("Professor", [])]
                horarios = [normalizar(h) for h in turma.get("Horário", [])]
                turmas.append(Turma(codigo, nome, professores, horarios))
        return turmas

    def get_turmas_disponiveis(self):
        return self.turmas_disponiveis
   
    def listar_todos_professores(self):
        """
        Retorna uma lista única com os nomes de todos os professores nas turmas disponíveis.
        """
        professores = set()
        for turma in self.get_turmas_disponiveis():
            professores.update(turma.professores)
        return sorted(professores)
