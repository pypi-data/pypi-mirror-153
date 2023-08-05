import csv
import os

DIRETORIO_BRUTO_COTA = r'D:\DIRETORIOS\COTA_BRUTOS'
DIRETORIO_COTAHIST = r'D:\DADOS_FINANCEIROS\Database_COTAHIST'

def cotahist():

    ATIVOS = [
        'PETR',
        'VALE',
        'VVAR',
        'BOVA',
        'ITUB',
        'BBDC',
        'COGN',
        'SUZB',
        'BBAS',
        'CSNA',
        'USIM',
        'GGBR',
        'MGLU',
        'JBSS',
        'CIEL',
        'PCAR',
        'MRFG',
        'IRBR',
        'BRAP',
        'SBSP',
        'ABEV',
        'B3SA',
        'VIIA',
        'TAEE',
        'B3SA',
        'LREN',
        'AMER',
        'AZUL',
        'BBSE',
        'BEEF',
        'BCAP',
        'BRFS',
        'BRML',
        'BRFS',
        'CASH',
        'CCRO',
        'CMIG',
        'CPLE',
        'CSAN',
        'CYRE',
        'EGIE',
        'ELET',
        'EMBR',
        'FLRY',
        'GOAU',
        'HAPV',
        'HYPE',
        'ITSA',
        'KLBN',
        'MULT',
        'NTCO',
        'PRIO',
        'QUAL',
        'RADL',
        'RAIL',
        'RENT',
        'UGPA',
        'WEGE',
        'YDUQ',
        'SANB'
    ]

    for caminho_path, dir_brutos, arquivo_buto in os.walk(DIRETORIO_BRUTO_COTA):
        for arquivo in arquivo_buto:
            print(arquivo)

            with open(os.path.join(caminho_path, arquivo), 'r') as arquivo_referencia:
                arquivo_txt = csv.reader(arquivo_referencia)
                for registro in arquivo_txt:
                    validacao = registro[0]

                    if validacao[0:2] != '01':
                        continue

                    ticker = validacao[12:16]

                    for acoes in ATIVOS:
                        if ticker != acoes:
                            continue

                        nome_arquivo = 'dados_' + ticker + '.txt'

                        os.chdir(DIRETORIO_COTAHIST)
                        analise_diretorio = os.path.exists(nome_arquivo)

                        if analise_diretorio:
                            with open(nome_arquivo, 'a', newline='') as csvfile:
                                writer = csv.writer(csvfile)
                                writer.writerow(registro)
                        else:
                            with open(nome_arquivo, 'w', newline='') as csv_planilha:
                                writer = csv.writer(csv_planilha)
                                writer.writerow(registro)


if __name__ == '__main__':
    cotahist()
