from zipfile import ZipFile
import os

diretorio = r'\\dados\Trades\HISTORICO\Historico_COTAHIST\DADOS_DIARIOS\ABRIL_2022'


for _, _, files_op in os.walk(diretorio):
    for opcoes in files_op:
        
        os.chdir(diretorio)
        z = ZipFile(opcoes, 'r')
        z.extractall()
        z.close()
