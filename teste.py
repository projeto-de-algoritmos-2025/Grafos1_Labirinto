import tkinter as tk
import random
import time
from collections import deque

# Tamanho do labirinto (deve ser ímpar para funcionar bem com a geração)
ALTURA = 21
LARGURA = 21
CELULA = 25

# Cores
COR_PAREDE = "black"
COR_CAMINHO = "white"
COR_INICIO = "green"
COR_FIM = "red"
COR_VISITADO = "lightblue"
COR_SOLUCAO = "blue"

class LabirintoApp:
    def __init__(self, root):
        self.root = root
        self.canvas = tk.Canvas(root, width=LARGURA * CELULA, height=ALTURA * CELULA)
        self.canvas.pack()
        self.labirinto = [['#'] * LARGURA for _ in range(ALTURA)]
        self.gerar_labirinto()
        self.inicio = (1, 1)
        self.fim = (ALTURA - 2, LARGURA - 2)
        self.labirinto[self.inicio[0]][self.inicio[1]] = 'S'
        self.labirinto[self.fim[0]][self.fim[1]] = 'E'
        self.desenhar_labirinto()
        self.root.after(500, self.bfs_animado)  # inicia animação após 0.5s

    def gerar_labirinto(self):
        def dfs(y, x):
            direcoes = [(0, 2), (0, -2), (2, 0), (-2, 0)]
            random.shuffle(direcoes)
            for dy, dx in direcoes:
                ny, nx = y + dy, x + dx
                if 0 < ny < ALTURA - 1 and 0 < nx < LARGURA - 1:
                    if self.labirinto[ny][nx] == '#':
                        self.labirinto[ny][nx] = ' '
                        self.labirinto[y + dy // 2][x + dx // 2] = ' '
                        dfs(ny, nx)

        self.labirinto[1][1] = ' '
        dfs(1, 1)

    def desenhar_labirinto(self, caminho=None, visitados=None):
        for y in range(ALTURA):
            for x in range(LARGURA):
                cor = COR_PAREDE
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

                self.canvas.create_rectangle(
                    x * CELULA, y * CELULA,
                    (x + 1) * CELULA, (y + 1) * CELULA,
                    fill=cor, outline="gray"
                )
        self.root.update()

    def bfs_animado(self):
        fila = deque()
        fila.append((self.inicio, [self.inicio]))
        visitados = set()
        direcoes = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        while fila:
            (y, x), caminho = fila.popleft()

            if (y, x) == self.fim:
                self.desenhar_labirinto(caminho=caminho)
                return

            visitados.add((y, x))
            self.desenhar_labirinto(visitados=visitados)

            time.sleep(0.01)  # controle da velocidade da animação

            for dy, dx in direcoes:
                ny, nx = y + dy, x + dx
                if 0 <= ny < ALTURA and 0 <= nx < LARGURA:
                    if self.labirinto[ny][nx] in (' ', 'E') and (ny, nx) not in visitados:
                        fila.append(((ny, nx), caminho + [(ny, nx)]))
                        visitados.add((ny, nx))


# Rodar aplicação
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Labirinto com Geração Aleatória + Animação BFS")
    app = LabirintoApp(root)
    root.mainloop()
