# Arquivo: funcoes.py

import arcade

# Constantes
LARGURA_TELA = 800
ALTURA_TELA = 600
COR_FUNDO = arcade.color.SKY_BLUE

TAMANHO_PROJETIL = 10
COR_PROJETIL = arcade.color.BLACK
DANO_PROJETIL = 100000000

INTERVALO_DISPARO = 0.1
INTERVALO_ADICIONAR_INIMIGO_PADRAO = 1
INTERVALO_ADICIONAR_SEMI_BOSS = 15
INTERVALO_ADICIONAR_BOSS = 30

def causar_dano_personagem(personagem, dano):
    """
    Função para causar dano ao personagem.

    Args:
        personagem (Personagem): O objeto do personagem que está recebendo o dano.
        dano (int): O valor do dano a ser causado.

    Returns:
        bool: True se o personagem morreu após receber o dano, False caso contrário.
    """
    personagem.vida -= dano
    if personagem.vida <= 0:
        return True
    return False
