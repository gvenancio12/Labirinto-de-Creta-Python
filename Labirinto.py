import sys
import random
import heapq
"""""
    Integrantes: Guilherme Venâncio, Antônio Helmano e João Miguel
"""""
class Labirinto:
    """
        Inicializa o grafo com base no arquivo lido.
        O grafo é armazenado como uma lista de adjacências.
    """
    
    def __init__(self, arquivo_path):
        # O grafo usa um dicionário (lista de adjacências) por ser eficiente em memória
        # para labirintos, que geralmente são grafos esparsos.
        self.grafo = {}
        self.num_vertices = 0
        self._ler_arquivo(arquivo_path)

    def _ler_arquivo(self, arquivo_caminho):
        # Método para ler o arquivo de txt e construir construir o grafo(labirinto).
        try:
            with open(arquivo_caminho, 'r') as f:
                self.num_vertices = int(f.readline().strip())
                num_arestas = int(f.readline().strip())
                
                # Inicializa a estrutura do grafo para cada vértice
                for i in range(self.num_vertices):
                    self.grafo[i] = []
                
                # Adiciona as arestas de forma bidirecional(o grafo não direcionado)
                for _ in range(num_arestas):
                    u, v, peso = map(int, f.readline().strip().split())
                    # Os elementos da lista de adjacências são tuplas (aresta, peso)
                    # que armazenam o vertice vizinho e o peso para chegar a ele.
                    self.grafo[u].append((v, peso))
                    self.grafo[v].append((u, peso))
                
                # Inicializa os parâmetros da simulação
                self.entrada = int(f.readline().strip())
                self.saida = int(f.readline().strip())
                self.pos_minotauro_inicial = int(f.readline().strip())
                self.percepcao_minotauro = int(f.readline().strip())
                self.tempo_maximo = int(f.readline().strip())
        except FileNotFoundError:
            print("Erro: O arquivo não foi encontrado.")
            sys.exit(1)
        except Exception as e:
            print("Ocorreu um erro ao ler o arquivo.")
            sys.exit(1)
    
    def dijkstra(self, inicio):
        """
        Executa o Algoritmo de Dijkstra a partir de um vértice de início.
        É usado passando a posição do minotaurto para farejar o jogador
        
        Retorna dois dicionários(estrutura com a melhor eficiência):
        1 - distancias: o menor custo para chegar em cada vértice a partir do início.
        2 - predecessores: permite reconstruir o caminho mais curto.
        """
        
        
        distancias = {vertice: float('inf') for vertice in range(self.num_vertices)}
        predecessores = {vertice: None for vertice in range(self.num_vertices)}
        distancias[inicio] = 0
        
        # Fila de prioridade (min-heap) para otimizar a busca pelo vértice mais próximo.
        # A fila de prioridade armazenará tuplas (distancia, vertice)
        fila_prioridade = [(0, inicio)]
        
        while fila_prioridade:
            distancia_atual, vertice_atual = heapq.heappop(fila_prioridade)
            
            # Ignora caminhos que já foram relaxados por outros mais curtos
            if distancia_atual > distancias[vertice_atual]:
                continue
            
             # Relaxamento de arestas: verifica se um novo caminho é mais curto
            for vizinho, peso in self.grafo[vertice_atual]:
                nova_distancia = distancia_atual + peso
                
                # Se encontramos um caminho mais curto para o vizinho
                # atualiza os dicionários de distancias e predecessores.
                if nova_distancia < distancias[vizinho]:
                    distancias[vizinho] = nova_distancia
                    predecessores[vizinho] = vertice_atual
                    heapq.heappush(fila_prioridade, (nova_distancia, vizinho))
                    
        return distancias, predecessores

    # Método para reconstruir um caminho.
    # Necessário para sabermos o caminho que o minotauro irá seguir
    # e os vértices que irá pular.
    def reconstruir_caminho(self, predecessores, inicio, fim):
        caminho = []
        vertice_atual = fim
        while vertice_atual is not None:
            caminho.append(vertice_atual)
            if vertice_atual == inicio:
                break
            vertice_atual = predecessores.get(vertice_atual)
        
        # Se não há caminho
        if caminho[-1] != inicio:
            return [] # Retorna caminho vazio

        return caminho[::-1] # Retorna o caminho do fim para o começo, então invertemos.

class Simulacao:
    def __init__(self, labirinto):
        self.labirinto = labirinto
        
        # Atributos do jogador
        self.pos_jogador = self.labirinto.entrada
        self.tempo_jogador = 0
        self.caminho_jogador = [self.labirinto.entrada] # Simula o novelo de lã para caso fique encurralado
        self.visitados_jogador = {self.labirinto.entrada} # Simula a memória para não visitar o mesmo lugar
        # Novamete um dicionario em visitados_jogador pois nao permite vertices repetidos e é mais eficiente para checar.
        
        # Atributos do minotaurto
        self.pos_minotauro = self.labirinto.pos_minotauro_inicial
        self.caminho_perseguicao_minotauro = [] 
        
        # Atributos da simulação
        self.turno = 0
        self.em_perseguicao = False
        self.turno_deteccao = None
        

    def _mover_jogador(self):
        """
            Executa um passo do jogador, usando a lógica de DFS aleatório.
        
        """
        
        vertice_atual = self.pos_jogador
        
        # Criamos uma cópia da lista de vizinhos
        vizinhos_disponiveis = list(self.labirinto.grafo[vertice_atual])
        random.shuffle(vizinhos_disponiveis) # Embaralhamos para garantir a aleatóriedade
        
        # Procura por um vizinho ainda não visitado
        proximo_movimento = None
        for vizinho, peso in vizinhos_disponiveis:
            if vizinho not in self.visitados_jogador:
                proximo_movimento = (vizinho, peso)
                break # Encontrou o próximo passo aleatório
        
        # Se tiver um vertice nao vititado, avança atualizando os dados necessários
        if proximo_movimento: 
            novo_vertice, peso = proximo_movimento # Descarrega as informações do próximo movimento 
            self.pos_jogador = novo_vertice # Atualiza a posição do jogador
            self.tempo_jogador += peso # Soma o peso ao tempo
            self.caminho_jogador.append(novo_vertice) # Adiciona o vertice ao novelo de lã
            self.visitados_jogador.add(novo_vertice) # Adicona o vertice ao conjunto de vertices visitados
            print(f"Turno {self.turno}: Jogador avança para o vértice {novo_vertice} (custo: {peso}). Tempo total: {self.tempo_jogador}")
        
        else: # Se ficar encurrlado, volta os vertices
            if len(self.caminho_jogador) > 1:
                self.caminho_jogador.pop()
                vertice_anterior = self.caminho_jogador[-1]
                
                peso_retorno = 0 # Calcula o custo do retorno
                for vizinho, peso in self.labirinto.grafo[vertice_atual]:
                    if vizinho == vertice_anterior:
                        peso_retorno = peso
                        break
                
                self.pos_jogador = vertice_anterior
                self.tempo_jogador += peso_retorno
                print(f"Turno {self.turno}: Jogador está em um beco sem saída. Retornando para {vertice_anterior} (custo: {peso_retorno}). Tempo total: {self.tempo_jogador}")
            else:
                print(f"Turno {self.turno}: Jogador está preso na entrada e não tem para onde ir.")

    # Movimento padrão do minotauro quando não está perseguindo, completamente aleatório
    def _mover_minotauro_aleatorio(self):
        vizinhos = self.labirinto.grafo[self.pos_minotauro]
        if vizinhos:
            proximo_vertice, _ = random.choice(vizinhos)
            self.pos_minotauro = proximo_vertice
            print(f"Turno {self.turno}: Minotauro move-se aleatoriamente para {self.pos_minotauro}")

    # Lógica para movimentação do minotauro
    def _mover_minotauro(self):
        # Roda Dijkstra para farejar o jogador
        distancias, predecessores = self.labirinto.dijkstra(self.pos_minotauro)
        distancia_ate_jogador = distancias[self.pos_jogador] 

        # Decidir se entra em modo de perseguição
        if distancia_ate_jogador <= self.labirinto.percepcao_minotauro:
            if not self.em_perseguicao:
                print(f"Turno {self.turno}: ALERTA! O Minotauro detectou o jogador a uma distância de {distancia_ate_jogador}!")
                self.em_perseguicao = True
                self.turno_deteccao = self.turno

            # reconstroi o caminho até o jogador jogador
            caminho_para_jogador = self.labirinto.reconstruir_caminho(predecessores, self.pos_minotauro, self.pos_jogador)
            
            # Move dois vértices por vez 
            if len(caminho_para_jogador) > 2: # Se tiver 2 vertices até o jogador
                self.pos_minotauro = caminho_para_jogador[2]
                movimento = caminho_para_jogador[:3]
            elif len(caminho_para_jogador) > 1: # Se tiver só um vertice, pula um
                self.pos_minotauro = caminho_para_jogador[1]
                movimento = caminho_para_jogador[:2]
            else: # Já está no mesmo vértice ou do lado
                movimento = [] # movimento[] é apenas para printar quais vertices ele pulou nesse turno

            print(f"Turno {self.turno}: Minotauro PERSEGUE o jogador. Movendo-se para {self.pos_minotauro} através de {movimento}")
            if self.em_perseguicao:
                self.caminho_perseguicao_minotauro.append(self.pos_minotauro)

        else:
            # Se não detectou ou o jogador saiu do alcance, move-se aleatoriamente
            self.em_perseguicao = False
            self._mover_minotauro_aleatorio()

    def run(self): # Loop principal do jogo
        print("--- INÍCIO DA SIMULAÇÃO ---")
        print(f"Jogador começa em {self.pos_jogador}, Saída em {self.labirinto.saida}")
        print(f"Minotauro começa em {self.pos_minotauro}")
        print(f"Tempo máximo: {self.labirinto.tempo_maximo}\n")

        while True:
            self.turno += 1 # Contagem dos turnos
            self._mover_jogador() # Jogador se move
            self._mover_minotauro() # Minotauro se move
            print("-" * 20)

            #Se o jogador está na saída, ganha
            if self.pos_jogador == self.labirinto.saida:
                self.gerar_relatorio_final("vitoria")
                break
            
            # Se o minotauro alcançar o jogador, 99% de chance de capturar 
            if self.pos_jogador == self.pos_minotauro:
                if random.random() <= 0.01:
                    self.gerar_relatorio_final("vitoria_sorte")
                else:
                    self.gerar_relatorio_final("derrota_captura")
                break
            
            # Se o tempo acabar, perde
            if self.tempo_jogador >= self.labirinto.tempo_maximo:
                self.gerar_relatorio_final("derrota_tempo")
                break
            

    # Método que gera o relatório
    def gerar_relatorio_final(self, resultado):
        print("\n--- FIM DA SIMULAÇÃO: RELATÓRIO ---")
        if resultado == "vitoria":
            print("Resultado: O prisioneiro escapou!")
        elif resultado == "derrota_captura":
            print(f"Resultado: O prisioneiro morreu. Foi capturado pelo Minotauro no vértice {self.pos_jogador}.")
        elif resultado == "derrota_tempo":
            print(f"Resultado: O prisioneiro morreu. A comida acabou.")
        elif resultado == "vitoria_sorte":
             print(f"Resultado: O prisioneiro sobreviveu! Em um encontro no vértice {self.pos_jogador}, ele derrotou o Minotauro.")

        tempo_restante = self.labirinto.tempo_maximo - self.tempo_jogador
        print(f"Tempo restante até acabar a comida: {max(0, tempo_restante)}")
        print(f"Sequência de vértices visitados pelo prisioneiro: {self.caminho_jogador}")
        
        if self.turno_deteccao:
            print(f"Momento da detecção do prisioneiro: Turno {self.turno_deteccao}")
            if resultado == "derrota_captura":
                print(f"Momento em que o Minotauro o alcançou: Turno {self.turno}")
            print(f"Caminho percorrido pelo Minotauro durante a perseguição: {self.caminho_perseguicao_minotauro}")
        else:
            print("O prisioneiro nunca foi detectado pelo Minotauro.")


# Coloque o diretório de onde esta seu arquivo txt e adicione barra inversa '\' em cada barra já existente.
meu_labirinto = Labirinto('C:\\Users\\Guilherme\\Desktop\\Labirinto-de-Creta-Python\\ExemploDeGrafo.txt')
simulacao = Simulacao(meu_labirinto)
simulacao.run()