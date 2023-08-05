import os
import time
import pandas as pd

B3_DATABASE = r'D:\DADOS_FINANCEIROS\Database_SEGUNDOS'
B3_OPCOES = r'D:\DADOS_FINANCEIROS\Database_OPÇÕES'


def dir_opcoes():
    """
    Utilizado para criar diretorios separados com os arquivos
    com todos os contratos de oções existente no banco de dados.
    """
    OPCOES = [
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

    for _, _, arquivos in os.walk(B3_DATABASE):
        for arquivo in arquivos:
            nome_csv = str(arquivo[0:4])
            print(nome_csv)

            for dados in OPCOES:
                if nome_csv != dados:
                    continue

                os.chdir(B3_OPCOES)
                analise_opcoes = os.path.exists('Bovespa_' + dados)

                if analise_opcoes:
                    os.chdir(B3_DATABASE)
                    csv = pd.read_csv(arquivo, sep=',')
                    diretorio_novo = os.path.join(
                        B3_OPCOES, 
                        'Bovespa_' + nome_csv, 
                        arquivo
                    )
                    csv.to_csv(diretorio_novo, index=False)
          
                    diretorio_opcoes = os.path.join(
                        B3_OPCOES, 
                        'Bovespa_OPCOES', 
                        arquivo
                    )
                    csv.to_csv(diretorio_opcoes, index=False)
                    
                else:
                    os.chdir(B3_OPCOES)
                    os.mkdir('Bovespa_' + nome_csv)

                    os.chdir(B3_DATABASE)
                    csv = pd.read_csv(arquivo, sep=',')
                    diretorio_novo = os.path.join(
                        B3_OPCOES, 
                        'Bovespa_' + nome_csv, 
                        arquivo
                    )
                    csv.to_csv(diretorio_novo, index=False)
                    
                    os.chdir(B3_OPCOES)
                    analise_opcoes = os.path.exists('Bovespa_OPCOES')

                    if analise_opcoes:
                        diretorio_opcoes = os.path.join(
                            B3_OPCOES, 
                            'Bovespa_OPCOES', 
                            arquivo
                        )
                        csv.to_csv(diretorio_opcoes, index=False)
                    else:
                        os.mkdir('Bovespa_OPCOES')                      
                        diretorio_opcoes = os.path.join(
                            B3_OPCOES, 
                            'Bovespa_OPCOES', 
                            arquivo
                        )
                        csv.to_csv(diretorio_opcoes, index=False)

if __name__ == '__main__':
    
    inicio = time.time()
    dir_opcoes()
    fim = time.time()
    print('O TEMPO DE EXECUÇÃO -------->', (fim - inicio) / 60)
