import unicodedata

def normalizar(texto):
    if not isinstance(texto, str):
        return texto
    texto = texto.strip().lower()
    texto = unicodedata.normalize('NFKD', texto)
    texto = ''.join(c for c in texto if not unicodedata.combining(c))
    return texto
