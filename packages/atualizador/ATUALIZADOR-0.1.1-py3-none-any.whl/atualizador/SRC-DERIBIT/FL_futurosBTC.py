
import os
import csv
import time

DIRETORIO = r'C:\Users\diaxt\Desktop\fl_futurosbtc'
PLANILHA = 'CO41JAN1022.csv'
ROBO_PLANILHA = 'BTCJAN1022F_BMF_I.csv'


def futuros_btc():
    """
    PRECISA TER O CABEÇALHO DO CO41, PRECISA REMOVER AS VIRGULAS
    """
    candle = {}

    os.chdir(DIRETORIO)
    with open(PLANILHA, 'r') as arquivo_referencia:
        arquivo_csv = csv.reader(arquivo_referencia, delimiter=';')
        for registro in arquivo_csv:
            tempo = registro[2]
            print(tempo[0:6])

            if registro[0] == '^Papel':
                continue

            field_name = [
                '<ticker>',
                '<date>',
                '<time>',
                '<trades>',
                '<close>',
                '<low>',
                '<high>',
                '<open>',
                '<vol>',
                '<qty>',
                '<aft>'
            ]

            candle[registro[0]] = {
                '<ticker>': registro[0],
                '<date>': registro[1],
                '<time>': tempo[0:6],
                '<trades>': 'N',
                '<close>': registro[3],
                '<low>': registro[4],
                '<high>': registro[5],
                '<open>': registro[6],
                '<vol>': 0,
                '<qty>': 0,
                '<aft>': 'N'
            }

            for titulos, valores in candle.items():
                os.chdir(DIRETORIO)
                analise_diretorio = os.path.exists(PLANILHA)

                if analise_diretorio:
                    os.chdir(DIRETORIO)
                    with open(ROBO_PLANILHA, 'a', newline='') as csvfile:
                        writer = csv.DictWriter(
                            csvfile, delimiter=',', fieldnames=field_name)
                        writer.writerow(valores)
                        csvfile.close()
                else:
                    os.chdir(DIRETORIO)
                    with open(ROBO_PLANILHA, 'w', newline='') as csv_planilha:
                        writer = csv.DictWriter(
                            csv_planilha,  delimiter=',', fieldnames=field_name)
                        writer.writeheader()
                        writer.writerow(valores)
                        csv_planilha.close()

            candle = {
            }


if __name__ == '__main__':

    futuros_btc()
