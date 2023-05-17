import re
#МЕСТО ДЛЯ ЭКСПЕРИМЕНТОВ



txt = 'Редиска Ты - редиска, Сосиска.'
txt = 'Ехал Ваня сосиска на коне, вел собачку на ремне (редиска).'
#txt =123
try:
    for e in badWords:
#    reg_exp = fr"{e}\b"
        ch = e[0] + (len(e) - 1) * '*'
    # замена(что, на  что, где, без учета регистра)
        txt = re.sub(fr"\b{e}\b", ch, txt, flags=re.IGNORECASE)
except TypeError:
    txt = 'Ошибка типа'
print(txt)
