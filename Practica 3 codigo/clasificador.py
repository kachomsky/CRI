# -*- coding: utf-8 -*-
import math
import calculs_mesures as cm

def predict_laplace(tweets, dicc_percent, dicc_paraules, positivas_totales, negativas_totales):
    """
    Fa una prediccio aplicant laplace en la classificacio.
    """        
    y_predicted = []
    
    for tweet in tweets:
        y_predicted.append(classificar(tweet, dicc_percent, dicc_paraules, positivas_totales, negativas_totales))
    
    return y_predicted

def predict_sense_laplace(tweets, dicc_percent, dicc_paraules):
    """
    Fa una prediccio sense aplicar laplace en la classificacio.
    """
    y_predicted = []
    
    for tweet in tweets:
        y_predicted.append(classificar_sense_laplace(tweet, dicc_percent, dicc_paraules))
    
    return y_predicted
    
def validar(y_predicted, y_correcte):
    """
    Valida amb diferents mesures com de bona ha sigut la prediccio.
    """
    TP, TN, FP, FN = cm.true_false_positive_and_negative(y_predicted, y_correcte, 1, 0)
    accuracy_result, precision_result, recall_result, specifity_result, f1score_result = cm.calcular_mesures(TP, FP, FN, TN)
    cm.printar_mesures(accuracy_result, precision_result, recall_result, specifity_result, f1score_result)

def classificar_sense_laplace(tweet, dicc_percent, dicc_paraules):
    """
    Realitza la classificacio de un tweet sense aplicar laplace.
    """
    productori_negatiu = 1
    productori_positiu = 1
    prob_pos = dicc_percent[1]/(dicc_percent[0] + dicc_percent[1])
    prob_neg = dicc_percent[0]/(dicc_percent[0] + dicc_percent[1])
    
    for word in tweet.split():
        if word in dicc_paraules:
            productori_negatiu *= (dicc_paraules[word][0]/dicc_percent[0])
            productori_positiu *= (dicc_paraules[word][1]/dicc_percent[1])                            

    prob_tweet_pos = prob_pos*productori_positiu
    prob_tweet_neg = prob_neg*productori_negatiu
    
    if prob_tweet_pos > prob_tweet_neg:
        return 1
    else:
        return 0

def classificar(tweet, dicc_percent, dicc_paraules, positivas_totales, negativas_totales):
    """
    Realitza la classificacio de un tweet aplicant laplace.
    """
    prob_pos = math.log(dicc_percent[1]/(dicc_percent[0] + dicc_percent[1]))
    prob_neg = math.log(dicc_percent[0]/(dicc_percent[0] + dicc_percent[1]))
    for word in tweet.split():
        if word not in dicc_paraules:
            prob_neg += math.log(1/float(negativas_totales + 1*(positivas_totales+negativas_totales)))
            prob_pos += math.log(1/float(positivas_totales + 1*(positivas_totales+negativas_totales)))

        else:
            prob_neg += math.log((dicc_paraules[word][0] + 1) / float(negativas_totales + 1*(positivas_totales+negativas_totales)))
            prob_pos += math.log((dicc_paraules[word][1] + 1) / float(positivas_totales + 1*(positivas_totales+negativas_totales)))                    
            
    if prob_pos > prob_neg:
        return 1
    else:
        return 0
