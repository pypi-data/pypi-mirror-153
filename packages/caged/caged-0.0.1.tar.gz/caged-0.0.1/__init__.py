import datetime as date
import pandas as pd

# Auxílio na criação do nome das colunas
def set_variables(year, month, colnames):
    estoque = f"estoque-{month}-{year}"
    colnames.append(estoque)

    admissoes = f"admissoes-{month}-{year}"
    colnames.append(admissoes)

    desligamentos = f"desligamentos-{month}-{year}"
    colnames.append(desligamentos)

    saldos = f"saldos-{month}-{year}"
    colnames.append(saldos)

    variacao = f"variacao-{month}-{year}"
    colnames.append(variacao)


# Criar o nome das colunas
def set_colnames():
    colnames = ['uf', 'code', 'city']

    # Adicionando aos meses-anos cada variável
    for year in range(2020, 2023):
        for month in range(1, 13):
            currentMonth = 3
            currentYear = date.datetime.now().year

            if year == currentYear and month == currentMonth + 1:
                break
            else:
                set_variables(year, month, colnames)
                month = ""
    return colnames


# Transformar dados em DataFrame
def set_city_to_dataframe(city, df_city):
    for year in range(2020, 2022 + 1):
        for month in range(1, 12 + 1):
            currentMonth = 3
            currentYear = date.datetime.now().year

            if year == currentYear and month == currentMonth + 1:
                break
            else:
                data = f"{month}-{year}"
                estoque = f"estoque-{month}-{year}"
                admissoes = f"admissoes-{month}-{year}"
                desligamentos = f"desligamentos-{month}-{year}"
                saldos = f"saldos-{month}-{year}"
                variacao = f"variacao-{month}-{year}"
                line = {
                    'data': data,
                    'estoque': city[f"{estoque}"].values[0],
                    'admissoes': city[f"{admissoes}"].values[0],
                    'desligamentos': city[f"{desligamentos}"].values[0],
                    'saldos': city[f"{saldos}"].values[0],
                    'variacao': city[f"{variacao}"].values[0],
                }
                df_city.loc[data] = line

# Pegar uma cidade pelo código
def get_city_by_code(code):
    # Criando um array para as colunas
    colnames = set_colnames()

    # Importando os dados
    uri = 'https://raw.githubusercontent.com/nogueira-guilherme/nepe-mercado-trabalho/master/Data/caged.csv'
    caged = pd.read_csv(uri)

    # Selecionando os dados de São João del-Rei
    city = caged[(caged['code'] == code)]
    city = city.fillna(0)  # substituir dos valores não identificados por zero

    # Criando um DataFrame para São João del-Rei
    df_city = pd.DataFrame(columns=['data', 'estoque', 'admissoes', 'desligamentos', 'saldos', 'variacao'])

    # Transformando o DataFrame: colunas->linhas
    set_city_to_dataframe(city, df_city)

    # Reiniciar os index das linhas
    df_city = df_city.reset_index()

    return df_city

# Pegar todas as cidades
def get_cities_first_time():
    # Criando um array para as colunas
    colnames = set_colnames()

    # Importando os dados
    uri = 'https://github.com/nogueira-guilherme/nepe-mercado-trabalho/blob/master/Data/caged.xlsx?raw=true'
    caged = pd.read_excel(uri, sheet_name='Tabela 8.1', usecols='B:EI', nrows=(5577 - 7), skiprows=6, names=colnames)

    return caged