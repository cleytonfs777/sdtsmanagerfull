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
    return valor_t.strip()


def inserereais(valor):
    valor_t = str(valor)
    valor_t = valor_t.replace('.', ',')
    valor_t = 'R$ ' + valor_t
    return valor_t

def separar_e_agrupar_entrada(entrada):
    """
    Função para separar uma string de entrada em listas aninhadas.
    Primeiro, divide a string por ';' para obter grupos.
    Cada grupo é então dividido por '|' para obter os elementos individuais.
    Espaços em branco e strings vazias são removidos.

    :param entrada: String contendo os dados a serem processados.
    :return: Lista de listas com os dados agrupados.
    """
    # Remover a parte inicial até o primeiro ": " se houver
    entrada_limpa = entrada.split(": ", 1)[-1]

    # Dividir a string em grupos separados por ";"
    grupos = entrada_limpa.split(";")

    # Dividir cada grupo em elementos separados por "|"
    # Remover espaços em branco e elementos vazios
    resultado = [list(filter(None, [item.strip() for item in grupo.split("|")])) for grupo in grupos if grupo.strip()]

    return resultado

if __name__ == "__main__":
    ...
