import csv
import pandas as pd
import os
import time

DIRETORIO_PERPETUAL = r'D:\TD_btcperpetual'


def selecionador_perpetual(arquivo):
    """
    Utilizado para selecionadr só os ativos perpetual
    dos dados_ETH e dados_BTC.
    """

    os.chdir(DIRETORIO_PERPETUAL)
    with open(arquivo, 'r') as csv_file:
        arquivo = csv.reader(csv_file, delimiter=';')
        for linha in arquivo:

            if linha[0] == 'YYYYMMDD':
                continue
            if linha[2] == 'BTC-PERPETUAL':

                os.chdir(DIRETORIO_PERPETUAL)
                analise_diretorio = os.path.exists('BTC_PERPETUAL.csv')

                DADOS_INTERESE = [linha[2], linha[0], linha[1], linha[4],
                                  linha[5], linha[6], linha[7], linha[8], linha[9]]

                print(DADOS_INTERESE[1])

                if analise_diretorio:
                    with open('BTC_PERPETUAL.CSV', 'a', newline='') as csv_file:
                        writer = csv.writer(csv_file, delimiter=';')
                        writer.writerow(DADOS_INTERESE)
                        csv_file.close()
                else:
                    os.chdir(DIRETORIO_PERPETUAL)
                    with open('BTC_PERPETUAL.CSV', 'w', newline='') as csv_file:
                        writer = csv.writer(csv_file, delimiter=';')
                        writer.writerow(DADOS_INTERESE)
                        csv_file.close()
                        csv_file.close()
            
            if linha[2] == 'ETH-PERPETUAL':

                os.chdir(DIRETORIO_PERPETUAL)
                analise_diretorio = os.path.exists('ETH_PERPETUAL.csv')

                DADOS_INTERESE = [linha[2], linha[0], linha[1], linha[4],
                                  linha[5], linha[6], linha[7], linha[8], linha[9]]

                print(DADOS_INTERESE[1])

                if analise_diretorio:
                    with open('ETH_PERPETUAL.CSV', 'a', newline='') as csv_file:
                        writer = csv.writer(csv_file, delimiter=';')
                        writer.writerow(DADOS_INTERESE)
                        csv_file.close()
                else:
                    os.chdir(DIRETORIO_PERPETUAL)
                    with open('ETH_PERPETUAL.CSV', 'w', newline='') as csv_file:
                        writer = csv.writer(csv_file, delimiter=';')
                        writer.writerow(DADOS_INTERESE)
                        csv_file.close()
                        csv_file.close()

def ajusta_arquivos():
    """
    Susbistirui pontos por virgulas.
    """

    os.chdir(DIRETORIO_PERPETUAL)
    arquivo_reader_BTC = pd.read_csv('BTC_PERPETUAL.CSV', 
                                 delimiter=';', 
                                 encoding='utf-8'
                                 )

    arquivo_reader_BTC['<OPEN>'] = arquivo_reader_BTC['<OPEN>'].str.replace(',', '.') 
    arquivo_reader_BTC['<HIGH>'] = arquivo_reader_BTC['<HIGT>'].str.replace(',', '.')
    arquivo_reader_BTC['<LOW>'] = arquivo_reader_BTC['<LOW>'].str.replace(',', '.')
    arquivo_reader_BTC['<CLOSE>'] = arquivo_reader_BTC['<CLOSE>'].str.replace(',', '.')
    arquivo_reader_BTC['<VOL>'] = arquivo_reader_BTC['<VOL>'].str.replace(',', '.')

    arquivo_reader_BTC.to_csv('BTC_PERPETUAL.CSV', index=False)

    os.chdir(DIRETORIO_PERPETUAL)

    arquivo_reader_ETH = pd.read_csv('ETH_PERPETUAL.CSV', 
                                 delimiter=';', 
                                 encoding='utf-8'
                                 )

    arquivo_reader_ETH['<OPEN>'] = arquivo_reader_ETH['<OPEN>'].str.replace(',', '.') 
    arquivo_reader_ETH['<HIGH>'] = arquivo_reader_ETH['<HIGT>'].str.replace(',', '.')
    arquivo_reader_ETH['<LOW>'] = arquivo_reader_ETH['<LOW>'].str.replace(',', '.')
    arquivo_reader_ETH['<CLOSE>'] = arquivo_reader_ETH['<CLOSE>'].str.replace(',', '.')
    arquivo_reader_ETH['<VOL>'] = arquivo_reader_ETH['<VOL>'].str.replace(',', '.')

    arquivo_reader_ETH.to_csv('BTC_PERPETUAL.CSV', index=False)



if __name__ == '__main__':

    inicio = time.time()
    selecionador_perpetual('dados_ETH.txt')
    ajusta_arquivos()
    fim = time.time()
    print('TEMPO DE EXECUÇÃO: ', (fim - inicio) / 60)
