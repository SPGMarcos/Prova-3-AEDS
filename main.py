"""Pipeline principal do projeto."""

import csv
import gc
import os
import time
import tracemalloc
from pathlib import Path

from src.algorithms import dijkstra, guloso
from src.benchmark import executar_benchmark_dijkstra, executar_benchmark_guloso
from src.parser import analisar_arquivo_grafo_com_estatisticas, definir_origem_destino
from src.plotting import plotar_comparacao_algoritmos, plotar_comparacoes

PASTA_DADOS = Path("data")
PASTA_RESULTADOS = Path("results")
PASTA_GRAFICOS = PASTA_RESULTADOS / "graphs"
MAX_N = 1_000_000


def garantir_pastas() -> None:
    """Cria as pastas essenciais do projeto."""
    for pasta in (PASTA_DADOS, PASTA_RESULTADOS, PASTA_GRAFICOS):
        pasta.mkdir(parents=True, exist_ok=True)


def ler_maximo_vertices() -> int:
    """Le N do ambiente e aplica o limite academico do trabalho."""
    maximo_vertices = int(os.environ.get("MAX_VERTICES", "30"))
    if maximo_vertices < 4:
        raise ValueError("O valor de N deve ser pelo menos 4.")
    if maximo_vertices > MAX_N:
        raise ValueError(f"O valor de N deve ser no maximo {MAX_N}.")
    return maximo_vertices


def estimar_arestas_grafo_completo(maximo_vertices: int) -> int:
    """Calcula quantas arestas teria o maior grafo completo do benchmark."""
    return maximo_vertices * (maximo_vertices - 1)


def encontrar_arquivos_dados() -> list[Path]:
    """Encontra automaticamente os arquivos .txt da pasta data."""
    return sorted(caminho for caminho in PASTA_DADOS.glob("*.txt") if caminho.is_file())


def _formatar_distancia(valor: float) -> str:
    if valor == float("inf"):
        return "sem caminho"
    if valor.is_integer():
        return str(int(valor))
    return f"{valor:.6f}"


def executar_algoritmo_na_instancia(
    grafo,
    nome_arquivo: str,
    nome_algoritmo: str,
    algoritmo,
    origem: int,
    destino: int,
) -> dict[str, object]:
    """Executa um algoritmo em uma instancia real com medicoes."""
    print(f"[INFO] Executando {nome_algoritmo}...")
    tracemalloc.start()
    inicio = time.perf_counter()
    distancias, caminhos, comparacoes = algoritmo(grafo, origem, [destino])
    tempo = time.perf_counter() - inicio
    _, pico = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    distancia = distancias.get(destino, float("inf"))
    caminho = caminhos.get(destino, [])
    if distancia == float("inf") or not caminho:
        print(f"[WARN] {nome_algoritmo}: nao encontrou caminho ate {destino}.")

    print(f"[INFO] Comparacoes: {comparacoes}")
    print(f"[INFO] Tempo: {tempo:.4f}s")

    return {
        "instancia": nome_arquivo,
        "algoritmo": nome_algoritmo,
        "distancia": distancia,
        "comparacoes": comparacoes,
        "tempo_segundos": tempo,
        "memoria_kb": pico / 1024,
        "vertices_no_caminho": len(caminho),
    }


def executar_instancia_real(caminho_arquivo: Path) -> list[dict[str, object]]:
    """Executa Dijkstra e guloso em uma instancia real."""
    print(f"\n[INFO] Carregando {caminho_arquivo.name}...")
    grafo, estatisticas = analisar_arquivo_grafo_com_estatisticas(str(caminho_arquivo))
    origem, destino = definir_origem_destino(grafo, estatisticas.max_vertex)

    print(f"[INFO] Formato: {estatisticas.detected_format}")
    print(f"[INFO] Vertices: {estatisticas.vertices}")
    print(f"[INFO] Arestas: {estatisticas.edges}")
    print(f"[INFO] Linhas processadas: {estatisticas.processed_lines}")
    print(f"[INFO] Linhas ignoradas: {estatisticas.skipped_lines}")
    print(f"[INFO] Linhas invalidas: {estatisticas.invalid_lines}")
    print(f"[INFO] Origem: {origem}")
    print(f"[INFO] Destino: {destino}")

    linhas: list[dict[str, object]] = []
    for nome_algoritmo, algoritmo in (("Dijkstra", dijkstra), ("Guloso", guloso)):
        linhas.append(
            executar_algoritmo_na_instancia(
                grafo,
                caminho_arquivo.name,
                nome_algoritmo,
                algoritmo,
                origem,
                destino,
            )
        )
    return linhas


def executar_instancias_reais() -> list[dict[str, object]]:
    """Processa todas as instancias .txt disponiveis em data."""
    resultados: list[dict[str, object]] = []
    arquivos_dados = encontrar_arquivos_dados()
    if not arquivos_dados:
        print("[WARN] Nenhum arquivo .txt encontrado em data/.")
        return resultados

    for caminho_arquivo in arquivos_dados:
        try:
            resultados.extend(executar_instancia_real(caminho_arquivo))
        except (OSError, ValueError) as error:
            print(f"[WARN] Falha ao processar {caminho_arquivo.name}: {error}")
        finally:
            gc.collect()
            print(f"[INFO] Memoria liberada apos {caminho_arquivo.name}.")
    return resultados


def gerar_graficos_benchmark(
    resultados_dijkstra: list[dict[str, float]],
    resultados_guloso: list[dict[str, float]],
) -> None:
    """Gera os graficos do benchmark."""
    plotar_comparacoes(
        resultados_dijkstra,
        "Dijkstra: Vertices x Comparacoes",
        str(PASTA_GRAFICOS / "dijkstra_comparacoes.png"),
    )
    plotar_comparacoes(
        resultados_guloso,
        "Heuristica Gulosa: Vertices x Comparacoes",
        str(PASTA_GRAFICOS / "guloso_comparacoes.png"),
    )
    plotar_comparacao_algoritmos(
        resultados_dijkstra,
        resultados_guloso,
        str(PASTA_GRAFICOS / "comparacao_algoritmos.png"),
    )


def imprimir_resultados_benchmark(
    resultados_dijkstra: list[dict[str, float]],
    resultados_guloso: list[dict[str, float]],
) -> None:
    """Imprime resultados organizados dos benchmarks."""
    print("\n=== Comparacoes nos benchmarks ===")
    print("Vertices | Dijkstra | Guloso")
    for linha_dijkstra, linha_guloso in zip(resultados_dijkstra, resultados_guloso):
        print(
            f"{int(linha_dijkstra['vertices']):>8} | "
            f"{int(linha_dijkstra['comparacoes']):>8} | "
            f"{int(linha_guloso['comparacoes']):>6}"
        )


def imprimir_resultados_reais(resultados_reais: list[dict[str, object]]) -> None:
    """Imprime resultados organizados das instancias reais."""
    if not resultados_reais:
        return

    print("\n=== Resultados das instancias reais ===")
    for linha in resultados_reais:
        distancia = _formatar_distancia(float(linha["distancia"]))
        print(
            f"{linha['instancia']} | {linha['algoritmo']} | "
            f"distancia={distancia} | comparacoes={linha['comparacoes']} | "
            f"tempo={linha['tempo_segundos']:.6f}s | "
            f"memoria={linha['memoria_kb']:.2f}KB | "
            f"vertices_no_caminho={linha['vertices_no_caminho']}"
        )


def salvar_tabelas_comparacoes(
    resultados_reais: list[dict[str, object]],
    resultados_dijkstra: list[dict[str, float]],
    resultados_guloso: list[dict[str, float]],
) -> None:
    """Salva as comparacoes obtidas nos testes."""
    caminho_reais = PASTA_RESULTADOS / "comparacoes_instancias_reais.csv"
    caminho_benchmark = PASTA_RESULTADOS / "comparacoes_benchmark.csv"

    with open(caminho_reais, "w", newline="", encoding="utf-8") as arquivo:
        campos = [
            "instancia",
            "algoritmo",
            "distancia",
            "comparacoes",
            "tempo_segundos",
            "memoria_kb",
            "vertices_no_caminho",
        ]
        escritor = csv.DictWriter(arquivo, fieldnames=campos)
        escritor.writeheader()
        for linha in resultados_reais:
            linha_formatada = dict(linha)
            linha_formatada["distancia"] = _formatar_distancia(float(linha["distancia"]))
            escritor.writerow(linha_formatada)

    with open(caminho_benchmark, "w", newline="", encoding="utf-8") as arquivo:
        campos = ["vertices", "comparacoes_dijkstra", "comparacoes_guloso"]
        escritor = csv.DictWriter(arquivo, fieldnames=campos)
        escritor.writeheader()
        for linha_dijkstra, linha_guloso in zip(resultados_dijkstra, resultados_guloso):
            escritor.writerow(
                {
                    "vertices": int(linha_dijkstra["vertices"]),
                    "comparacoes_dijkstra": int(linha_dijkstra["comparacoes"]),
                    "comparacoes_guloso": int(linha_guloso["comparacoes"]),
                }
            )

    print(f"[INFO] Resultados salvos em {PASTA_RESULTADOS}.")


def main() -> None:
    """Executa benchmarks, instancias reais, graficos e impressao dos resultados."""
    garantir_pastas()
    maximo_vertices = ler_maximo_vertices()

    print("=== Dijkstra x Heuristica Gulosa ===")
    print(f"[INFO] N maximo do benchmark: {maximo_vertices}")
    print(f"[INFO] Limite do enunciado para N: {MAX_N}")
    print(
        "[INFO] Maior grafo sintetico tera "
        f"{estimar_arestas_grafo_completo(maximo_vertices)} arestas."
    )

    resultados_reais = executar_instancias_reais()

    print("\n[INFO] Executando benchmarks sinteticos...")
    resultados_dijkstra = executar_benchmark_dijkstra(maximo_vertices)
    resultados_guloso = executar_benchmark_guloso(maximo_vertices)
    gerar_graficos_benchmark(resultados_dijkstra, resultados_guloso)
    salvar_tabelas_comparacoes(resultados_reais, resultados_dijkstra, resultados_guloso)

    imprimir_resultados_benchmark(resultados_dijkstra, resultados_guloso)
    imprimir_resultados_reais(resultados_reais)

    print("\n[INFO] Pipeline concluido.")
    print(f"[INFO] Graficos: {PASTA_GRAFICOS}")


if __name__ == "__main__":
    main()
