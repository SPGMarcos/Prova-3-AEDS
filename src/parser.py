"""Parser streaming para instancias reais grandes de grafos."""

import re
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path

from src.graph import Grafo, Peso

COMMENT_PREFIXES = ("#", "%", "//", "c ")
NUMBER_PATTERN = re.compile(r"[-+]?\d+(?:[.]\d+)?")
PROGRESS_INTERVAL = 100_000


@dataclass
class EstatisticasLeitura:
    """Metadados coletados durante a leitura de uma instancia."""

    file_path: str
    vertices: int = 0
    edges: int = 0
    invalid_lines: int = 0
    skipped_lines: int = 0
    max_vertex: int = 0
    detected_format: str = "desconhecido"
    processed_lines: int = 0


def _split_tokens(line: str) -> list[str]:
    """Divide uma linha sem depender de carregar o arquivo completo."""
    if "\t" in line:
        return [token for token in line.split("\t") if token]
    if ";" in line:
        return [token for token in line.split(";") if token]
    if "," in line:
        return [token for token in line.replace(",", " ").split() if token]
    return line.split()


def _is_comment_or_header(line: str) -> bool:
    """Detecta comentarios e cabecalhos conhecidos sem arestas."""
    lowered = line.lower()
    if lowered.startswith(COMMENT_PREFIXES):
        return True
    if lowered.startswith(
        ("p ", "vertices", "arestas", "source", "origem", "from", "tail", "node")
    ):
        return True
    return False


def _analisar_vertice(token: str) -> int:
    """Converte um token numerico em identificador inteiro de vertice."""
    if not re.fullmatch(r"[-+]?\d+", token):
        raise ValueError("identificador de vertice invalido")
    vertex = int(token)
    if vertex < 0:
        raise ValueError("identificador de vertice invalido")
    return vertex


def _analisar_peso(token: str) -> Peso:
    """Converte um token numerico em peso positivo."""
    if not NUMBER_PATTERN.fullmatch(token):
        raise ValueError("peso invalido")
    weight = float(token)
    if weight <= 0:
        raise ValueError("peso deve ser positivo")
    return weight


def _edge_columns(tokens: list[str]) -> tuple[str, str, str]:
    """Escolhe origem, destino e peso a partir dos numeros da linha."""
    if tokens and tokens[0].lower() in {"a", "e", "edge", "arc"}:
        tokens = tokens[1:]

    numeric_tokens = [token for token in tokens if NUMBER_PATTERN.fullmatch(token)]
    if len(numeric_tokens) < 3:
        raise ValueError("linha sem tres valores numericos")

    return numeric_tokens[0], numeric_tokens[1], numeric_tokens[2]


def _detect_separator(sample_line: str) -> str:
    """Identifica o separador mais provavel a partir da primeira aresta valida."""
    if "\t" in sample_line:
        return "tab"
    if ";" in sample_line:
        return "ponto-e-virgula"
    if "," in sample_line:
        return "virgula"
    return "espaco"


def _describe_format(sample_line: str) -> str:
    """Resume o formato detectado para logs."""
    separator = _detect_separator(sample_line)
    parts = sample_line.split(maxsplit=1)
    prefix = parts[0].lower() if parts else ""
    kind = "DIMACS/arco" if prefix in {"a", "e", "edge", "arc"} else "numerico"
    return f"{kind}, separador={separator}, colunas=origem destino peso"


def _adicionar_aresta_lida(
    grafo: defaultdict[int, list[tuple[int, Peso]]],
    origem: int,
    destino: int,
    peso: Peso,
) -> None:
    """Adiciona aresta mantendo vertices sem saida na lista de adjacencia."""
    grafo[origem].append((destino, peso))
    grafo[destino]


def analisar_arquivo_grafo_com_estatisticas(
    file_path: str,
) -> tuple[Grafo, EstatisticasLeitura]:
    """Le uma instancia grande linha por linha e retorna grafo e estatisticas."""
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"Arquivo nao encontrado: {file_path}")
    if path.stat().st_size == 0:
        raise ValueError(f"Arquivo vazio: {file_path}")

    grafo: defaultdict[int, list[tuple[int, Peso]]] = defaultdict(list)
    estatisticas = EstatisticasLeitura(file_path=str(file_path))
    primeira_linha_aresta = ""

    print(f"[INFO] Lendo {path.name}...")
    with open(path, "r", encoding="utf-8", errors="ignore") as file:
        for line_number, line in enumerate(file, start=1):
            estatisticas.processed_lines = line_number
            stripped = line.strip()
            if not stripped or _is_comment_or_header(stripped):
                estatisticas.skipped_lines += 1
            else:
                tokens = _split_tokens(stripped)

                try:
                    source_token, destination_token, weight_token = _edge_columns(tokens)
                    origem = _analisar_vertice(source_token)
                    destino = _analisar_vertice(destination_token)
                    peso = _analisar_peso(weight_token)
                    _adicionar_aresta_lida(grafo, origem, destino, peso)
                    estatisticas.edges += 1
                    estatisticas.max_vertex = max(estatisticas.max_vertex, origem, destino)
                    if not primeira_linha_aresta:
                        primeira_linha_aresta = stripped
                        estatisticas.detected_format = _describe_format(primeira_linha_aresta)
                        print(
                            f"[INFO] Separador detectado: "
                            f"{_detect_separator(primeira_linha_aresta)}"
                        )
                except ValueError as error:
                    estatisticas.invalid_lines += 1
                    if estatisticas.invalid_lines <= 5:
                        print(
                            f"[WARN] Linha {line_number} ignorada em {path.name}: {error}"
                        )

            if estatisticas.processed_lines % PROGRESS_INTERVAL == 0:
                print(
                    f"[INFO] Processadas {estatisticas.processed_lines} linhas "
                    f"({estatisticas.edges} arestas validas)..."
                )

    if not grafo:
        raise ValueError(f"Nenhuma aresta valida foi lida de {file_path}.")

    estatisticas.vertices = len(grafo)
    print(f"[INFO] Vertices encontrados: {estatisticas.vertices}")
    print(f"[INFO] Arestas encontradas: {estatisticas.edges}")
    print(f"[INFO] Maior vertice encontrado: {estatisticas.max_vertex}")
    return dict(grafo), estatisticas


def analisar_arquivo_grafo(file_path: str) -> Grafo:
    """Le uma instancia real e retorna somente a lista de adjacencia."""
    grafo, _ = analisar_arquivo_grafo_com_estatisticas(file_path)
    return grafo


def definir_origem_destino(grafo: Grafo, maior_vertice: int | None = None) -> tuple[int, int]:
    """Usa o vertice 1 como origem e o maior vertice como destino."""
    origem = 1
    destino = maior_vertice if maior_vertice is not None else max(grafo)
    if origem not in grafo:
        raise ValueError("A instancia nao possui o vertice de origem 1.")
    if destino not in grafo:
        raise ValueError("A instancia nao possui o vertice de destino calculado.")
    return origem, destino


# Aliases mantidos para compatibilidade.
ParseStats = EstatisticasLeitura
parse_graph_file_with_stats = analisar_arquivo_grafo_com_estatisticas
parse_graph_file = analisar_arquivo_grafo
infer_real_task_vertices = definir_origem_destino
