"""Graficos comparativos com matplotlib."""

import os


def _preparar_matplotlib() -> None:
    """Configura o matplotlib para gerar PNG sem janela grafica."""
    pasta_cache = os.path.join("results", ".matplotlib_cache")
    os.makedirs(pasta_cache, exist_ok=True)
    os.environ.setdefault("MPLCONFIGDIR", pasta_cache)

    import matplotlib

    matplotlib.use("Agg")


def plotar_comparacoes(
    resultados: list[dict[str, float]],
    titulo: str,
    caminho_saida: str,
) -> None:
    """Gera grafico de vertices por comparacoes."""
    _preparar_matplotlib()
    import matplotlib.pyplot as plt

    os.makedirs(os.path.dirname(caminho_saida), exist_ok=True)
    valores_x = [int(linha["vertices"]) for linha in resultados]
    valores_y = [int(linha["comparacoes"]) for linha in resultados]

    plt.figure(figsize=(10, 6))
    plt.plot(valores_x, valores_y, marker="o", linewidth=2)
    plt.title(titulo)
    plt.xlabel("Numero de vertices")
    plt.ylabel("Numero de comparacoes")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(caminho_saida, dpi=150)
    plt.close()


def plotar_comparacao_algoritmos(
    resultados_dijkstra: list[dict[str, float]],
    resultados_guloso: list[dict[str, float]],
    caminho_saida: str,
) -> None:
    """Compara Dijkstra e guloso no mesmo grafico."""
    _preparar_matplotlib()
    import matplotlib.pyplot as plt

    os.makedirs(os.path.dirname(caminho_saida), exist_ok=True)
    x_dijkstra = [int(linha["vertices"]) for linha in resultados_dijkstra]
    y_dijkstra = [int(linha["comparacoes"]) for linha in resultados_dijkstra]
    x_guloso = [int(linha["vertices"]) for linha in resultados_guloso]
    y_guloso = [int(linha["comparacoes"]) for linha in resultados_guloso]

    plt.figure(figsize=(10, 6))
    plt.plot(x_dijkstra, y_dijkstra, marker="o", linewidth=2, label="Dijkstra")
    plt.plot(x_guloso, y_guloso, marker="s", linewidth=2, label="Guloso")
    plt.title("Comparacao de Comparacoes")
    plt.xlabel("Numero de vertices")
    plt.ylabel("Numero de comparacoes")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(caminho_saida, dpi=150)
    plt.close()


# Aliases mantidos para compatibilidade.
plot_comparisons = plotar_comparacoes
plot_algorithm_comparison = plotar_comparacao_algoritmos
