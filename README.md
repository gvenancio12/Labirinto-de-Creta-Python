# Labirinto-de-Creta-Python

Neste projeto da disciplina de **Algoritmos em Grafos**, utilizamos a estrutura de grafos para representar e simular o mito do labirinto de Creta, onde um prisioneiro tenta escapar de um Minotauro.

## 🌟 Visão Geral do Projeto

O projeto modela o labirinto como um grafo não-direcionado e ponderado. Os vértices representam as câmaras ou cruzamentos, e as arestas representam os corredores, com pesos indicando o custo de tempo ou distância para percorrê-los.

O núcleo da simulação envolve a movimentação e a interação entre o **Prisioneiro** (Jogador) e o **Minotauro**, utilizando o algoritmo de Dijkstra para a lógica de perseguição.

## 🛠️ Detalhes da Implementação

### Estrutura de Grafos

O labirinto é representado por um **Grafo Não-Direcionado** onde:
* **Vértices:** Numerados sequencialmente (ex: 0 a N-1).
* **Arestas:** Armazenadas em uma lista de adjacência, contendo o vértice vizinho e o peso (custo) da aresta.

### Algoritmos e Lógica de Movimentação

| Entidade | Algoritmo/Lógica | Descrição |
| :--- | :--- | :--- |
| **Prisioneiro (Jogador)** | **Busca em Profundidade (Improvisada)** | O jogador tenta se mover para um vértice não visitado. Se ficar encurralado (beco sem saída), ele retrocede para o vértice anterior em seu caminho. |
| **Minotauro** | **Dijkstra + Lógica de Perseguição** | 1. **Detecção:** O Minotauro executa o Algoritmo de Dijkstra para calcular a distância mais curta até a posição atual do jogador. 2. **Perseguição:** Se a distância for menor ou igual à sua `percepcao_minotauro`, ele entra em modo de perseguição e se move **dois vértices** (passos) por vez na direção do jogador pelo caminho mais curto. 3. **Aleatório:** Caso contrário, ele se move para um vizinho aleatório. |

### Condições de Fim de Jogo

O jogo termina quando uma das seguintes condições é satisfeita:
1.  **Vitória:** O prisioneiro alcança o vértice de `saida`.
2.  **Derrota (Captura):** O Minotauro alcança o mesmo vértice que o prisioneiro (99% de chance de captura).
3.  **Derrota (Tempo):** O tempo total do jogador excede o `tempo_maximo` (simulando, por exemplo, o fim dos suprimentos).

---

## 💻 Como Executar

### Pré-requisitos
Apenas o Python é necessário para executar o projeto.

### 1. Estrutura do Arquivo

O script espera que o arquivo de código (`Labirinto.py`) e o arquivo de entrada (`ExemploDeGrafo.txt`) estejam configurados corretamente. Recomenda-se a seguinte estrutura:

### 2. Configuração do Caminho

No final do arquivo `Labirinto.py`, certifique-se de que o caminho para o arquivo de entrada esteja correto na sua máquina.

```python
# Mude este caminho para o local onde seu arquivo ExemploDeGrafo.txt está
# Coloque o diretório de onde esta seu arquivo txt e adicione barra inversa '\' em cada barra ja existente.
meu_labirinto = Labirinto('./ExemploDeGrafo.txt') 
simulacao = Simulacao(meu_labirinto)
simulacao.run()
