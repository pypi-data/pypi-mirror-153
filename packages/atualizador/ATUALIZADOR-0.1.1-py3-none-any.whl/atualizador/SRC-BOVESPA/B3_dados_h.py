import csv
import os
import pandas as pd
import shutil
import tempfile

DIRETORIO_COTA_H = r'D:\DADOS_FINANCEIROS\Database_DADOS_H'
DIRETORIO_COTAHIST = r'D:\DADOS_FINANCEIROS\Database_COTAHIST'
DIRETORIO_OPCOES = r'D:\DADOS_FINANCEIROS\Database_OPÇÕES\Bovespa_OPCOES'

def estrutura_dados_H():
    """
    Utilizado para modelar o arquivo para 
    o formato compatível do robô.
    """

    for caminho_path, dir_arquivos, arquivos_cota in os.walk(DIRETORIO_COTAHIST):
        for cotahist_txt in arquivos_cota:

            with open(os.path.join(caminho_path, cotahist_txt), 'r', newline='') as csv_file_cotahist:
                reader_cotahist = csv.reader(csv_file_cotahist)
                for rows in reader_cotahist:

                    COTAHIST = rows[0]
                    SYMBOL_COTA = COTAHIST[12:23].split()

                    # SE O ULTIMO CARACTER NÃO FOR NÚMERO, IRÁ IGNORAR:
                    #  if not list(SYMBOL_COTA[0])[-1].isdigit():
                    #      continue

                    DATE_COTA = COTAHIST[2:10]
                    HOURS_COTA = 000000000
                    UNDERLYNG_COTA = SYMBOL_COTA[0][0:4]
                    OPEN_COTA = COTAHIST[56:69]
                    HIGH_COTA = COTAHIST[69:82]
                    LOW_COTA = COTAHIST[82:95]
                    CLOSE_COTA = COTAHIST[108:121]
                    TRADES_COTA = COTAHIST[147:152]
                    VOL_COTA = COTAHIST[170:188]
                    DERIVATICO_COTA = 'S'

                    if int(COTAHIST[202:210]) > 20401231:
                        VENC_COTA = 0

                    if int(COTAHIST[202:210]) < 20401231:
                        VENC_COTA = COTAHIST[202:210]

    
                    if int(DATE_COTA) < 20211215:
                        continue
                    
                    # REMOVENDO OS ZEROS À ESQUERDA EM UMA LISTA:
                    REMOVEDOR_ZEROS_ESQUEDA = [
                        OPEN_COTA, 
                        HIGH_COTA, 
                        HIGH_COTA, 
                        LOW_COTA, 
                        CLOSE_COTA, 
                        VOL_COTA
                    ]

                    REMOVEDOR_ZEROS_ESQUEDA = [
                        zeros.lstrip('0') for zeros in REMOVEDOR_ZEROS_ESQUEDA
                    ]

                    VOL_COTA = REMOVEDOR_ZEROS_ESQUEDA[-1]

                    if int(OPEN_COTA) > 0:
                        if len(REMOVEDOR_ZEROS_ESQUEDA[0]) == 5:
                            OPEN_COTA = REMOVEDOR_ZEROS_ESQUEDA[0][0:3] + \
                                '.' + REMOVEDOR_ZEROS_ESQUEDA[0][3:]
                        elif len(REMOVEDOR_ZEROS_ESQUEDA[0]) == 4:
                            OPEN_COTA = REMOVEDOR_ZEROS_ESQUEDA[0][0:2] + \
                                '.' + REMOVEDOR_ZEROS_ESQUEDA[0][2:]
                        elif len(REMOVEDOR_ZEROS_ESQUEDA[0]) == 3:
                            OPEN_COTA = REMOVEDOR_ZEROS_ESQUEDA[0][0:1] + \
                                '.' + REMOVEDOR_ZEROS_ESQUEDA[0][1:]
                        elif len(REMOVEDOR_ZEROS_ESQUEDA[0]) == 2:
                            OPEN_COTA = '0' + '.' + REMOVEDOR_ZEROS_ESQUEDA[0]
                        elif len(REMOVEDOR_ZEROS_ESQUEDA[0]) == 1:
                            OPEN_COTA = '0' + '.' + '0' + \
                                REMOVEDOR_ZEROS_ESQUEDA[0]
                        else:
                            OPEN_COTA = '0'

                    if int(HIGH_COTA) > 0:
                        if len(REMOVEDOR_ZEROS_ESQUEDA[1]) == 5:
                            HIGH_COTA = REMOVEDOR_ZEROS_ESQUEDA[0][0:3] + \
                                '.' + REMOVEDOR_ZEROS_ESQUEDA[0][3:]
                        elif len(REMOVEDOR_ZEROS_ESQUEDA[1]) == 4:
                            HIGH_COTA = REMOVEDOR_ZEROS_ESQUEDA[0][0:2] + \
                                '.' + REMOVEDOR_ZEROS_ESQUEDA[0][2:]
                        elif len(REMOVEDOR_ZEROS_ESQUEDA[1]) == 3:
                            HIGH_COTA = REMOVEDOR_ZEROS_ESQUEDA[0][0:1] + \
                                '.' + REMOVEDOR_ZEROS_ESQUEDA[0][1:]
                        elif len(REMOVEDOR_ZEROS_ESQUEDA[1]) == 2:
                            HIGH_COTA = '0' + '.' + REMOVEDOR_ZEROS_ESQUEDA[0]
                        elif len(REMOVEDOR_ZEROS_ESQUEDA[1]) == 1:
                            HIGH_COTA = '0' + '.' + '0' + \
                                REMOVEDOR_ZEROS_ESQUEDA[0]
                        else:
                            HIGH_COTA = '0'

                    if int(LOW_COTA) > 0:
                        if len(REMOVEDOR_ZEROS_ESQUEDA[2]) == 5:
                            LOW_COTA = REMOVEDOR_ZEROS_ESQUEDA[0][0:3] + \
                                '.' + REMOVEDOR_ZEROS_ESQUEDA[0][3:]
                        elif len(REMOVEDOR_ZEROS_ESQUEDA[2]) == 4:
                            LOW_COTA = REMOVEDOR_ZEROS_ESQUEDA[0][0:2] + \
                                '.' + REMOVEDOR_ZEROS_ESQUEDA[0][2:]
                        elif len(REMOVEDOR_ZEROS_ESQUEDA[2]) == 3:
                            LOW_COTA = REMOVEDOR_ZEROS_ESQUEDA[0][0:1] + \
                                '.' + REMOVEDOR_ZEROS_ESQUEDA[0][1:]
                        elif len(REMOVEDOR_ZEROS_ESQUEDA[2]) == 2:
                            LOW_COTA = '0' + '.' + REMOVEDOR_ZEROS_ESQUEDA[0]
                        elif len(REMOVEDOR_ZEROS_ESQUEDA[2]) == 1:
                            LOW_COTA = '0' + '.' + '0' + \
                                REMOVEDOR_ZEROS_ESQUEDA[0]
                        else:
                            LOW_COTA = '0'

                    if int(CLOSE_COTA) > 0:
                        if len(REMOVEDOR_ZEROS_ESQUEDA[2]) == 5:
                            CLOSE_COTA = REMOVEDOR_ZEROS_ESQUEDA[0][0:3] + \
                                '.' + REMOVEDOR_ZEROS_ESQUEDA[0][3:]
                        elif len(REMOVEDOR_ZEROS_ESQUEDA[2]) == 4:
                            CLOSE_COTA = REMOVEDOR_ZEROS_ESQUEDA[0][0:2] + \
                                '.' + REMOVEDOR_ZEROS_ESQUEDA[0][2:]
                        elif len(REMOVEDOR_ZEROS_ESQUEDA[2]) == 3:
                            CLOSE_COTA = REMOVEDOR_ZEROS_ESQUEDA[0][0:1] + \
                                '.' + REMOVEDOR_ZEROS_ESQUEDA[0][1:]
                        elif len(REMOVEDOR_ZEROS_ESQUEDA[2]) == 2:
                            CLOSE_COTA = '0' + '.' + REMOVEDOR_ZEROS_ESQUEDA[0]
                        elif len(REMOVEDOR_ZEROS_ESQUEDA[2]) == 1:
                            CLOSE_COTA = '0' + '.' + '0' + \
                                REMOVEDOR_ZEROS_ESQUEDA[0]
                        else:
                            CLOSE_COTA = '0'

                    fieldnames_opcoes = [
                        'YYYYMMDD',
                        'HHMMSSFFF',
                        'ATIVO',
                        'SUBJACENTE',
                        'ABERTURA',
                        'MAXIMO',
                        'MINIMO',
                        'FECHAMENTO',
                        'NEGOCIOS',
                        'VOLUME',
                        'DERIVATIVO',
                        'VENCIMENTO'
                    ]

                    options_cotaH = {
                        'YYYYMMDD': int(DATE_COTA),
                        'HHMMSSFFF': HOURS_COTA,
                        'ATIVO': SYMBOL_COTA[0],
                        'SUBJACENTE': UNDERLYNG_COTA,
                        'ABERTURA': OPEN_COTA,
                        'MAXIMO': HIGH_COTA,
                        'MINIMO': LOW_COTA,
                        'FECHAMENTO': CLOSE_COTA,
                        'NEGOCIOS': TRADES_COTA,
                        'VOLUME': VOL_COTA,
                        'DERIVATIVO': DERIVATICO_COTA,
                        'VENCIMENTO': int(VENC_COTA)
                    }

                    os.chdir(DIRETORIO_COTA_H)
                    DADOS_OPCOES_H = 'dados_' + str(UNDERLYNG_COTA) + '_H.txt'
                    ANALISADOR_OPCOES = os.path.exists(DADOS_OPCOES_H)

                    if ANALISADOR_OPCOES:
                        os.chdir(DIRETORIO_COTA_H)
                        with open(DADOS_OPCOES_H, 'a', newline='') as csv_file:
                            writer = csv.DictWriter(
                                csv_file, delimiter=';', fieldnames=fieldnames_opcoes)
                            writer.writerow(options_cotaH)
                            csv_file.close()
                    else:
                        os.chdir(DIRETORIO_COTA_H)
                        with open(DADOS_OPCOES_H, 'w', newline='') as csv_file:
                            writer = csv.DictWriter(
                                csv_file, delimiter=';', fieldnames=fieldnames_opcoes)
                            writer.writeheader()
                            writer.writerow(options_cotaH)
                            csv_file.close()
            print(SYMBOL_COTA)
            # UTILIZADO PARA ORDENAR PELA DATA:
            os.chdir(DIRETORIO_COTA_H)
            ARQUIVO_NAO_ORDENADO = pd.read_csv(
                DADOS_OPCOES_H, encoding='UTF-8', sep=';')
            df_ordenado = ARQUIVO_NAO_ORDENADO.sort_values(by='YYYYMMDD')

            os.remove(DADOS_OPCOES_H)
            df_ordenado.to_csv(DADOS_OPCOES_H, sep=';', index=False)


def incrementa_time():
    """
    Utilizado para incrementar o time dentro do arquivo DADOS_H utilizando
    os arquivos separados de cada contraro de opções.
    """

    SYMBOL = {}

    for dirpath_opcoes, _, opcoes_files in os.walk(DIRETORIO_OPCOES):
        for rows in opcoes_files:

            OPCOES = rows[0:4]

            # ABRIR ARQUIVOS DAS OPCOES:
            with open(os.path.join(dirpath_opcoes, rows), 'r', newline='') as file_txt:
                reader_txt = csv.reader(
                    file_txt, delimiter=',')
                for data_opcoes in reader_txt:

                    if data_opcoes[0] == '<ticker>':
                        continue

                    TICKER = data_opcoes[0]
                    DATA = data_opcoes[1]
                    TIME = data_opcoes[2] + '000'

                    if int(DATA) < 20211215:
                        continue

                    if DATA not in SYMBOL:
                        SYMBOL[DATA] = []

                    SYMBOL[DATA].append(TIME)

           # ABRINDO DIRETORIO DO COTAHIST_H
            for dirpath, _, files in os.walk(DIRETORIO_COTA_H):
                for opcoes_H in files:

                    FIELDNAMES_COTA = opcoes_H.split('_')[1]
                    if FIELDNAMES_COTA == OPCOES:

                        # ABRIR ARQUIVOS DAS DADOS_H:
                        with open(os.path.join(dirpath, opcoes_H), 'r', newline='') as csv_file_h, \
                        tempfile.NamedTemporaryFile('w', delete=False) as out:

                            nome_temporario = out.name

                            reader_file = csv.reader(csv_file_h, delimiter=';')
                            for rows_opcoes in reader_file:

                                if rows_opcoes[0] == 'YYYYMMDD':
                                    with open(nome_temporario, 'w', newline='') as csv_file:
                                        writer = csv.writer(csv_file, delimiter=';')
                                        writer.writerow(rows_opcoes)
                                        csv_file.close()
                                    continue

                                TICKES_DADOS_H = rows_opcoes[2]
                                DATA_DADOS_H = int(rows_opcoes[0])
                                VENCIMENTO = rows_opcoes[-1]

                                
                                if TICKES_DADOS_H == TICKER:
                                    if str(DATA_DADOS_H) in SYMBOL:
                                        

                                        if SYMBOL[str(DATA_DADOS_H)] == []:
                                            
                                            print(TICKES_DADOS_H, str(DATA_DADOS_H))

                                            os.chdir(DIRETORIO_COTAHIST)
                                            analisador = os.path.exists('ERROS.txt')

                                            if analisador:
                                                with open('ERROS.txt', 'a', newline='') as csv_file:
                                                    writer = csv.writer(csv_file, delimiter=';')
                                                    writer.writerow([TICKES_DADOS_H, DATA_DADOS_H])
                                                    csv_file.close()
                                            else:
                                                with open('ERROS.txt', 'w', newline='') as csv_file:
                                                    writer = csv.writer(csv_file, delimiter=';')
                                                    writer.writerow([TICKES_DADOS_H, DATA_DADOS_H])
                                                    csv_file.close()

                                            rows_opcoes[1] == '000000000'

                                        os.chdir(dirpath)   
                                        if SYMBOL[str(DATA_DADOS_H)] != []:

                                            rows_opcoes[1] = SYMBOL[str(DATA_DADOS_H)].pop(-1)
                                    
                                        if VENCIMENTO[4:6] == '01':
                                            rows_opcoes[2] = OPCOES + '-' + VENCIMENTO[6:] + 'JAN' +  VENCIMENTO[2:4] + '-' + TICKES_DADOS_H[4:]
                                    
                                        if VENCIMENTO[4:6] == '02':
                                            rows_opcoes[2] = OPCOES + '-' + VENCIMENTO[6:] + 'FEB' +  VENCIMENTO[2:4] + '-' + TICKES_DADOS_H[4:]
                                    
                                        if VENCIMENTO[4:6] == '03':
                                            rows_opcoes[2] = OPCOES + '-' + VENCIMENTO[6:] + 'MAR' +  VENCIMENTO[2:4] + '-' + TICKES_DADOS_H[4:]
                                    
                                        if VENCIMENTO[4:6] == '04':
                                            rows_opcoes[2] = OPCOES + '-' + VENCIMENTO[6:] + 'APR' +  VENCIMENTO[2:4] + '-' + TICKES_DADOS_H[4:]

                                        if VENCIMENTO[4:6] == '05':
                                            rows_opcoes[2] = OPCOES + '-' + VENCIMENTO[6:] + 'MAY' +  VENCIMENTO[2:4] + '-' + TICKES_DADOS_H[4:]

                                        if VENCIMENTO[4:6] == '06':
                                            rows_opcoes[2] = OPCOES + '-' + VENCIMENTO[6:] + 'JUN' +  VENCIMENTO[2:4] + '-' + TICKES_DADOS_H[4:]
                                    
                                        if VENCIMENTO[4:6] == '07':
                                            rows_opcoes[2] = OPCOES + '-' + VENCIMENTO[6:] + 'JUL' +  VENCIMENTO[2:4] + '-' + TICKES_DADOS_H[4:]
                                    
                                        if VENCIMENTO[4:6] == '08':
                                            rows_opcoes[2] = OPCOES + '-' + VENCIMENTO[6:] + 'AUG' +  VENCIMENTO[2:4] + '-' + TICKES_DADOS_H[4:]
                                    
                                        if VENCIMENTO[4:6] == '09':
                                            rows_opcoes[2] = OPCOES + '-' + VENCIMENTO[6:] + 'SEP' +  VENCIMENTO[2:4] + '-' + TICKES_DADOS_H[4:]
                                    
                                        if VENCIMENTO[4:6] == '10':
                                            rows_opcoes[2] = OPCOES + '-' + VENCIMENTO[6:] + 'OCT' +  VENCIMENTO[2:4] + '-' + TICKES_DADOS_H[4:]
                                    
                                        if VENCIMENTO[4:6] == '11':
                                            rows_opcoes[2] = OPCOES + '-' + VENCIMENTO[6:] + 'NOV-' +  VENCIMENTO[2:4] + '-' + TICKES_DADOS_H[4:]
                                    
                                        if VENCIMENTO[4:6] == '12':
                                            rows_opcoes[2] = OPCOES + '-' + VENCIMENTO[6:] + 'DEC-' +  VENCIMENTO[2:4] + '-' + TICKES_DADOS_H[4:]

                                
                                with open(nome_temporario, 'a', newline='') as csv_file:
                                    writer = csv.writer(csv_file, delimiter=';')
                                    writer.writerow(rows_opcoes)
                                    csv_file.close()

                        os.chdir(DIRETORIO_COTA_H)
                        shutil.move(out.name, opcoes_H)  
                        SYMBOL = {} 


if __name__ == '__main__':
    incrementa_time()
