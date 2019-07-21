# -*- coding: utf-8 -*-
import numpy as np
import time
class CasellesParaula:
    """
    Clase que representa una variable per al backtracking. Representa el conjunt de 
    caselles que conformen una paraula en un crossword.
    params:
        -coordenada: llista que conte la fila i la columna on es troba l'inici de
                     aquesta variable en el crossword.
        -orientacio: indica si es una paraula horitzontal o vertical.
        -longitud: nombre de caracters que ocupa la paraula.
        -idParaula: identificador de la variable. Agafem com a identificador el 
                    numero que hi ha en el crossword en la casella on comença la variable.
        -paraula_asignada: quina paraula esta asignada a aquest conjunt de caselles
        -encreuaments: llista on estan indicats tots els encreuaments de la seguent manera:
                        [1,3,4,var,7]
                        primer valor: fila on es crea el encreuament 
                        segundo valor: col on es crea el encreuament 
                        tercer valor: posicion de la paraula on es troba aquest encreuament en la paraula amb la que s'encreua
                        cuarto valor: id de la paraula original 
                        quinto posicion: posicion de la paraula on es troba aquest encreuament en la paraula assignada a aquest objecte
    """
    def __init__(self, coordenada, orientacio, longitud, idParaula, paraula_asignada):
        self.coordenada = coordenada
        self.orientacio = orientacio
        self.longitud = longitud
        self.idParaula = idParaula
        self.paraula_asignada = paraula_asignada
        self.encreuaments = []

    def setEncreuaments(self, encreuaments):
        self.encreuaments = encreuaments

    def setParaulaAsignada(self, paraula_asignada):
        self.paraula_asignada = paraula_asignada

    def setCasellesOcupades(self, casellesOcupades):
        self.casellesOcupades = casellesOcupades

    def setDobleDireccio(self, dobleDireccio):
        self.dobleDireccio = dobleDireccio

def limitar_matriu(crossword):
    """
    Rodegem la matriu amb caracters '#' per a poder fer una comprovacio de les orientacions
    de les matrius de manera mes simple. Tambe evitem haver de manejar valors que van fora 
    de la matriu.
    """
    crossword = np.insert(crossword,0,"#",axis=1)    
    crossword = np.insert(crossword,len(crossword[0]),"#",axis=1)    
    crossword = np.insert(crossword,0,"#",axis=0)    
    crossword = np.insert(crossword,len(crossword),"#",axis=0)
    
    return crossword

def crearLlistaVariables(crossword):
    """
    Funcio que s'encarrega de crear la llista de variables que s'utilitzara en 
    el backtracking. Assigna la longitud y la orientacio a les variables.
    """
    llista_variables = []
    a = list(crossword.flatten())
        
    for i in range(1,len(a)):
        if a[i - 1] == "#" and "0" != a[i] and "#" != a[i]:
            
            llista_variables.append(CasellesParaula(np.argwhere(crossword == a[i]),'h',a[a.index(a[i]):].index("#"),a[i], ""))
        if a[i - crossword.shape[1]] == "#" and "0" != a[i] and "#" != a[i]:
            
            llista_variables.append(CasellesParaula(np.argwhere(crossword == a[i]), 'v', 0, a[i], ""))
    
    for var in llista_variables:
        if 'v' in var.orientacio:
            for i in range(var.coordenada[0][0],crossword.shape[0]):
                if crossword[i,var.coordenada[0][1]] == "#":
                    var.longitud = i - var.coordenada[0][0]
                    break
    return llista_variables

def diccionariLongitudParaules(path_fitxer_diccionari):
    """
    Funcio que pasat el path d'un fitxer amb un conjunt de paraules, crea un diccionari amb les longituds de les paraules
    i les paraules que pertanyen a aquesta longitud. Ex:
        {2: [ei, va], 3: [bou, eia] ... }
    """
    llista_paraules = open(path_fitxer_diccionari, 'r').read().splitlines()
    diccionari_paraules = dict()
    for paraula in llista_paraules:
        longitud = len(paraula)
        if longitud not in diccionari_paraules:
            diccionari_paraules[longitud] = []
        diccionari_paraules[longitud].append(paraula)  
 
    return diccionari_paraules

def casellesOcupades(lvna):
    """
    Funcio que asigna a les variables una llista amb totes les coordenades que ocupen
    les variables.
    """
    for var in lvna:
        lista_caselles_ocupades = []
        for i in range(0, var.longitud):
            if var.orientacio == 'h':                
                fila = var.coordenada[0][0]
                col = var.coordenada[0][1]+i
                coord_ocupada = [fila,col]
                lista_caselles_ocupades.append(coord_ocupada)
        
            if var.orientacio == 'v':                
                fila = var.coordenada[0][0]+i
                col = var.coordenada[0][1]
                coord_ocupada = [fila,col]
                lista_caselles_ocupades.append(coord_ocupada)
        
        var.setCasellesOcupades(lista_caselles_ocupades)

def identificarParaulesDosDireccions(lvna):
    """
    Funcio que assigna a les variables si tenen dos direccions o no
    """
    for variable in lvna:
        if isVerticalYHorizontal(variable.idParaula, lvna):
            variable.setDobleDireccio(True)
        else:
            variable.setDobleDireccio(False)

def isVerticalYHorizontal(id_var, lva):
    """
    Funcio que identifica quines variables tenen dos direccions, es a dir, poden
    anar tant horitzontals com verticals.
    """
    contador = 0
    correcte = False
    
    for variable in lva:
        if variable.idParaula == id_var:
            contador += 1
    if contador > 1:
        correcte = True

    return correcte

def comprobarEncreuaments(lvna):
    """
    Funcio que s'encarrega d'analitzar tots els encreuaments que es produeixen entre totes
    les variables que hi ha a la llista de variables que passem com a parametre.
    """    
    for var in lvna:
        llista_encreuaments = []
        for variable in lvna:            
            for coor_ocupada in var.casellesOcupades:                                
                for coor_ocupada_llista in variable.casellesOcupades:                    
                    if coor_ocupada == coor_ocupada_llista:                                            
                        if (not var.dobleDireccio and var.idParaula != variable.idParaula) or (var.dobleDireccio and var.idParaula != variable.idParaula):                                                                                                                                
                                if variable.orientacio == 'h':                                    
                                    posicio = abs(variable.coordenada[0][1] - coor_ocupada[1])                                    
                                    posicio_var = abs(var.coordenada[0][0] - coor_ocupada[0])
                                if variable.orientacio == 'v':
                                    posicio = abs(variable.coordenada[0][0] - coor_ocupada[0])                                   
                                    posicio_var = abs(var.coordenada[0][1] - coor_ocupada[1])                                
                                temp = coor_ocupada[:]
                                temp.append(posicio)
                                temp.append(variable)
                                temp.append(posicio_var)                                
                                var.encreuaments.append(temp)     
                        else:
                            if coor_ocupada == var.casellesOcupades[0] and var.orientacio != variable.orientacio:
                                temp = coor_ocupada[:]
                                temp.append(0)
                                temp.append(variable)
                                temp.append(0)
                                var.encreuaments.append(temp)

                                                            

def comprobarMateixaLletra(var, paraula):
    """
    Funcio que s'encarrega de determinar si la paraula d'una variable i una altra
    paraula tenen la mateixa lletra en les posicions on s'encreuen. Retorna un boolea.
    """
    correcte = False
    if not var.encreuaments:
        correcte = True            
    if var.encreuaments:        
        num_encreuaments = 0
        for encreuament in var.encreuaments:
            if encreuament[3].paraula_asignada or encreuament[3].paraula_asignada != "":
                num_encreuaments += 1
        correcte = False
        cont_encreuaments = 0
        for encreuament in var.encreuaments:
            if encreuament[3].paraula_asignada or encreuament[3].paraula_asignada != "":                
                if paraula[encreuament[4]] == encreuament[3].paraula_asignada[encreuament[2]]:
                    cont_encreuaments += 1

        if cont_encreuaments == num_encreuaments:
            correcte = True        

    return correcte    

def printMatrix(lva, crossword): 
    
    #Funcio que printa una matriu amb la solucio trobada del crossword.
       
    for paraula_llista in lva:
        if paraula_llista.paraula_asignada != "" and paraula_llista.paraula_asignada:                     
            fila = paraula_llista.coordenada[0][0]
            col = paraula_llista.coordenada[0][1]
            longitud = paraula_llista.longitud
            orientacio = paraula_llista.orientacio
            for i in range(0, longitud):
                #horitzontal
                if orientacio == 'h':
                    crossword[fila][col + i] = paraula_llista.paraula_asignada[i]
                    
                #vertical
                if orientacio == 'v':
                    crossword[fila + i][col] = paraula_llista.paraula_asignada[i]                    
                
    print(crossword)

def backtracking(lva, lvna, domini, crossword):
    """
    Funcio principal que s'encarrega de fer el backtracking, trobar unes variables que 
    compleixin totes les restriccions, i en cas de haver resposta, retornar una 
    llista amb aquestes variables. En cas de que no hi hagi solució, retornara None.
    """
    if not lvna:
        return lva          
    var = lvna[0]
    paraules = domini[var.longitud]    
    for paraula in paraules:        
        if comprobarMateixaLletra(var,paraula):                
                var.setParaulaAsignada(paraula)   
                printMatrix(lva, crossword)
                time.sleep(0.3)
                print(chr(27)+'[2j')
                print('\033c')
                print('\x1bc')
                paraules.remove(paraula)             
                lva.append(var)            
                if var in lvna:                    
                    lvna.remove(var)
                lva = lva[:]                
                res = backtracking(lva,lvna,domini, crossword)
                if res != None:
                    return res
                else:
                    var.paraula_asignada = ""
                    lva.remove(var)
                    lvna.insert(0,var) 
                    paraules.append(paraula)

    return None

def main():
    path = "../Database/"
    nom_fitxer_crossword = "crossword_CB.txt"
    nom_fitxer_diccionari = "diccionari_CB.txt"
    #Llegim el fitxer de crossword
    crossword = np.genfromtxt(path + nom_fitxer_crossword, dtype='U10', delimiter="\t", comments="!")
    #Rodegem la matriu amb #
    crossword = limitar_matriu(crossword)
    #Creem la llista de variables
    lvna = crearLlistaVariables(crossword)
    #Comprovem que no hi hagi cap variable amb longitud 1
    cont = 0
    for variable_lvna in lvna:
        if variable_lvna.longitud == 1:
            del lvna[cont]    
        cont += 1

    #Agafem tot el domini del fitxer de diccionari
    diccionari = diccionariLongitudParaules(path+nom_fitxer_diccionari)  
    #Calculem quines caselles ocupa cada variable.      
    casellesOcupades(lvna)
    identificarParaulesDosDireccions(lvna)
    comprobarEncreuaments(lvna)        
    lva = []    
    sol = backtracking(lva, lvna, diccionari, crossword)        
    printMatrix(sol, crossword)
    """for var in lvna:
        print("id : " + var.idParaula)
        if var.encreuaments:
            for encreuament in var.encreuaments:
                print("___________")
                print("coordenadas var")
                print(var.coordenada)
                print("fila:" + str(encreuament[0]))
                print("col:" + str(encreuament[1]))
                print("id original: " + str(encreuament[3].idParaula))
                print("orientacio encreuada: " + var.orientacio)
                print("orientacio original: " + str(encreuament[3].orientacio))
                print("paraula original: " + str(encreuament[2]))
                print("paraula creuada: " + str(encreuament[4]))
                print("___________")"""

if __name__ == '__main__':
    main()