import os,sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from tqdm import tqdm
from pdfminer.high_level import extract_text
import tabula
from PyPDF2 import PdfFileWriter, PdfFileReader
np.set_printoptions(suppress=True)
import camelot
import re
import pickle

import warnings
#warnings.filterwarnings("ignore", 'This pattern has match groups')

path_entrada = "../dados/1_dados_entrada"
path_tratados = "../dados/2_dados_tratados"

dic_ano_pag = {2020:[27,28], 2021:[28,29], 2022:[28,29]}

list_por_ano = []
for ano in list(dic_ano_pag.keys()):
    print(ano)
    arquivo = os.path.join(path_entrada, "PLOA" + str(ano) + "_anex.pdf")

    #### Página 1 ####
    dfs = camelot.read_pdf(arquivo, pages=str(dic_ano_pag[ano][0]), flavor='stream') #leitura da página

    # Import do pd.DataFrame com linhas e colunas de interesse
    df = dfs[0].df
    df = df.iloc[5:,:]
    #print(df)
    if len(df.columns) == 4:
        df = df.drop(columns=2)
    df.columns = ['acao', 'texto_acao', 'verba']

    # Ajuste das colunas cujas linhas que se desencontravam
    df_1 = df[df.acao != ''].iloc[:,:-1]
    df_2 = df[df.verba != ''].verba
    df_2.index = df_2.index - 1
    df = pd.concat((df_1,df_2), axis=1).reset_index(drop=True)

    df.acao = df.acao.astype(int) #Ajuste do código da ação
    df.verba = df.verba.str.replace('.','', regex=True).str.replace(',','.', regex=True).str.replace(r'R\$\s*','', regex=True).astype(float) #Ajuste da verba em R$ MILHÕES

    # Cria dataset com as funções, para servir de de/para
    df_funcao_1 = df[(df.acao > 700)&(df.acao < 7000)]
    df_funcao_1 = df_funcao_1.rename(columns={'acao':'funcao', 'texto_acao':'texto_funcao'})

    # Filtro apenas pelas ações e traz a função de cada ação do df_funcao_1
    df = df[df.acao > 7000]
    df['funcao'] = df.acao//10
    df_pag1 = pd.merge(df, df_funcao_1[['funcao','texto_funcao']], on='funcao', how='left')



    #### Página 2 ####
    dfs = camelot.read_pdf(arquivo, pages=str(dic_ano_pag[ano][1]), flavor='stream')

    # Import do pd.DataFrame com linhas e colunas de interesse
    df = dfs[0].df
    df = df.iloc[3:-1,:]
    if len(df.columns) == 4:
        df = df.drop(columns=2)
    df.columns = ['acao', 'texto_acao', 'verba']

    # Ajuste das colunas cujas linhas que se desencontravam
    df_1 = df[df.acao != ''].iloc[:,:-1]
    df_2 = df[df.verba != ''].verba
    df_2.index = df_2.index - 1
    df = pd.concat((df_1,df_2), axis=1).reset_index(drop=True)

    df.acao = df.acao.astype(int) #Ajuste do código da ação
    df.verba = df.verba.str.replace('.','', regex=True).str.replace(',','.', regex=True).str.replace(r'R\$\s*','', regex=True).astype(float) #Ajuste da verba em R$ MILHÕES

    # Cria dataset com as funções, para servir de de/para
    df_funcao_2 = df[(df.acao > 700)&(df.acao < 7000)]
    df_funcao_2 = df_funcao_2.rename(columns={'acao':'funcao', 'texto_acao':'texto_funcao'})
    df_funcao = pd.concat((df_funcao_1,df_funcao_2))

    # Filtro apenas pelas ações e traz a função de cada ação do df_funcao
    df = df[df.acao > 7000]
    df['funcao'] = df.acao//10
    df_pag2 = pd.merge(df, df_funcao[['funcao','texto_funcao']], on='funcao', how='left')

    # União dos datasets das duas páginas
    df_final = pd.concat((df_pag1, df_pag2)).reset_index(drop=True)
    
    df_final['ano'] = ano #Adição da coluna referente ao ano
    list_por_ano.append(df_final) #Inserção na lista para concatenação posterior

#Geração do dataset com todas as informações
df_finalissimo = pd.concat(list_por_ano)

# Salva o dataset em um arquivo pickle
arquivo_destino = os.path.join(path_tratados, "COFOG.pkl")
df_finalissimo.to_pickle(arquivo_destino)
