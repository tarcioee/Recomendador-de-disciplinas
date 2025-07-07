import unicodedata

def entrada_int(msg, minimo=None, maximo=None):
    while True:
        try:
            valor = int(input(msg))
            if minimo is not None and valor < minimo:
                print(f"Digite um valor >= {minimo}")
                continue
            if maximo is not None and valor > maximo:
                print(f"Digite um valor <= {maximo}")
                continue
            return valor
        except ValueError:
            print("Entrada inválida. Digite um número inteiro.")

def entrada_turnos_validos(msg="Quais turnos você tem disponíveis? (matutino, vespertino, noturno)", obrigatorio=True):
    turnos_validos = {"matutino", "vespertino", "noturno"}
    while True:
        entrada = input(msg + " (separe por vírgula): ").strip().lower()
        if not entrada and not obrigatorio:
            return []
        turnos = [t.strip() for t in entrada.split(",") if t.strip()]
        turnos_filtrados = [t for t in turnos if t in turnos_validos]

        if not turnos_filtrados:
            print("⚠️ Pelo menos um turno válido deve ser informado (matutino, vespertino ou noturno). Tente novamente.")
            continue

        return turnos_filtrados

def limpar_texto(texto, normalizar=True):
    texto = texto.strip().lower()
    if normalizar:
        texto = unicodedata.normalize('NFKD', texto)
        texto = ''.join(c for c in texto if not unicodedata.combining(c))
    return texto

def entrada_texto(msg, obrigatorio=True, normalizar=True):
    while True:
        texto = input(msg).strip()
        if obrigatorio and not texto:
            print("Entrada obrigatória. Tente novamente.")
            continue
        return limpar_texto(texto, normalizar) if texto else ""

def entrada_lista_texto(msg, obrigatorio=False, normalizar=True):
    while True:
        entrada = input(msg + " (separe por vírgula): ").strip()
        if not entrada and obrigatorio:
            print("Entrada obrigatória. Tente novamente.")
            continue
        if not entrada:
            return []
        itens = [limpar_texto(x, normalizar) for x in entrada.split(",") if x.strip()]
        if not itens and obrigatorio:
            print("Nenhum item válido encontrado. Tente novamente.")
            continue
        return itens

def entrada_lista_inteiros(msg, obrigatorio=False):
    while True:
        entrada = input(msg + " (ex: 1, 3, 5): ").strip()
        if not entrada and obrigatorio:
            print("Entrada obrigatória. Tente novamente.")
            continue
        if not entrada:
            return []
        try:
            valores = [int(x.strip()) for x in entrada.split(",") if x.strip()]
            if not valores and obrigatorio:
                print("Nenhum valor válido. Tente novamente.")
                continue
            return valores
        except ValueError:
            print("Todos os valores devem ser números inteiros separados por vírgula.")
