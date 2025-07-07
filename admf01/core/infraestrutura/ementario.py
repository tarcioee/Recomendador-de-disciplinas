import json
from core.dominio.disciplina import Disciplina
from core.utils.texto import normalizar  # função que tira acentos e coloca em minúsculas

class Ementario:
    def __init__(self, path):
        self.disciplinas = self._carregar_ementario(path)

    def _carregar_ementario(self, path):
        with open(path, 'r', encoding='utf-8') as f:
            dados = json.load(f)

        disciplinas = {}
        nome_para_codigo = {}

        # Primeiro passo: mapear todos os nomes → códigos
        for entrada in dados:
            codigo = normalizar(entrada.get("Código"))
            nome = normalizar(entrada.get("Nome"))
            nome_para_codigo[nome] = codigo

        # Segundo passo: criar objetos Disciplina com pré-requisitos já convertidos
        for entrada in dados:
            codigo = normalizar(entrada.get("Código"))
            nome = normalizar(entrada.get("Nome"))
            obrigatoria = normalizar(entrada.get("Natureza", "Optativa")) == "obrigatoria"
            semestre = entrada.get("Semestre")

            pre_raw = entrada.get("Pré-requisitos obrigatórios", [])

            if isinstance(pre_raw, list) and len(pre_raw) == 1 and normalizar(pre_raw[0]) == "nao tem":
                pre_requisitos = []
            else:
                pre_requisitos = [
                    nome_para_codigo.get(normalizar(p), normalizar(p))
                    for p in pre_raw
                ]

            disciplinas[codigo] = Disciplina(
                codigo=codigo,
                nome=nome,
                obrigatoria=obrigatoria,
                pre_requisitos=pre_requisitos,
                semestre=semestre
            )

        return disciplinas

    def get_disciplina(self, codigo):
        codigo = normalizar(codigo)
        return self.disciplinas.get(codigo)

    def listar_disciplinas_por_semestre(self):
        """
        Retorna um dicionário {semestre: [lista de disciplinas]} para os semestres 1 a 10.
        """
        por_semestre = {s: [] for s in range(1, 11)}
        for disciplina in self.disciplinas.values():
            if disciplina.semestre in por_semestre:
                por_semestre[disciplina.semestre].append(disciplina)
        return por_semestre
    
    def listar_nomes_disciplinas_por_semestre(self):
        """
        Retorna um dicionário {semestre: [nomes das disciplinas]} para os semestres 1 a 10.
        """
        por_semestre = {s: [] for s in range(1, 11)}
        for disciplina in self.disciplinas.values():
            if disciplina.semestre in por_semestre:
                por_semestre[disciplina.semestre].append(disciplina.nome)
        return por_semestre
    
    def listar_nomes_codigos_por_semestre(self):
        """
        Retorna um dicionário {semestre: [nome (código)]} para os semestres 1 a 10.
        """
        por_semestre = {s: [] for s in range(1, 11)}
        for disciplina in self.disciplinas.values():
            if disciplina.semestre in por_semestre:
                entrada = f"{disciplina.nome} ({disciplina.codigo})"
                por_semestre[disciplina.semestre].append(entrada)
        return por_semestre


