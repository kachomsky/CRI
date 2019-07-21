# -*- coding: utf-8 -*-
import PreprocesamentDades as proc_d
import math
import numpy as np

def info_gain_calc(data, particions_atribut, target_attribute):
    gain = 0
    data_rows = data['mostres']
    n = len(data_rows)             
    for clase_atribut in particions_atribut.keys():
        data_particionada = particions_atribut[clase_atribut]
        partition_n = len(data_particionada['mostres'])   
        etiquetes_particio = proc_d.clases_positives_negatives(data_particionada, target_attribute)
        entropia_particio = entropia(etiquetes_particio ,partition_n)
        gain += partition_n / n * entropia_particio

    return gain

def info_gain_continua(data, splits_mid_points, split_etiquetes):
    n = len(data)
    count = 0
    gain = 0
    for clase_atribut in splits_mid_points:
        partition_n = len(clase_atribut)
        etiquetes_particio = proc_d.clases_positives_negatives_target(split_etiquetes[count])        
        count += 1
        entropia_particio = entropia(etiquetes_particio ,partition_n)
        gain += partition_n / n * entropia_particio
    return gain

def entropia(clases, num_total):
    entropia = 0    
    for clase in clases.keys():
        porcentaje = clases[clase]/num_total
        entropia += - porcentaje * math.log(porcentaje, 2)
    return entropia

def prediccio(mostra, arbre, dicc_atr_col):
    if isinstance(arbre, tuple):
        arbre = arbre[0]
    if arbre.atribut in dicc_atr_col:        
        col_atr_root = dicc_atr_col[arbre.atribut]          
    
    if arbre.etiqueta is not None:        
        return arbre.etiqueta
    elif arbre.atribut is not None:
        for fill in arbre.fills: 
            #print("***************")
            #print(mostra)
            #print(mostra[col_atr_root])            
            return prediccio(mostra, arbre.fills[mostra[col_atr_root]], dicc_atr_col)

def true_false_positive_and_negative(prediccions, y_val, clase_positiva, clase_negativa):        
    prediccions = np.asarray(prediccions)
    y_val = np.asarray(y_val)

    TP = int(np.sum(np.logical_and(prediccions == clase_positiva, y_val == clase_positiva)))
    TN = int(np.sum(np.logical_and(prediccions == clase_negativa, y_val == clase_negativa)))
    FP = int(np.sum(np.logical_and(prediccions == clase_positiva, y_val == clase_negativa)))
    FN = int(np.sum(np.logical_and(prediccions == clase_negativa, y_val == clase_positiva)))
     
    return TP, TN, FP, FN

def accuracy(TP, TN, FP, FN):
    if (TP+TN+FP+FN) != 0:
        return ((TP + TN)/(TP+TN+FP+FN))*100
    else:
        #print("\nEl denominador per accuracy es cero")
        return 0

def precision(TP, FP):
    if (TP+FP) != 0:
        return (TP/(TP+FP))*100
    else:
        #print("\nEl denominador per precision es cero")
        return 0

def recall(TP, FN):
    if (TP+FN) != 0:
        return (TP/(TP+FN))*100
    else:
        #print("\nEl denominador per recall es cero")
        return 0

def specifity(TN, FP):
    if (TN+FP) != 0:
        return (TN/(TN+FP))*100
    else:
        #print("\nEl denominador de specifity es cero")
        return 0

def f1_score(precision, recall):
    if (precision + recall) != 0:
        return 2*precision*recall/(precision + recall)
    else:
        #print("\nEl denominador de f1 score es cero")
        return 0

def printar_mesures(accuracy_result, precision_result, recall_result, specifity_result,f1score):
    print("\n=====================")
    print("Accuracy")
    print(accuracy_result)
    print("Precision")
    print(precision_result)
    print("Recall")
    print(recall_result)
    print("Specifity:")
    print(specifity_result)
    print("F1 score:")
    print(f1score)        
    print("=====================")

def calcular_mesures(TP, FP, FN, TN):
    precision_result = precision(TP, FP)
    recall_result = recall(TP, FN)
    accuracy_result = accuracy(TP, TN, FP, FN)
    specifity_result = specifity(TN, FP)
    f1score = f1_score(precision_result, recall_result)
    return accuracy_result, precision_result, recall_result, specifity_result, f1score

def afegir_mesures_diccionari(dicc_mesures, accuracy_result, precision_result, recall_result, specifity_result, f1score):
    dicc_mesures['accuracy'].append(accuracy_result)
    dicc_mesures['precision'].append(precision_result)
    dicc_mesures['recall'].append(recall_result)
    dicc_mesures['specifity'].append(specifity_result)
    dicc_mesures['f1score'].append(f1score)
    return dicc_mesures

def calcular_mitjana_mesures(dicc_mesures):
    accuracy = np.mean(np.array(dicc_mesures['accuracy']))
    precision = np.mean(np.array(dicc_mesures['precision']))
    recall = np.mean(np.array(dicc_mesures['recall']))
    specifity = np.mean(np.array(dicc_mesures['specifity']))
    f1score = np.mean(np.array(dicc_mesures['f1score']))
    
    return accuracy,precision,recall,specifity,f1score
    

def calcular_mid_points(train_data, atribut, target):          
    train_data['mostres'] = train_data['mostres'][train_data['mostres'][:,train_data["atribut_col"][atribut]].argsort()][:]
    etiquetes = train_data["mostres"].transpose()[train_data["atribut_col"][target]][:]
    #etiquetes = list(etiquetes)
    valors_atribut = train_data["mostres"].transpose()[train_data["atribut_col"][atribut]][:]    
    valors_atribut = sorted(valors_atribut)
    num_total = len(valors_atribut)
    mid_points = []
    for i in range(0, num_total-1):
        if etiquetes[i] != etiquetes[i+1]:
            mid_points.append((valors_atribut[i] + valors_atribut[i+1])/2)
    info_gains = []
    #print(type(valors_atribut))
    valors_atribut = np.array(valors_atribut)
    
    for mid_point in mid_points:
        #info_gains.append(info_gain_continuous(train_data["mostres"], mid_point, valors_atribut, etiquetes))        
        b1 = valors_atribut[np.where(valors_atribut > mid_point)]
        b2 = valors_atribut[np.where(valors_atribut <= mid_point)]
        etiquetes_b1 = etiquetes[np.where(valors_atribut > mid_point)] 
        etiquetes_b2 = etiquetes[np.where(valors_atribut <= mid_point)] 
        split_mid_points = [b1, b2]
        split_etiquetes = [etiquetes_b1, etiquetes_b2]
        gain = info_gain_continua(valors_atribut,split_mid_points,split_etiquetes)
        info_gains.append(gain)
    
    maxInfoGain = max(info_gains)    
    index_mid_point = info_gains.index(maxInfoGain)    
    valor_c = mid_points[index_mid_point]
    return maxInfoGain, valor_c
    

  

def canviar_continuus_split(data, atribut, x_val):
    valors_atr = data["mostres"].transpose()[data["atribut_col"][atribut]]
    x_val_atr = x_val.transpose()[data["atribut_col"][atribut]]
    if proc_d.is_number(x_val_atr[0]):
        #print(x_val_atr)
        valor_llindar = valors_atr[0].split(" ")[1]
        #print(valor_llindar)
        i = 0        
        for valor in x_val_atr:
            if float(valor) > float(valor_llindar):
                x_val_atr[i] = '> '+str(valor_llindar)
            if float(valor) <= float(valor_llindar):
                x_val_atr[i] = '<= '+str(valor_llindar)
            i+=1
        x_val.transpose()[data["atribut_col"][atribut]] = x_val_atr
    
    return x_val
