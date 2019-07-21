# -*- coding: utf-8 -*-
import Node
import PreprocesamentDades as proc_d
import calculs_generals as cg

def id3(data, valors_unics, atributs_restants, atribut_target):   
    node = Node.Node()
    major_info_gain = None
    millor_atribut = None
    clases_millor_atribut = None
    
    positius_negatius = proc_d.clases_positives_negatives(data, atribut_target)       
    
    if len(positius_negatius.keys()) == 1:
        node.setEtiqueta(next(iter(positius_negatius.keys())))
        return node

    if len(atributs_restants) == 0:        
        node.setEtiqueta(proc_d.etiqueta_majoritaria(positius_negatius))
        return node

    n = len(data['mostres'])
    entropia_general = cg.entropia(positius_negatius, n)    

    for atribut in atributs_restants:        
        partitions = proc_d.particionarData(data, atribut)
        gain = cg.info_gain_calc(data, partitions, atribut_target)
        info_gain = entropia_general - gain
        if major_info_gain is None or info_gain > major_info_gain:
            major_info_gain = info_gain
            millor_atribut = atribut
            clases_millor_atribut = partitions
            
    if major_info_gain is None:
        node.setEtiqueta(cg.etiqueta_majoritaria(positius_negatius))
        return node
    
    node.setAtribut(millor_atribut)
    node.setFills({})

    atributs_restants = set(atributs_restants)
    atributs_restants.discard(millor_atribut)
    valors_unics_atribut = valors_unics[millor_atribut]
    
    for valor_atribut in valors_unics_atribut:
        if valor_atribut not in clases_millor_atribut.keys():            
            node_fill = Node.Node()
            node_fill.setEtiqueta(proc_d.etiqueta_majoritaria(positius_negatius))
            node.fills[valor_atribut] = node_fill                              
        else:
            partition = clases_millor_atribut[valor_atribut]        
            node.fills[valor_atribut] = id3(partition, valors_unics, atributs_restants, atribut_target)        
    return node

def id3_dades_continues(data, valors_unics, atributs_restants, atribut_target):   
    node = Node.Node()
    major_info_gain = None
    millor_atribut = None
    clases_millor_atribut = None
    split_continua = 0
    positius_negatius = proc_d.clases_positives_negatives(data, atribut_target)       
    
    if len(positius_negatius.keys()) == 1:
        node.setEtiqueta(next(iter(positius_negatius.keys())))
        return node

    if len(atributs_restants) == 0:        
        node.setEtiqueta(proc_d.etiqueta_majoritaria(positius_negatius))
        return node

    n = len(data['mostres'])
    entropia_general = cg.entropia(positius_negatius, n)    

    for atribut in atributs_restants:
        if proc_d.is_number(data['mostres'][:,data["atribut_col"][atribut]][0]):
            gain, split_continua = cg.calcular_mid_points(data, atribut, atribut_target)
            valors_atr = data["mostres"].transpose()[data["atribut_col"][atribut]]            
            valors_atr = valors_atr.astype(str)                         
                   
            count_valor = 0
            for valor in valors_atr:
                if valor.astype(int) > int(split_continua):
                    valors_atr = list(valors_atr)
                    valors_atr[count_valor] = '> '+str(split_continua)
                if valor.astype(int) <= int(split_continua):
                    valors_atr = list(valors_atr)
                    valors_atr[count_valor] = '<= '+str(split_continua)
                count_valor+=1
            
            data["mostres"].transpose()[data["atribut_col"][atribut]] = valors_atr            
            partitions = proc_d.particionarData(data, atribut)
            valors_unics = proc_d.valorsUnics(data)
            
        else:
            partitions = proc_d.particionarData(data, atribut)
            gain = cg.info_gain_calc(data, partitions, atribut_target)
        info_gain = entropia_general - gain
        if major_info_gain is None or info_gain > major_info_gain:
            major_info_gain = info_gain
            millor_atribut = atribut
            clases_millor_atribut = partitions
            
    if major_info_gain is None:
        node.setEtiqueta(proc_d.etiqueta_majoritaria(positius_negatius))
        return node
    
    node.setAtribut(millor_atribut)
    node.setFills({})

    atributs_restants = set(atributs_restants)
    atributs_restants.discard(millor_atribut)
    valors_unics_atribut = valors_unics[millor_atribut] 
    #print(valors_unics_atribut)
    for valor_atribut in valors_unics_atribut:
        if valor_atribut not in clases_millor_atribut.keys():            
            node_fill = Node.Node()
            node_fill.setEtiqueta(proc_d.etiqueta_majoritaria(positius_negatius))
            node.fills[valor_atribut] = node_fill                              
        else:
            partition = clases_millor_atribut[valor_atribut]        
            node.fills[valor_atribut] = id3(partition, valors_unics, atributs_restants, atribut_target)        
    return node, data
