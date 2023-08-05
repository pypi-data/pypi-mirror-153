#  Atualizar o Database
import csv
import os
import time
from atualizador.funcoes_mod.Funcoes import modelagem_tedesco


DIRETORIO = r'D:\TEDESCO\TD_BRUTOS'
DATABASE_TD = r'D:\TEDESCO\TD__Databse_ACOES'


def ACOES(DIRETORIO):
    """
    UTILIZADO PARA SELECIONAR AS AÇÕES
    DE INTESSES DO TEDESCO.
    """

    base = [
        'ABEV3',
        'ALPA4',
        'ALSO3',
        'AMAR3',
        'ASAI3',
        'AZUL4',
        'B3SA3',
        'BBAS3',
        'BBDC3',
        'BBDC4',
        'BBSE3',
        'BEEF3',
        'BRAP4',
        'BRFS3',
        'BRKM5',
        'BRML3',
        'CCRO3',
        'CESP6',
        'CIEL3',
        'CMIG4',
        'COGN3',
        'CPFE3',
        'CPLE6',
        'CRFB3',
        'CSAN3',
        'CSMG3',
        'CSNA3',
        'CVCB3',
        'CYRE3',
        'ECOR3',
        'EGIE3',
        'ELET3',
        'ELET6',
        'EMBR3',
        'ENBR3',
        'ENEV3',
        'EQTL3',
        'EZTC3',
        'FLRY3',
        'GGBR4',
        'GNDI3',
        'GOAU4',
        'GOLL4',
        'HAPV3',
        'HYPE3',
        'IRBR3',
        'ITSA4',
        'ITUB4',
        'JBSS3',
        'JHSF3',
        'LCAM3',
        'LIGT3',
        'LREN3',
        'LWSA3',
        'MDIA3',
        'MEAL3',
        'MGLU3',
        'MOVI3',
        'MRFG3',
        'MRVE3',
        'MULT3',
        'NEOE3',
        'NTCO3',
        'PCAR3',
        'PETR3',
        'PETR4',
        'PRIO3',
        'PSSA3',
        'QUAL3',
        'RADL3',
        'RAIL3',
        'RAPT4',
        'RENT3',
        'SBSP3',
        'SUZB3',
        'TIMS3',
        'TOTS3',
        'TRPL4',
        'UGPA3',
        'USIM5',
        'VALE3',
        'VIVT3',
        'WEGE3',
        'YDUQ3',
    ]

    candle = {}

    for caminho_path, dir_arquivo, arquivos in os.walk(DIRETORIO):
        for arquivo in arquivos:

            planilha = modelagem_tedesco(arquivo, DIRETORIO)

            os.chdir(planilha)
            with open(planilha, 'r') as arquivo_referencia:
                arquivo_csv = csv.reader(arquivo_referencia, delimiter=',')
                for registro in arquivo_csv:
                    ticker = registro[0]
                    date = registro[3]
                    tempo = registro[4]
                    # X
                    preco = registro[1]
                    qty = registro[2]
                    # Y
                    # Z

                    if ticker in '<ticker>':
                        continue

                    field_name = [
                        '<ticker>',
                        '<date>',
                        '<time>',
                        '<x>',
                        '<close>',
                        '<qty>',
                        '<y>',
                        '<z>'
                    ]

                    for dados in base:
                        if dados != ticker:
                            continue

                        candle[ticker] = {
                            '<ticker>': ticker,
                            '<date>': date,
                            '<time>': tempo,
                            '<x>': 'X',
                            '<close>': preco,
                            '<qty>': qty,
                            '<y>': 'Y',
                            '<z>': 'Z',
                        }

                        nome_csv = dados + '.csv'

                        print(nome_csv)

                        for titulos, valores in candle.items():
                            os.chdir(DATABASE_TD)
                            analise_diretorio = os.path.exists(nome_csv)

                            if analise_diretorio:
                                os.chdir(DATABASE_TD)
                                with open(nome_csv, 'a', newline='') as csvfile:
                                    writer = csv.DictWriter(
                                        csvfile, delimiter=';', fieldnames=field_name)
                                    writer.writerow(valores)
                                    csvfile.close()
                            else:
                                os.chdir(DATABASE_TD)
                                with open(nome_csv, 'w', newline='') as csv_planilha:
                                    writer = csv.DictWriter(
                                        csv_planilha,  delimiter=';', fieldnames=field_name)
                                    writer.writeheader()
                                    writer.writerow(valores)
                                    csv_planilha.close()

                        candle = {
                        }
            os.remove(planilha)


def arrumar_planilha():

    FILE_NAMES = ['<ticker>',
                  '<date>',
                  '<time>',
                  '<x>',
                  '<close>',
                  '<qty>',
                  '<y>',
                  '<z>'
                  ]

    candles = {}

    for _, _, arquivo in os.walk(DATABASE_TD):
        for dados in arquivo:
            os.chdir(DATABASE_TD)
            with open(dados, 'r') as csv_file:
                FILE = csv.reader(csv_file, delimiter=',')
                for registros in FILE:

                    candles[registros[0]] = {
                        '<ticker>': registros[0],
                        '<date>': registros[1],
                        '<time>': registros[2],
                        '<x>': registros[3],
                        '<close>': registros[4],
                        '<qty>': registros[5],
                        '<y>': registros[6],
                        '<z>': registros[7]
                    }

                    for itens, valores in candles.items():

                        os.chdir(R'D:\TD')
                        analise_arquivos = os.path.exists(dados)
                        if analise_arquivos:
                            with open(dados, 'a', newline='') as csv_file:
                                WRITER = csv.DictWriter(
                                    csv_file, delimiter=';', fieldnames=FILE_NAMES)
                                WRITER.writerow(valores)
                                csv_file.close()
                        else:
                            with open(dados, 'w', newline='') as csv_file:
                                WRITER = csv.DictWriter(
                                    csv_file, delimiter=';', fieldnames=FILE_NAMES)
                                WRITER.writerow(valores)
                                csv_file.close()
                    candles = {}


if __name__ == '__main__':
    inicio = time.time()
    ACOES(DIRETORIO)
    fim = time.time()
    print('TEMPO DE ZIP -------->', fim - inicio)
