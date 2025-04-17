import tkinter as tk  # Biblioteca para criar interface gráfica
import random          # Usado para gerar direções aleatórias na criação do labirinto
import time            # Usado para pausar a execução (animação)
from collections import deque  # Deque é uma fila eficiente para o algoritmo BFS

# Tamanho do labirinto (deve ser ímpar para funcionar corretamente com a geração)
ALTURA = 21
LARGURA = 33
CELULA = 25  # Tamanho de cada célula em pixels

# Definição de cores usadas na visualização
COR_PAREDE = "black"
COR_CAMINHO = "white"
COR_INICIO = "green"
COR_FIM = "red"
COR_VISITADO = "lightblue"
COR_SOLUCAO = "blue"

class LabirintoApp:
    def __init__(self, root):
        # Inicializa a janela e o canvas de desenho
        self.root = root
        self.canvas = tk.Canvas(root, width=LARGURA * CELULA, height=ALTURA * CELULA)
        self.canvas.pack()

        # Cria uma matriz de paredes inicialmente
        self.labirinto = [['#'] * LARGURA for _ in range(ALTURA)]

        # Gera o labirinto aleatoriamente usando DFS
        self.gerar_labirinto()

        # Define os pontos de início e fim
        self.inicio = (1, 1)
        self.fim = (ALTURA - 2, LARGURA - 2)

        # Marca o início e o fim no labirinto
        self.labirinto[self.inicio[0]][self.inicio[1]] = 'S'
        self.labirinto[self.fim[0]][self.fim[1]] = 'E'

        # Desenha o labirinto no canvas
        self.desenhar_labirinto()

        # Inicia o algoritmo BFS animado após 500ms
        self.root.after(500, self.bfs_animado)

    # Gera o labirinto usando uma DFS recursiva com movimentação em passos de 2
    def gerar_labirinto(self):
        def dfs(y, x):
            # Define as direções possíveis (cima, baixo, esquerda, direita), pulando 2 células
            direcoes = [(0, 2), (0, -2), (2, 0), (-2, 0)]
            random.shuffle(direcoes)  # Embaralha a ordem das direções para gerar labirintos únicos

            for dy, dx in direcoes:
                ny, nx = y + dy, x + dx
                # Verifica se está dentro dos limites do labirinto
                if 0 < ny < ALTURA - 1 and 0 < nx < LARGURA - 1:
                    if self.labirinto[ny][nx] == '#':  # Se ainda for parede
                        self.labirinto[ny][nx] = ' '  # Abre caminho no destino
                        self.labirinto[y + dy // 2][x + dx // 2] = ' '  # Abre o caminho intermediário
                        dfs(ny, nx)  # Continua a escavação a partir do novo ponto

        self.labirinto[1][1] = ' '  # Ponto inicial do labirinto
        dfs(1, 1)  # Inicia a DFS para escavar o labirinto

    # Desenha o labirinto no canvas, com suporte para destacar visitados e caminho final
    def desenhar_labirinto(self, caminho=None, visitados=None):
        for y in range(ALTURA):
            for x in range(LARGURA):
                cor = COR_PAREDE  # Cor padrão é parede

                # Define a cor com base no conteúdo da célula
                if self.labirinto[y][x] == 'S':
                    cor = COR_INICIO
                elif self.labirinto[y][x] == 'E':
                    cor = COR_FIM
                elif caminho and (y, x) in caminho:
                    cor = COR_SOLUCAO
                elif visitados and (y, x) in visitados:
                    cor = COR_VISITADO
                elif self.labirinto[y][x] == ' ':
                    cor = COR_CAMINHO

                # Desenha o retângulo correspondente à célula
                self.canvas.create_rectangle(
                    x * CELULA, y * CELULA,
                    (x + 1) * CELULA, (y + 1) * CELULA,
                    fill=cor, outline="gray"
                )

        self.root.update()  # Atualiza a interface com as alterações

    # Executa o algoritmo de busca em largura (BFS) com animação da exploração
    def bfs_animado(self):
        fila = deque()  # Fila para armazenar as posições a visitar
        fila.append((self.inicio, [self.inicio]))  # Adiciona a posição inicial e o caminho até ela
        visitados = set()  # Conjunto para registrar células já visitadas
        direcoes = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Cima, baixo, esquerda, direita

        while fila:
            (y, x), caminho = fila.popleft()  # Pega o próximo da fila

            if (y, x) in visitados:
                continue  # Pula se já foi visitado

            visitados.add((y, x))  # Marca como visitado
            self.desenhar_labirinto(visitados=visitados)  # Atualiza o desenho mostrando os visitados
            time.sleep(0.01)  # Pequena pausa para efeito visual da animação

            if (y, x) == self.fim:
                self.desenhar_labirinto(caminho=caminho)  # Mostra o caminho final
                return  # Termina a busca

            # Verifica os vizinhos
            for dy, dx in direcoes:
                ny, nx = y + dy, x + dx
                if 0 <= ny < ALTURA and 0 <= nx < LARGURA:
                    if self.labirinto[ny][nx] in (' ', 'E') and (ny, nx) not in visitados:
                        fila.append(((ny, nx), caminho + [(ny, nx)]))  # Adiciona o próximo ponto e o caminho até ele

# Executa o programa se o arquivo for rodado diretamente
if __name__ == "__main__":
    root = tk.Tk()  # Cria a janela principal
    root.title("Labirinto com Geração Aleatória + Animação BFS")  # Título da janela
    app = LabirintoApp(root)  # Instancia o app do labirinto
    root.mainloop()  # Inicia o loop principal da interface gráfica
