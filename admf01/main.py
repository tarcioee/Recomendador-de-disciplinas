# main.py
from core.infraestrutura.ementario import Ementario
from core.infraestrutura.guia_matricula import GuiaMatricula
from core.servicos.recomendador import Recomendador
from core.dominio.perfil_usuario import PerfilDoUsuario 
from core.utils.calculos import calcular_limite_disciplinas
from core.utils.saida import exibir_grade, exibir_grade_com_resumo, exibir_recomendacoes_personalizadas
from core.utils.agrupar import agrupar_usuario
from core.utils.entrada import entrada_int, entrada_turnos_validos, entrada_lista_texto, entrada_lista_inteiros


#entradas de dados do usuário
entrada_estudo=300
entrada_transporte=7
entrada_trabalho=0
entrada_semestres_concluidos=2
entrada_turnos_livres=["matutino", "noturno"]
entrada_professores_excluidos=["teste nulo"]
entrada_codigos_disciplinas_feitas=[""]

def main_cli():
    ementario = Ementario("dados/ementario.json")
    guia = GuiaMatricula("dados/guia_de_matricula.json")

    print("====== Pinguim Seletor ======")

    estudo = entrada_int("Quanto tempo (horas/semana) você planeja disponibilizar para ESTUDAR, considerando tempo em sala? ", 0)
    transporte = entrada_int("Quanto tempo (horas/semana) você gastará com TRANSPORTE? ", 0)
    trabalho = entrada_int("Quanto tempo (horas/semana) você trabalhará/estagiará? ", 0)
    semestres = entrada_lista_inteiros("Quais semestres inteiros você já concluiu? ", 0)
    turnos = entrada_turnos_validos()
    professores = entrada_lista_texto("Professores a banir")
    codigos_feitos = entrada_lista_texto("Liste códigos das disciplinas já cursadas, separadas por vírgula (ou deixe vazio para nenhum)")

    total_disciplinas = calcular_limite_disciplinas(estudo, transporte, trabalho)

    perfil = PerfilDoUsuario(
        turnos_livres=turnos,
        professores_excluidos=professores, 
        codigos_disciplinas_feitas=codigos_feitos,
        semestres_concluidos=semestres,
        limite_disciplinas=total_disciplinas,
        tempo_estudo=estudo,
        tempo_transporte=transporte,
        tempo_trabalho=trabalho
    )
    perfil.codigos_disciplinas_feitas = perfil.inferir_disciplinas_concluidas(ementario)
    perfil.grupos = agrupar_usuario(perfil.tempo_transporte, perfil.tempo_trabalho, perfil.tempo_estudo)

    recomendador = Recomendador(ementario, guia, perfil.semestres_concluidos)

    exibir_recomendacoes_personalizadas(perfil, recomendador)


if __name__ == "__main__":
    main_cli()