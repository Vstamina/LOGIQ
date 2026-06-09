"""
LOGIQ 2.0 — QAOA simulado local.

Este módulo executa uma simulação statevector pequena de QAOA, sem depender de serviços externos.
Ele não substitui o motor operacional de rotas. Serve para demonstrar, em cenário reduzido,
como a lógica do problema pode ser preparada para uma camada quântica real/simulada.
"""

from __future__ import annotations

import itertools
import math
from dataclasses import dataclass
from typing import Dict, Iterable, List, Tuple

import numpy as np
import pandas as pd


@dataclass
class QAOAResult:
    nodes: List[str]
    edges: List[Tuple[str, str, float]]
    alpha: float
    beta_weight: float
    gamma: float
    mixer_beta: float
    expected_cost: float
    exact_bitstring: str
    exact_cost: float
    qaoa_bitstring: str
    qaoa_cost: float
    qaoa_probability: float
    worst_valid_cost: float
    closeness_percent: float
    probabilities: pd.DataFrame
    valid_ranking: pd.DataFrame


def _weighted_edge_cost(data: Dict, alpha: float, beta_weight: float) -> float:
    return float(alpha * data.get("tempo_min", 0.0) + beta_weight * data.get("co2", 0.0))


def prepare_reduced_problem(graph, hub: str, max_nodes: int = 4, alpha: float = 0.5, beta_weight: float = 0.5):
    """
    Escolhe um cenário reduzido para simulação QAOA.
    Por padrão: Base/Hub + até 3 pontos de entrega.
    """
    if hub not in graph.nodes:
        hub = list(graph.nodes)[0]

    other_nodes = [n for n in graph.nodes if n != hub]
    chosen_nodes = [hub] + other_nodes[: max_nodes - 1]

    edges = []
    for u, v in itertools.combinations(chosen_nodes, 2):
        if graph.has_edge(u, v):
            data = graph[u][v]
            weight = _weighted_edge_cost(data, alpha, beta_weight)
            edges.append((u, v, float(weight)))

    return chosen_nodes, edges


def bitstring_for_index(index: int, n: int) -> str:
    return format(index, f"0{n}b")


def is_valid_bitstring(bitstring: str) -> bool:
    """Evita as combinações triviais em que todos os pontos ficam no mesmo grupo."""
    return len(set(bitstring)) > 1


def compute_costs(nodes: List[str], edges: List[Tuple[str, str, float]]) -> np.ndarray:
    """
    Custo tipo corte: soma o peso das arestas que ligam grupos diferentes.
    Este é um problema reduzido e demonstrativo, próximo à lógica Max-Cut/Ising.
    """
    n = len(nodes)
    idx = {node: i for i, node in enumerate(nodes)}
    costs = np.zeros(2**n, dtype=float)

    for state in range(2**n):
        bits = bitstring_for_index(state, n)
        c = 0.0
        for u, v, w in edges:
            if bits[idx[u]] != bits[idx[v]]:
                c += w
        costs[state] = c
    return costs


def valid_ranking_dataframe(nodes: List[str], edges: List[Tuple[str, str, float]], costs: np.ndarray) -> pd.DataFrame:
    n = len(nodes)
    idx = {node: i for i, node in enumerate(nodes)}
    records = []
    for state in range(2**n):
        bits = bitstring_for_index(state, n)
        if not is_valid_bitstring(bits):
            continue
        active_edges = []
        for u, v, _ in edges:
            if bits[idx[u]] != bits[idx[v]]:
                active_edges.append(f"{u} ↔ {v}")
        records.append({
            "bitstring": bits,
            "custo_ponderado": float(costs[state]),
            "arestas_ativadas": ", ".join(active_edges),
        })
    df = pd.DataFrame(records).sort_values("custo_ponderado").reset_index(drop=True)
    df.insert(0, "opcao", [f"Combinação {i+1}" for i in range(len(df))])
    return df


def apply_mixer_layer(state: np.ndarray, mixer_beta: float, n: int) -> np.ndarray:
    """Aplica U_B(beta)=prod_j exp(-i beta X_j) no statevector."""
    c = math.cos(mixer_beta)
    s = -1j * math.sin(mixer_beta)
    new_state = state.copy()

    for qubit in range(n):
        updated = new_state.copy()
        step = 1 << qubit
        for base in range(0, 2**n, step * 2):
            for offset in range(step):
                i0 = base + offset
                i1 = i0 + step
                a0 = new_state[i0]
                a1 = new_state[i1]
                updated[i0] = c * a0 + s * a1
                updated[i1] = s * a0 + c * a1
        new_state = updated
    return new_state


def qaoa_state(costs: np.ndarray, gamma: float, mixer_beta: float, p: int = 1) -> np.ndarray:
    n = int(math.log2(len(costs)))
    state = np.ones(2**n, dtype=complex) / math.sqrt(2**n)

    for _ in range(p):
        state = state * np.exp(-1j * gamma * costs)
        state = apply_mixer_layer(state, mixer_beta, n)
    return state


def expected_cost(state: np.ndarray, costs: np.ndarray) -> float:
    probs = np.abs(state) ** 2
    return float(np.sum(probs * costs))


def grid_search_qaoa(costs: np.ndarray, p: int = 1, grid_points: int = 15):
    """
    Busca simples de parâmetros. É suficiente para MVP e evita dependências pesadas.
    """
    best = None
    gammas = np.linspace(0, 2 * math.pi, grid_points)
    betas = np.linspace(0, math.pi, grid_points)

    for gamma in gammas:
        for mixer_beta in betas:
            state = qaoa_state(costs, gamma, mixer_beta, p=p)
            value = expected_cost(state, costs)
            if best is None or value < best[0]:
                best = (value, gamma, mixer_beta, state)
    return best


def probabilities_dataframe(state: np.ndarray, costs: np.ndarray) -> pd.DataFrame:
    n = int(math.log2(len(costs)))
    probs = np.abs(state) ** 2
    records = []
    for idx, prob in enumerate(probs):
        bits = bitstring_for_index(idx, n)
        records.append({
            "bitstring": bits,
            "probabilidade": float(prob),
            "custo_ponderado": float(costs[idx]),
            "valida": is_valid_bitstring(bits),
        })
    df = pd.DataFrame(records).sort_values("probabilidade", ascending=False).reset_index(drop=True)
    df.insert(0, "ranking", [f"Estado {i+1}" for i in range(len(df))])
    return df


def run_qaoa_demo(graph, hub: str, alpha: float = 0.5, beta_weight: float = 0.5, max_nodes: int = 4, p: int = 1, grid_points: int = 15) -> QAOAResult:
    total = alpha + beta_weight
    if total == 0:
        alpha_norm, beta_norm = 0.5, 0.5
    else:
        alpha_norm, beta_norm = alpha / total, beta_weight / total

    nodes, edges = prepare_reduced_problem(graph, hub, max_nodes=max_nodes, alpha=alpha_norm, beta_weight=beta_norm)
    costs = compute_costs(nodes, edges)
    ranking = valid_ranking_dataframe(nodes, edges, costs)

    exact_bitstring = str(ranking.iloc[0]["bitstring"])
    exact_cost = float(ranking.iloc[0]["custo_ponderado"])
    worst_valid_cost = float(ranking["custo_ponderado"].max())

    value, gamma, mixer_beta, state = grid_search_qaoa(costs, p=p, grid_points=grid_points)
    probs_df = probabilities_dataframe(state, costs)

    valid_probs = probs_df[probs_df["valida"]].copy()
    valid_probs = valid_probs.sort_values(["probabilidade", "custo_ponderado"], ascending=[False, True]).reset_index(drop=True)
    qaoa_bitstring = str(valid_probs.iloc[0]["bitstring"])
    qaoa_cost = float(valid_probs.iloc[0]["custo_ponderado"])
    qaoa_probability = float(valid_probs.iloc[0]["probabilidade"])

    if worst_valid_cost == exact_cost:
        closeness = 100.0
    else:
        closeness = 100.0 * (worst_valid_cost - qaoa_cost) / (worst_valid_cost - exact_cost)
    closeness = max(0.0, min(100.0, closeness))

    return QAOAResult(
        nodes=nodes,
        edges=edges,
        alpha=alpha_norm,
        beta_weight=beta_norm,
        gamma=float(gamma),
        mixer_beta=float(mixer_beta),
        expected_cost=float(value),
        exact_bitstring=exact_bitstring,
        exact_cost=exact_cost,
        qaoa_bitstring=qaoa_bitstring,
        qaoa_cost=qaoa_cost,
        qaoa_probability=qaoa_probability,
        worst_valid_cost=worst_valid_cost,
        closeness_percent=closeness,
        probabilities=probs_df,
        valid_ranking=ranking,
    )
