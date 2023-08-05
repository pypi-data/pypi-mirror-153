import csv
import os
import time

B3_FUTUROS = r'D:\DIRETORIOS\B3_FUTUROS'
DADOS_FINANCEIROS = r'D:\DADOS_FINANCEIROS'


def data_atual(arquivo):
    """
    Utilizado para retornar a ultima data do arquivo 
    selecionado.
    """
    os.chdir(DADOS_FINANCEIROS)
    data = None
    ticker = None

    with open(arquivo, 'r') as arquivo_referencia:
        arquivo_csv = csv.reader(arquivo_referencia, delimiter=',')
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
    for caminho_path, dir_arquivo, arquivos in os.walk(B3_FUTUROS):
        for arquivo in arquivos:
            if ticker == 'WDONAFUT':
                #  CONTRATO FUTURO ---> WDOF22
                if ultimo_date > 20211129 and ultimo_date < 20211229:

                    if arquivo != 'WDOF22_BMF_I.csv':
                        continue

                    with open(os.path.join(caminho_path, "WDOF22_BMF_I.csv"), 'r') as arquivo_referencia:
                        arquivo_csv = csv.reader(
                            arquivo_referencia, delimiter=',')
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
                                DADOS_FINANCEIROS, "WDONAFUT_BMF_I.csv")
                            with open(database_diretorio_futuros, 'a', newline='') as csvfile:
                                writer = csv.writer(csvfile)
                                writer.writerow(registro)
                                csvfile.close()

                #  CONTRATO FUTURO ---> WDOG22
                elif ultimo_date >= 20211229 and ultimo_date < 20220128:

                    if arquivo != 'WDOG22_BMF_I.csv':
                        continue

                    with open('WDOG22_BMF_I.csv', 'r') as arquivo_referencia:
                        arquivo_csv = csv.reader(
                            arquivo_referencia, delimiter=',')
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
                                DADOS_FINANCEIROS, "WDONAFUT_BMF_I.csv")
                            with open(database_diretorio_futuros, 'a', newline='') as csvfile:
                                writer = csv.writer(csvfile)
                                writer.writerow(registro)
                                csvfile.close()

                #  CONTRATO FUTURO ---> WDOH22
                elif ultimo_date >= 20220128 and ultimo_date < 20220224:

                    if arquivo != 'WDOH22_BMF_I.csv':
                        continue

                    with open('WDOH22_BMF_I.csv', 'r') as arquivo_referencia:
                        arquivo_csv = csv.reader(
                            arquivo_referencia, delimiter=',')
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
                                DADOS_FINANCEIROS, "WDONAFUT_BMF_I.csv")
                            with open(database_diretorio_futuros, 'a', newline='') as csvfile:
                                writer = csv.writer(csvfile)
                                writer.writerow(registro)
                                csvfile.close()

                #  CONTRATO FUTURO ---> WDOJ22
                elif ultimo_date >= 20220224 and ultimo_date < 20220330:

                    if arquivo != 'WDOJ22_BMF_I.csv':
                        continue

                    with open('WDOJ22_BMF_I.csv', 'r') as arquivo_referencia:
                        arquivo_csv = csv.reader(
                            arquivo_referencia, delimiter=',')
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
                                DADOS_FINANCEIROS, "WDONAFUT_BMF_I.csv")
                            with open(database_diretorio_futuros, 'a', newline='') as csvfile:
                                writer = csv.writer(csvfile)
                                writer.writerow(registro)
                                csvfile.close()

                #  CONTRATO FUTURO ---> WDOK22
                elif ultimo_date >= 20220330 and ultimo_date < 20220428:

                    if arquivo != 'WDOK22_BMF_I.csv':
                        continue

                    with open('WDOK22_BMF_I.csv', 'r') as arquivo_referencia:
                        arquivo_csv = csv.reader(
                            arquivo_referencia, delimiter=',')
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
                                DADOS_FINANCEIROS, "WDONAFUT_BMF_I.csv")
                            with open(database_diretorio_futuros, 'a', newline='') as csvfile:
                                writer = csv.writer(csvfile)
                                writer.writerow(registro)
                                csvfile.close()

                #  CONTRATO FUTURO ---> WDOM22
                elif ultimo_date >= 20220428 and ultimo_date < 20220530:

                    if arquivo != 'WDOM22_BMF_I.csv':
                        continue

                    with open('WDOM22_BMF_I.csv', 'r') as arquivo_referencia:
                        arquivo_csv = csv.reader(
                            arquivo_referencia, delimiter=',')
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
                                DADOS_FINANCEIROS, "WDONAFUT_BMF_I.csv")
                            with open(database_diretorio_futuros, 'a', newline='') as csvfile:
                                writer = csv.writer(csvfile)
                                writer.writerow(registro)
                                csvfile.close()

                #  CONTRATO FUTURO ---> WDON22
                elif ultimo_date >= 20220530 and ultimo_date < 20220629:

                    if arquivo != 'WDON22_BMF_I.csv':
                        continue

                    with open('WDON22_BMF_I.csv', 'r') as arquivo_referencia:
                        arquivo_csv = csv.reader(
                            arquivo_referencia, delimiter=',')
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
                                DADOS_FINANCEIROS, "WDONAFUT_BMF_I.csv")
                            with open(database_diretorio_futuros, 'a', newline='') as csvfile:
                                writer = csv.writer(csvfile)
                                writer.writerow(registro)
                                csvfile.close()

                #  CONTRATO FUTURO ---> WDOQ22
                elif ultimo_date >= 20220629 and ultimo_date < 20220728:

                    if arquivo != 'WDOQ22_BMF_I.csv':
                        continue

                    with open('WDOQ22_BMF_I.csv', 'r') as arquivo_referencia:
                        arquivo_csv = csv.reader(
                            arquivo_referencia, delimiter=',')
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
                                DADOS_FINANCEIROS, "WDONAFUT_BMF_I.csv")
                            with open(database_diretorio_futuros, 'a', newline='') as csvfile:
                                writer = csv.writer(csvfile)
                                writer.writerow(registro)
                                csvfile.close()

                #  CONTRATO FUTURO ---> WDOU22
                elif ultimo_date >= 20220728 and ultimo_date < 20220830:

                    if arquivo != 'WDOU22_BMF_I.csv':
                        continue

                    with open('WDOU22_BMF_I.csv', 'r') as arquivo_referencia:
                        arquivo_csv = csv.reader(
                            arquivo_referencia, delimiter=',')
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
                                DADOS_FINANCEIROS, "WDONAFUT_BMF_I.csv")
                            with open(database_diretorio_futuros, 'a', newline='') as csvfile:
                                writer = csv.writer(csvfile)
                                writer.writerow(registro)
                                csvfile.close()

                #  CONTRATO FUTURO ---> WDOV22
                elif ultimo_date >= 20220830 and ultimo_date < 20220929:

                    if arquivo != 'WDOV22_BMF_I.csv':
                        continue

                    with open('WDOV22_BMF_I.csv', 'r') as arquivo_referencia:
                        arquivo_csv = csv.reader(
                            arquivo_referencia, delimiter=',')
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
                                DADOS_FINANCEIROS, "WDONAFUT_BMF_I.csv")
                            with open(database_diretorio_futuros, 'a', newline='') as csvfile:
                                writer = csv.writer(csvfile)
                                writer.writerow(registro)
                                csvfile.close()

                #  CONTRATO FUTURO ---> WDOX22
                elif ultimo_date >= 20220929 and ultimo_date < 20221028:

                    if arquivo != 'WDOX22_BMF_I.csv':
                        continue

                    with open('WDOX22_BMF_I.csv', 'r') as arquivo_referencia:
                        arquivo_csv = csv.reader(
                            arquivo_referencia, delimiter=',')
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
                                DADOS_FINANCEIROS, "WDONAFUT_BMF_I.csv")
                            with open(database_diretorio_futuros, 'a', newline='') as csvfile:
                                writer = csv.writer(csvfile)
                                writer.writerow(registro)
                                csvfile.close()

                #  CONTRATO FUTURO ---> WDOZ22
                elif ultimo_date >= 20221028 and ultimo_date < 20221129:

                    if arquivo != 'WDOZ22_BMF_I.csv':
                        continue

                    with open('WDOZ22_BMF_I.csv', 'r') as arquivo_referencia:
                        arquivo_csv = csv.reader(
                            arquivo_referencia, delimiter=',')
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
                                DADOS_FINANCEIROS, "WDONAFUT_BMF_I.csv")
                            with open(database_diretorio_futuros, 'a', newline='') as csvfile:
                                writer = csv.writer(csvfile)
                                writer.writerow(registro)
                                csvfile.close()

                #  CONTRATO FUTURO ---> WDOF23
                elif ultimo_date >= 20221129 and ultimo_date < 20221229:

                    if arquivo != 'WDOF23_BMF_I.csv':
                        continue

                    with open('WDOF223_BMF_I.csv', 'r') as arquivo_referencia:
                        arquivo_csv = csv.reader(
                            arquivo_referencia, delimiter=',')
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
                                DADOS_FINANCEIROS, "WDONAFUT_BMF_I.csv")
                            with open(database_diretorio_futuros, 'a', newline='') as csvfile:
                                writer = csv.writer(csvfile)
                                writer.writerow(registro)
                                csvfile.close()
            elif ticker == 'DOLNAFUT':
                #  CONTRATO FUTURO ---> DOLF22
                if ultimo_date > 20211129 and ultimo_date < 20211229:

                    if arquivo != 'DOLF22_BMF_I.csv':
                        continue

                    with open("DOLF22_BMF_I.csv", 'r') as arquivo_referencia:
                        arquivo_csv = csv.reader(
                            arquivo_referencia, delimiter=',')
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
                                DADOS_FINANCEIROS, "DOLNAFUT_BMF_I.csv")
                            with open(database_diretorio_futuros, 'a', newline='') as csvfile:
                                writer = csv.writer(csvfile)
                                writer.writerow(registro)
                                csvfile.close()

                #  CONTRATO FUTURO ---> DOLG22
                elif ultimo_date >= 20211229 and ultimo_date < 20220128:

                    if arquivo != 'DOLG22_BMF_I.csv':
                        continue

                    with open('DOLG22_BMF_I.csv', 'r') as arquivo_referencia:
                        arquivo_csv = csv.reader(
                            arquivo_referencia, delimiter=',')
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
                                DADOS_FINANCEIROS, "DOLNAFUT_BMF_I.csv")
                            with open(database_diretorio_futuros, 'a', newline='') as csvfile:
                                writer = csv.writer(csvfile)
                                writer.writerow(registro)
                                csvfile.close()

                #  CONTRATO FUTURO ---> DOLH22
                elif ultimo_date >= 20220128 and ultimo_date < 20220224:

                    if arquivo != 'DOLH22_BMF_I.csv':
                        continue

                    with open('DOLH22_BMF_I.csv', 'r') as arquivo_referencia:
                        arquivo_csv = csv.reader(
                            arquivo_referencia, delimiter=',')
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
                                DADOS_FINANCEIROS, "DOLNAFUT_BMF_I.csv")
                            with open(database_diretorio_futuros, 'a', newline='') as csvfile:
                                writer = csv.writer(csvfile)
                                writer.writerow(registro)
                                csvfile.close()

                #  CONTRATO FUTURO ---> DOLJ22
                elif ultimo_date >= 20220224 and ultimo_date < 20220330:

                    if arquivo != 'DOLJ22_BMF_I.csv':
                        continue

                    with open('DOLJ22_BMF_I.csv', 'r') as arquivo_referencia:
                        arquivo_csv = csv.reader(
                            arquivo_referencia, delimiter=',')
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
                                DADOS_FINANCEIROS, "DOLNAFUT_BMF_I.csv")
                            with open(database_diretorio_futuros, 'a', newline='') as csvfile:
                                writer = csv.writer(csvfile)
                                writer.writerow(registro)
                                csvfile.close()

                #  CONTRATO FUTURO ---> DOLK22
                elif ultimo_date >= 20220330 and ultimo_date < 20220428:

                    if arquivo != 'DOLK22_BMF_I.csv':
                        continue

                    with open('DOLK22_BMF_I.csv', 'r') as arquivo_referencia:
                        arquivo_csv = csv.reader(
                            arquivo_referencia, delimiter=',')
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
                                DADOS_FINANCEIROS, "DOLNAFUT_BMF_I.csv")
                            with open(database_diretorio_futuros, 'a', newline='') as csvfile:
                                writer = csv.writer(csvfile)
                                writer.writerow(registro)
                                csvfile.close()

                #  CONTRATO FUTURO ---> DOLM22
                elif ultimo_date >= 20220428 and ultimo_date < 20220530:

                    if arquivo != 'DOLM22_BMF_I.csv':
                        continue

                    with open('DOLM22_BMF_I.csv', 'r') as arquivo_referencia:
                        arquivo_csv = csv.reader(
                            arquivo_referencia, delimiter=',')
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
                                DADOS_FINANCEIROS, "DOLNAFUT_BMF_I.csv")
                            with open(database_diretorio_futuros, 'a', newline='') as csvfile:
                                writer = csv.writer(csvfile)
                                writer.writerow(registro)
                                csvfile.close()

                #  CONTRATO FUTURO ---> DOLN22
                elif ultimo_date >= 20220530 and ultimo_date < 20220629:

                    if arquivo != 'DOLN22_BMF_I.csv':
                        continue

                    with open('DOLN22_BMF_I.csv', 'r') as arquivo_referencia:
                        arquivo_csv = csv.reader(
                            arquivo_referencia, delimiter=',')
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
                                DADOS_FINANCEIROS, "DOLNAFUT_BMF_I.csv")
                            with open(database_diretorio_futuros, 'a', newline='') as csvfile:
                                writer = csv.writer(csvfile)
                                writer.writerow(registro)
                                csvfile.close()

                #  CONTRATO FUTURO ---> DOLQ22
                elif ultimo_date >= 20220629 and ultimo_date < 20220728:

                    if arquivo != 'DOLQ22_BMF_I.csv':
                        continue

                    with open('DOLQ22_BMF_I.csv', 'r') as arquivo_referencia:
                        arquivo_csv = csv.reader(
                            arquivo_referencia, delimiter=',')
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
                                DADOS_FINANCEIROS, "DOLNAFUT_BMF_I.csv")
                            with open(database_diretorio_futuros, 'a', newline='') as csvfile:
                                writer = csv.writer(csvfile)
                                writer.writerow(registro)
                                csvfile.close()

                #  CONTRATO FUTURO ---> DOLU22
                elif ultimo_date >= 20220728 and ultimo_date < 20220830:

                    if arquivo != 'DOLU22_BMF_I.csv':
                        continue

                    with open('DOLU22_BMF_I.csv', 'r') as arquivo_referencia:
                        arquivo_csv = csv.reader(
                            arquivo_referencia, delimiter=',')
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
                                DADOS_FINANCEIROS, "DOLNAFUT_BMF_I.csv")
                            with open(database_diretorio_futuros, 'a', newline='') as csvfile:
                                writer = csv.writer(csvfile)
                                writer.writerow(registro)
                                csvfile.close()

                #  CONTRATO FUTURO ---> DOLV22
                elif ultimo_date >= 20220830 and ultimo_date < 20220929:

                    if arquivo != 'DOLV22_BMF_I.csv':
                        continue

                    with open('DOLV22_BMF_I.csv', 'r') as arquivo_referencia:
                        arquivo_csv = csv.reader(
                            arquivo_referencia, delimiter=',')
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
                                DADOS_FINANCEIROS, "DOLNAFUT_BMF_I.csv")
                            with open(database_diretorio_futuros, 'a', newline='') as csvfile:
                                writer = csv.writer(csvfile)
                                writer.writerow(registro)
                                csvfile.close()

                #  CONTRATO FUTURO ---> DOLX22
                elif ultimo_date >= 20220929 and ultimo_date < 20221028:

                    if arquivo != 'DOLX22_BMF_I.csv':
                        continue

                    with open('DOLX22_BMF_I.csv', 'r') as arquivo_referencia:
                        arquivo_csv = csv.reader(
                            arquivo_referencia, delimiter=',')
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
                                DADOS_FINANCEIROS, "DOLNAFUT_BMF_I.csv")
                            with open(database_diretorio_futuros, 'a', newline='') as csvfile:
                                writer = csv.writer(csvfile)
                                writer.writerow(registro)
                                csvfile.close()

                #  CONTRATO FUTURO ---> DOLZ22
                elif ultimo_date >= 20221028 and ultimo_date < 20221129:

                    if arquivo != 'DOLZ22_BMF_I.csv':
                        continue

                    with open('DOLZ22_BMF_I.csv', 'r') as arquivo_referencia:
                        arquivo_csv = csv.reader(
                            arquivo_referencia, delimiter=',')
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
                                DADOS_FINANCEIROS, "DOLNAFUT_BMF_I.csv")
                            with open(database_diretorio_futuros, 'a', newline='') as csvfile:
                                writer = csv.writer(csvfile)
                                writer.writerow(registro)
                                csvfile.close()

                #  CONTRATO FUTURO ---> DOLF23
                elif ultimo_date >= 20221129 and ultimo_date < 20221229:

                    if arquivo != 'DOLF23_BMF_I.csv':
                        continue

                    with open('DOLF23_BMF_I.csv', 'r') as arquivo_referencia:
                        arquivo_csv = csv.reader(
                            arquivo_referencia, delimiter=',')
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
                                DADOS_FINANCEIROS, "DOLNAFUT_BMF_I.csv")
                            with open(database_diretorio_futuros, 'a', newline='') as csvfile:
                                writer = csv.writer(csvfile)
                                writer.writerow(registro)
                                csvfile.close()

            elif ticker == 'WINNAFUT':

                #  CONTRATO FUTURO ---> WING22
                if ultimo_date >= 20211214 and ultimo_date < 20220216:
                    if arquivo != 'WING22_BMF_I.csv':
                        continue

                    with open("WING22_BMF_I.csv", 'r') as arquivo_referencia:
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

                            registro[0] = 'WINNAFUT'
                            print(ticker_futuro, data_atual)

                            database_diretorio_futuros = os.path.join(
                                DADOS_FINANCEIROS, "WINNAFUT_BMF_I.csv")
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
                                DADOS_FINANCEIROS, "WINNAFUT_BMF_I.csv")
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
                                DADOS_FINANCEIROS, "WINNAFUT_BMF_I.csv")
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
                                DADOS_FINANCEIROS, "WINNAFUT_BMF_I.csv")
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
                                DADOS_FINANCEIROS, "WINNAFUT_BMF_I.csv")
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
                                DADOS_FINANCEIROS, "WINNAFUT_BMF_I.csv")
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
                                DADOS_FINANCEIROS, "WINNAFUT_BMF_I.csv")
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
                                DADOS_FINANCEIROS, "INDNAFUT_BMF_I.csv")
                            with open(database_diretorio_futuros, 'a', newline='') as csvfile:
                                writer = csv.writer(csvfile)
                                writer.writerow(registro)
                                csvfile.close()

                #  CONTRATO FUTURO ---> INDJ22
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
                                DADOS_FINANCEIROS, "INDNAFUT_BMF_I.csv")
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
                                DADOS_FINANCEIROS, "INDNAFUT_BMF_I.csv")
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
                                DADOS_FINANCEIROS, "INDNAFUT_BMF_I.csv")
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
                                DADOS_FINANCEIROS, "INDNAFUT_BMF_I.csv")
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
                                DADOS_FINANCEIROS, "INDNAFUT_BMF_I.csv")
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
                                DADOS_FINANCEIROS, "INDNAFUT_BMF_I.csv")
                            with open(database_diretorio_futuros, 'a', newline='') as csvfile:
                                writer = csv.writer(csvfile)
                                writer.writerow(registro)
                                csvfile.close()


if __name__ == '__main__':
    
    inicio = time.time()

    date, ticker = data_atual("INDNAFUT_BMF_I.csv")
    concatenar_contratos(int(date), ticker)
    
    fim = time.time()
    print(f'Tempo de execução ---> {(fim - inicio) / 60}')
