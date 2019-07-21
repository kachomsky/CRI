# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import time
import procesament_dades as prd
import clasificador as cl

def main():
    start = time.time()
    print("** Carregant dades **\n\n")
    path = "Sentiment-Analysis-Dataset/"
    file = "FinalStemmedSentimentAnalysisDataset.csv"  
    dataset = pd.read_csv(path + file, sep=";")
    dataset = dataset.dropna()
    tweets = np.array(dataset['tweetText'])
    labels = np.array(dataset['sentimentLabel'])    
    opcio = 2
    print("===== Selecciona la opcio =====")
    print("\t1. Sense aplicar Laplace Smoothing")
    print("\t2. Aplicant Laplace Smoothing")
    opcio = input("Opcio:")
    
    #Holdout 80% training 20% test
    if opcio == '1':    
        #Sense utilitzar laplace
        print(" *** Executant sense aplicar laplace amb holdout T80% V20% ***")
        x_train, y_train, x_val, y_val = prd.split_data(tweets, labels, 0.8) #per defecte 0.8 de train
        clases = dataset["sentimentLabel"]
        dicc_percent, total = prd.crearDiccionariPercentatgesClases(clases)   
        dicc_paraules, positivos_totales, negativas_totales = prd.crearDiccionariParaules(x_train, y_train)        
        y_predicted = cl.predict_sense_laplace(x_val, dicc_percent, dicc_paraules)        
        cl.validar(y_predicted, y_val)
    
    if opcio == '2':
        #Utilitzant laplace
        print(" *** Executant aplicant laplace amb holdout T80% V20% ***")
        x_train, y_train, x_val, y_val = prd.split_data(tweets, labels,0.8) #per defecte 0.8 de train
        clases = dataset["sentimentLabel"]
        dicc_percent, total = prd.crearDiccionariPercentatgesClases(clases)                      
        dicc_paraules, positivos_totales, negativas_totales = prd.crearDiccionariParaules(x_train, y_train)
        #Descomentar linia de a sota per eliminar paraules de diccionari.
        #dicc_paraules = eliminar_paraulas_uniques(dicc_paraules)
        y_predicted = cl.predict_laplace(x_val, dicc_percent, dicc_paraules, positivos_totales, negativas_totales)        
        cl.validar(y_predicted, y_val)
                
    end = time.time()
    print(str(end - start) + " seconds")


if __name__ == "__main__":
    main()