# Arquivo: inimigos.py

import arcade
import random
from funcoes import *


class Inimigo:
    def __init__(self, vida, velocidade_movimento, cor, tamanho, dano):
        self.vida = vida
        self.velocidade_movimento = velocidade_movimento
        self.cor = cor
        self.tamanho = tamanho
        self.dano = dano


class InimigoPadrao(Inimigo):
    def __init__(self):
        super().__init__(vida=100, velocidade_movimento=2, cor=arcade.color.RED, tamanho=30, dano=10)


class SemiBoss(Inimigo):
    def __init__(self):
        super().__init__(vida=200, velocidade_movimento=3, cor=arcade.color.YELLOW, tamanho=40, dano=20)


class Boss(Inimigo):
    def __init__(self):
        super().__init__(vida=500, velocidade_movimento=1, cor=arcade.color.PURPLE, tamanho=60, dano=50)


def criar_inimigo_padrao():
    return InimigoPadrao()


def criar_semi_boss():
    return SemiBoss()


def criar_boss():
    return Boss()
