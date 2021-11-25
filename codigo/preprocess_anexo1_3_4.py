import os
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from tqdm import tqdm
from pdfminer.high_level import extract_text
import tabula
from PyPDF2 import PdfFileWriter, PdfFileReader

import re
import pickle

import warnings
#warnings.filterwarnings("ignore", 'This pattern has match groups')

# Para rodar no linux, é necessário tirar a barra do começo do path por lagum motivo

# Pasta com os arquivos que serão processados
path_entrada = "dados/1_dados_entrada"
# Pasta com os arquivos após o processamento
path_tratados = "dados/2_dados_tratados"
exemplo = os.path.join(path_entrada, "PLOA2015_anex.pdf")

# Arquivos de cada ano, e as respectivas páginas em cada arquivo
dic_ano_pag = {2015: [1, 4, 5], 2016: [1, 4, 5], 2017: [1, 3, 4],
               2018: [1, 3, 4], 2019: [1, 3, 4], 2020: [], 2021: [], 2022: []}

# Selecionar as páginas referentes aos anexos 1,3 e 4
text = extract_text(exemplo, page_numbers=[4])
print(text)

# Processar os dados de todos os anos disponíveis, colocar em um pandas.DataFrame e salvar em arquivos pickle (.pkl)
