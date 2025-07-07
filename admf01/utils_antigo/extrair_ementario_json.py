# Versão ajustada: detecta campos com startswith para maior robustez contra formatações inconsistentes
def processar_bloco_disciplina_flexivel(bloco_linhas):
    disciplina = {}
    i = 0

    def extrair_valor(linha_idx):
        return bloco_linhas[linha_idx + 1].strip() if linha_idx + 1 < len(bloco_linhas) else None

    while i < len(bloco_linhas):
        linha = bloco_linhas[i].strip()

        if linha.startswith("Nome:"):
            disciplina["Nome"] = extrair_valor(i)
            i += 1
        elif linha.startswith("Código:"):
            disciplina["Código"] = extrair_valor(i)
            i += 1
        elif linha.startswith("Departamento:"):
            disciplina["Departamento"] = extrair_valor(i)
            i += 1
        elif linha.startswith("C.H.:"):
            disciplina["C.H."] = extrair_valor(i)
            i += 1
        elif linha.startswith("Modalidade:"):
            disciplina["Modalidade"] = extrair_valor(i)
            i += 1
        elif linha.startswith("Função:"):
            disciplina["Função"] = extrair_valor(i)
            i += 1
        elif linha.startswith("Natureza:"):
            disciplina["Natureza"] = extrair_valor(i)
            i += 1
        elif linha.startswith("Pré-requisitos obrigatórios:"):
            disciplina["Pré-requisitos obrigatórios"] = extrair_valor(i)
            i += 1
        elif linha.startswith("Pré-requisitos recomendados:"):
            disciplina["Pré-requisitos recomendados"] = extrair_valor(i)
            i += 1
        elif linha.startswith("Módulo de alunos:"):
            disciplina["Módulo de alunos"] = extrair_valor(i)
            i += 1
        elif linha.startswith("Ementa:"):
            ementa = linha.replace("Ementa:", "").strip()
            j = i + 1
            while j < len(bloco_linhas) and not bloco_linhas[j].startswith("Nome:"):
                ementa += " " + bloco_linhas[j].strip()
                j += 1
            disciplina["Ementa"] = ' '.join(ementa.split())
            i = j - 1

        i += 1

    return disciplina

# Reprocessar blocos com função ajustada
disciplinas_reprocessadas = []
for bloco_str in blocos:
    if not bloco_str.strip():
        continue

    bloco_linhas = bloco_str.strip().split('\n')
    dados = processar_bloco_disciplina_flexivel(bloco_linhas)

    if dados and dados.get('Nome'):
        disciplinas_reprocessadas.append(dados)

# Mostrar as 5 primeiras disciplinas para inspeção visual
disciplinas_reprocessadas[:5]
