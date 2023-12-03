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


texto = "Meu main destino comum|capital|4470|95.1|56.22|100|2023-12-07|DLF|Aj-Geral|adescentralizar|R$ 7.844,44|                                                       ;Meu main destino comum|custeio|4469|95.1|56.22|100|2023-12-12|12ºBBM|DLF|descentralizado|R$ 150.000,00|                                                       "

print(separar_e_agrupar_entrada(texto))