# -*- coding: utf-8 -*-
import numpy as np
def true_false_positive_and_negative(prediccions, y_val, clase_positiva, clase_negativa): 
    """
    Calcula la matriu de confusio
    """       
    prediccions = np.asarray(prediccions)
    y_val = np.asarray(y_val)

    TP = int(np.sum(np.logical_and(prediccions == clase_positiva, y_val == clase_positiva)))
    TN = int(np.sum(np.logical_and(prediccions == clase_negativa, y_val == clase_negativa)))
    FP = int(np.sum(np.logical_and(prediccions == clase_positiva, y_val == clase_negativa)))
    FN = int(np.sum(np.logical_and(prediccions == clase_negativa, y_val == clase_positiva)))
     
    return TP, TN, FP, FN

def accuracy(TP, TN, FP, FN):
    """
    Calcula el accuracy
    """
    if (TP+TN+FP+FN) != 0:
        return ((TP + TN)/(TP+TN+FP+FN))*100
    else:
        #print("\nEl denominador per accuracy es cero")
        return 0

def precision(TP, FP):
    """
    Calcula la precision
    """
    if (TP+FP) != 0:
        return (TP/(TP+FP))*100
    else:
        #print("\nEl denominador per precision es cero")
        return 0

def recall(TP, FN):
    """
    Calcula el recall
    """
    if (TP+FN) != 0:
        return (TP/(TP+FN))*100
    else:
        #print("\nEl denominador per recall es cero")
        return 0

def specifity(TN, FP):
    """
    Calcula specifity
    """
    if (TN+FP) != 0:
        return (TN/(TN+FP))*100
    else:
        #print("\nEl denominador de specifity es cero")
        return 0

def f1_score(precision, recall):
    """
    Calcula el f1 score
    """
    if (precision + recall) != 0:
        return 2*precision*recall/(precision + recall)
    else:
        #print("\nEl denominador de f1 score es cero")
        return 0

def printar_mesures(accuracy_result, precision_result, recall_result, specifity_result,f1score):
    """
    Printa les diferentes mesures de manera que es puguin llegir facilment
    """
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
    """
    Crida a totes les funcions de les diferents medides per calcularles en una unica funcio
    """
    precision_result = precision(TP, FP)
    recall_result = recall(TP, FN)
    accuracy_result = accuracy(TP, TN, FP, FN)
    specifity_result = specifity(TN, FP)
    f1score_result = f1_score(precision_result, recall_result)
    return accuracy_result, precision_result, recall_result, specifity_result, f1score_result
