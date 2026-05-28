# Comparação de Algoritmos de Caminho Mínimo 🚗📊

Dijkstra + Heurística Gulosa + Benchmarks + Grafos Direcionados

Projeto acadêmico desenvolvido para análise e comparação entre o algoritmo de Dijkstra e uma heurística gulosa aplicados ao problema de caminho mínimo em grafos direcionados ponderados.

O sistema realiza:

* Geração automática de grafos completos;
* Execução dos algoritmos;
* Contagem de comparações;
* Benchmarks de desempenho;
* Leitura de grandes instâncias reais;
* Geração de gráficos comparativos.

---

# 📌 Visão Geral

O projeto compara duas abordagens para o problema de caminho mínimo:

## 🔹 Algoritmo de Dijkstra

Algoritmo clássico de caminho mínimo que garante a solução ótima em grafos com pesos positivos.

## 🔹 Heurística Gulosa

Estratégia baseada na escolha local da menor aresta disponível, utilizada como comparação educacional e de desempenho.

O objetivo é analisar:

* Crescimento do número de comparações;
* Diferenças de complexidade;
* Qualidade das soluções;
* Comportamento em grafos grandes.

---

# 🎯 Objetivos do Projeto

* Implementar o algoritmo de Dijkstra;
* Implementar uma heurística gulosa;
* Comparar desempenho entre abordagens;
* Medir número de comparações;
* Gerar gráficos de crescimento;
* Executar testes em instâncias reais;
* Facilitar análise acadêmica dos algoritmos.

---

# 🧠 Arquitetura do Projeto

Fluxo principal:

Geração/Leitura do Grafo → Execução dos Algoritmos → Benchmark → Coleta de Métricas → Geração de Gráficos

---

# 📁 Estrutura do Projeto

```text
project/
│
├── data/
│
├── src/
│   ├── graph.py
│   ├── algorithms.py
│   ├── benchmark.py
│   ├── plotting.py
│   └── parser.py
│
├── results/
│   └── graphs/
│
├── main.py
├── README.md
└── requirements.txt
```

---

# ⚙️ Principais Funcionalidades

## 🔹 Geração de Grafos

Criação automática de grafos:

* completos;
* direcionados;
* ponderados;
* com pesos positivos aleatórios.

Os pesos são gerados utilizando:

```python
random.randint(1, 100)
```

---

## 🔹 Algoritmo de Dijkstra

Implementação eficiente utilizando:

* `heapq`;
* lista de adjacência;
* relaxamento de arestas;
* fila de prioridade.

O algoritmo retorna:

* menores distâncias;
* caminhos encontrados;
* número de comparações.

### ✔ Características

* Garante caminho mínimo;
* Funciona com pesos positivos;
* Excelente robustez.

---

## 🔹 Heurística Gulosa

A heurística gulosa seleciona sempre a menor aresta local disponível.

### ✔ Características

* Simples;
* Rápida;
* Fácil de entender;
* Não garante solução ótima.

O algoritmo evita ciclos utilizando controle de vértices visitados.

---

# 📊 Benchmarks e Testes

Os benchmarks geram grafos completos variando:

```text
4, 5, 6, ..., N
```

Para cada grafo:

* uma origem aleatória é escolhida;
* os algoritmos são executados;
* comparações são contabilizadas;
* tempo de execução é medido;
* memória utilizada pode ser monitorada.

---

# 📈 Gráficos Gerados

Os gráficos são salvos em:

```text
results/graphs/
```

Arquivos gerados:

* `dijkstra_comparisons.png`
* `greedy_comparisons.png`
* `algorithm_comparison.png`

Os gráficos mostram:

* crescimento do número de comparações;
* comportamento dos algoritmos;
* diferença de complexidade.

---

# 🌎 Instâncias Reais

O sistema suporta execução em grandes redes viárias:

* NY_dist.txt
* NY_time.txt
* SF_dist.txt
* SF_time.txt

## 📌 Características das Instâncias

### Nova York

* 264.346 vértices
* 733.846 arestas

### San Francisco

* 321.270 vértices
* 800.172 arestas

O parser realiza leitura otimizada linha por linha para reduzir consumo de memória.

---

# 🔍 Contagem de Comparações

O projeto contabiliza comparações realizadas internamente pelos algoritmos.

## Dijkstra

São contabilizadas:

* verificações de relaxamento;
* comparações de distância;
* controle de vértices visitados;
* atualizações da fila de prioridade.

## Heurística Gulosa

São contabilizadas:

* escolha da menor aresta local;
* verificações de visitados;
* decisões de avanço no caminho.

---

# 🚀 Como Executar

## Instalar Dependências

```bash
pip install -r requirements.txt
```

---

## Executar o Projeto

```bash
python main.py
```

---

## Alterar Número Máximo de Vértices

Linux/macOS:

```bash
MAX_VERTICES=100 python main.py
```

PowerShell:

```powershell
$env:MAX_VERTICES=100
python main.py
```

---

# 📡 Como Adicionar Instâncias

Coloque os arquivos dentro da pasta:

```text
data/
```

Formato esperado:

```text
origem destino peso
```

Exemplo:

```text
1 2 10
2 5 7
5 9 3
```

---

# 📊 Comparação Entre Algoritmos

## 🔹 Dijkstra

✔ Garante solução ótima
✔ Mais robusto
✔ Usa fila de prioridade
✔ Melhor precisão

❌ Pode possuir maior custo computacional

---

## 🔹 Heurística Gulosa

✔ Simples
✔ Fácil implementação
✔ Menor complexidade local

❌ Não garante menor caminho
❌ Sensível à estrutura do grafo

---

# 📈 Análise dos Resultados

Em grafos completos, o número de arestas cresce rapidamente:

```text
N × (N - 1)
```

Isso aumenta:

* número de comparações;
* custo computacional;
* uso de memória.

O Dijkstra tende a possuir maior controle interno, enquanto a heurística gulosa sacrifica qualidade da solução em troca de simplicidade.

---

# 🛡️ Características Técnicas

* Estrutura enxuta;
* Código modular;
* Lista de adjacência;
* Uso de `heapq`;
* Parser otimizado;
* Benchmarks automatizados;
* Geração automática de gráficos;
* Código comentado;
* Estrutura acadêmica simplificada.

---

# 👨‍💻 Autor

Marcos Gabriel Ferreira Miranda

Desenvolvedor de Software | IoT | Automação Residencial e Agrícola

Belo Horizonte - MG
