from flask import Flask, render_template, request
from core.infraestrutura.ementario import Ementario
from core.infraestrutura.guia_matricula import GuiaMatricula
from core.servicos.recomendador import Recomendador
from core.dominio.perfil_usuario import PerfilDoUsuario
from core.utils.calculos import calcular_limite_disciplinas
from core.utils.agrupar import agrupar_usuario
from core.utils.saida import teste_exibir_recomendacoes_personalizadas, determinar_ordem_grade_fuzzy
import os
 
app = Flask(__name__)
 
ementario = Ementario("dados/ementario.json")
guia = GuiaMatricula("dados/guia_de_matricula.json")
  
@app.route("/") 
def index():
    print("Carregando index.html")
    return render_template("index.html")

@app.route("/recomendar", methods=["POST"]) 
def recomendar():
    estudo = int(request.form['tempo_estudo']) 
    transporte = int(request.form['tempo_transporte']) 
    trabalho = int(request.form['tempo_trabalho'])
    #semestres = [int(s.strip()) for s in request.form['semestres_concluidos'].split(',') if s.strip().isdigit()]
    semestres = [int(s) for s in request.form.getlist('semestres_concluidos')]

    turnos = request.form.getlist('turnos_livres')
    print(turnos)
    professores = [p.strip() for p in request.form['professores_excluidos'].split(',') if p.strip()]
    codigos_feitos = [c.strip().lower() for c in request.form['codigos_disciplinas_feitas'].split(',') if c.strip()]

    limite = calcular_limite_disciplinas(estudo, transporte, trabalho)
    perfil = PerfilDoUsuario(
        turnos_livres=turnos,
        professores_excluidos=professores,
        codigos_disciplinas_feitas=codigos_feitos,
        semestres_concluidos=semestres,
        limite_disciplinas=limite,
        tempo_estudo=estudo,
        tempo_transporte=transporte,
        tempo_trabalho=trabalho
    )
    perfil.codigos_disciplinas_feitas = perfil.inferir_disciplinas_concluidas(ementario)
    perfil.grupos = agrupar_usuario(perfil.tempo_transporte, perfil.tempo_trabalho, perfil.tempo_estudo)

    recomendador = Recomendador(ementario, guia, perfil.semestres_concluidos)

    recomendacoes = []

    ordem = determinar_ordem_grade_fuzzy(perfil)
    ajuste_limite = {"recomendada": 0, "mais fácil": -1, "desafiadora": 1}

    for tipo in ordem:
        limite = max(1, perfil.limite_disciplinas + ajuste_limite[tipo])
        grade = recomendador.recomendar(
            perfil.codigos_disciplinas_feitas,
            perfil.turnos_livres,
            perfil.professores_excluidos,
            limite
        )
        disciplinas = []
        for disciplina, turma in grade:
            disciplinas.append({
                "nome": disciplina.nome,
                "codigo": disciplina.codigo,
                "professores": turma.professores,
                "horarios": turma.horarios,
            })
        recomendacoes.append({
            "tipo": tipo,
            "disciplinas": disciplinas
        })

    return render_template("recomendacoes.html",
                           grupos=perfil.grupos,
                           recomendacoes=recomendacoes)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
