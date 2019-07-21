# -*- coding: utf-8 -*-

import PreprocesamentDades as proc_d
import numpy as np
import calculs_generals as cg
import id3_arbres
import c45_arbres

def main():    
    print("====   ESCOLLIR NIVELL   ====")
    nivell = input("1. Nivell C: id3 i C4.5\n2. Nivell B: Tractament de dades continues\n3. Nivell A: Tractament missings\n")    
    print("\t====   Escollir tipus arbre ====")
    tipus_arbre = input("\t 1. id3 \n\t 2. C4.5\n")
    
    tipus_arbre = '2'
    nivell = '2'
    base_dades = '1'
    
    if (tipus_arbre == '1' or tipus_arbre == '2') and nivell == '1':
        print("\t====   Escollir tamany base dades ====")
        base_dades = input("\t 1. Gran (Mushroom) \n\t 2. Petita (Jugar tennis)\n")
        if base_dades == '1':
            path = "agaricus-lepiota.csv"
            dataframe = proc_d.llegirCSVCanviantNaN(path)
            dataframe = proc_d.netejarDadesIncorrectes(dataframe)
            header = ["classes","cap-shape","cap-surface","cap-color","bruises",
                      "odor","gill-attachment","gill-spacing","gill-size",
                      "gill-color","stalk-shape","stalk-root","stalk-surface-above-ring",
                      "stalk-surface-below-ring","stalk-color-above-ring","stalk-color-below-ring",
                      "veil-type","veil-color","ring-number","ring-type","spore-print-color",
                      "population","habitat"]
            mostres = dataframe.iloc[:, 0:].values
            y = dataframe.iloc[:,0].values            
            #x_train, y_train, x_val, y_val = proc_d.split_data(mostres, y, 0.8)        
            data = {}
            data['header'] = header
            #data['mostres'] = x_train    
            atribut_target = header[0]
            dicc_atr_col, dicc_col_atr = proc_d.assignarNumColumnaAtribut(header)
            data['atribut_col'] = dicc_atr_col
            data['col_atribut'] = dicc_col_atr                    
            atributs_restants = header[1:]
        if base_dades == '2':
            path = "dataset.csv"
            dataframe = proc_d.llegirCSV(path)
            dataframe = proc_d.netejarDadesIncorrectes(dataframe)
            header = list(dataframe)
            header.pop(0)
            mostres = dataframe.iloc[:, 1:].values        
            y = dataframe.iloc[:,-1].values            
            #x_train, y_train, x_val, y_val = proc_d.split_data(mostres, y, 0.8)        
            data = {}
            data['header'] = header
            #data['mostres'] = x_train    
            atribut_target = header[-1]
            dicc_atr_col, dicc_col_atr = proc_d.assignarNumColumnaAtribut(header)
            data['atribut_col'] = dicc_atr_col
            data['col_atribut'] = dicc_col_atr                    
            atributs_restants = header[:-1]
        
        percentatges_training = [0.5, 0.7, 0.8]
        
        for percentatge in percentatges_training:
            x_train, y_train, x_val, y_val = proc_d.split_data(mostres, y, percentatge)        
            data['mostres'] = x_train             
            valors_unics_atributs = proc_d.valorsUnics(data)            
            if tipus_arbre == '1':
                node_root = id3_arbres.id3(data, valors_unics_atributs, atributs_restants, atribut_target)
            if tipus_arbre == '2':
                node_root = c45_arbres.c45(data, valors_unics_atributs, atributs_restants, atribut_target)
            
            prediccions = []
            
            for mostra in x_val:            
                prediccions.append(cg.prediccio(mostra, node_root, dicc_atr_col))
                    
            if base_dades == '1':
                TP, TN, FP, FN = cg.true_false_positive_and_negative(prediccions, y_val, 'e', 'p')       
            if base_dades == '2':
                TP, TN, FP, FN = cg.true_false_positive_and_negative(prediccions, y_val, 'Si', 'No')       
            accuracy_result, precision_result, recall_result, specifity_result, f1score = cg.calcular_mesures(TP,FP,FN,TN)
            print("\nMesures HoldOut "+str(percentatge) +" training:")
            cg.printar_mesures(accuracy_result, precision_result, recall_result, specifity_result, f1score)
                        
        proc_d.printar_arbre(node_root)
        #K-Fold
        parts_kfold = proc_d.k_fold_random(mostres, 6)
        dicc_mesures = {'accuracy':[], 'precision':[], 'recall':[], 'specifity':[], 'f1score':[]}
        
        for part in parts_kfold:
            prediccions = []
            data['mostres'] = part[1]
            if tipus_arbre == '1':
                node_root = id3_arbres.id3(data, valors_unics_atributs, atributs_restants, atribut_target)
            if tipus_arbre == '2':
                node_root = c45_arbres.c45(data, valors_unics_atributs, atributs_restants, atribut_target)
            y_val = part[0].transpose()[0]            
            for mostra in part[0]:            
                prediccions.append(cg.prediccio(mostra, node_root, dicc_atr_col))
            if base_dades == '1':                
                TP, TN, FP, FN = cg.true_false_positive_and_negative(prediccions, y_val, 'e', 'p')       
            if base_dades == '2':
                TP, TN, FP, FN = cg.true_false_positive_and_negative(prediccions, y_val, 'Si', 'No')       
            accuracy_result, precision_result, recall_result, specifity_result, f1score = cg.calcular_mesures(TP,FP,FN,TN)
            dicc_mesures = cg.afegir_mesures_diccionari(dicc_mesures, accuracy_result, precision_result, recall_result, specifity_result, f1score)
        accuracy_result, precision_result, recall_result, specifity_result, f1score = cg.calcular_mitjana_mesures(dicc_mesures)
        print("\nMesures K-Fold:")
        cg.printar_mesures(accuracy_result, precision_result, recall_result, specifity_result, f1score)
    
    if (tipus_arbre == '1' or tipus_arbre == '2') and nivell == '2':    
        path = "adult.csv"
        dataframe = proc_d.llegirCSVCanviantNaN(path)
        dataframe = proc_d.netejarDadesIncorrectes(dataframe)
        header = ["age","workclass","fnlwgt","education","education-num",
                  "marital-status","occupation","relationship",
                  "race","sex","capital-gain","capital-loss","hours-per-week",
                  "native-country","over50K"]
        mostres = dataframe.iloc[:, 0:].values  
        y = dataframe.iloc[:,-1].values
        atribut_target = header[-1]        
        data = {}
        data['header'] = header
        dicc_atr_col, dicc_col_atr = proc_d.assignarNumColumnaAtribut(header)
        data['atribut_col'] = dicc_atr_col
        data['col_atribut'] = dicc_col_atr
        atributs_restants = header[:-1]  
        
        percentatges_training = [0.5, 0.7, 0.8]
        
        for percentatge in percentatges_training:
            x_train, y_train, x_val, y_val = proc_d.split_data(mostres, y, percentatge)        
            data['mostres'] = x_train             
            valors_unics_atributs = proc_d.valorsUnics(data)            
            if tipus_arbre == '1':
                node_root = id3_arbres.id3_dades_continues(data, valors_unics_atributs, atributs_restants, atribut_target)
            if tipus_arbre == '2':
                node_root = c45_arbres.c45_dades_continues(data, valors_unics_atributs, atributs_restants, atribut_target)
            
            for atribut in atributs_restants:
                x_val = cg.canviar_continuus_split(data, atribut, x_val)[:]
            
            prediccions = []
            
            for mostra in x_val:            
                prediccions.append(cg.prediccio(mostra, node_root, dicc_atr_col))
                    
            TP, TN, FP, FN = cg.true_false_positive_and_negative(prediccions, y_val, '>50K', '<=50K')       
            accuracy_result, precision_result, recall_result, specifity_result, f1score = cg.calcular_mesures(TP,FP,FN,TN)
            print("\nMesures HoldOut "+str(percentatge) +" training:")
            cg.printar_mesures(accuracy_result, precision_result, recall_result, specifity_result, f1score)
        proc_d.printar_arbre(node_root)
        
        """valors_unics_atributs = proc_d.valorsUnics(data)           
        print("Creant arbre...")
        if tipus_arbre == '1':
                node_root = id3_arbres.id3_dades_continues(data, valors_unics_atributs, atributs_restants, atribut_target)
        if tipus_arbre == '2':
            node_root = c45_arbres.c45_dades_continues(data, valors_unics_atributs, atributs_restants, atribut_target)
        #proc_d.printar_arbre(node_root)
        for atribut in atributs_restants:
            x_val = cg.canviar_continuus_split(data, atribut, x_val)[:]
        
        prediccions = []
        
        for mostra in x_val:            
            prediccions.append(cg.prediccio(mostra, node_root, dicc_atr_col))
        
        TP, TN, FP, FN = cg.true_false_positive_and_negative(prediccions, y_val, '>50K', '<=50K')       
        accuracy_result, precision_result, recall_result, specifity_result, f1score = cg.calcular_mesures(TP,FP,FN,TN)
        print("\nMesures HoldOut 80% training 20% validacio:")
        cg.printar_mesures(accuracy_result, precision_result, recall_result, specifity_result, f1score)"""
        
        #K-fold
        #parts_kfold = proc_d.k_fold_random(mostres, 3)
        #dicc_mesures = {'accuracy':[], 'precision':[], 'recall':[], 'specifity':[], 'f1score':[]}
        #print(parts_kfold)"""
        
        """for part in parts_kfold:
            prediccions = []
            data['mostres'] = part[1]
            node_root,data = id3_dades_continues(data, valors_unics_atributs, atributs_restants, atribut_target)
            for atribut in atributs_restants:
                part[0] = canviar_continuus_split(data, atribut, part[0])[:]
            y_val = part[0].transpose()[0]                                   
            for mostra in part[0]:            
                #print(mostra)
                prediccions.append(prediccio(mostra, node_root, dicc_atr_col))
            TP, TN, FP, FN = true_false_positive_and_negative(prediccions, y_val, '>50K', '<=50K')       
            accuracy_result, precision_result, recall_result, specifity_result, f1score = calcular_mesures(TP,FP,FN,TN)
            dicc_mesures = afegir_mesures_diccionari(dicc_mesures, accuracy_result, precision_result, recall_result, specifity_result, f1score)
        accuracy_result, precision_result, recall_result, specifity_result, f1score = calcular_mitjana_mesures(dicc_mesures)
        print("\nMesures K-Fold:")
        printar_mesures(accuracy_result, precision_result, recall_result, specifity_result, f1score)"""
        
        """node_root = id3_2(data, valors_unics_atributs, atributs_restants, atribut_target)
        printar_arbre(node_root)
        
        prediccions = []
        
        for mostra in x_val:            
            prediccions.append(prediccio(mostra, node_root, dicc_atr_col))
        
        TP, TN, FP, FN = true_false_positive_and_negative(prediccions, y_val, '>50K', '<=50K')       
        accuracy_result, precision_result, recall_result, specifity_result, f1score = calcular_mesures(TP,FP,FN,TN)
        print("\nMesures HoldOut 80% training 20% validacio:")
        printar_mesures(accuracy_result, precision_result, recall_result, specifity_result, f1score)"""                   
        #K-Fold
        """parts_kfold = k_fold_random(mostres, 3)
        dicc_mesures = {'accuracy':[], 'precision':[], 'recall':[], 'specifity':[], 'f1score':[]}
        
        for part in parts_kfold:
            prediccions = []
            data['mostres'] = part[1]
            node_root = id3(data, valors_unics_atributs, atributs_restants, atribut_target)
            y_val = part[0].transpose()[0]            
            for mostra in part[0]:            
                prediccions.append(prediccio(mostra, node_root, dicc_atr_col))
            TP, TN, FP, FN = true_false_positive_and_negative(prediccions, y_val, 'e', 'p')       
            accuracy_result, precision_result, recall_result, specifity_result, f1score = calcular_mesures(TP,FP,FN,TN)
            dicc_mesures = afegir_mesures_diccionari(dicc_mesures, accuracy_result, precision_result, recall_result, specifity_result, f1score)
        accuracy_result, precision_result, recall_result, specifity_result, f1score = calcular_mitjana_mesures(dicc_mesures)
        print("\nMesures K-Fold:")
        printar_mesures(accuracy_result, precision_result, recall_result, specifity_result, f1score)"""
        
        #Leave One Out
        """dicc_mesures = {'accuracy':[], 'precision':[], 'recall':[], 'specifity':[], 'f1score':[]}
        for i in range(0,len(mostres)):
            prediccions = []            
            mostres_train = mostres[:]
            x_val = mostres_train[i]
            x_train = np.delete(mostres_train,i,0)
            data['mostres'] = x_train
            y_val = x_val.transpose()[0]  
            node_root = id3(data, valors_unics_atributs, atributs_restants, atribut_target)
            prediccions.append(prediccio(x_val, node_root, dicc_atr_col))            
            TP, TN, FP, FN = true_false_positive_and_negative(prediccions, y_val, 'e', 'p')
            accuracy_result, precision_result, recall_result, specifity_result, f1score = calcular_mesures(TP,FP,FN,TN)
            dicc_mesures = afegir_mesures_diccionari(dicc_mesures, accuracy_result, precision_result, recall_result, specifity_result, f1score)
        accuracy_result, precision_result, recall_result, specifity_result, f1score = calcular_mitjana_mesures(dicc_mesures)
        print("\nMesures Leave one out:")
        printar_mesures(accuracy_result, precision_result, recall_result, specifity_result, f1score)"""
    else:
        print("\nOpcio no valida")
    
if __name__ == '__main__':
    main()