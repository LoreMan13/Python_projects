'''
FEITO NO VSCODE JUPYTER NOTEBOOK
Autor: Gustavo Henrique de Souza Cavalcante
Data: 15/01/2025
Instituição: ETEC Presidente Vargas
Link da base de dados: https://drive.google.com/file/d/1182KDE9aqoyhWruD45leq3D1RhUm4M6i/view?usp=sharing
Cada %% representa uma nova célula no notebook
'''
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import copy as cp
#Importação das bibliotecas iniciais

# %%
#Criação do dataset
dataset = pd.read_csv('cancelamentos.csv')
display(dataset)

# %%
#Tratamento dos dados
dataset_tratado = dataset.dropna()

#Agregação de dados em faixas de valores
dataset_tratado['tempo_como_cliente'] = pd.cut(
    dataset_tratado['tempo_como_cliente'], 
    bins = 10,     
    labels=['1-6', '6 - 12', '12 - 18', '18 - 24', '24 - 30', 
            '30 - 36', '36 - 42', '42 - 48', '48 - 54', '54 - 60'] #anos
    )

dataset_tratado['dias_atraso'] = pd.cut(
        dataset_tratado['dias_atraso'], 
        bins = 10,
        labels=['0-3 dias', '3-6 dias', '6-9 dias', '9-12 dias', '12-15 dias', 
                '15-18 dias', '18-21 dias', '21-24 dias', '24-27 dias', '27-30 dias']
        )

dataset_tratado['total_gasto'] = pd.cut(
        dataset_tratado['total_gasto'], 
        bins = 10,
        labels=['0-100 R$', '100-200 R$', '200-300 R$', '300-400 R$', '400-500 R$', 
                '500-600 R$', '600-700 R$', '700-800 R$', '800-900 R$', '900-1000 R$']
        )
display(dataset_tratado)

# %%
#Análise dos dados
cancelamentos_prop = display(dataset_tratado['cancelou'].value_counts(normalize = True).map("{:.2%}".format))  
cancelamentos_brut = display(dataset_tratado['cancelou'].value_counts())
#duracao_crt_prop = display(dataset_tratado.groupby('duracao_contrato').median(numeric_only = True).sort_values(by = 'duracao_contrato', ascending = True)) 

#transofrmação da variável categórica em numérica
prop_canXdur = dataset_tratado.groupby(['duracao_contrato', 'cancelou']).size().unstack(fill_value=0)
display(prop_canXdur)

prop_canXtmc = dataset_tratado.groupby(['tempo_como_cliente', 'cancelou']).size().unstack(fill_value = 0)
display(prop_canXtmc)

prop_canXlig = dataset_tratado.groupby(['ligacoes_callcenter', 'cancelou']).size().unstack(fill_value = 0)
display(prop_canXlig)

prop_canXdia = dataset_tratado.groupby(['dias_atraso', 'cancelou']).size().unstack(fill_value = 0)
display(prop_canXdia)

prop_canXass = dataset_tratado.groupby(['assinatura', 'cancelou']).size().unstack(fill_value = 0)
display(prop_canXass)

prop_gstXcan = dataset_tratado.groupby(['total_gasto', 'cancelou']).size().unstack(fill_value = 0)
display(prop_gstXcan)

# %%
#visualização dos dados
fig, axes = plt.subplots(2, 3, figsize = (22, 12))
fig.suptitle('Análise dos cancelamentos', fontsize = 20)

#Gráfico de histograma de cancelamentos
prop_canXdur.plot(
    kind='bar',
    stacked=True,
    color=['blue', 'red'],
    edgecolor='black',
    ax=axes[1, 0]
)
axes[0, 0].set_xlabel('Duração do Contrato')
axes[0, 0].set_ylabel('Número de Cancelamentos')

prop_canXtmc.plot(
    kind='bar',
    stacked=True,
    color=['purple', 'white'],
    edgecolor='black',
    ax=axes[0, 1]
)
axes[0, 1].set_xlabel('Tempo como Cliente')
axes[0, 1].set_ylabel('Número de Cancelamentos')

prop_canXlig.plot(
    kind='bar',
    stacked=True,
    color=['green', 'yellow'],
    edgecolor='black',
    ax=axes[0, 2]
)
axes[0, 2].set_xlabel('Ligações ao Call Center')
axes[0, 2].set_ylabel('Número de Cancelamentos')

prop_canXdia.plot(
    kind='barh',
    stacked=True,
    color=['orange', 'black'],
    edgecolor='black',
    ax=axes[0, 0]
)
axes[1, 0].set_xlabel('Número de Cancelamentos')
axes[1, 0].set_ylabel('Dias de Atraso')

prop_canXass.plot(
    kind='bar',
    stacked=True,
    color=['pink', 'brown'],
    edgecolor='black',
    ax=axes[1, 1]
)
axes[1, 1].set_xlabel('Assinatura')
axes[1, 1].set_ylabel('Número de Cancelamentos')

prop_gstXcan.plot(
    kind='bar',
    stacked=True,
    color=['gray', 'blue'],
    edgecolor='black',
    ax=axes[1, 2]
)
axes[1, 2].set_xlabel('Total Gasto')
axes[1, 2].set_ylabel('Número de Cancelamentos')

#salvar a imagem

plt.savefig("analise_cancelamentos.jpg", format="jpg", dpi=300)  # Define o formato e a resolução


