import os
import pandas as pd

DIRETORIO_CRYPTO = r'D:\DIRETORIOS\CRYPTO_BRUTOS'


def format_file():
    """
    Utilizado para montar a planilha utilizado no robô para crypto.

    PASSOS: 

    1- ADICIONAR o arquivo.txt que está no HISTORICO_TXT
    2- Mudar o nome do txt para csv 
    3- Colocar o arquivo novo no diretorio
    4- TYPE *.csv > nomecrypto_BMF_I.TXT
    5- ADICIONAR COPIA NO HISTORICO TXT
    6- ADICIONAR cabeçalho
        <unixepoch>,<open>,<high>,<low>,<close>,<vol>,<tempfech>,<ig>,<qty>,<ig>,<ig>,<ig>
    7- MUDAR NOMES DAS CRYPTO NO CODIGO
    8- rodar o codigo
    """

    nome_arquivo = 'XRPUSDT_BMF_I.txt'
    nome_crypto = 'XRPUSDT'

    os.chdir(DIRETORIO_CRYPTO)
    csv = pd.read_csv(nome_arquivo, sep=',')

    novo_arquivo_csv = pd.DataFrame(csv, columns=['<ticker>', '<unixepoch>', '<open>', '<high>', '<low>', '<close>',
                                                  '<vol>', '<tempfech>', '<ig>', '<qty>', '<ig>', '<ig>', '<ig>'])
    novo_arquivo_csv['<ticker>'] = nome_crypto
    print(novo_arquivo_csv)
    novo_arquivo_csv.to_csv('XRPUSDT_BMF_I.csv', index=False)


if __name__ == '__main__':
    format_file()
