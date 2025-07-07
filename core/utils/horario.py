# utils/horario.py
import re
from datetime import time

dias = {
    "SEG": 0,
    "TER": 1,
    "QUA": 2,
    "QUI": 3,
    "SEX": 4,
    "SAB": 5,
    "DOM": 6,
}

def parse_horario(hstr):
    """
    Ex: "SEG 07:00 às 08:50" ou "seg 07:00 as 08:50" → (0, time(7,0), time(8,50))
    """
    hstr = hstr.strip().upper()
    match = re.match(r"(SEG|TER|QUA|QUI|SEX|SAB|DOM)\s+(\d{2}:\d{2})\s+(?:ÀS|AS)\s+(\d{2}:\d{2})", hstr)
    if not match:
        return None
    dia, inicio, fim = match.groups()
    return (dias[dia], _parse_time(inicio), _parse_time(fim))


def _parse_time(tstr):
    h, m = map(int, tstr.split(":"))
    return time(h, m)

def tem_conflito(horarios1, horarios2):
    """
    Retorna True se houver sobreposição entre os horários de duas turmas.
    """
    blocos1 = [b for h in horarios1 if (b := parse_horario(h))]
    blocos2 = [b for h in horarios2 if (b := parse_horario(h))]


    for d1, i1, f1 in blocos1:
        for d2, i2, f2 in blocos2:
            if d1 != d2:
                continue
            if i1 < f2 and i2 < f1:  # interseção real
                return True
    return False

def faixa_turno(turno_nome):
    faixas = {
        "matutino": (time(7, 0), time(12, 30)),
        "vespertino": (time(13, 0), time(18, 30)),
        "noturno": (time(18, 30), time(22, 10)),
    }
    return faixas.get(turno_nome.lower())
