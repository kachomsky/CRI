# -*- coding: utf-8 -*-
class Node():
    """
    Clase que representa l'estructura d'un node
    """
    def __init__(self):
        self.etiqueta = None
        self.atribut = None
        self.fills = None
    
    def setEtiqueta(self, etiqueta):
        self.etiqueta = etiqueta
    
    def setAtribut(self, atribut ):
        self.atribut = atribut
    
    def setFills(self, fills):
        self.fills = fills
    