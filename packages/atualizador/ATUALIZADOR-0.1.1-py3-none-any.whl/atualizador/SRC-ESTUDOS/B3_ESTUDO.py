import csv
import numpy
import os
import pandas
from atualizador.funcoes_mod.Funcoes import modelagem_segundos_b3


"""
#  DIRETORIO DIAX:
DIRETORIO_ESTUD = r'D:\DIRETORIO_ESTUDOS\DIRETORIO_ESTUD'
DIRETORIO_BRUTO_ESTUD = r'D:\DIRETORIO_ESTUDOS\BRUTOS_ESTUD'
"""
#  DIRETORIO HOME:
DIRETORIO_ESTUD = r'C:\DIRETORIOS\DIRETORIO_ESTUDOS\DATABASE_ESTUD'
DIRETORIO_BRUTO_ESTUD = r'C:\DIRETORIOS\DIRETORIO_ESTUDOS\BRUTOS_ESTUD'


def montagem_candles():

    ATIVOS_INTERESSE = ['ABEV3']
    CANDLES = {}
    FORMADOR_MINUTOS = {}

    FIELD_NAMES = [
        '<ticker>',
        '<date>',
        '<time>',
        '<close>',
        '<low>',
        '<high>',
        '<open>',
    ]

    CANDLE_ID_1D = 20221216

    INICIALIZADOR = None

    for dir_path, dir, arquivos in os.walk(DIRETORIO_BRUTO_ESTUD):
        for arquivos_brutos in arquivos:
            planilha = modelagem_segundos_b3(arquivos_brutos, DIRETORIO_BRUTO_ESTUD, DIRETORIO_ESTUD) 
            
            print(planilha)  
            os.chdir(DIRETORIO_ESTUD)
            with open(planilha, 'r') as arquivo_referencia:
                arquivo_modelador = csv.reader(arquivo_referencia, delimiter=',')
                for linhas in arquivo_modelador:
                    
                    if linhas[0] == '<ticker>':
                        continue
                    
                    TICKER = linhas[0]
                    PRECO = float(linhas[1])
                    TIME_ATUAL = int(linhas[3][0:4])
                    DATA = int(linhas[5])

                    if TICKER not in ATIVOS_INTERESSE:
                        continue
                    if INICIALIZADOR == None:

                        CANDLE_ID_1_MINUTO = TIME_ATUAL + 1
                        CANDLE_ID_2_MINUTO = TIME_ATUAL + 2
                        # CANDLE_ID_03M = TIME_ATUAL + 3
                        # CANDLE_ID_04M = TIME_ATUAL + 4
                        # CANDLE_ID_05M = TIME_ATUAL + 5
                        # CANDLE_ID_06M = TIME_ATUAL + 6
                        # CANDLE_ID_07M = TIME_ATUAL + 7
                        # CANDLE_ID_08M = TIME_ATUAL + 8
                        # CANDLE_ID_09M = TIME_ATUAL + 9
                        # CANDLE_ID_10M = TIME_ATUAL + 10
                        # CANDLE_ID_15M = TIME_ATUAL + 15
                        # CANDLE_ID_30M = TIME_ATUAL + 30
                        # CANDLE_ID_60M = TIME_ATUAL + 60
                        # CANDLE_ID_120M = TIME_ATUAL + 120
                        # CANDLE_ID_240M = TIME_ATUAL + 240

                        INICIALIZADOR = 'TRUE'
                    
                    if TICKER not in FORMADOR_MINUTOS:
                        FORMADOR_MINUTOS[TICKER] = {
                            '1_MINUTO': {
                                '<PRECO>': [PRECO]
                            },
                            '2_MINUTO': {
                                '<PRECO>': [PRECO]
                            }
                        }
                    else:
                        if TIME_ATUAL != CANDLE_ID_1_MINUTO:
                            FORMADOR_MINUTOS[TICKER]['1_MINUTO']['<PRECO>'].append(PRECO)
                            print(TIME_ATUAL)
                        if TIME_ATUAL == CANDLE_ID_1_MINUTO:
                            for tick, time in FORMADOR_MINUTOS.items():
                                for tempo, valores in time.items():
                                    if tempo == '1_MINUTO':    
                                        if tick not in CANDLES:
                                            if TIME_ATUAL - 1 == 1003:
                                                CANDLES[tick] = {
                                                    '1_MINUTO': {
                                                        '<TICKER>': [tick],
                                                        '<DATA>': [DATA],
                                                        '<TIME>': [TIME_ATUAL - 1],
                                                        '<ABERTURA>': [FORMADOR_MINUTOS[tick]['1_MINUTO']['<PRECO>'][0]],
                                                        '<MAXIMA>': [max(FORMADOR_MINUTOS[tick]['1_MINUTO']['<PRECO>'])],
                                                        '<MINIMA>': [min(FORMADOR_MINUTOS[tick]['1_MINUTO']['<PRECO>'])],
                                                        '<FECHAMENTO>': [FORMADOR_MINUTOS[tick]['1_MINUTO']['<PRECO>'][-1]],
                                                        '<AMPLITUDE>': [max(FORMADOR_MINUTOS[tick]['1_MINUTO']['<PRECO>']) - min(FORMADOR_MINUTOS[tick]['1_MINUTO']['<PRECO>'])] 
                                                    },   
                                                    '2_MINUTO': {
                                                        '<TICKER>': [tick],
                                                        '<DATA>': [DATA],
                                                        '<TIME>': [TIME_ATUAL - 2],
                                                        '<ABERTURA>': [FORMADOR_MINUTOS[tick]['2_MINUTO']['<PRECO>'][0]],
                                                        '<MAXIMA>': [max(FORMADOR_MINUTOS[tick]['2_MINUTO']['<PRECO>'])],
                                                        '<MINIMA>': [min(FORMADOR_MINUTOS[tick]['2_MINUTO']['<PRECO>'])],
                                                        '<FECHAMENTO>': [FORMADOR_MINUTOS[tick]['2_MINUTO']['<PRECO>'][-1]],
                                                        '<AMPLITUDE>': [max(FORMADOR_MINUTOS[tick]['2_MINUTO']['<PRECO>']) - min(FORMADOR_MINUTOS[tick]['2_MINUTO']['<PRECO>'])] 
                                                    }   
                                                }
                                                FORMADOR_MINUTOS[TICKER]['2_MINUTO'] = {
                                                    '<PRECO>': []
                                                }        
                                            else:                                                 
                                                CANDLES[tick] = {
                                                    '1_MINUTO': {
                                                        '<TICKER>': [tick],
                                                        '<DATA>': [DATA],
                                                        '<TIME>': [TIME_ATUAL - 1],
                                                        '<ABERTURA>': [FORMADOR_MINUTOS[tick]['1_MINUTO']['<PRECO>'][0]],
                                                        '<MAXIMA>': [max(FORMADOR_MINUTOS[tick]['1_MINUTO']['<PRECO>'])],
                                                        '<MINIMA>': [min(FORMADOR_MINUTOS[tick]['1_MINUTO']['<PRECO>'])],
                                                        '<FECHAMENTO>': [FORMADOR_MINUTOS[tick]['1_MINUTO']['<PRECO>'][-1]],
                                                        '<AMPLITUDE>': [max(FORMADOR_MINUTOS[tick]['1_MINUTO']['<PRECO>']) - min(FORMADOR_MINUTOS[tick]['1_MINUTO']['<PRECO>'])] 
                                                    }
                                                }      
                                                                                
                                        else:
                                            CANDLES[tick]['1_MINUTO']['<TICKER>'].append(tick)
                                            CANDLES[tick]['1_MINUTO']['<DATA>'].append(DATA)
                                            CANDLES[tick]['1_MINUTO']['<TIME>'].append(TIME_ATUAL - 1)
                                            CANDLES[tick]['1_MINUTO']['<ABERTURA>'].append(FORMADOR_MINUTOS[tick]['1_MINUTO']['<PRECO>'][0])
                                            CANDLES[tick]['1_MINUTO']['<MAXIMA>'].append(max(FORMADOR_MINUTOS[tick]['1_MINUTO']['<PRECO>']))
                                            CANDLES[tick]['1_MINUTO']['<MINIMA>'].append(min(FORMADOR_MINUTOS[tick]['1_MINUTO']['<PRECO>']))
                                            CANDLES[tick]['1_MINUTO']['<FECHAMENTO>'].append(FORMADOR_MINUTOS[tick]['1_MINUTO']['<PRECO>'][-1])
                                            CANDLES[tick]['1_MINUTO']['<AMPLITUDE>'].append(max(FORMADOR_MINUTOS[tick]['1_MINUTO']['<PRECO>']) - min(FORMADOR_MINUTOS[tick]['1_MINUTO']['<PRECO>']))
                        
                            FORMADOR_MINUTOS[TICKER]['1_MINUTO'] = {
                                '<PRECO>': [PRECO]
                            }
                            CANDLE_ID_1_MINUTO += 1
                            
                        if TIME_ATUAL != CANDLE_ID_2_MINUTO:
                            FORMADOR_MINUTOS[TICKER]['2_MINUTO']['<PRECO>'].append(PRECO)

                        if TIME_ATUAL == CANDLE_ID_2_MINUTO:
                            for tick, time in FORMADOR_MINUTOS.items():
                                for tempo, valores in time.items():
                                    if tempo == '2_MINUTO':
                                        if '2_MINUTO' not in CANDLES[tick]:
                                            CANDLES[tick]['2_MINUTO'] = {
                                                '<TICKER>': [tick],
                                                '<DATA>': [DATA],
                                                '<TIME>': [TIME_ATUAL - 1],
                                                '<ABERTURA>': [FORMADOR_MINUTOS[tick]['2_MINUTO']['<PRECO>'][0]],
                                                '<MAXIMA>': [max(FORMADOR_MINUTOS[tick]['2_MINUTO']['<PRECO>'])],
                                                '<MINIMA>': [min(FORMADOR_MINUTOS[tick]['2_MINUTO']['<PRECO>'])],
                                                '<FECHAMENTO>': [FORMADOR_MINUTOS[tick]['2_MINUTO']['<PRECO>'][-1]],
                                                '<AMPLITUDE>': [max(FORMADOR_MINUTOS[tick]['2_MINUTO']['<PRECO>']) - min(FORMADOR_MINUTOS[tick]['1_MINUTO']['<PRECO>'])] 
                                            } 
                                        else:
                                            CANDLES[tick]['2_MINUTO']['<TICKER>'].append(tick)
                                            CANDLES[tick]['2_MINUTO']['<DATA>'].append(DATA)
                                            CANDLES[tick]['2_MINUTO']['<TIME>'].append(TIME_ATUAL - 1)
                                            CANDLES[tick]['2_MINUTO']['<ABERTURA>'].append(FORMADOR_MINUTOS[tick]['2_MINUTO']['<PRECO>'][0])
                                            CANDLES[tick]['2_MINUTO']['<MAXIMA>'].append(max(FORMADOR_MINUTOS[tick]['2_MINUTO']['<PRECO>']))
                                            CANDLES[tick]['2_MINUTO']['<MINIMA>'].append(min(FORMADOR_MINUTOS[tick]['2_MINUTO']['<PRECO>']))
                                            CANDLES[tick]['2_MINUTO']['<FECHAMENTO>'].append(FORMADOR_MINUTOS[tick]['2_MINUTO']['<PRECO>'][-1])
                                            CANDLES[tick]['2_MINUTO']['<AMPLITUDE>'].append(max(FORMADOR_MINUTOS[tick]['2_MINUTO']['<PRECO>']) - min(FORMADOR_MINUTOS[tick]['1_MINUTO']['<PRECO>']))

                            FORMADOR_MINUTOS[TICKER]['2_MINUTO'] = {
                                '<PRECO>': [PRECO]
                            }
                            CANDLE_ID_2_MINUTO += 2
                            

                print(CANDLES['ABEV3']['2_MINUTO']['<TIME>'])
                print('-------------------------------')
                print(CANDLES['ABEV3']['2_MINUTO']['<ABERTURA>'])
                print('-------------------------------')
                print(CANDLES['ABEV3']['2_MINUTO']['<FECHAMENTO>'])
                print('-------------------------------')
                print(CANDLES['ABEV3']['2_MINUTO']['<MINIMA>'])
                print('-------------------------------')
                print(CANDLES['ABEV3']['2_MINUTO']['<MAXIMA>'])
if __name__ == '__main__':
    montagem_candles()
                    