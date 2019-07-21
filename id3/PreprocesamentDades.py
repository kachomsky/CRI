# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import calculs_generals as cg
import random

def llegirCSVCanviantNaN(path):
    """
    Funcio que llegeix un fitxer CSV i canvia els valor missing (?) per NaN
    """
    data = pd.read_csv(path, na_values=['?'], engine='python', header=None)    
    return data  

def llegirCSV(path):
    """
    Funcio que llegeix un fitxer CSV
    """
    data = pd.read_csv(path)
    return data

def eliminarValorsContinus(data):
    """
    Funcio que elimina els valors continus del dataframe i es queda amb 
    els categorics.
    """
    data = data.select_dtypes(include='object')
    return data

def netejarDadesIncorrectes(data):
    """
    Funcio que elimina les mostres que contenen dades missing.
    """
    print("---- Netejant dades ----")
    data.dropna(inplace=True)
    print("---- S'han eliminar les mostres que contenen NaN ----")    
    return data

def assignarNumColumnaAtribut(header):
    """
    Funcio que asocia a cada un dels atributs quina columna ocupa i viceversa.
    Retorna un diccionari. Ex:
        diccionari_atributs_col: {'Altura':0, 'Edad':1}
        diccionari_col_atribut: {0:'Altura', 1:'Edad'}
    """
    diccionari_atributs_col = {}
    count = 0
    for atribut in header:
        diccionari_atributs_col[atribut] = count
        count += 1
    
    count = 0
    diccionari_col_atribut = {}
    for atribut in header:
        diccionari_col_atribut[count] = atribut
        count += 1
    return diccionari_atributs_col, diccionari_col_atribut

def valorsUnics(data):
    """
    Retorna un diccionari indicant quins son els possibles valors que pot tenir
    cadascun dels atributs. Ex:
        { workclass : ['Private', 'State-gov','Self-emp-not-inc'...], 
          education: ['Bachelors', 'Masters'...] }
    """
    dicc_valors_unics = {}
    mostres = data['mostres'].transpose()
    count = 0
    for mostra in mostres:
        dicc_valors_unics[data['col_atribut'][count]] = list(set(mostra))
        count += 1
    
    return dicc_valors_unics

def clases_positives_negatives(data, atribut_target):
    """
    Funcio que retorna un diccionari amb quants exemplars positius i negatius 
    hi ha en data. Ex:
        {Si : 7, No : 5}
    """
    mostres = data['mostres']
    col_atribut = data['atribut_col'][atribut_target]
    mostres= mostres.transpose()
    clases = {}
    for mostra in mostres[col_atribut]:
        if mostra in clases:
            clases[mostra] += 1
        else:
            clases[mostra] = 1
    return clases

def clases_positives_negatives_target(atribut_target):
    clases = {}
    for mostra in atribut_target:
        if mostra in clases:
            clases[mostra] += 1
        else:
            clases[mostra] = 1
    return clases

def dividirAtributClases(data, atribut):
    """
    Divideix la informacio d'un atribut segons els seus posibles valors. 
    Agafem totes les files de cada posible valor per separat i creem una
    estructura data de cadascuna.
    """
    atribut_clases = {}
    data_rows = data['mostres']
    partition_att_idx = data['atribut_col'][atribut]
    for row in data_rows:
        row_val = row[partition_att_idx]
        if row_val not in atribut_clases.keys():
            atribut_clases[row_val] = {
                'atribut_col': data['atribut_col'],
                'col_atribut': data['col_atribut'],
                'mostres': list()
            }
        atribut_clases[row_val]['mostres'].append(row)
    for valor in atribut_clases.keys():
        atribut_clases[valor]['mostres'] = np.array(atribut_clases[valor]['mostres'])    
    return atribut_clases

def split_data(x, y, train_ratio=0.8):
    indices = np.arange(x.shape[0])
    np.random.shuffle(indices)
    n_train = int(np.floor(x.shape[0]*train_ratio))
    indices_train = indices[:n_train]
    n_val = len(indices) - n_train
    indices_val = indices[-n_val:]
    x_train = x[indices_train, :]
    y_train = y[indices_train]
    x_val = x[indices_val, :]
    y_val = y[indices_val]
    return x_train, y_train, x_val, y_val

def is_number(valor):
    try:
        valor = int(valor)
        return True
    except ValueError:
        return False
    
def etiqueta_majoritaria(etiquetes):
    majoritaria = max(etiquetes, key=lambda k: etiquetes[k])       
    return majoritaria

def particionarData(data, atribut_a_partir):
    return dividirAtributClases(data, atribut_a_partir)

def split_info(data, atribut):
    num_total = len(data['mostres'])
    split_info = cg.entropia(clases_positives_negatives(data, atribut), num_total)    
    return split_info
    
def k_fold_random(data, k):
    particiones_kfold = []    
    for i in range(k):        
        data = list(data)
        random.shuffle(data)    
        #residu = len(data)%k
        tamany_parts = int(len(data)/k)
        data = np.array(data)    
        val_data = data[0:tamany_parts]
        train_data = data[tamany_parts:]
        train_and_validation = [train_data,val_data]
        #train_and_validation.append(val_data)
        particiones_kfold.append(train_and_validation)
    return particiones_kfold
        
def printar_arbre(t, level=0, indent=5):      
    if level > 0:
        prefixed_str = ' ' * (indent * (level - 1)) + '|---'
    else:
        prefixed_str = ''

    if isinstance(t, tuple):
        t = t[0]
    if t.atribut is not None:        
        print(prefixed_str + t.atribut)
        prefixed_str = ' ' * (indent * (level)) + 'O---'
        for fill in t.fills:
            print(prefixed_str + str(fill))
            printar_arbre(t.fills[fill], level+2)
    elif t.etiqueta is not None:        
        print(prefixed_str + t.etiqueta)