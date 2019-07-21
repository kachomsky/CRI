# -*- coding: utf-8 -*-
from collections import Counter
import numpy as np

def split_data(x, y, train_ratio=0.8):
    """
    Divideix el dataset en un conjunt de entrenament i un conjunt de validacio
    """
    indices = np.arange(x.shape[0])
    np.random.shuffle(indices)
    n_train = int(np.floor(x.shape[0]*train_ratio))
    x_train = x[:n_train]
    y_train = y[:n_train]
    x_val = x[n_train:]
    y_val = y[n_train:]
    return x_train, y_train, x_val, y_val

def crearDiccionariPercentatgesClases(clases):
    """
    Crea un diccionari on tenim com a clau 0 o 1, fent referencia 0->negatiu, 1->positiu
    i com a valor el numero total de tweets positius o negatius.
    Ex:
        {0: 1293, 1: 300}
    """
    dicc_count = Counter(clases)
    dicc_percentatges = {}
    total = dicc_count[0] + dicc_count[1]
    dicc_percentatges[0] = dicc_count[0]
    dicc_percentatges[1]= dicc_count[1]
    return dicc_percentatges, total  
    
def crearDiccionariParaules(tweets, labels):
    """
    Crea un diccionari de paraules on tenim com a clau cadascuna de les paraules
    dels tweets i com a valor un altre diccionari, el cual te com a clau 0->negatiu
    1->positiu, indicant cuantes vegades aquesta paraula es negativa o positiva.
    Ex:
        {'hola':{0: 200, 1: 500}}
    """
    #probar con numpy
    diccionari_paraules = {}
    palabras_positivas_totales = 0
    palabras_negativas_totales = 0
    for i in range(len(tweets)): 
        words = tweets[i].split()        
        clase = labels[i]
        for word in words:
            if clase == 0:
                palabras_negativas_totales += 1
            else:
                palabras_positivas_totales += 1
                
            if word in diccionari_paraules:                                
                diccionari_paraules[word][clase] += 1
            else:
                diccionari_paraules[word] = {}
                diccionari_paraules[word][0] = 0
                diccionari_paraules[word][1] = 0
                diccionari_paraules[word][clase] += 1

    return diccionari_paraules, palabras_positivas_totales, palabras_negativas_totales

def eliminar_paraulas_uniques(dicc_paraules):
    """
    Elimina les paraules que nomes surten una vegada en el diccionari.
    """
    keys_eliminar = [k for k,v in dicc_paraules.items() if v[0] == 1 or v[1] == 1]
    for c in keys_eliminar:
        dicc_paraules.pop(c, None)
    return dicc_paraules

def eliminar_meitat_diccionari(dicc_paraules):
    """
    Elimina la meitat de les paraules que surten en el diccionari.
    """
    keys_eliminar = np.array(list(dicc_paraules.keys()))
    n_keys_eliminar = int(len(keys_eliminar)/2)
    keys_eliminar = keys_eliminar[:n_keys_eliminar]
    for c in keys_eliminar:
        dicc_paraules.pop(c, None)
    return dicc_paraules

def eliminar_quart_diccionari(dicc_paraules):
    """
    Elimina un quart de les paraules que surten en el diccionari.
    """
    keys_eliminar = np.array(list(dicc_paraules.keys()))
    n_keys_eliminar = int(len(keys_eliminar)/4)
    keys_eliminar = keys_eliminar[:n_keys_eliminar]
    for c in keys_eliminar:
        dicc_paraules.pop(c, None)
    return dicc_paraules
