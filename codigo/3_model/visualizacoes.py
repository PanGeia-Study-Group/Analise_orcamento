import os,sys
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from typing import Callable, Any, Iterable

sys.path.append('..\\..')
DATA_PATH_TRATADOS = "../../dados/2_dados_tratados"

def filtragem_dataset(aux, args, ):
    valor = ['brasileiro']
    for dicio in args:
        chave = list(dicio.keys())[0]
        valor = list(dicio.values())[0]
        aux = aux[aux[chave].isin(valor)]
    valor = '|'.join(valor)

    return aux, valor

def historico_orcamento(orcamento:pd.DataFrame, *args:dict) -> go.Figure:
    '''
    Calcula o histórico do orçamento filtrado para algum

    Parâmetros:
    -----------
        1. orcamento {pd.DataFrame}: 
            arquivo com o histórico orçamentário;
        2. args {dict}:
            dicionário com os filtros que serão aplicados no dataset.
  
    Saídas:
    -------
        1. fig {plotly.graph_objects.Figure}:
            figura com o gráfico do histórico do orçamento
    '''

    aux = orcamento.copy()
    aux, valor = filtragem_dataset(aux, args)

    aux = aux.groupby('exercicios').sum().reset_index()

    fig = go.Figure()
    fig.add_trace(go.Scatter(name='Orçamento inicial', x=aux.exercicios, y=aux.orcamento_inicial, mode='lines+markers'))
    fig.add_trace(go.Scatter(name='Orçamento atualizado', x=aux.exercicios, y=aux.orcamento_atualizado, mode='lines+markers'))
    fig.add_trace(go.Scatter(name='Orçamento empenhado', x=aux.exercicios, y=aux.orcamento_empenhado, mode='lines+markers'))
    fig.add_trace(go.Scatter(name='Orçamento realizado', x=aux.exercicios, y=aux.orcamento_realizado, mode='lines+markers'))


    fig.update_layout(title='Orçamento: ' + valor,
                      yaxis_title='Orçamento (em R$)')

    return fig

def composicao_filtro(orcamento:pd.DataFrame, 
                      subdivisao:str, 
                      intervalo:list = [np.datetime64('2014'), np.datetime64('2021')], 
                      *args:dict) -> go.Figure:
    '''
    Calcula a composição média do orçamento por subdivisão

    Parâmetros:
    -----------
        1. orcamento {pd.DataFrame}: 
            arquivo com o histórico orçamentário;
        2. subdivisao {str}:
            variável pelo qual o orçamento será plotado
        3. intervalo {list}:
            intervalo de tempo analisado com as datas em questão
        4. args {dict}:
            dicionário com os filtros que serão aplicados no dataset.

  
    Saídas:
    -------
        1. fig {plotly.graph_objects.Figure}:
            figura com o gráfico da composição do orçamento
    '''

    aux = orcamento.copy()
    aux, valor = filtragem_dataset(aux, args)

    aux = aux[(aux.exercicios >= intervalo[0])&(aux.exercicios <= intervalo[1])]
    aux = aux.groupby([subdivisao, 'exercicios']).sum().reset_index()

    fig = go.Figure()
    if intervalo[0].astype(object).year == intervalo[1].astype(object).year:
        aux2 = aux[aux.exercicios.dt.year == int(np.datetime_as_string(intervalo[1], unit='Y'))]
        fig.add_trace(go.Pie(labels=aux2[subdivisao], values=aux2.orcamento_realizado))
        fig.update_layout(title_text='Orçamento: ' + valor)

    else:        
        data_pivo = intervalo[0]
        while data_pivo <= intervalo[1]:
            aux2 = aux[aux.exercicios.dt.year == int(np.datetime_as_string(data_pivo, unit='Y'))]
            fig.add_trace(go.Bar(x=aux2[subdivisao], y=aux2.orcamento_realizado, name=np.datetime_as_string(data_pivo, unit='Y')))
            data_pivo += np.timedelta64(1,'Y')


        fig.update_yaxes(type="log")
        fig.update_layout(title='Orçamento: ' + valor,
                          yaxis_title='Orçamento (em R$)',
                          xaxis={'categoryorder':'total descending'})

    return fig


def comparacao(orcamento:pd.DataFrame, 
               subdivisao:str, 
               intervalo:list = [np.datetime64('2014'), np.datetime64('2021')], 
               *args:dict) -> go.Figure:
    '''
    Calcula a composição média do orçamento por subdivisão

    Parâmetros:
    -----------
        1. orcamento {pd.DataFrame}: 
            arquivo com o histórico orçamentário;
        2. subdivisao {str}:
            variável pelo qual o orçamento será plotado
        3. intervalo {list}:
            anos a serem comparados
        4. args {dict}:
            dicionário com os filtros que serão aplicados no dataset.

  
    Saídas:
    -------
        1. fig {plotly.graph_objects.Figure}:
            figura com o gráfico da composição do orçamento
    '''

    aux = orcamento.copy()
    aux['orcamento_realizado'] = aux['orcamento_realizado']/1e9
    aux, valor = filtragem_dataset(aux, args)
    aux_total = (aux.groupby(subdivisao).sum()/aux.exercicios.nunique()).reset_index().sort_values('orcamento_realizado', ascending=False).iloc[:5, :].sort_values(subdivisao)

    fig = go.Figure()

    for ano in intervalo:
        aux1 = aux[aux.exercicios.dt.year == int(np.datetime_as_string(ano, unit='Y'))]
        aux1 = aux1[aux1[subdivisao].isin(aux_total[subdivisao])]
        aux1 = aux1.groupby(subdivisao).sum().reset_index().sort_values(subdivisao)
        aux1 = pd.concat((aux1, aux_total.reset_index().rename(columns={'orcamento_realizado': 'media_total'})['media_total']), axis=1)
        
        aux1['orcamento_realizado'] = 100*aux1['orcamento_realizado']/aux1['media_total']
        aux1 = aux1.append(aux1.iloc[0,:]) 


        fig.add_trace(go.Scatterpolar(theta=aux1[subdivisao], r=aux1.orcamento_realizado, fill='toself', name=str(ano)))    
        fig.update_layout(title_text='Orçamento: ' + valor)

    return fig



if __name__ == '__main__':
    orcamento = pd.read_pickle(os.path.join(DATA_PATH_TRATADOS, 'orcamento_tratado.pkl'))
    PIB = pd.read_pickle(os.path.join(DATA_PATH_TRATADOS, 'PIB.pkl'))

    fig1 = historico_orcamento(orcamento, {'nome_orgao_sup':['Ministério da Educação']}, {'nome_orgao_sub':['Fundação Universidade Federal de Uberlândia']})
    fig2 = composicao_filtro(orcamento, 'nome_funcao', [np.datetime64('2014'), np.datetime64('2014')], {'nome_orgao_sup':['Ministério da Educação']})
    fig3 = comparacao(orcamento, 'nome_orgao_sup', [np.datetime64('2014'), np.datetime64('2021')])

    fig1.show()
    fig2.show()
    fig3.show()

