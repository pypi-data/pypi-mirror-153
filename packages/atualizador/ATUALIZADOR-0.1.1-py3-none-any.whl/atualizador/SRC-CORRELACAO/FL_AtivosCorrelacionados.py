from atualizador.funcoes_mod.Funcoes import modelagem_segundos_b3
import csv
import os
import time

# DIRETORIOS DIAX:
B3_BRUTOS = r'D:\DIRETORIOS\BRUTOS_CORRELACIONADOS'
B3_DATABASE = r'D:\DADOS_FINANCEIROS\Database_CORRELACAO'
B3_FUTUROS_CORRELACIONADOS = r'D:\DIRETORIOS\B3_FUTUROS_CORRELACIONADOS'

# DIRETORIOS HOME:
# B3_BRUTOS = r'C:\DIRETORIOS\BRUTOS_CORRELACAO'
# B3_DATABASE = r'C:\DIRETORIOS\Database_CORRELACAO'
# B3_FUTUROS_CORRELACIONADOS = r'C:\DIRETORIOS\B3_FUTUROS_CORRELACIONADOS'


def modelagem_correlacao():
    """
    Utilizado para criar o arquvio de interesse do
    Felipe.
    """
    ult_candle = None
    conversor = 10000000
    candles = {}

    LISTA_VALORES = [
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0
    ]

    INTERRESE_ATIVOS = [
        'RRRP3_',
        'ALPA4_',
        'ABEV3_',
        'AZUL3_'
        'AMER3_',
        'ASAI3_',
        'AURE3_',
        'AZUL4_',
        'B3SA3_',
        'BPAN4_',
        'BBSE3_',
        'BRML3_',
        'BBDC3_',
        'BBDC4_',
        'BRAP4_',
        'BBAS3_',
        'BRKM5_',
        'BRFS3_',
        'CRFB3_',
        'CCRO3_',
        'CMIG4_',
        'CIEL3_',
        'COGN3_',
        'CPLE6_',
        'CSAN3_',
        'CSAN3_',
        'CPFE3_',
        'CMIN3_',
        'CVCB3_',
        'CYRE3_',
        'DXCO3_',
        'ECOR3_',
        'ELET3_',
        'ELET6_',
        'EMBR3_',
        'ENBR3_',
        'ENEV3_',
        'EGIE3_',
        'EQTL3_',
        'EZTC3_',
        'FLRY3_',
        'GGBR4_',
        'GOAU4_',
        'GOLL4_',
        'NTCO3_',
        'SOMA3_',
        'HAPV3_',
        'HYPE3_',
        'IRBR3_',
        'ITSA4_',
        'ITUB4_',
        'JBSS3_',      
        'JBSS3_',
        'LIGT3_',
        'RENT3_',
        'LCAM3_',
        'LWSA3_',
        'AMAR3_',
        'LREN3_',
        'MGLU3_',
        'MRFG3_',
        'CASH3_',
        'BEEF3_',
        'MOVI3_',
        'MRVE3_',
        'MULT3_',
        'PCAR3_',
        'PETR3_',
        'PETR4_',
        'PRIO3_',
        'PETZ3_',
        'PSSA3_',
        'POSI3_',
        'QUAL3_',
        'RADL3_',
        'RDOR3_',
        'RAIL3_',
        'SBSP3_',
        'STBP3_',
        'CSNA3_',
        'SLCE3_',
        'SUZB3_',
        'VIVT3_',
        'TIMS3_',
        'TOTS3_',
        'UGPA3_',
        'USIM5_',
        'VALE3_',
        'VIIA3_',
        'VBBR3_',
        'WEGE3_',
        'YDUQ3_',
        'GNDI3_',
        'JHSF3_',
        'MDIA3_',
        'MEAL3_',
        'NEOE3_',
        'RAPT4_',
        'TRPL4_',
        'TAEE4_',
        'TAEE3_',
        'ALSO3_',
        'CESP6_',
        'SUZB5_',
        'VALE5_',
        'VIVT4_',
        'ITUB3_',
        'DASA3_',
        'BRPR3_',
        'PDGR3_',
        'MILS3_',
        'GFSA3_',
        'OIBR3_',
        'OIBR4_',
        'BRSR6_',
        'ODPV3_',
        'RSID3_',
        'EVEN3_',
        'POMO4_',
        'MYPK3_',
        'SEER3_',
        'LPSB3_',
        'ANIM3_',
        'BBRK3_',
        'DIRR3_',
        'KEPL3_',
        'LEVE3_',
        'VLID3_',
        'PFRM3_',
        'TGMA3_',
        'UCAS3_',
        'CMIG3_',
        'CSMG3_',
        'ARZZ3_',
        'SLED4_',
        'ABCB4_',
        'TGNA3_',  
        'USIM3_',
        'CPLE3_',
        'GRND3_',
        'SMTO3_',
        'HBOR3_',
        'TUPY3_',
        'TCSA3_',
        'JSLG3_',
        'COCE5_',
        'RDNI3_',
        'SHOW3_',
        'UNIP6_',
        'GUAR3_',
        'LOGN3_',
        'INDG22',
        'INDJ22',
        'INDM22',
        'INDQ22',
        'INDV22',
        'INDZ22'
    ]

    for _, _, arquivos in os.walk(B3_BRUTOS):
        for arquivo in arquivos:
            # os.chdir(B3_BRUTOS)
            planilha = modelagem_segundos_b3(arquivo, B3_BRUTOS, B3_DATABASE)

            with open(planilha, 'r') as arquivo_referencia:
                arquivo_csv = csv.reader(arquivo_referencia, delimiter=',')
                for registro in arquivo_csv:

                    if registro[0] == '<ticker>':
                        continue

                    nome_csv = str(registro[0])

                    for dados in INTERRESE_ATIVOS:
                        if nome_csv != dados:    
                            continue

                        preco = registro[1]
                        tempo = registro[3]
                        date = int(registro[5])
                        candle_id = int(tempo) // conversor

                        if candle_id != ult_candle:
                           
                            if candle_id != 9 and ult_candle != 9 and candle_id != 19 and ult_candle != None:
                                nome_csv_novo = 'B3_60MIN_CORRELACAO.csv'
                                print(date, nome_csv, ult_candle, candle_id)
                                for ticker_dicioin, valores in candles.items():
                                    
                                    if date  >= 20211214 and date < 20220216 :
                                        if 'INDG22' == ticker_dicioin: 
                                            print(date, ticker_dicioin)
                                            LISTA_VALORES[2] = candles['INDG22']['<INDG22>']
                                    if date >= 20220216 and date < 20220412:
                                        if 'INDJ22' == ticker_dicioin: 
                                            print(date, ticker_dicioin)
                                            LISTA_VALORES[2] = candles['INDJ22']['<INDJ22>']                                    
                                    if date >= 20220412 and date < 20220614:
                                        if 'INDM22' == ticker_dicioin: 
                                            print(date, ticker_dicioin)
                                            LISTA_VALORES[2] = candles['INDM22']['<INDM22>']                                    
                                    if date >= 20220614 and date < 20220816:
                                        if 'INDQ22' == ticker_dicioin: 
                                            print(date, ticker_dicioin)
                                            LISTA_VALORES[2] = candles['INDQ22']['<INDQ22>'] 
                                    if date >= 20220816 and date < 20221011:
                                        if 'INDV22' == ticker_dicioin: 
                                            print(date, ticker_dicioin)
                                            LISTA_VALORES[2] = candles['INDV22']['<INDV22>'] 
                                    if date >= 20221011 and date < 20221213:
                                        if 'INDZ22' == ticker_dicioin: 
                                            print(date, ticker_dicioin)
                                            LISTA_VALORES[2] = candles['INDZ22']['<INDZ22>'] 
                                    
                                    if 'ABEV3' == ticker_dicioin:  
                                        LISTA_VALORES[0] = candles['ABEV3']['AAAAMMDD']
                                        LISTA_VALORES[1] = candles['ABEV3']['HHMM']
                                        LISTA_VALORES[3] = candles['ABEV3']['<ABEV3>']
                                    if 'PRIO3' == ticker_dicioin:
                                        LISTA_VALORES[4] = candles['PRIO3']['<PRIO3>']
                                    if 'PETR4' == ticker_dicioin:
                                        LISTA_VALORES[5] = candles['PETR4']['<PETR4>']
                                    if 'VALE3' == ticker_dicioin:
                                        LISTA_VALORES[6] = candles['VALE3']['<VALE3>']
                                    if 'AZUL4' == ticker_dicioin:
                                        LISTA_VALORES[7] = candles['AZUL4']['<AZUL4>']
                                    if 'MGLU3' == ticker_dicioin:
                                        LISTA_VALORES[8] = candles['MGLU3']['<MGLU3>']
                                    if 'JHSF3' == ticker_dicioin:
                                        LISTA_VALORES[9] = candles['JHSF3']['<JHSF3>']
                                    if 'BRML3' == ticker_dicioin:
                                        LISTA_VALORES[10] = candles['BRML3']['<BRML3>']

                            print(LISTA_VALORES)
                            if LISTA_VALORES[0] != 0:  
                                #  ATUALIZAR DADOS DO DATABASE:
                                os.chdir(B3_DATABASE)
                                analise_diretorio = os.path.exists(nome_csv_novo)
                                if analise_diretorio:
                                    with open(nome_csv_novo, 'a', newline='') as csvfile:
                                        writer = csv.writer(csvfile)
                                        writer.writerow(LISTA_VALORES)
                                        csvfile.close()
                                else:
                                    LISTA_VALORES = [
                                        'AAAAMMDD',
                                        'HHMM',
                                        'INDFUT',
                                        'ABEV3',
                                        'PRIO3',
                                        'PETR4',
                                        'VALE3',
                                        'AZUL4',
                                        'MGLU3',
                                        'JHSF3',
                                        'BRML3'
                                    ]  

                                    with open(nome_csv_novo, 'w', newline='') as csv_planilha:
                                        writer = csv.writer(csv_planilha)
                                        writer.writerow(LISTA_VALORES)
                                        csv_planilha.close()

                            ult_candle = candle_id
                            candles = {}
                            LISTA_VALORES = [
                                0,
                                0,
                                0,
                                0,
                                0,
                                0,
                                0,
                                0,
                                0,
                                0,
                                0
                            ]

                        os.chdir(B3_DATABASE)
                        if not candles:
                            # Primeira vez que o symbolo aparece no candle_id
                            if len(str(candle_id)) == 1:
                                tempo = '0' + str(candle_id) + '00'

                                if nome_csv == 'ABEV3':
                                    candles[nome_csv] = {
                                        'AAAAMMDD': date,
                                        'HHMM': tempo,
                                        '<ABEV3>': float(preco),
                                    }
                                elif nome_csv == 'PRIO3':
                                    candles[nome_csv] = {
                                        'AAAAMMDD': date,
                                        'HHMM': tempo,
                                        '<PRIO3>': float(preco),
                                    }
                                elif nome_csv == 'PETR4':
                                    candles[nome_csv] = {
                                        'AAAAMMDD': date,
                                        'HHMM': tempo,
                                        '<PETR4>': float(preco),
                                    }
                                elif nome_csv == 'VALE3':
                                    candles[nome_csv] = {
                                        'AAAAMMDD': date,
                                        'HHMM': tempo,
                                        '<VALE3>': float(preco),
                                    }
                                elif nome_csv == 'AZUL4':
                                    candles[nome_csv] = {
                                        'AAAAMMDD': date,
                                        'HHMM': tempo,
                                        '<AZUL4>': float(preco),
                                    }
                                elif nome_csv == 'MGLU3':
                                    candles[nome_csv] = {
                                        'AAAAMMDD': date,
                                        'HHMM': tempo,
                                        '<MGLU3>': float(preco),
                                    }
                                elif nome_csv == 'JHSF3':
                                    candles[nome_csv] = {
                                        'AAAAMMDD': date,
                                        'HHMM': tempo,
                                        '<JHSF3>': float(preco),
                                    }
                                elif nome_csv == 'BRML3':
                                    candles[nome_csv] = {
                                        'AAAAMMDD': date,
                                        'HHMM': tempo,
                                        '<BRML3>': float(preco),
                                    }
                                elif nome_csv == 'INDG22':
                                    candles[nome_csv] = {
                                        'AAAAMMDD': date,
                                        'HHMM': tempo,
                                        '<INDG22>': float(preco),
                                    }
                                elif nome_csv == 'INDJ22':
                                    candles[nome_csv] = {
                                        'AAAAMMDD': date,
                                        'HHMM': tempo,
                                        '<INDJ22>': float(preco),
                                    }
                                elif nome_csv == 'INDM22':
                                    candles[nome_csv] = {
                                        'AAAAMMDD': date,
                                        'HHMM': tempo,
                                        '<INDM22>': float(preco),
                                    }
                                elif nome_csv == 'INDQ22':
                                    candles[nome_csv] = {
                                        'AAAAMMDD': date,
                                        'HHMM': tempo,
                                        '<INDQ22>': float(preco),
                                    }
                                elif nome_csv == 'INDV22':
                                    candles[nome_csv] = {
                                        'AAAAMMDD': date,
                                        'HHMM': tempo,
                                        '<INDV22>': float(preco),
                                    }
                                elif nome_csv == 'INDZ22':
                                    candles[nome_csv] = {
                                        'AAAAMMDD': date,
                                        'HHMM': tempo,
                                        '<INDZ22>': float(preco),
                                    }
                            
                            elif len(str(candle_id)) == 2:
                                tempo = str(candle_id) + '00'

                                if nome_csv == 'ABEV3':
                                    candles[nome_csv] = {
                                        'AAAAMMDD': date,
                                        'HHMM': tempo,
                                        '<ABEV3>': float(preco),
                                    }
                                elif nome_csv == 'PRIO3':
                                    candles[nome_csv] = {
                                        'AAAAMMDD': date,
                                        'HHMM': tempo,
                                        '<PRIO3>': float(preco),
                                    }
                                elif nome_csv == 'PETR4':
                                    candles[nome_csv] = {
                                        'AAAAMMDD': date,
                                        'HHMM': tempo,
                                        '<PETR4>': float(preco),
                                    }
                                elif nome_csv == 'VALE3':
                                    candles[nome_csv] = {
                                        'AAAAMMDD': date,
                                        'HHMM': tempo,
                                        '<VALE3>': float(preco),
                                    }
                                elif nome_csv == 'AZUL4':
                                    candles[nome_csv] = {
                                        'AAAAMMDD': date,
                                        'HHMM': tempo,
                                        '<AZUL4>': float(preco),
                                    }
                                elif nome_csv == 'MGLU3':
                                    candles[nome_csv] = {
                                        'AAAAMMDD': date,
                                        'HHMM': tempo,
                                        '<MGLU3>': float(preco),
                                    }
                                elif nome_csv == 'JHSF3':
                                    candles[nome_csv] = {
                                        'AAAAMMDD': date,
                                        'HHMM': tempo,
                                        '<JHSF3>': float(preco),
                                    }
                                elif nome_csv == 'BRML3':
                                    candles[nome_csv] = {
                                        'AAAAMMDD': date,
                                        'HHMM': tempo,
                                        '<BRML3>': float(preco),
                                    }
                                elif nome_csv == 'INDG22':
                                    candles[nome_csv] = {
                                        'AAAAMMDD': date,
                                        'HHMM': tempo,
                                        '<INDG22>': float(preco),
                                    }
                                elif nome_csv == 'INDJ22':
                                    candles[nome_csv] = {
                                        'AAAAMMDD': date,
                                        'HHMM': tempo,
                                        '<INDJ22>': float(preco),
                                    }
                                elif nome_csv == 'INDM22':
                                    candles[nome_csv] = {
                                        'AAAAMMDD': date,
                                        'HHMM': tempo,
                                        '<INDM22>': float(preco),
                                    }
                                elif nome_csv == 'INDQ22':
                                    candles[nome_csv] = {
                                        'AAAAMMDD': date,
                                        'HHMM': tempo,
                                        '<INDQ22>': float(preco),
                                    }
                                elif nome_csv == 'INDV22':
                                    candles[nome_csv] = {
                                        'AAAAMMDD': date,
                                        'HHMM': tempo,
                                        '<INDV22>': float(preco),
                                    }
                                elif nome_csv == 'INDZ22':
                                    candles[nome_csv] = {
                                        'AAAAMMDD': date,
                                        'HHMM': tempo,
                                        '<INDZ22>': float(preco),
                                    }
                        else:
                            ticker_diferente = True
                            for ticker_dicio, valores in candles.items():
                                if nome_csv == ticker_dicio:
                                    ticker_diferente = False

                                    if len(str(candle_id)) == 1:
                                        tempo = '0' + str(candle_id) + '00'

                                        if nome_csv == 'ABEV3':
                                            candles[nome_csv] = {
                                                'AAAAMMDD': date,
                                                'HHMM': tempo,
                                                '<ABEV3>': float(preco),
                                            }
                                        elif nome_csv == 'PRIO3':
                                            candles[nome_csv] = {
                                                'AAAAMMDD': date,
                                                'HHMM': tempo,
                                                '<PRIO3>': float(preco),
                                            }
                                        elif nome_csv == 'PETR4':
                                            candles[nome_csv] = {
                                                'AAAAMMDD': date,
                                                'HHMM': tempo,
                                                '<PETR4>': float(preco),
                                            }
                                        elif nome_csv == 'VALE3':
                                            candles[nome_csv] = {
                                                'AAAAMMDD': date,
                                                'HHMM': tempo,
                                                '<VALE3>': float(preco),
                                            }
                                        elif nome_csv == 'AZUL4':
                                            candles[nome_csv] = {
                                                'AAAAMMDD': date,
                                                'HHMM': tempo,
                                                '<AZUL4>': float(preco),
                                            }
                                        elif nome_csv == 'MGLU3':
                                            candles[nome_csv] = {
                                                'AAAAMMDD': date,
                                                'HHMM': tempo,
                                                '<MGLU3>': float(preco),
                                            }
                                        elif nome_csv == 'JHSF3':
                                            candles[nome_csv] = {
                                                'AAAAMMDD': date,
                                                'HHMM': tempo,
                                                '<JHSF3>': float(preco),
                                            }
                                        elif nome_csv == 'BRML3':
                                            candles[nome_csv] = {
                                                'AAAAMMDD': date,
                                                'HHMM': tempo,
                                                '<BRML3>': float(preco),
                                            }

                                        elif nome_csv == 'INDG22':
                                            candles[nome_csv] = {
                                                'AAAAMMDD': date,
                                                'HHMM': tempo,
                                                '<INDG22>': float(preco),
                                            }
                                        elif nome_csv == 'INDJ22':
                                            candles[nome_csv] = {
                                                'AAAAMMDD': date,
                                                'HHMM': tempo,
                                                '<INDJ22>': float(preco),
                                            }
                                        elif nome_csv == 'INDM22':
                                            candles[nome_csv] = {
                                                'AAAAMMDD': date,
                                                'HHMM': tempo,
                                                '<INDM22>': float(preco),
                                            }
                                        elif nome_csv == 'INDQ22':
                                            candles[nome_csv] = {
                                                'AAAAMMDD': date,
                                                'HHMM': tempo,
                                                '<INDQ22>': float(preco),
                                            }
                                        elif nome_csv == 'INDV22':
                                            candles[nome_csv] = {
                                                'AAAAMMDD': date,
                                                'HHMM': tempo,
                                                '<INDV22>': float(preco),
                                            }
                                        elif nome_csv == 'INDZ22':
                                            candles[nome_csv] = {
                                                'AAAAMMDD': date,
                                                'HHMM': tempo,
                                                '<INDZ22>': float(preco),
                                            }

                                    elif len(str(candle_id)) == 2:
                                        tempo = str(candle_id) + '00'

                                        if nome_csv == 'ABEV3':
                                            candles[nome_csv] = {
                                                'AAAAMMDD': date,
                                                'HHMM': tempo,
                                                '<ABEV3>': float(preco),
                                            }
                                        elif nome_csv == 'PRIO3':
                                            candles[nome_csv] = {
                                                'AAAAMMDD': date,
                                                'HHMM': tempo,
                                                '<PRIO3>': float(preco),
                                            }
                                        elif nome_csv == 'PETR4':
                                            candles[nome_csv] = {
                                                'AAAAMMDD': date,
                                                'HHMM': tempo,
                                                '<PETR4>': float(preco),
                                            }
                                        elif nome_csv == 'VALE3':
                                            candles[nome_csv] = {
                                                'AAAAMMDD': date,
                                                'HHMM': tempo,
                                                '<VALE3>': float(preco),
                                            }
                                        elif nome_csv == 'AZUL4':
                                            candles[nome_csv] = {
                                                'AAAAMMDD': date,
                                                'HHMM': tempo,
                                                '<AZUL4>': float(preco),
                                            }
                                        elif nome_csv == 'MGLU3':
                                            candles[nome_csv] = {
                                                'AAAAMMDD': date,
                                                'HHMM': tempo,
                                                '<MGLU3>': float(preco),
                                            }
                                        elif nome_csv == 'JHSF3':
                                            candles[nome_csv] = {
                                                'AAAAMMDD': date,
                                                'HHMM': tempo,
                                                '<JHSF3>': float(preco),
                                            }
                                        elif nome_csv == 'BRML3':
                                            candles[nome_csv] = {
                                                'AAAAMMDD': date,
                                                'HHMM': tempo,
                                                '<BRML3>': float(preco),
                                            }
                                        elif nome_csv == 'INDG22':
                                            candles[nome_csv] = {
                                                'AAAAMMDD': date,
                                                'HHMM': tempo,
                                                '<INDG22>': float(preco),
                                            }
                                        elif nome_csv == 'INDJ22':
                                            candles[nome_csv] = {
                                                'AAAAMMDD': date,
                                                'HHMM': tempo,
                                                '<INDJ22>': float(preco),
                                            }
                                        elif nome_csv == 'INDM22':
                                            candles[nome_csv] = {
                                                'AAAAMMDD': date,
                                                'HHMM': tempo,
                                                '<INDM22>': float(preco),
                                            }
                                        elif nome_csv == 'INDQ22':
                                            candles[nome_csv] = {
                                                'AAAAMMDD': date,
                                                'HHMM': tempo,
                                                '<INDQ22>': float(preco),
                                            }
                                        elif nome_csv == 'INDV22':
                                            candles[nome_csv] = {
                                                'AAAAMMDD': date,
                                                'HHMM': tempo,
                                                '<INDV22>': float(preco),
                                            }
                                        elif nome_csv == 'INDZ22':
                                            candles[nome_csv] = {
                                                'AAAAMMDD': date,
                                                'HHMM': tempo,
                                                '<INDZ22>': float(preco),
                                            }

                            if not ticker_diferente:
                                continue

                            if len(str(candle_id)) == 1:
                                tempo = '0' + str(candle_id) + '00'
                                
                                if nome_csv == 'ABEV3':
                                    candles[nome_csv] = {
                                        'AAAAMMDD': date,
                                        'HHMM': tempo,
                                        '<ABEV3>': float(preco),
                                    }
                                elif nome_csv == 'PRIO3':
                                    candles[nome_csv] = {
                                        'AAAAMMDD': date,
                                        'HHMM': tempo,
                                        '<PRIO3>': float(preco),
                                    }
                                elif nome_csv == 'PETR4':
                                    candles[nome_csv] = {
                                        'AAAAMMDD': date,
                                        'HHMM': tempo,
                                        '<PETR4>': float(preco),
                                    }
                                elif nome_csv == 'VALE3':
                                    candles[nome_csv] = {
                                        'AAAAMMDD': date,
                                        'HHMM': tempo,
                                        '<VALE3>': float(preco),
                                    }
                                elif nome_csv == 'AZUL4':
                                    candles[nome_csv] = {
                                        'AAAAMMDD': date,
                                        'HHMM': tempo,
                                        '<AZUL4>': float(preco),
                                    }
                                elif nome_csv == 'MGLU3':
                                    candles[nome_csv] = {
                                        'AAAAMMDD': date,
                                        'HHMM': tempo,
                                        '<MGLU3>': float(preco)
                                    }
                                elif nome_csv == 'JHSF3':
                                    candles[nome_csv] = {
                                        'AAAAMMDD': date,
                                        'HHMM': tempo,
                                        '<JHSF3>': float(preco),
                                    }
                                elif nome_csv == 'BRML3':
                                    candles[nome_csv] = {
                                        'AAAAMMDD': date,
                                        'HHMM': tempo,
                                        '<BRML3>': float(preco),
                                    }
                                elif nome_csv == 'INDG22':
                                    candles[nome_csv] = {
                                        'AAAAMMDD': date,
                                        'HHMM': tempo,
                                        '<INDG22>': float(preco),
                                    }
                                elif nome_csv == 'INDJ22':
                                    candles[nome_csv] = {
                                        'AAAAMMDD': date,
                                        'HHMM': tempo,
                                        '<INDJ22>': float(preco),
                                    }
                                elif nome_csv == 'INDM22':
                                    candles[nome_csv] = {
                                        'AAAAMMDD': date,
                                        'HHMM': tempo,
                                        '<INDM22>': float(preco),
                                    }
                                elif nome_csv == 'INDQ22':
                                    candles[nome_csv] = {
                                        'AAAAMMDD': date,
                                        'HHMM': tempo,
                                        '<INDQ22>': float(preco),
                                    }
                                elif nome_csv == 'INDV22':
                                    candles[nome_csv] = {
                                        'AAAAMMDD': date,
                                        'HHMM': tempo,
                                        '<INDV22>': float(preco),
                                    }
                                elif nome_csv == 'INDZ22':
                                    candles[nome_csv] = {
                                        'AAAAMMDD': date,
                                        'HHMM': tempo,
                                        '<INDZ22>': float(preco),
                                    }

                            elif len(str(candle_id)) == 2:
                                tempo = str(candle_id) + '00'
                                
                                if nome_csv == 'ABEV3':
                                    candles[nome_csv] = {
                                        'AAAAMMDD': date,
                                        'HHMM': tempo,
                                        '<ABEV3>': float(preco),
                                    }
                                elif nome_csv == 'PRIO3':
                                    candles[nome_csv] = {
                                        'AAAAMMDD': date,
                                        'HHMM': tempo,
                                        '<PRIO3>': float(preco),
                                    }
                                elif nome_csv == 'PETR4':
                                    candles[nome_csv] = {
                                        'AAAAMMDD': date,
                                        'HHMM': tempo,
                                        '<PETR4>': float(preco),
                                    }
                                elif nome_csv == 'VALE3':
                                    candles[nome_csv] = {
                                        'AAAAMMDD': date,
                                        'HHMM': tempo,
                                        '<VALE3>': float(preco),
                                    }
                                elif nome_csv == 'AZUL4':
                                    candles[nome_csv] = {
                                        'AAAAMMDD': date,
                                        'HHMM': tempo,
                                        '<AZUL4>': float(preco),
                                    }
                                elif nome_csv == 'MGLU3':
                                    candles[nome_csv] = {
                                        'AAAAMMDD': date,
                                        'HHMM': tempo,
                                        '<MGLU3>': float(preco),
                                    }
                                elif nome_csv == 'JHSF3':
                                    candles[nome_csv] = {
                                        'AAAAMMDD': date,
                                        'HHMM': tempo,
                                        '<JHSF3>': float(preco),
                                    }
                                elif nome_csv == 'BRML3':
                                    candles[nome_csv] = {
                                        'AAAAMMDD': date,
                                        'HHMM': tempo,
                                        '<BRML3>': float(preco),
                                    }
                                elif nome_csv == 'INDG22':
                                    candles[nome_csv] = {
                                        'AAAAMMDD': date,
                                        'HHMM': tempo,
                                        '<INDG22>': float(preco),
                                    }
                                elif nome_csv == 'INDJ22':
                                    candles[nome_csv] = {
                                        'AAAAMMDD': date,
                                        'HHMM': tempo,
                                        '<INDJ22>': float(preco),
                                    }
                                elif nome_csv == 'INDM22':
                                    candles[nome_csv] = {
                                        'AAAAMMDD': date,
                                        'HHMM': tempo,
                                        '<INDM22>': float(preco),
                                    }
                                elif nome_csv == 'INDQ22':
                                    candles[nome_csv] = {
                                        'AAAAMMDD': date,
                                        'HHMM': tempo,
                                        '<INDQ22>': float(preco),
                                    }
                                elif nome_csv == 'INDV22':
                                    candles[nome_csv] = {
                                        'AAAAMMDD': date,
                                        'HHMM': tempo,
                                        '<INDV22>': float(preco),
                                    }
                                elif nome_csv == 'INDZ22':
                                    candles[nome_csv] = {
                                        'AAAAMMDD': date,
                                        'HHMM': tempo,
                                        '<INDZ22>': float(preco),
                                    }

                print(candle_id, nome_csv)
                if candle_id == 17 or candle_id == 18 or candle_id == 19:
                    nome_csv_novo = 'B3_60MIN_CORRELACAO.csv'
                    if candle_id and candle_id != 19:
                        for ticker_dicioin, valores in candles.items():

                            if date  >= 20211214 and date < 20220216:
                                if 'INDG22' == ticker_dicioin: 
                                    print(date, ticker_dicioin, candle_id)
                                    LISTA_VALORES[2] = candles['INDG22']['<INDG22>']
                            if date >= 20220216 and date < 20220412:
                                if 'INDJ22' == ticker_dicioin: 
                                    print(date, ticker_dicioin)
                                    LISTA_VALORES[2] = candles['INDJ22']['<INDJ22>']                                    
                            if date >= 20220412 and date < 20220614:
                                if 'INDM22' == ticker_dicioin: 
                                    print(date, ticker_dicioin)
                                    LISTA_VALORES[2] = candles['INDM22']['<INDM22>']                                    
                            if date >= 20220614 and date < 20220816:
                                if 'INDQ22' == ticker_dicioin: 
                                    print(date, ticker_dicioin)
                                    LISTA_VALORES[2] = candles['INDQ22']['<INDQ22>'] 
                            if date >= 20220816 and date < 20221011:
                                if 'INDV22' == ticker_dicioin: 
                                    print(date, ticker_dicioin)
                                    LISTA_VALORES[2] = candles['INDV22']['<INDV22>'] 
                            if date >= 20221011 and date < 20221213:
                                if 'INDZ22' == ticker_dicioin: 
                                    print(date, ticker_dicioin)
                                    LISTA_VALORES[2] = candles['INDZ22']['<INDZ22>'] 
                            
                            if 'ABEV3' == ticker_dicioin:  
                                LISTA_VALORES[0] = candles['ABEV3']['AAAAMMDD']
                                LISTA_VALORES[1] = candles['ABEV3']['HHMM']
                                LISTA_VALORES[3] = candles['ABEV3']['<ABEV3>']
                            if 'PRIO3' == ticker_dicioin:
                                LISTA_VALORES[4] = candles['PRIO3']['<PRIO3>']
                            if 'PETR4' == ticker_dicioin:
                                LISTA_VALORES[5] = candles['PETR4']['<PETR4>']
                            if 'VALE3' == ticker_dicioin:
                                LISTA_VALORES[6] = candles['VALE3']['<VALE3>']
                            if 'AZUL4' == ticker_dicioin:
                                LISTA_VALORES[7] = candles['AZUL4']['<AZUL4>']
                            if 'MGLU3' == ticker_dicioin:
                                LISTA_VALORES[8] = candles['MGLU3']['<MGLU3>']
                            if 'JHSF3' == ticker_dicioin:
                                LISTA_VALORES[9] = candles['JHSF3']['<JHSF3>']
                            if 'BRML3' == ticker_dicioin:
                                LISTA_VALORES[10] = candles['BRML3']['<BRML3>']

                    print(LISTA_VALORES)
                    if LISTA_VALORES[0] != 0:  
                        #  ATUALIZAR DADOS DO DATABASE:
                        os.chdir(B3_DATABASE)
                        analise_diretorio = os.path.exists(nome_csv_novo)
                        if analise_diretorio:
                            with open(nome_csv_novo, 'a', newline='') as csvfile:
                                writer = csv.writer(csvfile)
                                writer.writerow(LISTA_VALORES)
                                csvfile.close()
                        else:
                            LISTA_VALORES = [
                                'AAAAMMDD',
                                'HHMM',
                                'INDFUT',
                                'ABEV3',
                                'PRIO3',
                                'PETR4',
                                'VALE3',
                                'AZUL4',
                                'MGLU3',
                                'JHSF3',
                                'BRML3'
                            ]  

                            with open(nome_csv_novo, 'w', newline='') as csv_planilha:
                                writer = csv.writer(csv_planilha)
                                writer.writerow(LISTA_VALORES)
                                csv_planilha.close()

                    ult_candle = candle_id
                    candles = {}
                    LISTA_VALORES = [
                        0,
                        0,
                        0,
                        0,
                        0,
                        0,
                        0,
                        0,
                        0,
                        0,
                        0
                    ]
            os.chdir(B3_DATABASE)
            os.remove('Database.csv')


if __name__ == "__main__":

    inicio = time.time()
    modelagem_correlacao()
    fim = time.time()

    print('TEMPO DE EXECUÇÃO -------->', (fim - inicio) / 60)