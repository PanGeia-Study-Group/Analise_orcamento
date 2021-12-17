import os,sys
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from typing import Callable, Any, Iterable

sys.path.append('..\\..')
DATA_PATH_TRATADOS = "../../dados/2_dados_tratados"

def historico_orcamento(orcamento:pd.DataFrame) -> go.Figure:
    '''
    Calcula o histórico do orçamento inicial, atualizado, empenhado e realizado

    Parâmetros:
    -----------
        1. orcamento {pd.DataFrame}: 
            arquivo com o histórico orçamentário.

    Saídas:
    -------
        1. fig {plotly.graph_objects.Figure}:
            figura com o gráfico do histórico do orçamento
    '''
    aux = orcamento.groupby('exercicios').sum().reset_index()
    aux.iloc[:, 1:] = aux.iloc[:, 1:]/1e9

    fig = go.Figure()
    fig.add_trace(go.Scatter(name='Orçamento inicial', x=aux.exercicios, y=aux.orcamento_inicial, mode='lines'))
    fig.add_trace(go.Scatter(name='Orçamento atualizado', x=aux.exercicios, y=aux.orcamento_atualizado, mode='lines'))
    fig.add_trace(go.Scatter(name='Orçamento empenhado', x=aux.exercicios, y=aux.orcamento_empenhado, mode='lines'))
    fig.add_trace(go.Scatter(name='Orçamento realizado', x=aux.exercicios, y=aux.orcamento_realizado, mode='lines'))


    fig.update_layout(title='Orçamento brasileiro de 2014 a 2021',
                      yaxis_title='Orçamento (em R$ bilhões)')

    return fig

def historico_orcamento_filter(orcamento:pd.DataFrame, filtros:dict) -> go.Figure:
    '''
    Calcula o histórico do orçamento filtrado para algum

    Parâmetros:
    -----------
        1. orcamento {pd.DataFrame}: 
            arquivo com o histórico orçamentário;
        2. filtros {dict}:
            dicionário com as keys e os valores a serem filtrados.
  
    Saídas:
    -------
        1. fig {plotly.graph_objects.Figure}:
            figura com o gráfico do histórico do orçamento
    '''
    chaves = list(filtros.keys())
    valores = list(filtros.values())

    aux = orcamento.copy()
    for i, chave in enumerate(chaves):
        aux = aux[aux[chave].isin(valores[i])]
    aux = aux.groupby('exercicios').sum().reset_index()
    aux.iloc[:, 1:] = aux.iloc[:, 1:]/1e9

    fig = go.Figure()
    fig.add_trace(go.Scatter(name='Orçamento inicial', x=aux.exercicios, y=aux.orcamento_inicial, mode='lines'))
    fig.add_trace(go.Scatter(name='Orçamento atualizado', x=aux.exercicios, y=aux.orcamento_atualizado, mode='lines'))
    fig.add_trace(go.Scatter(name='Orçamento empenhado', x=aux.exercicios, y=aux.orcamento_empenhado, mode='lines'))
    fig.add_trace(go.Scatter(name='Orçamento realizado', x=aux.exercicios, y=aux.orcamento_realizado, mode='lines'))


    fig.update_layout(title='Orçamento brasileiro de 2014 a 2021',
                      yaxis_title='Orçamento (em R$ bilhões)')

    return fig

if __name__ == '__main__':
    orcamento = pd.read_pickle(os.path.join(DATA_PATH_TRATADOS, 'orcamento_tratado.pkl'))
    PIB = pd.read_pickle(os.path.join(DATA_PATH_TRATADOS, 'PIB.pkl'))

    fig1 = historico_orcamento(orcamento)
    fig2 = historico_orcamento_filter(orcamento, {'nome_orgao_sup':['Ministério da Educação']})
    fig1.show()
    fig2.show()