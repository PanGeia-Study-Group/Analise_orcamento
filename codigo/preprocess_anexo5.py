import os,sys
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

path_entrada = "../dados/1_dados_entrada"
exemplo = os.path.join(path_entrada, "PLOA2015_anex.pdf")

# Selecionar as páginas em que estão a tabela do anexo 2
list_dfs = tabula.read_pdf(exemplo, pages=[6,7,8,9]) # Lista com as tabelas encontradas nas páginas selecionadas

print(len(list_dfs))

# Processar os dados de todos os anos disponíveis, colocar em um pandas.DataFrame e salvar em arquivos pickle (.pkl)