import os,sys
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go

sys.path.append('..\\..')
DATA_PATH_TRATADOS = "../../dados/2_dados_tratados"

def historico_orcamento(orcamento):
    aux = orcamento.groupby('exercicios').sum().reset_index()
    aux.iloc[:, 1:] = aux.iloc[:, 1:]/1e9

    fig = go.Figure()
    fig.add_trace(go.Scatter(name='Orçamento inicial', x=aux.exercicios, y=aux.orcamento_inicial, mode='lines'))
    fig.add_trace(go.Scatter(name='Orçamento atualizado', x=aux.exercicios, y=aux.orcamento_atualizado, mode='lines'))
    fig.add_trace(go.Scatter(name='Orçamento empenhado', x=aux.exercicios, y=aux.orcamento_empenhado, mode='lines'))
    fig.add_trace(go.Scatter(name='Orçamento realizado', x=aux.exercicios, y=aux.orcamento_realizado, mode='lines'))


    fig.update_layout(title='Orçamento brasileiro de 2014 a 2021',
                      yaxis_title='Orçamento (em R$ trilhões)')

    return fig

if __name__ == '__main__':
    orcamento = pd.read_pickle(os.path.join(DATA_PATH_TRATADOS, 'orcamento_tratado.pkl'))
    PIB = pd.read_pickle(os.path.join(DATA_PATH_TRATADOS, 'PIB.pkl'))

    fig = historico_orcamento(orcamento)
    fig.show()