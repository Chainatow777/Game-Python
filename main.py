import arcade
import random
from funcoes import *
from personagens import *
from inimigos import *

class MeuJogo(arcade.Window):
    MULTIPLO_INIMIGOS = 5
    DURACAO_PROJETEIS_EXTRA = 20.0

    def __init__(self, largura, altura, titulo, personagem):
        super().__init__(largura, altura, titulo)

        arcade.set_background_color(COR_FUNDO)

        self.personagem = personagem
        self.personagem_x = LARGURA_TELA // 2
        self.personagem_y = ALTURA_TELA // 2

        self.mover_esquerda = False
        self.mover_direita = False
        self.mover_cima = False
        self.mover_baixo = False

        self.inimigos = []
        self.projetis = []
        self.projetis_extra = []
        self.habilidade_ativa = False
        self.escudo_ativo = False
        self.tempo_escudo = 0

        self.timer_disparo = 0
        self.timer_disparo_extra = 0 
        self.timer_adicionar_inimigo_padrao = 0
        self.timer_adicionar_semi_boss = 0
        self.timer_adicionar_boss = 0

        self.tempo_vivo = 0
        self.inimigos_mortos = 0
        self.game_over = False

        self.temporizador = 0

    def reset_game(self):
        self.personagem_x = LARGURA_TELA // 2
        self.personagem_y = ALTURA_TELA // 2
        self.mover_esquerda = False
        self.mover_direita = False
        self.mover_cima = False
        self.mover_baixo = False
        self.inimigos = []
        self.projetis = []
        self.timer_disparo = 0
        self.timer_adicionar_inimigo_padrao = 0
        self.timer_adicionar_semi_boss = 0
        self.timer_adicionar_boss = 0
        self.inimigos_mortos = 0
        self.game_over = False

    def on_restart_game(self):
        self.reset_game()
        arcade.close_window()
        main()

    def disparar_projetil(self, vel_x, vel_y, cor):
        self.projetis.append(
            [self.personagem_x, self.personagem_y, vel_x, vel_y, cor, self.personagem.projeteis_tamanho])

    def exibir_info_habilidade(self):
        pass

    def on_draw(self):
        arcade.start_render()

        # Desenha o contador de vida do personagem selecionado
        arcade.draw_text(f"Vida: {self.personagem.vida}", 10, ALTURA_TELA - 30, arcade.color.BLACK, 14)

        # Desenha o contador de inimigos mortos
        arcade.draw_text(f"Inimigos mortos: {self.inimigos_mortos}", 10, ALTURA_TELA - 50, arcade.color.BLACK, 14)

        arcade.draw_text(f"Tempo: {int(self.temporizador)}", LARGURA_TELA // 2, ALTURA_TELA - 30, arcade.color.BLACK, 14, anchor_x="center")

        # Desenha o personagem, inimigos e projéteis
        arcade.draw_rectangle_filled(self.personagem_x, self.personagem_y, self.personagem.tamanho,
                                     self.personagem.tamanho, self.personagem.cor)
        for inimigo in self.inimigos:
            arcade.draw_rectangle_filled(inimigo[0], inimigo[1], inimigo[5], inimigo[5], inimigo[4])
        for projetil in self.projetis:
            arcade.draw_rectangle_filled(projetil[0], projetil[1], projetil[5], projetil[5], projetil[4])

        # Desenha tela de Game Over, se aplicável
        if self.game_over:
            arcade.draw_text("Game Over", LARGURA_TELA // 2, ALTURA_TELA // 2,
                             arcade.color.RED, font_size=50, anchor_x="center")
            arcade.draw_text("Pressione R para tentar novamente", LARGURA_TELA // 2, ALTURA_TELA // 2 - 50,
                             arcade.color.WHITE, font_size=20, anchor_x="center")
            arcade.draw_text(f"Tempo Vivo: {int(self.tempo_vivo)} segundos", LARGURA_TELA // 2, ALTURA_TELA // 2 - 100,
                             arcade.color.BLACK, font_size=20, anchor_x="center")
            arcade.draw_text(f"Inimigos Mortos: {self.inimigos_mortos}", LARGURA_TELA // 2, ALTURA_TELA // 2 - 130,
                             arcade.color.BLACK, font_size=20, anchor_x="center")
            
    def disparar_projetil_extra(self):
    # Disparar projétil extra em todas as direções
        self.disparar_projetil(-self.personagem.velocidade_projeteis, 0, self.personagem.projeteis_cor)  # Esquerda
        self.disparar_projetil(self.personagem.velocidade_projeteis, 0, self.personagem.projeteis_cor)   # Direita
        self.disparar_projetil(0, self.personagem.velocidade_projeteis, self.personagem.projeteis_cor)   # Cima
        self.disparar_projetil(0, -self.personagem.velocidade_projeteis, self.personagem.projeteis_cor)  # Baixo

    def update(self, delta_time):
        if not self.game_over:
            self.tempo_vivo += delta_time
            if self.mover_esquerda:
                self.personagem_x -= self.personagem.velocidade_movimento
            elif self.mover_direita:
                self.personagem_x += self.personagem.velocidade_movimento
            elif self.mover_cima:
                self.personagem_y += self.personagem.velocidade_movimento
            elif self.mover_baixo:
                self.personagem_y -= self.personagem.velocidade_movimento
            
            self.temporizador += delta_time
            self.personagem_x = max(25, min(LARGURA_TELA - 25, self.personagem_x))
            self.personagem_y = max(25, min(ALTURA_TELA - 25, self.personagem_y))

            # Lógica de movimento dos inimigos e detecção de colisões com o personagem
            for inimigo in self.inimigos:
                dif_x = self.personagem_x - inimigo[0]
                dif_y = self.personagem_y - inimigo[1]
                distancia = (dif_x ** 2 + dif_y ** 2) ** 0.5
                if distancia != 0:
                    inimigo[0] += inimigo[3] * dif_x / distancia
                    inimigo[1] += inimigo[3] * dif_y / distancia

                if distancia < (self.personagem.tamanho + inimigo[5]) / 2:
                    if causar_dano_personagem(self.personagem, inimigo[6]):  # Se o personagem morrer
                        print("Você morreu!")
                        self.game_over = True

            # Lógica de movimento e detecção de colisões dos projéteis
            for projetil in self.projetis:
                projetil[0] += projetil[2]
                projetil[1] += projetil[3]
                for inimigo in self.inimigos:
                    if abs(projetil[0] - inimigo[0]) < inimigo[5] / 2 and abs(projetil[1] - inimigo[1]) < inimigo[5] / 2:
                        inimigo[2] -= DANO_PROJETIL
                        if inimigo[2] <= 0:
                            self.inimigos.remove(inimigo)
                            self.inimigos_mortos += 1  # Incrementar o contador de inimigos mortos
                        self.projetis.remove(projetil)
                        break

            # Lógica de disparar projéteis do personagem
            self.timer_disparo += delta_time
            if self.timer_disparo >= INTERVALO_DISPARO:
                if self.mover_esquerda:
                    self.disparar_projetil(-self.personagem.velocidade_projeteis, 0, self.personagem.projeteis_cor)
                elif self.mover_direita:
                    self.disparar_projetil(self.personagem.velocidade_projeteis, 0, self.personagem.projeteis_cor)
                elif self.mover_cima:
                    self.disparar_projetil(0, self.personagem.velocidade_projeteis, self.personagem.projeteis_cor)
                elif self.mover_baixo:
                    self.disparar_projetil(0, -self.personagem.velocidade_projeteis, self.personagem.projeteis_cor)
                self.timer_disparo = 0

            # Lógica de adicionar inimigos com base em intervalos de tempo
            self.timer_adicionar_inimigo_padrao += delta_time
            self.timer_adicionar_semi_boss += delta_time
            self.timer_adicionar_boss += delta_time

            if self.timer_adicionar_inimigo_padrao >= INTERVALO_ADICIONAR_INIMIGO_PADRAO:
                self.adicionar_inimigo(criar_inimigo_padrao)
                self.timer_adicionar_inimigo_padrao = 0
            elif self.timer_adicionar_semi_boss >= INTERVALO_ADICIONAR_SEMI_BOSS:
                self.adicionar_inimigo(criar_semi_boss)
                self.timer_adicionar_semi_boss = 0
            elif self.timer_adicionar_boss >= INTERVALO_ADICIONAR_BOSS:
                self.adicionar_inimigo(criar_boss)
                self.timer_adicionar_boss = 0

            # Verificar se o contador de inimigos mortos atingiu um múltiplo de 5
            if self.inimigos_mortos % self.MULTIPLO_INIMIGOS == 0 and self.inimigos_mortos != 0:
                # Disparar projéteis extras
                self.disparar_projetil_extra()
                # Configurar o tempo de duração dos projéteis extras
                self.timer_disparo_extra = self.DURACAO_PROJETEIS_EXTRA
          
    def adicionar_inimigo(self, tipo_inimigo):
        x = random.randint(0, LARGURA_TELA)
        y = random.randint(0, ALTURA_TELA)
        inimigo = tipo_inimigo()
        self.inimigos.append([x, y, inimigo.vida, inimigo.velocidade_movimento, inimigo.cor, inimigo.tamanho, inimigo.dano])

    def on_key_press(self, key, modifiers):
        if key == arcade.key.LEFT:
            self.mover_esquerda = True
        elif key == arcade.key.RIGHT:
            self.mover_direita = True
        elif key == arcade.key.UP:
            self.mover_cima = True
        elif key == arcade.key.DOWN:
            self.mover_baixo = True
        elif key == arcade.key.R and self.game_over:
            self.on_restart_game()

    def on_key_release(self, key, modifiers):
        if key == arcade.key.LEFT:
            self.mover_esquerda = False
        elif key == arcade.key.RIGHT:
            self.mover_direita = False
        elif key == arcade.key.UP:
            self.mover_cima = False
        elif key == arcade.key.DOWN:
            self.mover_baixo = False


def exibir_informacoes_personagem(personagem):
    print("\nInformações do personagem:")
    print(f"Nome: {personagem.nome}")
    print(f"Vida: {personagem.vida}")
    print(f"Velocidade de Movimento: {personagem.velocidade_movimento}")

def main():
    while True:
        print("\nEscolha seu personagem:")
        print("1. Guerreiro")
        print("2. Purgador")
        print("3. Feiticeira")
        print("4. Bardo")
        escolha = input("\nDigite o número correspondente ao personagem desejado (ou 'q' para sair): ")

        if escolha == "1":
            personagem = Guerreiro()
        elif escolha == "2":
            personagem = Purgador()
        elif escolha == "3":
            personagem = Feiticeira()
        elif escolha == "4":
            personagem = Bardo()
        elif escolha.lower() == "q":
            print("Saindo do jogo.")
            return
        else:
            print("Escolha inválida.")
            continue

        # Exibir informações do personagem selecionado
        exibir_informacoes_personagem(personagem)

        # Confirmar escolha do personagem
        confirmacao = input(f"\nDeseja confirmar a escolha de {personagem.nome}? (s/n): ")
        if confirmacao.lower() == "s":
            # Inicializar o jogo somente após a confirmação do usuário
            jogo = MeuJogo(LARGURA_TELA, ALTURA_TELA, "Meu Jogo", personagem)
            arcade.run()
            break
        else:
            print("\nSeleção cancelada. Retornando à seleção de personagem.")

if __name__ == "__main__":
    main()
