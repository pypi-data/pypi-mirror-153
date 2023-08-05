import os
import pandas as pd
import time

B3_DATABASE = r'D:\DADOS_FINANCEIROS\Database_SEGUNDOS'
B3_TICKERS = r'D:\DADOS_FINANCEIROS\Database_TICKERS'
B3_FUTUROS = r'D:\DIRETORIOS\B3_FUTUROS'


def selecionador_B3():

    tickrs = [ 
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
        'LOGN3_'
        ]

    outros = [
        'BOVA11_',
        'TAEE11_',
        'SANB11_',
        'SAPR11_',
        'KLBN11_',
        'ENGI11_',
        'BPAC11_',
        'SULA11_',
        'BIDI11_',
        'IGTI11_',
        'STBP11_',
        'ALUP11_',
        'GPIV33_'
        ]
    
    futuros = [
        'WINF21_',
        'WING21_',
        'WINH21_',
        'WINJ21_',
        'WINK21_',
        'WINM21_',
        'WINN21_',
        'WINQ21_',
        'WINU21_',
        'WINV21_',
        'WINX21_',
        'WINZ21_',
        'WDOF21_',
        'WDOG21_',
        'WDOH21_',
        'WDOJ21_',
        'WDOK21_',
        'WDOM21_',
        'WDON21_',
        'WDOQ21_',
        'WDOU21_',
        'WDOV21_',
        'WDOX21_',
        'WDOZ21_',
        'WING22_',
        'WINH22_',
        'WINJ22_',
        'WINK22_',
        'WINM22_',
        'WINN22_',
        'WINQ22_',
        'WINU22_',
        'WINV22_',
        'WINX22_',
        'WINZ22_',
        'WDOF22_',
        'WDOG22_',
        'WDOH22_',
        'WDOJ22_',
        'WDOK22_',
        'WDOM22_',
        'WDON22_',
        'WDOQ22_',
        'WDOU22_',
        'WDOV22_',
        'WDOX22_',
        'WDOZ22_',
        'INDF21_',
        'INDG21_',
        'INDH21_',
        'INDJ21_',
        'INDK21_',
        'INDM21_',
        'INDN21_',
        'INDQ21_',
        'INDU21_',
        'INDV21_',
        'INDX21_',
        'INDZ21_',
        'DOLF21_',
        'DOLG21_',
        'DOLH21_',
        'DOLJ21_',
        'DOLK21_',
        'DOLM21_',
        'DOLN21_',
        'DOLQ21_',
        'DOLU21_',
        'DOLV21_',
        'DOLX21_',
        'DOLZ21_',
        'INDF22_',
        'INDG22_',
        'INDH22_',
        'INDJ22_',
        'INDK22_',
        'INDM22_',
        'INDN22_',
        'INDQ22_',
        'INDU22_',
        'INDV22_',
        'INDX22_',
        'INDZ22_',
        'DOLF22_',
        'DOLG22_',
        'DOLH22_',
        'DOLJ22_',
        'DOLK22_',
        'DOLM22_',
        'DOLN22_',
        'DOLQ22_',
        'DOLU22_',
        'DOLV22_',
        'DOLX22_',
        'DOLZ22_',
        ]   

    for _, _, arquivos in os.walk(B3_DATABASE):
        for arquivo in arquivos:
            nome_acoes = str(arquivo[0:6])
            nome_outros = str(arquivo[0:7])
            nome_futuros = str(arquivo[0:7])
            teste = False

            for dados in tickrs:
                if nome_acoes != dados:
                    continue
                os.chdir(B3_DATABASE)
                csv = pd.read_csv(arquivo, sep=',')
                diretorio_novo = os.path.join(B3_TICKERS, arquivo)
                csv.to_csv(diretorio_novo, index=False)
                print(arquivo, '-------> VALIDO')
                teste = True
            
            if not teste:
                for dados in outros:
                    if nome_outros != dados:
                        continue
                    os.chdir(B3_DATABASE)
                    csv = pd.read_csv(arquivo, sep=',')
                    diretorio_novo = os.path.join(B3_TICKERS, arquivo)
                    csv.to_csv(diretorio_novo, index=False)
                    print(arquivo, '-------> VALIDO')
                    teste = True
                if not teste:
                    for dados in futuros:
                        if nome_futuros != dados:
                            continue
                        os.chdir(B3_DATABASE)
                        csv = pd.read_csv(arquivo, sep=',')

                        if nome_futuros[0:3] == 'DOL': 
                            diretorio_novo = os.path.join(B3_FUTUROS, arquivo)
                            csv.to_csv(diretorio_novo, index=False)
                            print(arquivo, '-------> VALIDO')
                        elif nome_futuros[0:3] == 'IND': 
                            diretorio_novo = os.path.join(B3_FUTUROS, arquivo)
                            csv.to_csv(diretorio_novo, index=False)
                            print(arquivo, '-------> VALIDO')
                        elif nome_futuros[0:3] == 'WDO': 
                            diretorio_novo = os.path.join(B3_FUTUROS, arquivo)
                            csv.to_csv(diretorio_novo, index=False)
                            print(arquivo, '-------> VALIDO')
                        else:
                            diretorio_novo = os.path.join(B3_FUTUROS , arquivo)
                            csv.to_csv(diretorio_novo, index=False)
                            print(arquivo, '-------> VALIDO')
                            

if __name__ == '__main__':
    inicio = time.time()
    selecionador_B3()
    fim = time.time()
    print('TEMPO DE EXECUÇÃO: ', (fim - inicio) / 60)