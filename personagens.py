import arcade

class Guerreiro:
    def __init__(self):
        self.nome = "Guerreiro"
        self.vida = 1100
        self.velocidade_movimento = 5
        self.velocidade_projeteis = 10
        self.projeteis_cor = arcade.color.RED  # Vermelho
        self.projeteis_tamanho = 10
        self.tamanho = 50  # Tamanho do personagem
        self.cor = arcade.color.BLUE  # Cor do personagem

class Purgador:
    def __init__(self):
        self.nome = "Purgador"
        self.vida = 1000120
        self.velocidade_movimento = 10
        self.velocidade_projeteis = 20
        self.projeteis_cor = arcade.color.GREEN  # Verde
        self.projeteis_tamanho = 130
        self.tamanho = 1 # Tamanho do personagem
        self.cor = arcade.color.YELLOW  # Cor do personagem

class Feiticeira:
    def __init__(self):
        self.nome = "Feiticeira"
        self.vida = 1180
        self.velocidade_movimento = 4
        self.velocidade_projeteis = 8
        self.projeteis_cor = arcade.color.BLUE  # Azul
        self.projeteis_tamanho = 10
        self.tamanho = 45  # Tamanho do personagem
        self.cor = arcade.color.PURPLE  # Cor do personagem

class Bardo:
    def __init__(self):
        self.nome = "Bardo"
        self.vida = 1190
        self.velocidade_movimento = 5
        self.velocidade_projeteis = 9
        self.projeteis_cor = arcade.color.YELLOW  # Amarelo
        self.projeteis_tamanho = 10
        self.tamanho = 35  # Tamanho do personagem
        self.cor = arcade.color.ORANGE  # Cor do personagem
