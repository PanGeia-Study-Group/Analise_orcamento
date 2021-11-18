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
path_file = os.path.join(path_entrada, "PLOA2015_incompleta.pdf")

output = PdfFileWriter()
for page in range(15,24):
    input_pdf = PdfFileReader(path_file)
    output.addPage(input_pdf.getPage(page))
    path_split = os.path.join(path_entrada, "PLOA2015_anex.pdf")
with open(path_split, "wb") as output_stream:
    output.write(output_stream)

'''
text = extract_text(path_file, page_numbers=[26]) 
print(text)
'''
#df = tabula.read_pdf(path_file, pages=56)
#print(df[0].columns)
