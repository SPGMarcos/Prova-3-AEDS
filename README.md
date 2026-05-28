# Dijkstra x Heuristica Gulosa

## Objetivo

Este projeto compara o algoritmo de Dijkstra com uma heuristica gulosa para o problema de caminho minimo em grafo direcionado ponderado.

O trabalho considera:

- uma unica origem;
- multiplos destinos nos testes sinteticos;
- origem 1 e ultimo vertice nas instancias reais;
- contagem de comparacoes;
- geracao de graficos para o relatorio.

## Estrutura

```text
project/
|-- data/
|-- src/
|   |-- algorithms.py
|   |-- benchmark.py
|   |-- graph.py
|   |-- parser.py
|   `-- plotting.py
|-- results/
|-- main.py
|-- README.md
`-- requirements.txt
```

## Como executar

Instale a dependencia usada para gerar os graficos:

```bash
pip install -r requirements.txt
```

Execute:

```bash
python main.py
```

Por padrao, o benchmark gera grafos completos de 4 ate 30 vertices. Para mudar o valor de `N` no PowerShell:

```powershell
$env:MAX_VERTICES=100
python main.py
```

O valor maximo aceito para `N` e 1.000.000, conforme o enunciado. Esse valor e um limite superior, nao significa que o teste precise obrigatoriamente ser executado ate 1.000.000 vertices.

Como o benchmark usa grafos completos direcionados, o maior grafo possui:

```text
N * (N - 1) arestas
```

Para `N = 1.000.000`, isso passaria de 999 bilhoes de arestas, o que nao e viavel em memoria comum. Por isso o projeto deixa `N` configuravel e usa `30` como valor padrao para gerar os graficos de forma segura.

## Arquivos de entrada

Os arquivos reais devem ficar em `data/`. O programa detecta automaticamente todos os `.txt`.

Instancias esperadas:

- `NY_dist.txt`
- `NY_time.txt`
- `SF_dist.txt`
- `SF_time.txt`

O parser foi feito para arquivos grandes. Ele le linha por linha, ignora cabecalhos, comentarios, linhas vazias e linhas invalidas. Cada aresta deve ter:

```text
origem destino peso
```

Tambem sao aceitos separadores por espaco, virgula, tabulacao ou ponto-e-virgula.

## Implementacao

O grafo usa lista de adjacencia:

```text
vertice -> [(vizinho, peso), ...]
```

Essa estrutura evita matriz de adjacencia e e mais adequada para as instancias reais, que possuem centenas de milhares de vertices e arestas.

### Dijkstra

O Dijkstra esta em `src/algorithms.py`, na funcao `dijkstra()`.

Ele usa fila de prioridade com `heapq`. A cada passo, remove o vertice com menor distancia conhecida e relaxa suas arestas. Como os pesos sao positivos, o algoritmo encontra o menor caminho corretamente.

### Heuristica gulosa

A heuristica gulosa esta em `src/algorithms.py`, na funcao `guloso()`.

Ela escolhe, a cada passo, a menor aresta disponivel a partir do vertice atual, sem revisitar vertices. Essa estrategia e simples e serve para comparacao, mas nao garante o menor caminho global.

## Testes sinteticos

O arquivo `src/benchmark.py` gera grafos completos direcionados com 4, 5, 6, ..., N vertices.

Para cada grafo:

- escolhe uma origem;
- usa todos os outros vertices como destino;
- executa Dijkstra;
- executa a heuristica gulosa;
- conta comparacoes;
- mede tempo e memoria de pico.

## Instancias reais

Para as instancias reais, o programa usa:

```text
origem = 1
destino = maior vertice encontrado no arquivo
```

O parser identifica o maior vertice durante a leitura, sem carregar o arquivo inteiro em memoria.

## Saidas geradas

Os graficos ficam em:

```text
results/graphs/
```

Arquivos gerados:

- `dijkstra_comparacoes.png`
- `guloso_comparacoes.png`
- `comparacao_algoritmos.png`

As tabelas de apoio para o relatorio ficam em:

- `results/comparacoes_instancias_reais.csv`
- `results/comparacoes_benchmark.csv`

## Observacao sobre a heuristica gulosa

A heuristica gulosa pode nao encontrar caminho em algumas instancias reais, mesmo quando Dijkstra encontra. Isso acontece porque a decisao local de menor aresta pode levar a um ponto sem saida. Esse comportamento e esperado para uma heuristica simples e ajuda na comparacao com o Dijkstra.
