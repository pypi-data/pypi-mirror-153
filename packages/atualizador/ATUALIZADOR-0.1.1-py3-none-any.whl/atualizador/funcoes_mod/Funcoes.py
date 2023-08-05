def modelagem_tedesco(arquivo_txt, diretorio):
    """
    Utilizado para modelar o DataFrame com os itens de
    interesse do Tedesco. 
    """    
    import os
    import pandas as pd

    os.chdir(diretorio)
    arquivo_txt = pd.read_csv(arquivo_txt, sep=';')

    arquivo_txt.drop('RptDt', axis=1, inplace=True)
    arquivo_txt.drop('UpdActn', axis=1, inplace=True)
    arquivo_txt.drop('TradgSsnId', axis=1, inplace=True)
    arquivo_txt.drop('TradId', axis=1, inplace=True)
    arquivo_txt.rename(columns={'TckrSymb': '<ticker>'}, inplace=True)
    arquivo_txt.rename(columns={'GrssTradAmt': '<preco>'}, inplace=True)
    arquivo_txt.rename(columns={'TradQty': '<qty>'}, inplace=True)
    arquivo_txt.rename(columns={'NtryTm': '<tempo>'}, inplace=True)
    arquivo_txt.rename(columns={'TradDt': '<date>'}, inplace=True)
    arquivo_txt['<date>'] = arquivo_txt['<date>'].str.replace('-', '')
    arquivo_txt['<time>'] = arquivo_txt['<tempo>'].astype(str)
    # arquivo_txt['<tempo>'] = arquivo_txt['<tempo>'].astype(str)
    # arquivo_txt['<time>'] = arquivo_txt['<tempo>']
    arquivo_txt.drop('<tempo>', axis=1, inplace=True)

    # os.chdir(diretorio)
    nome_arquivo = 'Database.csv'
    arquivo_txt.to_csv(nome_arquivo, index=False)

    return nome_arquivo


def modelagem_milissegundos_b3(arquivo_txt):
    """Usada para excluir e preparar o arquivo da BOVESPA para começar 
    a trabalhar detro dos dados no tempo em milissegundos.
    """

    arquivo_txt.drop('RptDt', axis=1, inplace=True)
    arquivo_txt.drop('UpdActn', axis=1, inplace=True)
    arquivo_txt.drop('TradgSsnId', axis=1, inplace=True)
    arquivo_txt.rename(columns={'TradQty': '<trades>'}, inplace=True)
    arquivo_txt.rename(columns={'TckrSymb': '<ticker>'}, inplace=True)
    arquivo_txt.rename(columns={'GrssTradAmt': '<preco>'}, inplace=True)
    arquivo_txt.rename(columns={'TradId': '<qty>'}, inplace=True)
    arquivo_txt.rename(columns={'NtryTm': '<tempo>'}, inplace=True)
    arquivo_txt.rename(columns={'TradDt': '<date>'}, inplace=True)
    arquivo_txt['<preco>'] = arquivo_txt['<preco>'].str.replace(',', '.')
    arquivo_txt['<preco>'] = arquivo_txt['<preco>'].astype(float)
    arquivo_txt['<vol>'] = arquivo_txt['<qty>'] * arquivo_txt['<preco>']
    arquivo_txt['<time>'] = arquivo_txt['<tempo>'].astype(str)
    #arquivo_txt['<tempo>'] = arquivo_txt['<tempo>'].astype(str)
    #arquivo_txt['<time>'] = arquivo_txt['<tempo>']
    arquivo_txt.drop('<tempo>', axis=1, inplace=True)
    

def modelagem_segundos_b3(txt, diretorio_bruto, diretorio_b3_database):
    """Usada para excluir e preparar o arquivo da BOVESPA para começar 
    a trabalhar detro dos dados nos periodos de 1 minuto.
    
    COLUNA DA B3:
    RptDt -> DATA DA INFORMAÇÃO
    TckrSymb -> SIMBOLO
    UpdActn -> 0=NEGOCIO NOVO, 2=CANCELAMENTO
    GrssTradAmt -> PRECO DO NEGOCIO
    TradQty -> QUANTIDADE DE NEGOCIO
    NtryTm -> HORA DO NEGOCIO FECHADO
    TradId -> NUMERO DO NEGOCIO
    TradgSsnId -> 1= SESSÃO REGULAR, 6=ALFER HOURS 
    TradDt -> DATA DO PREGÃO
    """
    import os
    import pandas as pd

    os.chdir(diretorio_bruto)
    txt_arquivo = pd.read_csv(txt, sep=';')

    txt_arquivo.drop('RptDt', axis=1, inplace=True)
    txt_arquivo.drop('UpdActn', axis=1, inplace=True)
    txt_arquivo.drop('TradgSsnId', axis=1, inplace=True)
    txt_arquivo.rename(columns={'TradQty': '<trades>'}, inplace=True)
    txt_arquivo.rename(columns={'TckrSymb': '<ticker>'}, inplace=True)
    txt_arquivo.rename(columns={'GrssTradAmt': '<preco>'}, inplace=True)
    txt_arquivo.rename(columns={'TradId': '<qty>'}, inplace=True)
    txt_arquivo.rename(columns={'NtryTm': '<time>'}, inplace=True)
    txt_arquivo.rename(columns={'TradDt': '<date>'}, inplace=True)
    txt_arquivo['<preco>'] = txt_arquivo['<preco>'].str.replace(',', '.')
    txt_arquivo['<preco>'] = txt_arquivo['<preco>'].astype(float)
    txt_arquivo['<date>'] = txt_arquivo['<date>'].str.replace('-', '')
    txt_arquivo['<vol>'] = txt_arquivo['<qty>'] * txt_arquivo['<preco>']

    os.chdir(diretorio_b3_database)
    nome_arquivo = 'Database.csv'
    txt_arquivo.to_csv(nome_arquivo, index=False)

    return nome_arquivo


# ----------------------------------------------------------------------- #


def montagem_candles_estudos(txt, diretorio_bruto, diretorio_b3_database):
    """Usada para excluir e preparar o arquivo da BOVESPA para começar 
    a trabalhar detro dos dados nos periodos de estudos.
    COLUNA DA B3:
        RptDt ->
        TckrSymb ->
        UpdActn ->
        GrssTradAmt ->
        TradQty ->
        NtryTm ->
        TradId ->
        TradgSsnId ->
        TradDt ->
    """
    import os
    import pandas as pd

    os.chdir(diretorio_bruto)
    txt_arquivo = pd.read_csv(txt, sep=';')

    txt_arquivo.drop('RptDt', axis=1, inplace=True)
    txt_arquivo.drop('UpdActn', axis=1, inplace=True)
    txt_arquivo.drop('TradgSsnId', axis=1, inplace=True)
    txt_arquivo.rename(columns={'TradQty': '<trades>'}, inplace=True)
    txt_arquivo.rename(columns={'TckrSymb': '<ticker>'}, inplace=True)
    txt_arquivo.rename(columns={'GrssTradAmt': '<preco>'}, inplace=True)
    txt_arquivo.rename(columns={'TradId': '<qty>'}, inplace=True)
    txt_arquivo.rename(columns={'NtryTm': '<time>'}, inplace=True)
    txt_arquivo.rename(columns={'TradDt': '<date>'}, inplace=True)
    txt_arquivo['<preco>'] = txt_arquivo['<preco>'].str.replace(',', '.')
    txt_arquivo['<date>'] = txt_arquivo['<date>'].str.replace('-', '')
    txt_arquivo['<preco>'] = txt_arquivo['<preco>'].astype(float)
    txt_arquivo['<vol>'] = txt_arquivo['<qty>'] * txt_arquivo['<preco>']

    nome_arquivo = 'Database.csv'
    os.chdir(diretorio_b3_database)
    txt_arquivo.to_csv('Database.csv', index=False)

    return nome_arquivo


def b3_planilha_segundos(analise_ticker, diretorio_dados_novos, ticker_dados):
    """Utilizado para estruturar a planilha que será
    usado no robô no tempo em milissegundos.
    """
    import os

    import pandas as pd

    csv = analise_ticker
    arquivo_robo = pd.DataFrame(data=[],
                                index=[],
                                columns=['<ticker>',
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
                                )
    for dados in csv['<time>'].unique():
        """Parareorganizar as informações que
        serão salvas na nova planilha.
        """
        tempo_unique = csv[csv['<time>'] == dados]
        ticker = tempo_unique['<ticker>'].unique()
        ticker = ticker[0]
        date = tempo_unique['<date>'].unique()
        date = date[0]
        time = str(dados) + '00'
        trades = tempo_unique['<trades>'].sum()
        close = tempo_unique['<preco>'].iloc[-1]
        low = min(tempo_unique['<preco>'])
        high = max(tempo_unique['<preco>'])
        openn = tempo_unique['<preco>'].iloc[0]
        vol = tempo_unique['<vol>'].sum()
        tradqty = tempo_unique['<qty>'].sum()
        aft = 'N'

        arquivo_robo = arquivo_robo.append({'<ticker>': ticker,
                                            '<date>': date,
                                            '<time>': time,
                                            '<trades>': trades,
                                            '<close>': close,
                                            '<low>': low,
                                            '<high>': high,
                                            '<open>': openn,
                                            '<vol>': vol,
                                            '<qty>': tradqty,
                                            '<aft>': aft
                                            }, ignore_index=True)

    arquivo_robo['<date>'] = arquivo_robo['<date>'].str.replace('-', '')
    nome_csv = ticker_dados + '_BMF_I' + '.csv'
    planilha_local = os.path.join(diretorio_dados_novos, nome_csv)
    arquivo_robo.to_csv(planilha_local, index=False)

    return planilha_local
