import csv
import os
import time
from atualizador.funcoes_mod.Funcoes import modelagem_tedesco

DIRETORIO = r'D:\TEDESCO\TD_BRUTOS'
B3_FUTUROS = r'D:\TEDESCO\TD_DOLAR'
TD_DATABASE_DOLAR = r'D:\TEDESCO\TD_DATABASE_DOLAR'


def DOLAR(DIRETORIO):

    futuros = [
        'WDOF21',
        'WDOG21',
        'WDOH21',
        'WDOJ21',
        'WDOK21',
        'WDOM21',
        'WDON21',
        'WDOQ21',
        'WDOU21',
        'WDOV21',
        'WDOX21',
        'WDOZ21',
        'WDOF22',
        'WDOG22',
        'WDOH22',
        'WDOJ22',
        'WDOK22',
        'WDOM22',
        'WDON22',
        'WDOQ22',
        'WDOU22',
        'WDOV22',
        'WDOX22',
        'WDOZ22',
        'DOLF21',
        'DOLG21',
        'DOLH21',
        'DOLJ21',
        'DOLK21',
        'DOLM21',
        'DOLN21',
        'DOLQ21',
        'DOLU21',
        'DOLV21',
        'DOLX21',
        'DOLZ21',
        'DOLF22',
        'DOLG22',
        'DOLH22',
        'DOLJ22',
        'DOLK22',
        'DOLM22',
        'DOLN22',
        'DOLQ22',
        'DOLU22',
        'DOLV22',
        'DOLX22',
        'DOLZ22',
    ]

    candle = {}

    for _, _, arquivos in os.walk(DIRETORIO):
        for arquivo in arquivos:
            os.chdir(DIRETORIO)
            nome_arquivo = arquivo

            planilha = modelagem_tedesco(nome_arquivo, DIRETORIO)

            os.chdir(DIRETORIO)
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

                    for dados in futuros:
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
                            os.chdir(B3_FUTUROS)
                            analise_diretorio = os.path.exists(nome_csv)

                            if analise_diretorio:
                                os.chdir(B3_FUTUROS)
                                with open(nome_csv, 'a', newline='') as csvfile:
                                    writer = csv.DictWriter(
                                        csvfile, delimiter=';', fieldnames=field_name)
                                    writer.writerow(valores)
                                    csvfile.close()
                            else:
                                os.chdir(B3_FUTUROS)
                                with open(nome_csv, 'w', newline='') as csv_planilha:
                                    writer = csv.DictWriter(
                                        csv_planilha,  delimiter=';', fieldnames=field_name)
                                    writer.writeheader()
                                    writer.writerow(valores)
                                    csv_planilha.close()

                        candle = {}


def data_atual(arquivo):
    """
    Utilizado para retornar a ultima data dispónivel 
    no arquivo mais atualizado.
    """

    os.chdir(TD_DATABASE_DOLAR)
    data = None
    ticker = None

    with open(arquivo, 'r') as arquivo_referencia:
        arquivo_csv = csv.reader(arquivo_referencia, delimiter=';')
        for registro in arquivo_csv:

            if registro[0] == '<ticker>':
                continue
            

            data = registro[1]
            ticker = registro[0]

    print(ticker)
    print(data)

    return data, ticker


def concatenar_contratos(ultimo_date, ticker):
    """
    Utilizado para concatenar os contratos, precisa ser atualizado
    todo o final de ano, precisamos desconsiderar o ultimo dia de 
    contrato e já pegar os candles do proximo contrato.
    """
    
    for _, _, arquivos in os.walk(B3_FUTUROS):
        os.chdir(B3_FUTUROS)
        for arquivo in arquivos:



            # --------------------- MINI DOLAR FUTURO --------------------- # 



            if ticker == 'WDONAFUT':
                #  CONTRATO FUTURO ---> WDOF22
                if ultimo_date > 20211129 and ultimo_date < 20211229:

                    if arquivo != 'WDOF22.csv':
                        continue

                    with open("WDOF22.csv", 'r') as arquivo_referencia:
                        arquivo_csv = csv.reader(
                            arquivo_referencia, delimiter=';')
                        for registro in arquivo_csv:

                            ticker_futuro = registro[0]

                            if ticker_futuro == '<ticker>':
                                continue

                            data_atual = int(registro[1])
                            tempo_atual = str(registro[2])

                            if data_atual <= 20211129 or data_atual > 20211229:
                                continue

                            if ultimo_date >= data_atual:
                                continue

                            if len(tempo_atual) == 5:
                                tempo_atual = "0" + tempo_atual

                            registro[0] = 'WDONAFUT'
                            print(ticker_futuro, data_atual)

                            database_diretorio_futuros = os.path.join(
                                TD_DATABASE_DOLAR, "WDONAFUT_TD.csv")
                            with open(database_diretorio_futuros, 'a', newline='') as csvfile:
                                writer = csv.writer(csvfile, delimiter=';')
                                writer.writerow(registro)
                                csvfile.close()

                #  CONTRATO FUTURO ---> WDOG22
                elif ultimo_date >= 20211229 and ultimo_date < 20220128:

                    if arquivo != 'WDOG22.csv':
                        continue

                    with open('WDOG22.csv', 'r') as arquivo_referencia:
                        arquivo_csv = csv.reader(
                            arquivo_referencia, delimiter=';')
                        for registro in arquivo_csv:

                            ticker_futuro = registro[0]

                            if ticker_futuro == '<ticker>':
                                continue

                            data_atual = int(registro[1])
                            tempo_atual = str(registro[2])

                            if data_atual <= 20211229 or data_atual > 20220128:
                                continue

                            if ultimo_date >= data_atual:
                                continue

                            if len(tempo_atual) == 5:
                                tempo_atual = "0" + tempo_atual

                            registro[0] = 'WDONAFUT'
                            print(ticker_futuro, data_atual)

                            database_diretorio_futuros = os.path.join(
                                TD_DATABASE_DOLAR, "WDONAFUT_TD.csv")
                            with open(database_diretorio_futuros, 'a', newline='') as csvfile:
                                writer = csv.writer(csvfile, delimiter=';')
                                writer.writerow(registro)
                                csvfile.close()

                #  CONTRATO FUTURO ---> WDOH22
                elif ultimo_date >= 20220128 and ultimo_date < 20220224:

                    if arquivo != 'WDOH22.csv':
                        continue

                    with open('WDOH22.csv', 'r') as arquivo_referencia:
                        arquivo_csv = csv.reader(
                            arquivo_referencia, delimiter=';')
                        for registro in arquivo_csv:

                            ticker_futuro = registro[0]

                            if ticker_futuro == '<ticker>':
                                continue

                            data_atual = int(registro[1])
                            tempo_atual = str(registro[2])

                            if data_atual <= 20220128 or data_atual > 20220224:
                                continue

                            if ultimo_date >= data_atual:
                                continue

                            if len(tempo_atual) == 5:
                                tempo_atual = "0" + tempo_atual

                            registro[0] = 'WDONAFUT'
                            print(ticker_futuro, data_atual)

                            database_diretorio_futuros = os.path.join(
                                TD_DATABASE_DOLAR, "WDONAFUT_TD.csv")
                            with open(database_diretorio_futuros, 'a', newline='') as csvfile:
                                writer = csv.writer(csvfile, delimiter=';')
                                writer.writerow(registro)
                                csvfile.close()

                #  CONTRATO FUTURO ---> WDOJ22
                elif ultimo_date >= 20220224 and ultimo_date < 20220330:

                    if arquivo != 'WDOJ22.csv':
                        continue

                    with open('WDOJ22.csv', 'r') as arquivo_referencia:
                        arquivo_csv = csv.reader(
                            arquivo_referencia, delimiter=';')
                        for registro in arquivo_csv:

                            ticker_futuro = registro[0]
                            if ticker_futuro == '<ticker>':
                                continue

                            data_atual = int(registro[1])
                            tempo_atual = str(registro[2])

                            if data_atual <= 20220224 or data_atual > 20220330:
                                continue

                            if ultimo_date >= data_atual:
                                continue

                            if len(tempo_atual) == 5:
                                tempo_atual = "0" + tempo_atual

                            registro[0] = 'WDONAFUT'
                            print(ticker_futuro, data_atual)

                            database_diretorio_futuros = os.path.join(
                                TD_DATABASE_DOLAR, "WDONAFUT_TD.csv")
                            with open(database_diretorio_futuros, 'a', newline='') as csvfile:
                                writer = csv.writer(csvfile, delimiter=';')
                                writer.writerow(registro)
                                csvfile.close()

                #  CONTRATO FUTURO ---> WDOK22
                elif ultimo_date >= 20220330 and ultimo_date < 20220428:

                    if arquivo != 'WDOK22.csv':
                        continue

                    with open('WDOK22.csv', 'r') as arquivo_referencia:
                        arquivo_csv = csv.reader(
                            arquivo_referencia, delimiter=';')
                        for registro in arquivo_csv:

                            ticker_futuro = registro[0]
                            if ticker_futuro == '<ticker>':
                                continue

                            data_atual = int(registro[1])
                            tempo_atual = str(registro[2])

                            if data_atual <= 20220330 or data_atual > 20220428:
                                continue

                            if int(date) >= data_atual:
                                continue

                            if len(tempo_atual) == 5:
                                tempo_atual = "0" + tempo_atual

                            registro[0] = 'WDONAFUT'
                            print(ticker_futuro, data_atual)

                            database_diretorio_futuros = os.path.join(
                                TD_DATABASE_DOLAR, "WDONAFUT_TD.csv")
                            with open(database_diretorio_futuros, 'a', newline='') as csvfile:
                                writer = csv.writer(csvfile, delimiter=';')
                                writer.writerow(registro)
                                csvfile.close()

                #  CONTRATO FUTURO ---> WDOM22
                elif ultimo_date >= 20220428 and ultimo_date < 20220530:

                    if arquivo != 'WDOM22.csv':
                        continue

                    with open('WDOM22.csv', 'r') as arquivo_referencia:
                        arquivo_csv = csv.reader(
                            arquivo_referencia, delimiter=';')
                        for registro in arquivo_csv:

                            ticker_futuro = registro[0]
                            if ticker_futuro == '<ticker>':
                                continue

                            data_atual = int(registro[1])
                            tempo_atual = str(registro[2])

                            if data_atual <= 20220428 or data_atual > 20220530:
                                continue

                            if ultimo_date >= data_atual:
                                continue

                            if len(tempo_atual) == 5:
                                tempo_atual = "0" + tempo_atual

                            registro[0] = 'WDONAFUT'
                            print(ticker_futuro, data_atual)

                            database_diretorio_futuros = os.path.join(
                                TD_DATABASE_DOLAR, "WDONAFUT_TD.csv")
                            with open(database_diretorio_futuros, 'a', newline='') as csvfile:
                                writer = csv.writer(csvfile, delimiter=';')
                                writer.writerow(registro)
                                csvfile.close()

                #  CONTRATO FUTURO ---> WDON22
                elif ultimo_date >= 20220530 and ultimo_date < 20220629:

                    if arquivo != 'WDON22.csv':
                        continue

                    with open('WDON22.csv', 'r') as arquivo_referencia:
                        arquivo_csv = csv.reader(
                            arquivo_referencia, delimiter=';')
                        for registro in arquivo_csv:

                            ticker_futuro = registro[0]
                            if ticker_futuro == '<ticker>':
                                continue

                            data_atual = int(registro[1])
                            tempo_atual = str(registro[2])

                            if data_atual <= 20220530 or data_atual > 20220629:
                                continue

                            if ultimo_date >= data_atual:
                                continue

                            if len(tempo_atual) == 5:
                                tempo_atual = "0" + tempo_atual

                            registro[0] = 'WDONAFUT'
                            print(ticker_futuro, data_atual)

                            database_diretorio_futuros = os.path.join(
                                TD_DATABASE_DOLAR, "WDONAFUT_TD.csv")
                            with open(database_diretorio_futuros, 'a', newline='') as csvfile:
                                writer = csv.writer(csvfile, delimiter=';')
                                writer.writerow(registro)
                                csvfile.close()

                #  CONTRATO FUTURO ---> WDOQ22
                elif ultimo_date >= 20220629 and ultimo_date < 20220728:

                    if arquivo != 'WDOQ22.csv':
                        continue

                    with open('WDOQ22.csv', 'r') as arquivo_referencia:
                        arquivo_csv = csv.reader(
                            arquivo_referencia, delimiter=';')
                        for registro in arquivo_csv:

                            ticker_futuro = registro[0]
                            if ticker_futuro == '<ticker>':
                                continue

                            data_atual = int(registro[1])
                            tempo_atual = str(registro[2])

                            if data_atual <= 20220629 or data_atual > 20220728:
                                continue

                            if ultimo_date >= data_atual:
                                continue

                            if len(tempo_atual) == 5:
                                tempo_atual = "0" + tempo_atual

                            registro[0] = 'WDONAFUT'
                            print(ticker_futuro, data_atual)

                            database_diretorio_futuros = os.path.join(
                                TD_DATABASE_DOLAR, "WDONAFUT_TD.csv")
                            with open(database_diretorio_futuros, 'a', newline='') as csvfile:
                                writer = csv.writer(csvfile, delimiter=';')
                                writer.writerow(registro)
                                csvfile.close()

                #  CONTRATO FUTURO ---> WDOU22
                elif ultimo_date >= 20220728 and ultimo_date < 20220830:

                    if arquivo != 'WDOU22.csv':
                        continue

                    with open('WDOU22.csv', 'r') as arquivo_referencia:
                        arquivo_csv = csv.reader(
                            arquivo_referencia, delimiter=';')
                        for registro in arquivo_csv:

                            ticker_futuro = registro[0]
                            if ticker_futuro == '<ticker>':
                                continue

                            data_atual = int(registro[1])
                            tempo_atual = str(registro[2])

                            if data_atual <= 20220728 or data_atual > 20220830:
                                continue

                            if ultimo_date >= data_atual:
                                continue

                            if len(tempo_atual) == 5:
                                tempo_atual = "0" + tempo_atual

                            registro[0] = 'WDONAFUT'
                            print(ticker_futuro, data_atual)

                            database_diretorio_futuros = os.path.join(
                                TD_DATABASE_DOLAR, "WDONAFUT_TD.csv")
                            with open(database_diretorio_futuros, 'a', newline='') as csvfile:
                                writer = csv.writer(csvfile, delimiter=';')
                                writer.writerow(registro)
                                csvfile.close()

                #  CONTRATO FUTURO ---> WDOV22
                elif ultimo_date >= 20220830 and ultimo_date < 20220929:

                    if arquivo != 'WDOV22.csv':
                        continue

                    with open('WDOV22.csv', 'r') as arquivo_referencia:
                        arquivo_csv = csv.reader(
                            arquivo_referencia, delimiter=';')
                        for registro in arquivo_csv:

                            ticker_futuro = registro[0]
                            if ticker_futuro == '<ticker>':
                                continue

                            data_atual = int(registro[1])
                            tempo_atual = str(registro[2])

                            if data_atual <= 20220830 or data_atual > 20220929:
                                continue

                            if ultimo_date >= data_atual:
                                continue

                            if len(tempo_atual) == 5:
                                tempo_atual = "0" + tempo_atual

                            registro[0] = 'WDONAFUT'
                            print(ticker_futuro, data_atual)

                            database_diretorio_futuros = os.path.join(
                                TD_DATABASE_DOLAR, "WDONAFUT_TD.csv")
                            with open(database_diretorio_futuros, 'a', newline='') as csvfile:
                                writer = csv.writer(csvfile, delimiter=';')
                                writer.writerow(registro)
                                csvfile.close()

                #  CONTRATO FUTURO ---> WDOX22
                elif ultimo_date >= 20220929 and ultimo_date < 20221028:

                    if arquivo != 'WDOX22.csv':
                        continue

                    with open('WDOX22.csv', 'r') as arquivo_referencia:
                        arquivo_csv = csv.reader(
                            arquivo_referencia, delimiter=';')
                        for registro in arquivo_csv:

                            ticker_futuro = registro[0]
                            if ticker_futuro == '<ticker>':
                                continue

                            data_atual = int(registro[1])
                            tempo_atual = str(registro[2])

                            if data_atual <= 20220929 or data_atual > 20221028:
                                continue

                            if ultimo_date >= data_atual:
                                continue

                            if len(tempo_atual) == 5:
                                tempo_atual = "0" + tempo_atual

                            registro[0] = 'WDONAFUT'
                            print(ticker_futuro, data_atual)

                            database_diretorio_futuros = os.path.join(
                                TD_DATABASE_DOLAR, "WDONAFUT_TD.csv")
                            with open(database_diretorio_futuros, 'a', newline='') as csvfile:
                                writer = csv.writer(csvfile, delimiter=';')
                                writer.writerow(registro)
                                csvfile.close()

                #  CONTRATO FUTURO ---> WDOZ22
                elif ultimo_date >= 20221028 and ultimo_date < 20221129:

                    if arquivo != 'WDOZ22.csv':
                        continue

                    with open('WDOZ22.csv', 'r') as arquivo_referencia:
                        arquivo_csv = csv.reader(
                            arquivo_referencia, delimiter=';')
                        for registro in arquivo_csv:

                            ticker_futuro = registro[0]
                            if ticker_futuro == '<ticker>':
                                continue

                            data_atual = int(registro[1])
                            tempo_atual = str(registro[2])

                            if data_atual <= 20221028 or data_atual > 20221129:
                                continue

                            if ultimo_date >= data_atual:
                                continue

                            if len(tempo_atual) == 5:
                                tempo_atual = "0" + tempo_atual

                            registro[0] = 'WDONAFUT'
                            print(ticker_futuro, data_atual)

                            database_diretorio_futuros = os.path.join(
                                TD_DATABASE_DOLAR, "WDONAFUT_TD.csv")
                            with open(database_diretorio_futuros, 'a', newline='') as csvfile:
                                writer = csv.writer(csvfile, delimiter=';')
                                writer.writerow(registro)
                                csvfile.close()

                #  CONTRATO FUTURO ---> WDOF23
                elif ultimo_date >= 20221129 and ultimo_date < 20221229:

                    if arquivo != 'WDOF23.csv':
                        continue

                    with open('WDOF223.csv', 'r') as arquivo_referencia:
                        arquivo_csv = csv.reader(
                            arquivo_referencia, delimiter=';')
                        for registro in arquivo_csv:

                            ticker_futuro = registro[0]
                            if ticker_futuro == '<ticker>':
                                continue

                            data_atual = int(registro[1])
                            tempo_atual = str(registro[2])

                            if data_atual <= 20221129 or data_atual > 20221229:
                                continue

                            if ultimo_date >= data_atual:
                                continue

                            if len(tempo_atual) == 5:
                                tempo_atual = "0" + tempo_atual

                            registro[0] = 'WDONAFUT'
                            print(ticker_futuro, data_atual)

                            database_diretorio_futuros = os.path.join(
                                TD_DATABASE_DOLAR, "WDONAFUT_TD.csv")
                            with open(database_diretorio_futuros, 'a', newline='') as csvfile:
                                writer = csv.writer(csvfile, delimiter=';')
                                writer.writerow(registro)
                                csvfile.close()



            # --------------------- DOLAR FUTURO --------------------- # 



            elif ticker == 'DOLNAFUT':
                #  CONTRATO FUTURO ---> DOLF22
                if ultimo_date > 20211129 and ultimo_date < 20211229:

                    if arquivo != 'DOLF22.csv':
                        continue

                    with open("DOLF22.csv", 'r') as arquivo_referencia:
                        arquivo_csv = csv.reader(
                            arquivo_referencia, delimiter=';')
                        for registro in arquivo_csv:

                            ticker_futuro = registro[0]

                            if ticker_futuro == '<ticker>':
                                continue

                            data_atual = int(registro[1])
                            tempo_atual = str(registro[2])

                            if data_atual <= 20211129 or data_atual > 20211229:
                                continue

                            if ultimo_date >= data_atual:
                                continue

                            if len(tempo_atual) == 5:
                                tempo_atual = "0" + tempo_atual

                            registro[0] = 'DOLNAFUT'
                            print(ticker_futuro, data_atual)

                            database_diretorio_futuros = os.path.join(
                                TD_DATABASE_DOLAR, "DOLNAFUT_TD.csv")
                            with open(database_diretorio_futuros, 'a', newline='') as csvfile:
                                writer = csv.writer(csvfile, delimiter=';')
                                writer.writerow(registro)
                                csvfile.close()

                #  CONTRATO FUTURO ---> DOLG22
                elif ultimo_date >= 20211229 and ultimo_date < 20220128:

                    if arquivo != 'DOLG22.csv':
                        continue

                    with open('DOLG22.csv', 'r') as arquivo_referencia:
                        arquivo_csv = csv.reader(
                            arquivo_referencia, delimiter=';')
                        for registro in arquivo_csv:

                            ticker_futuro = registro[0]

                            if ticker_futuro == '<ticker>':
                                continue

                            data_atual = int(registro[1])
                            tempo_atual = str(registro[2])

                            if data_atual <= 20211229 or data_atual > 20220128:
                                continue

                            if ultimo_date >= data_atual:
                                continue

                            if len(tempo_atual) == 5:
                                tempo_atual = "0" + tempo_atual

                            registro[0] = 'DOLNAFUT'
                            print(ticker_futuro, data_atual)

                            database_diretorio_futuros = os.path.join(
                                TD_DATABASE_DOLAR, "DOLNAFUT_TD.csv")
                            with open(database_diretorio_futuros, 'a', newline='') as csvfile:
                                writer = csv.writer(csvfile, delimiter=';')
                                writer.writerow(registro)
                                csvfile.close()

                #  CONTRATO FUTURO ---> DOLH22
                elif ultimo_date >= 20220128 and ultimo_date < 20220224:

                    if arquivo != 'DOLH22.csv':
                        continue

                    with open('DOLH22.csv', 'r') as arquivo_referencia:
                        arquivo_csv = csv.reader(
                            arquivo_referencia, delimiter=';')
                        for registro in arquivo_csv:

                            ticker_futuro = registro[0]

                            if ticker_futuro == '<ticker>':
                                continue

                            data_atual = int(registro[1])
                            tempo_atual = str(registro[2])

                            if data_atual <= 20220128 or data_atual > 20220224:
                                continue

                            if ultimo_date >= data_atual:
                                continue

                            if len(tempo_atual) == 5:
                                tempo_atual = "0" + tempo_atual

                            registro[0] = 'DOLNAFUT'
                            print(ticker_futuro, data_atual)

                            database_diretorio_futuros = os.path.join(
                                TD_DATABASE_DOLAR, "DOLNAFUT_TD.csv")
                            with open(database_diretorio_futuros, 'a', newline='') as csvfile:
                                writer = csv.writer(csvfile, delimiter=';')
                                writer.writerow(registro)
                                csvfile.close()

                #  CONTRATO FUTURO ---> DOLJ22
                elif ultimo_date >= 20220224 and ultimo_date < 20220330:

                    if arquivo != 'DOLJ22.csv':
                        continue

                    with open('DOLJ22.csv', 'r') as arquivo_referencia:
                        arquivo_csv = csv.reader(
                            arquivo_referencia, delimiter=';')
                        for registro in arquivo_csv:

                            ticker_futuro = registro[0]
                            if ticker_futuro == '<ticker>':
                                continue

                            data_atual = int(registro[1])
                            tempo_atual = str(registro[2])

                            if data_atual <= 20220224 or data_atual > 20220330:
                                continue

                            if ultimo_date >= data_atual:
                                continue

                            if len(tempo_atual) == 5:
                                tempo_atual = "0" + tempo_atual

                            registro[0] = 'DOLNAFUT'
                            print(ticker_futuro, data_atual)

                            database_diretorio_futuros = os.path.join(
                                TD_DATABASE_DOLAR, "DOLNAFUT_TD.csv")
                            with open(database_diretorio_futuros, 'a', newline='') as csvfile:
                                writer = csv.writer(csvfile, delimiter=';')
                                writer.writerow(registro)
                                csvfile.close()

                #  CONTRATO FUTURO ---> DOLK22
                elif ultimo_date >= 20220330 and ultimo_date < 20220428:

                    if arquivo != 'DOLK22.csv':
                        continue

                    with open('DOLK22.csv', 'r') as arquivo_referencia:
                        arquivo_csv = csv.reader(
                            arquivo_referencia, delimiter=';')
                        for registro in arquivo_csv:

                            ticker_futuro = registro[0]
                            if ticker_futuro == '<ticker>':
                                continue

                            data_atual = int(registro[1])
                            tempo_atual = str(registro[2])

                            if data_atual <= 20220330 or data_atual > 20220428:
                                continue

                            if int(date) >= data_atual:
                                continue

                            if len(tempo_atual) == 5:
                                tempo_atual = "0" + tempo_atual

                            registro[0] = 'DOLNAFUT'
                            print(ticker_futuro, data_atual)

                            database_diretorio_futuros = os.path.join(
                                TD_DATABASE_DOLAR, "DOLNAFUT_TD.csv")
                            with open(database_diretorio_futuros, 'a', newline='') as csvfile:
                                writer = csv.writer(csvfile, delimiter=';')
                                writer.writerow(registro)
                                csvfile.close()

                #  CONTRATO FUTURO ---> DOLM22
                elif ultimo_date >= 20220428 and ultimo_date < 20220530:

                    if arquivo != 'DOLM22.csv':
                        continue

                    with open('DOLM22.csv', 'r') as arquivo_referencia:
                        arquivo_csv = csv.reader(
                            arquivo_referencia, delimiter=';')
                        for registro in arquivo_csv:

                            ticker_futuro = registro[0]
                            if ticker_futuro == '<ticker>':
                                continue

                            data_atual = int(registro[1])
                            tempo_atual = str(registro[2])

                            if data_atual <= 20220428 or data_atual > 20220530:
                                continue

                            if ultimo_date >= data_atual:
                                continue

                            if len(tempo_atual) == 5:
                                tempo_atual = "0" + tempo_atual

                            registro[0] = 'DOLNAFUT'
                            print(ticker_futuro, data_atual)

                            database_diretorio_futuros = os.path.join(
                                TD_DATABASE_DOLAR, "DOLNAFUT_TD.csv")
                            with open(database_diretorio_futuros, 'a', newline='') as csvfile:
                                writer = csv.writer(csvfile, delimiter=';')
                                writer.writerow(registro)
                                csvfile.close()

                #  CONTRATO FUTURO ---> DOLN22
                elif ultimo_date >= 20220530 and ultimo_date < 20220629:

                    if arquivo != 'DOLN22.csv':
                        continue

                    with open('DOLN22.csv', 'r') as arquivo_referencia:
                        arquivo_csv = csv.reader(
                            arquivo_referencia, delimiter=';')
                        for registro in arquivo_csv:

                            ticker_futuro = registro[0]
                            if ticker_futuro == '<ticker>':
                                continue

                            data_atual = int(registro[1])
                            tempo_atual = str(registro[2])

                            if data_atual <= 20220530 or data_atual > 20220629:
                                continue

                            if ultimo_date >= data_atual:
                                continue

                            if len(tempo_atual) == 5:
                                tempo_atual = "0" + tempo_atual

                            registro[0] = 'DOLNAFUT'
                            print(ticker_futuro, data_atual)

                            database_diretorio_futuros = os.path.join(
                                TD_DATABASE_DOLAR, "DOLNAFUT_TD.csv")
                            with open(database_diretorio_futuros, 'a', newline='') as csvfile:
                                writer = csv.writer(csvfile, delimiter=';')
                                writer.writerow(registro)
                                csvfile.close()

                #  CONTRATO FUTURO ---> DOLQ22
                elif ultimo_date >= 20220629 and ultimo_date < 20220728:

                    if arquivo != 'DOLQ22.csv':
                        continue

                    with open('DOLQ22.csv', 'r') as arquivo_referencia:
                        arquivo_csv = csv.reader(
                            arquivo_referencia, delimiter=';')
                        for registro in arquivo_csv:

                            ticker_futuro = registro[0]
                            if ticker_futuro == '<ticker>':
                                continue

                            data_atual = int(registro[1])
                            tempo_atual = str(registro[2])

                            if data_atual <= 20220629 or data_atual > 20220728:
                                continue

                            if ultimo_date >= data_atual:
                                continue

                            if len(tempo_atual) == 5:
                                tempo_atual = "0" + tempo_atual

                            registro[0] = 'DOLNAFUT'
                            print(ticker_futuro, data_atual)

                            database_diretorio_futuros = os.path.join(
                                TD_DATABASE_DOLAR, "DOLNAFUT_TD.csv")
                            with open(database_diretorio_futuros, 'a', newline='') as csvfile:
                                writer = csv.writer(csvfile, delimiter=';')
                                writer.writerow(registro)
                                csvfile.close()

                #  CONTRATO FUTURO ---> DOLU22
                elif ultimo_date >= 20220728 and ultimo_date < 20220830:

                    if arquivo != 'DOLU22.csv':
                        continue

                    with open('DOLU22.csv', 'r') as arquivo_referencia:
                        arquivo_csv = csv.reader(
                            arquivo_referencia, delimiter=';')
                        for registro in arquivo_csv:

                            ticker_futuro = registro[0]
                            if ticker_futuro == '<ticker>':
                                continue

                            data_atual = int(registro[1])
                            tempo_atual = str(registro[2])

                            if data_atual <= 20220728 or data_atual > 20220830:
                                continue

                            if ultimo_date >= data_atual:
                                continue

                            if len(tempo_atual) == 5:
                                tempo_atual = "0" + tempo_atual

                            registro[0] = 'DOLNAFUT'
                            print(ticker_futuro, data_atual)

                            database_diretorio_futuros = os.path.join(
                                TD_DATABASE_DOLAR, "DOLNAFUT_TD.csv")
                            with open(database_diretorio_futuros, 'a', newline='') as csvfile:
                                writer = csv.writer(csvfile, delimiter=';')
                                writer.writerow(registro)
                                csvfile.close()

                #  CONTRATO FUTURO ---> DOLV22
                elif ultimo_date >= 20220830 and ultimo_date < 20220929:

                    if arquivo != 'DOLV22.csv':
                        continue

                    with open('DOLV22.csv', 'r') as arquivo_referencia:
                        arquivo_csv = csv.reader(
                            arquivo_referencia, delimiter=';')
                        for registro in arquivo_csv:

                            ticker_futuro = registro[0]
                            if ticker_futuro == '<ticker>':
                                continue

                            data_atual = int(registro[1])
                            tempo_atual = str(registro[2])

                            if data_atual <= 20220830 or data_atual > 20220929:
                                continue

                            if ultimo_date >= data_atual:
                                continue

                            if len(tempo_atual) == 5:
                                tempo_atual = "0" + tempo_atual

                            registro[0] = 'DOLNAFUT'
                            print(ticker_futuro, data_atual)

                            database_diretorio_futuros = os.path.join(
                                TD_DATABASE_DOLAR, "DOLNAFUT_TD.csv")
                            with open(database_diretorio_futuros, 'a', newline='') as csvfile:
                                writer = csv.writer(csvfile, delimiter=';')
                                writer.writerow(registro)
                                csvfile.close()

                #  CONTRATO FUTURO ---> DOLX22
                elif ultimo_date >= 20220929 and ultimo_date < 20221028:

                    if arquivo != 'DOLX22.csv':
                        continue

                    with open('DOLX22.csv', 'r') as arquivo_referencia:
                        arquivo_csv = csv.reader(
                            arquivo_referencia, delimiter=';')
                        for registro in arquivo_csv:

                            ticker_futuro = registro[0]
                            if ticker_futuro == '<ticker>':
                                continue

                            data_atual = int(registro[1])
                            tempo_atual = str(registro[2])

                            if data_atual <= 20220929 or data_atual > 20221028:
                                continue

                            if ultimo_date >= data_atual:
                                continue

                            if len(tempo_atual) == 5:
                                tempo_atual = "0" + tempo_atual

                            registro[0] = 'DOLNAFUT'
                            print(ticker_futuro, data_atual)

                            database_diretorio_futuros = os.path.join(
                                TD_DATABASE_DOLAR,"DOLNAFUT_TD.csv")
                            with open(database_diretorio_futuros, 'a', newline='') as csvfile:
                                writer = csv.writer(csvfile, delimiter=';')
                                writer.writerow(registro)
                                csvfile.close()

                #  CONTRATO FUTURO ---> DOLZ22
                elif ultimo_date >= 20221028 and ultimo_date < 20221129:

                    if arquivo != 'DOLZ22.csv':
                        continue

                    with open('DOLZ22.csv', 'r') as arquivo_referencia:
                        arquivo_csv = csv.reader(
                            arquivo_referencia, delimiter=';')
                        for registro in arquivo_csv:

                            ticker_futuro = registro[0]
                            if ticker_futuro == '<ticker>':
                                continue

                            data_atual = int(registro[1])
                            tempo_atual = str(registro[2])

                            if data_atual <= 20221028 or data_atual > 20221129:
                                continue

                            if ultimo_date >= data_atual:
                                continue

                            if len(tempo_atual) == 5:
                                tempo_atual = "0" + tempo_atual

                            registro[0] = 'DOLNAFUT'
                            print(ticker_futuro, data_atual)

                            database_diretorio_futuros = os.path.join(
                                TD_DATABASE_DOLAR, "DOLNAFUT_TD.csv")
                            with open(database_diretorio_futuros, 'a', newline='') as csvfile:
                                writer = csv.writer(csvfile, delimiter=';')
                                writer.writerow(registro)
                                csvfile.close()

                #  CONTRATO FUTURO ---> DOLF23
                elif ultimo_date >= 20221129 and ultimo_date < 20221229:

                    if arquivo != 'DOLF23.csv':
                        continue

                    with open('DOLF23.csv', 'r') as arquivo_referencia:
                        arquivo_csv = csv.reader(
                            arquivo_referencia, delimiter=';')
                        for registro in arquivo_csv:

                            ticker_futuro = registro[0]
                            if ticker_futuro == '<ticker>':
                                continue

                            data_atual = int(registro[1])
                            tempo_atual = str(registro[2])

                            if data_atual <= 20221129 or data_atual > 20221229:
                                continue

                            if ultimo_date >= data_atual:
                                continue

                            if len(tempo_atual) == 5:
                                tempo_atual = "0" + tempo_atual

                            registro[0] = 'DOLNAFUT'
                            print(ticker_futuro, data_atual)

                            database_diretorio_futuros = os.path.join(
                                TD_DATABASE_DOLAR, "DOLNAFUT_TD.csv")
                            with open(database_diretorio_futuros, 'a', newline='') as csvfile:
                                writer = csv.writer(csvfile, delimiter=';')
                                writer.writerow(registro)
                                csvfile.close()




            # --------------------- MINI INDICE FUTURO --------------------- # 



            elif ticker == 'WINNAFUT':

                #  CONTRATO FUTURO ---> WING22
                if ultimo_date >= 20211214 and ultimo_date < 20220216:
                    if arquivo != 'WING22_BMF_I.csv':
                        continue

                    with open("WING22_BMF_I.csv", 'r') as arquivo_referencia:
                        arquivo_csv = csv.reader(
                            arquivo_referencia, delimiter=';')
                        for registro in arquivo_csv:

                            ticker_futuro = registro[0]

                            if ticker_futuro == '<ticker>':
                                continue

                            data_atual = int(registro[1])
                            tempo_atual = str(registro[2])

                            if data_atual <= 20211214 or data_atual > 20220216:
                                continue

                            if ultimo_date >= data_atual:
                                continue

                            if len(tempo_atual) == 5:
                                tempo_atual = "0" + tempo_atual

                            registro[0] = 'WINNAFUT'
                            print(ticker_futuro, data_atual)

                            database_diretorio_futuros = os.path.join(
                                TD_DATABASE_DOLAR, "WINNAFUT_BMF_I.csv")
                            with open(database_diretorio_futuros, 'a', newline='') as csvfile:
                                writer = csv.writer(csvfile)
                                writer.writerow(registro)
                                csvfile.close()

                #  CONTRATO FUTURO ---> WINF22
                elif ultimo_date >= 20220216 and ultimo_date < 20220412:

                    if arquivo != 'WINJ22_BMF_I.csv':
                        continue

                    with open("WINJ22_BMF_I.csv", 'r') as arquivo_referencia:
                        arquivo_csv = csv.reader(
                            arquivo_referencia, delimiter=',')
                        for registro in arquivo_csv:

                            ticker_futuro = registro[0]

                            if ticker_futuro == '<ticker>':
                                continue

                            data_atual = int(registro[1])
                            tempo_atual = str(registro[2])

                            if data_atual <= 20220216 or data_atual > 20220412:
                                continue

                            if ultimo_date >= data_atual:
                                continue

                            if len(tempo_atual) == 5:
                                tempo_atual = "0" + tempo_atual

                            registro[0] = 'WINNAFUT'
                            print(ticker_futuro, data_atual)

                            database_diretorio_futuros = os.path.join(
                                TD_DATABASE_DOLAR, "WINNAFUT_BMF_I.csv")
                            with open(database_diretorio_futuros, 'a', newline='') as csvfile:
                                writer = csv.writer(csvfile)
                                writer.writerow(registro)
                                csvfile.close()

                #  CONTRATO FUTURO ---> WINM22
                elif ultimo_date >= 20220412 and ultimo_date < 20220614:

                    if arquivo != 'WINM22_BMF_I.csv':
                        continue

                    with open("WINM22_BMF_I.csv", 'r') as arquivo_referencia:
                        arquivo_csv = csv.reader(
                            arquivo_referencia, delimiter=',')
                        for registro in arquivo_csv:

                            ticker_futuro = registro[0]

                            if ticker_futuro == '<ticker>':
                                continue

                            data_atual = int(registro[1])
                            tempo_atual = str(registro[2])

                            if data_atual <= 20220412 or data_atual > 20220614:
                                continue

                            if ultimo_date >= data_atual:
                                continue

                            if len(tempo_atual) == 5:
                                tempo_atual = "0" + tempo_atual

                            registro[0] = 'WINNAFUT'
                            print(ticker_futuro, data_atual)

                            database_diretorio_futuros = os.path.join(
                                TD_DATABASE_DOLAR, "WINNAFUT_BMF_I.csv")
                            with open(database_diretorio_futuros, 'a', newline='') as csvfile:
                                writer = csv.writer(csvfile)
                                writer.writerow(registro)
                                csvfile.close()

                #  CONTRATO FUTURO ---> WINQ22
                elif ultimo_date >= 20220614 and ultimo_date < 20220816:

                    if arquivo != 'WINQ22_BMF_I.csv':
                        continue

                    with open("WINQ22_BMF_I.csv", 'r') as arquivo_referencia:
                        arquivo_csv = csv.reader(
                            arquivo_referencia, delimiter=',')
                        for registro in arquivo_csv:

                            ticker_futuro = registro[0]

                            if ticker_futuro == '<ticker>':
                                continue

                            data_atual = int(registro[1])
                            tempo_atual = str(registro[2])

                            if data_atual <= 20220614 or data_atual > 20220816:
                                continue

                            if ultimo_date >= data_atual:
                                continue

                            if len(tempo_atual) == 5:
                                tempo_atual = "0" + tempo_atual

                            registro[0] = 'WINNAFUT'
                            print(ticker_futuro, data_atual)

                            database_diretorio_futuros = os.path.join(
                                TD_DATABASE_DOLAR, "WINNAFUT_BMF_I.csv")
                            with open(database_diretorio_futuros, 'a', newline='') as csvfile:
                                writer = csv.writer(csvfile)
                                writer.writerow(registro)
                                csvfile.close()

                #  CONTRATO FUTURO ---> WINV22
                elif ultimo_date >= 20220816 and ultimo_date < 20221011:

                    if arquivo != 'WINV22_BMF_I.csv':
                        continue

                    with open("WINV22_BMF_I.csv", 'r') as arquivo_referencia:
                        arquivo_csv = csv.reader(
                            arquivo_referencia, delimiter=',')
                        for registro in arquivo_csv:

                            ticker_futuro = registro[0]

                            if ticker_futuro == '<ticker>':
                                continue

                            data_atual = int(registro[1])
                            tempo_atual = str(registro[2])

                            if data_atual <= 20220816 or data_atual > 20221011:
                                continue

                            if ultimo_date >= data_atual:
                                continue

                            if len(tempo_atual) == 5:
                                tempo_atual = "0" + tempo_atual

                            registro[0] = 'WINNAFUT'
                            print(ticker_futuro, data_atual)

                            database_diretorio_futuros = os.path.join(
                                TD_DATABASE_DOLAR, "WINNAFUT_BMF_I.csv")
                            with open(database_diretorio_futuros, 'a', newline='') as csvfile:
                                writer = csv.writer(csvfile)
                                writer.writerow(registro)
                                csvfile.close()

                #  CONTRATO FUTURO ---> WINZ22
                elif ultimo_date >= 20221011 and ultimo_date < 20221213:

                    if arquivo != 'WINZ22_BMF_I.csv':
                        continue

                    with open("WINZ22_BMF_I.csv", 'r') as arquivo_referencia:
                        arquivo_csv = csv.reader(
                            arquivo_referencia, delimiter=',')
                        for registro in arquivo_csv:

                            ticker_futuro = registro[0]

                            if ticker_futuro == '<ticker>':
                                continue

                            data_atual = int(registro[1])
                            tempo_atual = str(registro[2])

                            if data_atual <= 20221011 or data_atual > 20221213:
                                continue

                            if ultimo_date >= data_atual:
                                continue

                            if len(tempo_atual) == 5:
                                tempo_atual = "0" + tempo_atual

                            registro[0] = 'WINNAFUT'
                            print(ticker_futuro, data_atual)

                            database_diretorio_futuros = os.path.join(
                                TD_DATABASE_DOLAR, "WINNAFUT_BMF_I.csv")
                            with open(database_diretorio_futuros, 'a', newline='') as csvfile:
                                writer = csv.writer(csvfile)
                                writer.writerow(registro)
                                csvfile.close()

                #  CONTRATO FUTURO ---> WING23
                elif ultimo_date >= 20221213 and ultimo_date < 20230214:

                    if arquivo != 'WING23_BMF_I.csv':
                        continue

                    with open("WING23_BMF_I.csv", 'r') as arquivo_referencia:
                        arquivo_csv = csv.reader(
                            arquivo_referencia, delimiter=',')
                        for registro in arquivo_csv:

                            ticker_futuro = registro[0]

                            if ticker_futuro == '<ticker>':
                                continue

                            data_atual = int(registro[1])
                            tempo_atual = str(registro[2])

                            if data_atual <= 20221213 or data_atual > 20230214:
                                continue

                            if ultimo_date >= data_atual:
                                continue

                            if len(tempo_atual) == 5:
                                tempo_atual = "0" + tempo_atual

                            registro[0] = 'WINNAFUT'
                            print(ticker_futuro, data_atual)

                            database_diretorio_futuros = os.path.join(
                                TD_DATABASE_DOLAR, "WINNAFUT_BMF_I.csv")
                            with open(database_diretorio_futuros, 'a', newline='') as csvfile:
                                writer = csv.writer(csvfile)
                                writer.writerow(registro)
                                csvfile.close()

            elif ticker == 'INDNAFUT':

                #  CONTRATO FUTURO ---> INDG22
                if ultimo_date >= 20211214 and ultimo_date < 20220216:

                    if arquivo != 'INDG22_BMF_I.csv':
                        continue

                    with open("INDG22_BMF_I.csv", 'r') as arquivo_referencia:
                        arquivo_csv = csv.reader(
                            arquivo_referencia, delimiter=',')
                        for registro in arquivo_csv:

                            ticker_futuro = registro[0]

                            if ticker_futuro == '<ticker>':
                                continue

                            data_atual = int(registro[1])
                            tempo_atual = str(registro[2])

                            if data_atual <= 20211214 or data_atual > 20220216:
                                continue

                            if ultimo_date >= data_atual:
                                continue

                            if len(tempo_atual) == 5:
                                tempo_atual = "0" + tempo_atual

                            registro[0] = 'INDNAFUT'
                            print(ticker_futuro, data_atual)

                            database_diretorio_futuros = os.path.join(
                                TD_DATABASE_DOLAR, "INDNAFUT_BMF_I.csv")
                            with open(database_diretorio_futuros, 'a', newline='') as csvfile:
                                writer = csv.writer(csvfile)
                                writer.writerow(registro)
                                csvfile.close()

                #  CONTRATO FUTURO ---> INDG22
                elif ultimo_date >= 20220216 and ultimo_date < 20220412:

                    if arquivo != 'INDJ22_BMF_I.csv':
                        continue

                    with open("INDJ22_BMF_I.csv", 'r') as arquivo_referencia:
                        arquivo_csv = csv.reader(
                            arquivo_referencia, delimiter=',')
                        for registro in arquivo_csv:

                            ticker_futuro = registro[0]

                            if ticker_futuro == '<ticker>':
                                continue

                            data_atual = int(registro[1])
                            tempo_atual = str(registro[2])

                            if data_atual <= 20220216 or data_atual > 20220412:
                                continue

                            if ultimo_date >= data_atual:
                                continue

                            if len(tempo_atual) == 5:
                                tempo_atual = "0" + tempo_atual

                            registro[0] = 'INDNAFUT'
                            print(ticker_futuro, data_atual)

                            database_diretorio_futuros = os.path.join(
                                TD_DATABASE_DOLAR, "INDNAFUT_BMF_I.csv")
                            with open(database_diretorio_futuros, 'a', newline='') as csvfile:
                                writer = csv.writer(csvfile)
                                writer.writerow(registro)
                                csvfile.close()

                #  CONTRATO FUTURO ---> INDM22
                elif ultimo_date >= 20220412 and ultimo_date < 20220614:

                    if arquivo != 'INDM22_BMF_I.csv':
                        continue

                    with open("INDM22_BMF_I.csv", 'r') as arquivo_referencia:
                        arquivo_csv = csv.reader(
                            arquivo_referencia, delimiter=',')
                        for registro in arquivo_csv:

                            ticker_futuro = registro[0]

                            if ticker_futuro == '<ticker>':
                                continue

                            data_atual = int(registro[1])
                            tempo_atual = str(registro[2])

                            if data_atual <= 20220412 or data_atual > 20220614:
                                continue

                            if ultimo_date >= data_atual:
                                continue

                            if len(tempo_atual) == 5:
                                tempo_atual = "0" + tempo_atual

                            registro[0] = 'INDNAFUT'
                            print(ticker_futuro, data_atual)

                            database_diretorio_futuros = os.path.join(
                                TD_DATABASE_DOLAR, "INDNAFUT_BMF_I.csv")
                            with open(database_diretorio_futuros, 'a', newline='') as csvfile:
                                writer = csv.writer(csvfile)
                                writer.writerow(registro)
                                csvfile.close()

                #  CONTRATO FUTURO ---> INDQ22
                elif ultimo_date >= 20220614 and ultimo_date < 20220816:

                    if arquivo != 'INDQ22_BMF_I.csv':
                        continue

                    with open("INDQ22_BMF_I.csv", 'r') as arquivo_referencia:
                        arquivo_csv = csv.reader(
                            arquivo_referencia, delimiter=',')
                        for registro in arquivo_csv:

                            ticker_futuro = registro[0]

                            if ticker_futuro == '<ticker>':
                                continue

                            data_atual = int(registro[1])
                            tempo_atual = str(registro[2])

                            if data_atual <= 20220614 or data_atual > 20220816:
                                continue

                            if ultimo_date >= data_atual:
                                continue

                            if len(tempo_atual) == 5:
                                tempo_atual = "0" + tempo_atual

                            registro[0] = 'INDNAFUT'
                            print(ticker_futuro, data_atual)

                            database_diretorio_futuros = os.path.join(
                                TD_DATABASE_DOLAR, "INDNAFUT_BMF_I.csv")
                            with open(database_diretorio_futuros, 'a', newline='') as csvfile:
                                writer = csv.writer(csvfile)
                                writer.writerow(registro)
                                csvfile.close()

                #  CONTRATO FUTURO ---> INDV22
                elif ultimo_date >= 20220816 and ultimo_date < 20221011:

                    if arquivo != 'INDV22_BMF_I.csv':
                        continue

                    with open("INDV22_BMF_I.csv", 'r') as arquivo_referencia:
                        arquivo_csv = csv.reader(
                            arquivo_referencia, delimiter=',')
                        for registro in arquivo_csv:

                            ticker_futuro = registro[0]

                            if ticker_futuro == '<ticker>':
                                continue

                            data_atual = int(registro[1])
                            tempo_atual = str(registro[2])

                            if data_atual <= 20220816 or data_atual > 20221011:
                                continue

                            if ultimo_date >= data_atual:
                                continue

                            if len(tempo_atual) == 5:
                                tempo_atual = "0" + tempo_atual

                            registro[0] = 'INDNAFUT'
                            print(ticker_futuro, data_atual)

                            database_diretorio_futuros = os.path.join(
                                TD_DATABASE_DOLAR, "INDNAFUT_BMF_I.csv")
                            with open(database_diretorio_futuros, 'a', newline='') as csvfile:
                                writer = csv.writer(csvfile)
                                writer.writerow(registro)
                                csvfile.close()

                #  CONTRATO FUTURO ---> INDZ22
                elif ultimo_date >= 20221011 and ultimo_date < 20221213:

                    if arquivo != 'INDZ22_BMF_I.csv':
                        continue

                    with open("INDZ22_BMF_I.csv", 'r') as arquivo_referencia:
                        arquivo_csv = csv.reader(
                            arquivo_referencia, delimiter=',')
                        for registro in arquivo_csv:

                            ticker_futuro = registro[0]

                            if ticker_futuro == '<ticker>':
                                continue

                            data_atual = int(registro[1])
                            tempo_atual = str(registro[2])

                            if data_atual <= 20221011 or data_atual > 20221213:
                                continue

                            if ultimo_date >= data_atual:
                                continue

                            if len(tempo_atual) == 5:
                                tempo_atual = "0" + tempo_atual

                            registro[0] = 'INDNAFUT'
                            print(ticker_futuro, data_atual)

                            database_diretorio_futuros = os.path.join(
                                TD_DATABASE_DOLAR, "INDNAFUT_BMF_I.csv")
                            with open(database_diretorio_futuros, 'a', newline='') as csvfile:
                                writer = csv.writer(csvfile)
                                writer.writerow(registro)
                                csvfile.close()

                #  CONTRATO FUTURO ---> INDG23
                elif ultimo_date >= 20221213 and ultimo_date < 20230214:

                    if arquivo != 'INDG23_BMF_I.csv':
                        continue

                    with open("INDG23_BMF_I.csv", 'r') as arquivo_referencia:
                        arquivo_csv = csv.reader(
                            arquivo_referencia, delimiter=',')
                        for registro in arquivo_csv:

                            ticker_futuro = registro[0]

                            if ticker_futuro == '<ticker>':
                                continue

                            data_atual = int(registro[1])
                            tempo_atual = str(registro[2])

                            if data_atual <= 20221213 or data_atual > 20230214:
                                continue

                            if ultimo_date >= data_atual:
                                continue

                            if len(tempo_atual) == 5:
                                tempo_atual = "0" + tempo_atual

                            registro[0] = 'INDNAFUT'
                            print(ticker_futuro, data_atual)

                            database_diretorio_futuros = os.path.join(
                                TD_DATABASE_DOLAR, "INDNAFUT_BMF_I.csv")
                            with open(database_diretorio_futuros, 'a', newline='') as csvfile:
                                writer = csv.writer(csvfile)
                                writer.writerow(registro)
                                csvfile.close()


if __name__ == '__main__':

    inicio = time.time()

    date, ticker = data_atual("WDONAFUT_TD.csv")
    concatenar_contratos(int(date), ticker)
    fim = time.time()
    print(f'Tempo de execução ---> {(fim - inicio) / 60}')
