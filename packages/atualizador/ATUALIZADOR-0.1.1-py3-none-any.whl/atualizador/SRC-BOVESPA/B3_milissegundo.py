#  Atualizar o Database
import csv
import os
import time
from atualizador.funcoes_mod.Funcoes import modelagem_milissegundos_b3

DIRETORIO_B3_BRUTOS = r'D:\DIRETORIO_CODIGOS\MILISEGUNDOS_BRUTO'
DIRETORIO_DATABASE = r'D:\HISTORICO\Database_MILISEG'


def montagem_candles_milissegundos():
    """
    Utilizado para a criação de arquivos de SEGUNDOS de todos
    os ativos negociados na B3.
    """    
    
    ult_candle = None
    conversor = 1
    candles = {}

    for caminho_path, dir_arquivo, arquivos in os.walk(DIRETORIO_B3_BRUTOS):
        for arquivo in arquivos:

            planilha = modelagem_milissegundos_b3(arquivo, DIRETORIO_B3_BRUTOS, DIRETORIO_DATABASE)

            os.chdir(DIRETORIO_DATABASE)
            with open(planilha, 'r') as arquivo_referencia:
                arquivo_csv = csv.reader(arquivo_referencia, delimiter=',')
                for registro in arquivo_csv:
                    ticker = registro[0]
                    preco = registro[1]
                    trades = registro[2]
                    tempo = registro[3]
                    qty = registro[4]
                    date = registro[5]
                    vol = registro[6]
                    aft = 'N'

                    if ticker in '<ticker>':
                        continue

                    candle_id = int(tempo) // conversor

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

                    if candle_id != ult_candle:

                        #  ATUALIZAR DADOS DO DATABASE:
                        for ticker_dicioin, valores in candles.items():
                            nome_csv = str(ticker_dicioin) + '_BMF_I' + '.csv'
                            print(nome_csv, '--------------------------->', candle_id)

                            os.chdir(DIRETORIO_DATABASE)
                            analise_diretorio = os.path.exists(nome_csv)
                            if analise_diretorio:
                                os.chdir(DIRETORIO_DATABASE)
                                with open(nome_csv, 'a', newline='') as csvfile:
                                    writer = csv.DictWriter(csvfile, fieldnames=field_name)
                                    writer.writerow(valores)
                                    csvfile.close()
                            else:
                                os.chdir(DIRETORIO_DATABASE)
                                with open(nome_csv, 'w', newline='') as csv_planilha:
                                    writer = csv.DictWriter(csv_planilha, fieldnames=field_name)
                                    writer.writeheader()
                                    writer.writerow(valores)
                                    csv_planilha.close()

                        ult_candle = candle_id
                        candles = {}

                    os.chdir(DIRETORIO_DATABASE)
                    if not candles:
                        # Primeira vez que o symbolo aparece no candle_id
                        # (time, open, close, low, high, vol)

                        candles[ticker] = {
                            '<ticker>': ticker,
                            '<date>': date,
                            '<time>': tempo,
                            '<trades>': float(trades),
                            '<close>': float(preco),
                            '<low>': float(preco),
                            '<high>': float(preco),
                            '<open>': float(preco),
                            '<vol>': float(vol),
                            '<qty>': float(qty),
                            '<aft>': aft
                        }
                    else:
                        ticker_diferente = True
                        for ticker_dicio, valores in candles.items():
                            if ticker == ticker_dicio:
                                ticker_diferente = False
                                for dados, valores2 in valores.items():
                                    if dados != '<ticker>' or '<date>' or '<time>' or '<close>' or '<aft>':
                                        if dados == '<trades>':
                                            trades1 = float(valores2) + float(trades)
                                        elif dados == '<low>':
                                            low = min(float(valores2), float(preco))
                                        elif dados == '<high>':
                                            high = max(float(valores2), float(preco))
                                        elif dados == '<open>':
                                            openn = float(valores2)
                                        elif dados == '<vol>':
                                            vol1 = float(valores2) + float(vol)
                                        elif dados == '<qty>':
                                            qty1 = float(valores2) + float(qty)
                                            candles[ticker] = {
                                                '<ticker>': ticker,
                                                '<date>': date,
                                                '<time>': tempo,
                                                '<trades>': trades1,
                                                '<close>': float(preco),
                                                '<low>': low,
                                                '<high>': high,
                                                '<open>': openn,
                                                '<vol>': vol1,
                                                '<qty>': qty1,
                                                '<aft>': aft
                                            }
                        if not ticker_diferente:
                            continue

                        candles[ticker] = {
                            '<ticker>': ticker,
                            '<date>': date,
                            '<time>': tempo,
                            '<trades>': float(trades),
                            '<close>': float(preco),
                            '<low>': float(preco),
                            '<high>': float(preco),
                            '<open>': float(preco),
                            '<vol>': float(vol),
                            '<qty>': float(qty),
                            '<aft>': aft
                        }


if __name__ == '__main__':
    
    inicio = time.time()
    montagem_candles_milissegundos()
    fim = time.time()
    print('TEMPO DE EXECUÇÃO -------->', (fim - inicio) / 60)
