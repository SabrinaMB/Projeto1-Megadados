# string = """
# Gente!! Olha só o #sabia #tetinha que eu vi no parque!! Super bem-acompanhada @elainerf @deborah.123 amo voces S2!!
# """

def passaro_parser(texto):
    lista = []
    start = 0
    end = 0

    while start < len(texto):

        if texto[start] != "#":
            start += 1
        else:
            end = start + 1

            while ((texto[end].isalpha()) or (texto[end] == "-")):
                end += 1

            lista.append(texto[start + 1:end])

        end += 1
        start = end

    return lista

def pessoa_parser(texto):
    lista = []
    start = 0
    end = 0

    while start < len(texto):

        if texto[start] != "@":
            start += 1
        else:
            end = start + 1

            while texto[end] != " ":
                end += 1

            lista.append(texto[start + 1:end])

        end += 1
        start = end

    return lista

# print(passaro_parser(string))
# print(pessoa_parser(string))