def trataelementoitem(elemento):
    elemento_t = str(elemento)
    # pega os 4 primeiros caracteres. Se tiver exatamente 4 pega todos
    # se tiver menos de 4 completa com 0 a direita
    elemento_t = elemento_t[:4].zfill(4)

    # Adiciona um '.' entre os 2 primeiros caracteres e os 2 ultimos
    elemento_t = elemento_t[:2] + '.' + elemento_t[2:]

    return elemento_t


def removereais(valor):
    valor_t = str(valor)
    valor_t = valor_t.replace('R$', '')
    valor_t = valor_t.replace('.', '')
    valor_t = valor_t.replace(',', '.')
    return valor_t


def inserereais(valor):
    valor_t = str(valor)
    valor_t = valor_t.replace('.', ',')
    valor_t = 'R$ ' + valor_t
    return valor_t


if __name__ == "__main__":
    ...
