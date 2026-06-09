import base64
import itertools
import os
import math
import unicodedata
from urllib.parse import quote_plus

import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd
import streamlit as st
from PIL import Image
from modules.qaoa_engine import run_qaoa_demo

# ============================================================
# LOGIQ MVP V5.0 — módulo 2.0 com QAOA simulado local
# ============================================================

st.set_page_config(
    page_title="LOGIQ | Otimização de Rotas",
    page_icon="🚚",
    layout="wide",
    initial_sidebar_state="expanded",
)

DEFAULT_EXCEL_PATH = os.path.join("data", "logiq_planilha_completa_mvp.xlsx")
DEFAULT_VAN_IMAGE = os.path.join("assets", "van_logiq.png")
DEFAULT_CYCLE_IMAGE = os.path.join("assets", "ciclo_decisao_logiq.png")

# ============================================================
# CSS
# ============================================================

st.markdown(
    """
    <style>
    .block-container {
        padding-top: 1.2rem;
        padding-bottom: 2rem;
        max-width: 1480px;
        padding-left: 2.2rem;
        padding-right: 2.2rem;
    }

    /* Sidebar padrão à esquerda: mais estável no Streamlit Cloud e melhor em telas menores */
    section[data-testid="stSidebar"] > div {
        background: #EEF3F8;
        padding-top: 2rem;
    }

    .hero-title {
        font-size: 58px;
        font-weight: 900;
        color: #FFFFFF;
        margin-bottom: 10px;
        line-height: 1.05;
        letter-spacing: 0.5px;
    }

    .hero-subtitle {
        font-size: 24px;
        color: #DCEAF5;
        margin-bottom: 22px;
        line-height: 1.45;
        max-width: 980px;
    }

    .chip {
        display: inline-block;
        padding: 10px 17px;
        border-radius: 999px;
        background: rgba(255,255,255,0.13);
        border: 1px solid rgba(255,255,255,0.22);
        color: #FFFFFF;
        font-size: 16px;
        font-weight: 700;
        margin-right: 10px;
        margin-bottom: 10px;
    }

    .hero-card {
        width: 100%;
        background: linear-gradient(90deg, #041A2F 0%, #0B3559 100%);
        border-radius: 30px;
        padding: 34px 40px;
        display: flex;
        align-items: center;
        gap: 34px;
        min-height: 245px;
        box-shadow: 0px 10px 30px rgba(11,31,51,0.16);
        margin-bottom: 18px;
        overflow: hidden;
    }

    .hero-van-wrap {
        flex: 0 0 280px;
        height: 175px;
        border-radius: 22px;
        background: rgba(255,255,255,0.96);
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 10px;
        box-shadow: inset 0px 0px 0px 1px rgba(255,255,255,0.35), 0px 8px 18px rgba(0,0,0,0.14);
    }

    .hero-van-wrap img {
        width: 100%;
        height: 100%;
        object-fit: contain;
        border-radius: 16px;
    }

    .hero-content {
        flex: 1;
        min-width: 0;
    }

    .status-card {
        background: #FFFBEA;
        border: 1px solid #F3D66B;
        color: #624600;
        border-radius: 18px;
        padding: 18px 22px;
        font-size: 18px;
        line-height: 1.65;
        margin-bottom: 20px;
    }

    .status-card strong {
        color: #0B1F33;
    }

    @media (max-width: 1100px) {
        .hero-card {
            flex-direction: column;
            align-items: flex-start;
        }
        .hero-van-wrap {
            width: 100%;
            max-width: 360px;
        }
    }

    .section-title {
        font-size: 36px;
        font-weight: 900;
        color: #0B1F33;
        margin-top: 12px;
        margin-bottom: 10px;
        line-height: 1.15;
    }

    .section-subtitle {
        font-size: 20px;
        color: #475569;
        margin-bottom: 22px;
        line-height: 1.55;
        max-width: 1100px;
    }

    .big-card {
        background: #FFFFFF;
        border: 1px solid #DCEAF5;
        border-radius: 20px;
        padding: 26px;
        box-shadow: 0px 4px 18px rgba(11,31,51,0.07);
        margin-bottom: 20px;
    }

    .route-card {
        background: linear-gradient(180deg, #FFFFFF 0%, #F8FBFE 100%);
        border: 2px solid #DCEAF5;
        border-radius: 22px;
        padding: 28px;
        box-shadow: 0px 5px 20px rgba(11,31,51,0.08);
        margin-bottom: 22px;
    }

    .metric-card {
        background: #FFFFFF;
        border: 1px solid #DCEAF5;
        border-radius: 17px;
        padding: 22px;
        box-shadow: 0px 4px 14px rgba(11,31,51,0.05);
        text-align: center;
        height: 100%;
    }

    .metric-label {
        font-size: 17px;
        color: #475569;
        margin-bottom: 8px;
    }

    .metric-value {
        font-size: 31px;
        font-weight: 900;
        color: #0B1F33;
    }

    .route-sequence {
        font-size: 23px;
        line-height: 1.9;
        color: #005CA9;
        font-weight: 800;
        word-spacing: 3px;
    }

    .business-note {
        background: #F8FBFE;
        border-left: 6px solid #005CA9;
        padding: 18px 20px;
        border-radius: 12px;
        color: #0B1F33;
        font-size: 18px;
        line-height: 1.55;
        margin-top: 12px;
        margin-bottom: 20px;
    }

    .info-box {
        background: #FFFBEA;
        border: 1px solid #F6E7A1;
        color: #7A5B00;
        border-radius: 12px;
        padding: 15px 18px;
        font-size: 17px;
        line-height: 1.5;
        margin-bottom: 16px;
    }

    .step-card {
        background: #FFFFFF;
        border: 1px solid #DCEAF5;
        border-radius: 18px;
        padding: 20px;
        box-shadow: 0px 4px 14px rgba(11,31,51,0.05);
        min-height: 205px;
        margin-bottom: 12px;
    }

    .step-number {
        width: 40px;
        height: 40px;
        border-radius: 50%;
        background: #005CA9;
        color: #FFFFFF;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        font-weight: 900;
        margin-bottom: 12px;
        font-size: 19px;
    }

    .step-title {
        font-size: 23px;
        font-weight: 900;
        color: #0B1F33;
        margin-bottom: 10px;
    }

    .step-body {
        font-size: 17px;
        color: #475569;
        line-height: 1.55;
    }

    .sidebar-callout {
        background: #FFFFFF;
        border: 1px solid #DCEAF5;
        border-radius: 14px;
        padding: 14px 16px;
        color: #0B1F33;
        font-size: 15px;
        line-height: 1.5;
        margin-bottom: 12px;
    }

    .gmaps-button a {
        display: inline-block;
        background: #005CA9;
        color: #FFFFFF !important;
        padding: 13px 18px;
        border-radius: 12px;
        text-decoration: none;
        font-weight: 800;
        font-size: 17px;
        margin-top: 6px;
    }

    .explain-box {
        background: #FFFFFF;
        border: 1px solid #DCEAF5;
        border-radius: 16px;
        padding: 18px 20px;
        color: #0B1F33;
        font-size: 17px;
        line-height: 1.65;
        margin: 12px 0 18px 0;
        box-shadow: 0px 3px 12px rgba(11,31,51,0.04);
    }

    .pqc-card {
        background: linear-gradient(180deg, #F8FBFE 0%, #FFFFFF 100%);
        border: 2px solid #BFD7EA;
        border-radius: 18px;
        padding: 22px;
        color: #0B1F33;
        font-size: 17px;
        line-height: 1.65;
        margin: 18px 0;
        box-shadow: 0px 4px 14px rgba(11,31,51,0.05);
    }

    .simple-title {
        font-size: 22px;
        font-weight: 900;
        color: #0B1F33;
        margin-bottom: 8px;
    }

    div[data-testid="stMetric"] {
        background: #FFFFFF;
        padding: 16px;
        border-radius: 15px;
        border: 1px solid #DCEAF5;
        box-shadow: 0px 3px 12px rgba(11,31,51,0.05);
    }


    /* Abas maiores e mais legíveis */
    button[data-baseweb="tab"] {
        font-size: 20px !important;
        font-weight: 800 !important;
        padding: 14px 18px !important;
    }

    button[data-baseweb="tab"] p {
        font-size: 20px !important;
        font-weight: 800 !important;
    }

    div[data-baseweb="tab-list"] {
        gap: 12px !important;
        border-bottom: 1px solid #DCEAF5;
        margin-bottom: 18px;
    }

    .infinity-card {
        background: #FFFFFF;
        border: 1px solid #DCEAF5;
        border-radius: 22px;
        padding: 26px 28px;
        box-shadow: 0px 4px 18px rgba(11,31,51,0.06);
        margin: 18px 0 18px 0;
        position: relative;
        overflow: hidden;
    }

    .infinity-symbol {
        position: absolute;
        right: 28px;
        top: 8px;
        font-size: 190px;
        line-height: 1;
        color: rgba(0,92,169,0.08);
        font-weight: 900;
        pointer-events: none;
    }

    .infinity-title {
        font-size: 26px;
        font-weight: 900;
        color: #0B1F33;
        margin-bottom: 8px;
        position: relative;
        z-index: 2;
    }

    .infinity-subtitle {
        font-size: 18px;
        color: #475569;
        line-height: 1.55;
        margin-bottom: 18px;
        max-width: 850px;
        position: relative;
        z-index: 2;
    }

    .flow-row {
        display: flex;
        flex-wrap: wrap;
        gap: 12px;
        position: relative;
        z-index: 2;
    }

    .flow-pill {
        background: #F8FBFE;
        border: 1px solid #BFD7EA;
        border-radius: 999px;
        padding: 11px 16px;
        font-size: 16px;
        font-weight: 800;
        color: #0B1F33;
        display: inline-flex;
        align-items: center;
        gap: 8px;
    }

    .flow-number {
        background: #005CA9;
        color: #FFFFFF;
        border-radius: 50%;
        width: 28px;
        height: 28px;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        font-size: 15px;
        font-weight: 900;
    }


    .route-mini-title {
        font-size: 18px;
        font-weight: 900;
        color: #0B1F33;
        margin: 18px 0 10px 0;
        position: relative;
        z-index: 2;
    }

    .route-step-row {
        display: flex;
        flex-wrap: wrap;
        gap: 10px;
        align-items: center;
        position: relative;
        z-index: 2;
        margin-top: 8px;
    }

    .route-step-pill {
        background: #0B1F33;
        color: #FFFFFF;
        border-radius: 999px;
        padding: 10px 14px;
        font-size: 15px;
        font-weight: 800;
        display: inline-flex;
        align-items: center;
        gap: 8px;
        box-shadow: 0px 3px 10px rgba(11,31,51,0.10);
    }

    .route-arrow {
        color: #005CA9;
        font-weight: 900;
        font-size: 20px;
    }


    .result-block {
        background: #FFFFFF;
        border: 1px solid #DCEAF5;
        border-radius: 24px;
        padding: 26px;
        margin-top: 22px;
        margin-bottom: 24px;
        box-shadow: 0 6px 18px rgba(11, 31, 58, 0.06);
    }

    .cycle-image-card {
        background: #FFFFFF;
        border: 1px solid #DCEAF5;
        border-radius: 24px;
        padding: 18px;
        margin-top: 24px;
        margin-bottom: 24px;
        box-shadow: 0 6px 18px rgba(11, 31, 58, 0.06);
        overflow: hidden;
    }

    .cycle-image-card img {
        width: 100%;
        border-radius: 18px;
        display: block;
    }



    .info-dot {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 18px;
        height: 18px;
        border-radius: 50%;
        background: #E0F2FE;
        border: 1px solid #7DD3FC;
        color: #005CA9;
        font-size: 12px;
        font-weight: 900;
        margin-left: 6px;
        cursor: help;
        vertical-align: text-top;
    }

    .quantum-mini-note {
        background: #F8FBFE;
        border: 1px solid #DCEAF5;
        border-radius: 16px;
        padding: 16px 18px;
        color: #334155;
        font-size: 16px;
        line-height: 1.55;
        margin: 14px 0 18px 0;
    }

    .quality-panel {
        background: linear-gradient(180deg, #FFFFFF 0%, #F8FBFE 100%);
        border: 1px solid #DCEAF5;
        border-radius: 22px;
        padding: 22px 24px;
        margin: 14px 0 18px 0;
        box-shadow: 0px 4px 18px rgba(11,31,51,0.06);
    }

    .quality-panel-title {
        font-size: 24px;
        font-weight: 900;
        color: #0B1F33;
        margin-bottom: 6px;
    }

    .quality-panel-subtitle {
        font-size: 16px;
        color: #475569;
        line-height: 1.5;
        margin-bottom: 10px;
    }

    .speedometer-wrap {
        display: flex;
        align-items: center;
        gap: 22px;
        flex-wrap: wrap;
        margin-top: 6px;
    }

    .speedometer-svg {
        max-width: 430px;
        width: 100%;
        height: auto;
    }

    .speedometer-text {
        flex: 1;
        min-width: 260px;
        color: #334155;
        font-size: 16px;
        line-height: 1.55;
    }

    .quality-badge {
        display: inline-block;
        background: #0B1F33;
        color: #FFFFFF;
        border-radius: 999px;
        padding: 8px 13px;
        font-weight: 900;
        font-size: 15px;
        margin-top: 8px;
    }

    </style>
    """,
    unsafe_allow_html=True,
)

# ============================================================
# FUNÇÕES
# ============================================================

def normalize_text(value):
    value = str(value).strip().lower()
    value = unicodedata.normalize("NFKD", value)
    value = "".join(c for c in value if not unicodedata.combining(c))
    value = value.replace("₂", "2").replace("²", "2")
    value = value.replace(" ", "_").replace("-", "_").replace("/", "_")
    return value


def display_name(point):
    if str(point).strip().lower() == "hub":
        return "Base"
    return str(point)


def display_name_full(point):
    if str(point).strip().lower() == "hub":
        return "Base (Hub)"
    return str(point)


def display_route(route_list):
    return " → ".join(display_name(p) for p in route_list)


def format_sequence(route_list):
    return " → ".join([f"{i+1}. {display_name(p)}" for i, p in enumerate(route_list)])


def route_steps_html(route_list):
    """
    Monta os passos da rota para exibir dentro do ciclo visual.
    Mantém a leitura curta, sem poluir a tela.
    """
    pieces = []
    for i, point in enumerate(route_list, start=1):
        label = display_name(point)
        pieces.append(f'<span class="route-step-pill"><b>{i}</b> {label}</span>')
        if i < len(route_list):
            pieces.append('<span class="route-arrow">→</span>')
    return "".join(pieces)


def find_column(df, options):
    normalized = {normalize_text(col): col for col in df.columns}
    for option in options:
        norm_opt = normalize_text(option)
        if norm_opt in normalized:
            return normalized[norm_opt]
    for norm_col, original_col in normalized.items():
        for option in options:
            if normalize_text(option) in norm_col:
                return original_col
    return None


def load_routes(uploaded_file=None):
    if uploaded_file is not None:
        excel = pd.ExcelFile(uploaded_file)
        source_name = "planilha enviada por você"
    else:
        excel = pd.ExcelFile(DEFAULT_EXCEL_PATH)
        source_name = "base simulada de demonstração"

    chosen_sheet = None
    chosen_df = None
    for sheet in excel.sheet_names:
        temp = pd.read_excel(excel, sheet_name=sheet)
        cols = [normalize_text(c) for c in temp.columns]
        if any("origem" in c for c in cols) and any("destino" in c for c in cols):
            chosen_sheet = sheet
            chosen_df = temp
            break

    if chosen_df is None:
        raise ValueError("Não encontrei uma aba com origem e destino.")

    df = chosen_df.copy()
    col_origin = find_column(df, ["origem"])
    col_destiny = find_column(df, ["destino"])
    col_distance = find_column(df, ["distancia_km", "distancia", "km"])
    col_time = find_column(df, ["tempo_min", "tempo", "minutos"])
    col_cost = find_column(df, ["custo_rs", "custo", "r$"])
    col_co2 = find_column(df, ["co2_estimado", "co2", "carbono", "emissao", "emissão"])

    missing = []
    for label, col in [
        ("origem", col_origin),
        ("destino", col_destiny),
        ("distancia_km", col_distance),
        ("tempo_min", col_time),
        ("custo_rs", col_cost),
        ("co2_estimado", col_co2),
    ]:
        if col is None:
            missing.append(label)
    if missing:
        raise ValueError("Colunas faltando: " + ", ".join(missing))

    routes = pd.DataFrame({
        "origem": df[col_origin].astype(str),
        "destino": df[col_destiny].astype(str),
        "distancia_km": pd.to_numeric(df[col_distance], errors="coerce"),
        "tempo_min": pd.to_numeric(df[col_time], errors="coerce"),
        "custo_rs": pd.to_numeric(df[col_cost], errors="coerce"),
        "co2": pd.to_numeric(df[col_co2], errors="coerce"),
    })
    routes = routes.dropna()
    routes = routes[routes["origem"] != routes["destino"]]
    return routes, chosen_sheet, source_name


def load_points_meta(uploaded_file=None):
    """
    Lê a aba Pontos, quando existir, para buscar nomes amigáveis e endereços/coordenadas para Google Maps.
    O sistema continua calculando por id, mas o Maps precisa de endereço real ou latitude/longitude.
    """
    try:
        if uploaded_file is not None:
            excel = pd.ExcelFile(uploaded_file)
        else:
            excel = pd.ExcelFile(DEFAULT_EXCEL_PATH)

        point_sheet = None
        for sheet in excel.sheet_names:
            if normalize_text(sheet) in ["pontos", "locais", "clientes"]:
                point_sheet = sheet
                break

        if point_sheet is None:
            return {}

        df = pd.read_excel(excel, sheet_name=point_sheet)
        col_id = find_column(df, ["id", "ponto", "codigo", "código", "nome"])
        col_label = find_column(df, ["nome_exibicao", "nome", "label", "descricao", "descrição"])
        col_address = find_column(df, ["endereco_maps", "endereço_maps", "endereco", "endereço", "maps_query"])
        col_lat = find_column(df, ["latitude", "lat"])
        col_lon = find_column(df, ["longitude", "lon", "lng"])

        if col_id is None:
            return {}

        meta = {}
        for _, row in df.iterrows():
            point_id = str(row[col_id]).strip()
            label = str(row[col_label]).strip() if col_label is not None and pd.notna(row[col_label]) else display_name(point_id)
            maps_query = None
            if col_lat is not None and col_lon is not None and pd.notna(row[col_lat]) and pd.notna(row[col_lon]):
                maps_query = f"{row[col_lat]},{row[col_lon]}"
            elif col_address is not None and pd.notna(row[col_address]):
                maps_query = str(row[col_address]).strip()

            meta[point_id] = {"label": label, "maps_query": maps_query}
        return meta
    except Exception:
        return {}


def map_query_for(point, points_meta):
    info = points_meta.get(str(point), {}) if points_meta else {}
    return info.get("maps_query") or display_name(point)


def build_graph(routes):
    graph = nx.Graph()
    for _, row in routes.iterrows():
        graph.add_edge(
            row["origem"],
            row["destino"],
            distancia_km=float(row["distancia_km"]),
            tempo_min=float(row["tempo_min"]),
            custo_rs=float(row["custo_rs"]),
            co2=float(row["co2"]),
        )
    return graph


def route_metrics(graph, route):
    totals = {"distancia_km": 0.0, "tempo_min": 0.0, "custo_rs": 0.0, "co2": 0.0}
    for start, end in zip(route[:-1], route[1:]):
        if not graph.has_edge(start, end):
            return None
        edge = graph[start][end]
        totals["distancia_km"] += edge["distancia_km"]
        totals["tempo_min"] += edge["tempo_min"]
        totals["custo_rs"] += edge["custo_rs"]
        totals["co2"] += edge["co2"]
    return totals


def calculate_score(metrics, criterion, max_values, weights):
    if criterion == "Andar menos":
        return metrics["distancia_km"]
    if criterion == "Chegar mais rápido":
        return metrics["tempo_min"]
    if criterion == "Gastar menos":
        return metrics["custo_rs"]
    if criterion == "Emitir menos CO₂":
        return metrics["co2"]

    score = 0.0
    score += weights["distancia_km"] * (metrics["distancia_km"] / max_values["distancia_km"])
    score += weights["tempo_min"] * (metrics["tempo_min"] / max_values["tempo_min"])
    score += weights["custo_rs"] * (metrics["custo_rs"] / max_values["custo_rs"])
    score += weights["co2"] * (metrics["co2"] / max_values["co2"])
    return score


def find_best_route(graph, hub, criterion, weights):
    clients = [node for node in graph.nodes if node != hub]
    if len(clients) > 8:
        raise ValueError("Para esta versão do MVP, use até 8 pontos de entrega.")

    records = []
    for permutation in itertools.permutations(clients):
        route = [hub] + list(permutation) + [hub]
        metrics = route_metrics(graph, route)
        if metrics is not None:
            records.append({
                "rota_lista": route,
                "rota": display_route(route),
                "distancia_km": metrics["distancia_km"],
                "tempo_min": metrics["tempo_min"],
                "custo_rs": metrics["custo_rs"],
                "co2": metrics["co2"],
            })

    ranking = pd.DataFrame(records)
    if ranking.empty:
        return None, ranking

    max_values = {
        "distancia_km": ranking["distancia_km"].max(),
        "tempo_min": ranking["tempo_min"].max(),
        "custo_rs": ranking["custo_rs"].max(),
        "co2": ranking["co2"].max(),
    }
    ranking["score"] = ranking.apply(
        lambda row: calculate_score(
            {"distancia_km": row["distancia_km"], "tempo_min": row["tempo_min"], "custo_rs": row["custo_rs"], "co2": row["co2"]},
            criterion,
            max_values,
            weights,
        ),
        axis=1,
    )
    ranking = ranking.sort_values("score").reset_index(drop=True)
    ranking.insert(0, "opcao", [f"Rota {i+1}" for i in range(len(ranking))])
    return ranking.iloc[0].to_dict(), ranking


def quantum_inspired_demo(graph, alpha, beta):
    nodes = list(graph.nodes)
    records = []
    for bits_tuple in itertools.product([0, 1], repeat=len(nodes)):
        if len(set(bits_tuple)) == 1:
            continue
        bitstring = "".join(str(bit) for bit in bits_tuple)
        cost = 0.0
        active_edges = []
        for start, end, data in graph.edges(data=True):
            if bits_tuple[nodes.index(start)] != bits_tuple[nodes.index(end)]:
                cost += alpha * data["tempo_min"] + beta * data["co2"]
                active_edges.append(f"{display_name(start)} ↔ {display_name(end)}")
        records.append({"bitstring": bitstring, "custo_ponderado": round(cost, 4), "arestas_ativadas": ", ".join(active_edges)})
    df = pd.DataFrame(records).sort_values("custo_ponderado").reset_index(drop=True)
    df.insert(0, "opcao_quantica", [f"Bitstring {i+1}" for i in range(len(df))])
    return df


def get_quality_panel_data(q_df, q_best):
    """
    Transforma o custo ponderado em uma leitura visual simples.
    Quanto mais perto de 100%, mais perto da melhor nota dentro da simulação.
    """
    min_cost = float(q_df["custo_ponderado"].min())
    max_cost = float(q_df["custo_ponderado"].max())
    best_cost = float(q_best["custo_ponderado"])

    if max_cost == min_cost:
        quality = 100.0
    else:
        quality = 100.0 * (max_cost - best_cost) / (max_cost - min_cost)

    quality = max(0.0, min(100.0, quality))

    if quality >= 90:
        label = "Muito perto da melhor nota"
    elif quality >= 70:
        label = "Boa configuração"
    elif quality >= 45:
        label = "Configuração intermediária"
    else:
        label = "Longe da melhor nota"

    return quality, label, min_cost, max_cost


def _polar_to_cartesian(cx, cy, r, angle_deg):
    angle_rad = math.radians(angle_deg)
    return cx + r * math.cos(angle_rad), cy - r * math.sin(angle_rad)


def _svg_arc_path(cx, cy, r, start_angle, end_angle):
    x1, y1 = _polar_to_cartesian(cx, cy, r, start_angle)
    x2, y2 = _polar_to_cartesian(cx, cy, r, end_angle)
    large_arc = 1 if abs(end_angle - start_angle) > 180 else 0
    sweep = 0
    return f"M {x1:.2f} {y1:.2f} A {r} {r} 0 {large_arc} {sweep} {x2:.2f} {y2:.2f}"


def render_quality_panel(q_df, q_best):
    quality, label, min_cost, max_cost = get_quality_panel_data(q_df, q_best)

    cx, cy, radius = 220, 190, 145
    needle_angle = 180 - (quality * 1.8)
    nx_, ny_ = _polar_to_cartesian(cx, cy, radius - 20, needle_angle)

    segment_colors = ["#DBEAFE", "#BFDBFE", "#93C5FD", "#60A5FA", "#38BDF8", "#0EA5E9", "#005CA9"]
    segment_paths = []
    total_span = 180
    gap = 3
    segment_span = total_span / len(segment_colors)

    for idx, color in enumerate(segment_colors):
        start_angle = 180 - (idx * segment_span) - gap
        end_angle = 180 - ((idx + 1) * segment_span) + gap
        path = _svg_arc_path(cx, cy, radius, start_angle, end_angle)
        segment_paths.append(f'<path d="{path}" fill="none" stroke="{color}" stroke-width="28" stroke-linecap="round"/>')

    svg_segments = "".join(segment_paths)

    st.markdown(
        f"""
        <div class="quality-panel">
            <div class="quality-panel-title">Proximidade da melhor nota</div>
            <div class="quality-panel-subtitle">
                O marcador mostra onde a melhor configuração demonstrativa ficou dentro da simulação. Quanto mais à direita, mais perto da melhor nota.
            </div>
            <div class="speedometer-wrap">
                <svg class="speedometer-svg" viewBox="0 0 440 245" role="img" aria-label="Marcador de proximidade da melhor nota">
                    <text x="28" y="224" font-size="14" font-weight="700" fill="#64748B">Pior</text>
                    <text x="195" y="55" font-size="14" font-weight="700" fill="#64748B">Médio</text>
                    <text x="365" y="224" font-size="14" font-weight="700" fill="#64748B">Melhor</text>
                    {svg_segments}
                    <line x1="{cx}" y1="{cy}" x2="{nx_:.2f}" y2="{ny_:.2f}" stroke="#0B1F33" stroke-width="8" stroke-linecap="round"/>
                    <circle cx="{cx}" cy="{cy}" r="17" fill="#0B1F33"/>
                    <circle cx="{cx}" cy="{cy}" r="8" fill="#FFFFFF"/>
                    <text x="{cx}" y="{cy+42}" text-anchor="middle" font-size="30" font-weight="900" fill="#0B1F33">{quality:.0f}%</text>
                </svg>
                <div class="speedometer-text">
                    <span class="quality-badge">{label}</span><br><br>
                    <b>Como ler:</b> a menor nota é a melhor. O painel transforma essa nota em uma escala simples de 0% a 100%.<br>
                    <b>Melhor nota da simulação:</b> {min_cost:.3f}<br>
                    <b>Pior nota da simulação:</b> {max_cost:.3f}
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

def google_maps_url(route_list, points_meta=None):
    if not route_list or len(route_list) < 2:
        return "https://www.google.com/maps"
    origin = quote_plus(map_query_for(route_list[0], points_meta))
    destination = quote_plus(map_query_for(route_list[-1], points_meta))
    waypoints = "|".join(quote_plus(map_query_for(p, points_meta)) for p in route_list[1:-1])
    return f"https://www.google.com/maps/dir/?api=1&origin={origin}&destination={destination}&waypoints={waypoints}&travelmode=driving"


def build_segments_table(graph, route_list):
    rows = []
    for i, (start, end) in enumerate(zip(route_list[:-1], route_list[1:]), start=1):
        edge = graph[start][end]
        rows.append({
            "trecho": f"Trecho {i}",
            "saída": display_name(start),
            "chegada": display_name(end),
            "distância km": round(edge["distancia_km"], 2),
            "tempo min": round(edge["tempo_min"], 1),
            "custo R$": round(edge["custo_rs"], 2),
            "CO₂": round(edge["co2"], 2),
        })
    return pd.DataFrame(rows)


def load_van_image():
    if os.path.exists(DEFAULT_VAN_IMAGE):
        return Image.open(DEFAULT_VAN_IMAGE)
    return None


def image_to_base64(path):
    if not os.path.exists(path):
        return None
    with open(path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


def render_cycle_image_block():
    cycle_b64 = image_to_base64(DEFAULT_CYCLE_IMAGE)
    if cycle_b64:
        html = f"""
        <div class=\"cycle-image-card\">
            <img src=\"data:image/png;base64,{cycle_b64}\" alt=\"Ciclo de decisão LOGIQ\">
        </div>
        """
        st.markdown(html, unsafe_allow_html=True)
    else:
        st.warning("A imagem do ciclo não foi encontrada em assets/ciclo_decisao_logiq.png")


def draw_operator_route(graph, route_list):
    fig, ax = plt.subplots(figsize=(14, 8))

    route_edges = list(zip(route_list[:-1], route_list[1:]))
    route_nodes = list(dict.fromkeys(route_list))

    # Layout fixo apenas quando TODOS os pontos da rota cabem na base simples.
    fixed_pos = {
        "Hub": (-1.1, 0.0),
        "Cliente A": (-0.55, -0.78),
        "Cliente B": (-0.48, 0.78),
        "Cliente C": (0.30, -0.82),
        "Cliente E": (0.38, 0.02),
        "Cliente F": (1.10, 0.72),
        "Cliente D": (1.18, -0.22),
    }
    if set(route_nodes).issubset(set(fixed_pos.keys())):
        pos = fixed_pos
    else:
        route_graph_layout = graph.subgraph(route_nodes).copy()
        pos = nx.spring_layout(route_graph_layout, seed=18, k=1.45)
    segment_colors = ["#005CA9", "#1F7A8C", "#2A9D8F", "#E76F51", "#7B2CBF", "#F4A261", "#264653", "#118AB2", "#EF476F"]

    # Desenha só a rota escolhida no painel do operador.
    for node in route_nodes:
        x, y = pos[node]
        color = "#005CA9" if node == "Hub" else "#DCEAF5"
        font_color = "white" if node == "Hub" else "#0B1F33"
        ax.scatter([x], [y], s=1800, color=color, edgecolor="#0B1F33", linewidth=2.5, zorder=10)
        ax.text(x, y, display_name(node), ha="center", va="center", fontsize=13, fontweight="bold", color=font_color, zorder=11)

    # Trechos com cores diferentes e números afastados da linha.
    for i, (start, end) in enumerate(route_edges, start=1):
        color = segment_colors[(i - 1) % len(segment_colors)]
        x1, y1 = pos[start]
        x2, y2 = pos[end]
        dx = x2 - x1
        dy = y2 - y1
        mx = x1 + dx * 0.52
        my = y1 + dy * 0.52
        norm = max((dx ** 2 + dy ** 2) ** 0.5, 0.001)
        offx = -dy / norm * 0.06
        offy = dx / norm * 0.06

        ax.annotate(
            "",
            xy=(x2, y2),
            xytext=(x1, y1),
            arrowprops=dict(arrowstyle="-|>", lw=5.0, color=color, shrinkA=22, shrinkB=24, mutation_scale=24),
            zorder=6,
        )
        ax.text(
            mx + offx,
            my + offy,
            str(i),
            fontsize=12,
            fontweight="bold",
            color="white",
            ha="center",
            va="center",
            bbox=dict(boxstyle="circle,pad=0.35", facecolor=color, edgecolor="white", linewidth=1.8),
            zorder=20,
        )
        edge = graph[start][end]
        ax.text(
            mx - offx,
            my - offy,
            f"{edge['distancia_km']:.1f} km",
            fontsize=10,
            color="#0B1F33",
            ha="center",
            va="center",
            bbox=dict(boxstyle="round,pad=0.18", facecolor="white", edgecolor="#DCEAF5", alpha=0.95),
            zorder=19,
        )

    # Paradas nos nós, sem poluir a linha.
    step_map = {}
    for idx, point in enumerate(route_list, start=1):
        step_map.setdefault(point, []).append(idx)
    for node, steps in step_map.items():
        x, y = pos[node]
        label = "/".join(str(s) for s in steps)
        ax.text(
            x,
            y - 0.13,
            f"Parada {label}",
            fontsize=10,
            color="#0B1F33",
            ha="center",
            va="center",
            bbox=dict(boxstyle="round,pad=0.24", facecolor="#FFFFFF", edgecolor="#005CA9", linewidth=1.2),
            zorder=21,
        )

    ax.set_title("Rota recomendada | sequência de execução", fontsize=25, fontweight="bold", color="#0B1F33", pad=18)
    ax.axis("off")
    ax.margins(0.18)
    return fig


def build_top_routes_chart(ranking):
    top10 = ranking.head(10).copy()
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.bar(top10["opcao"], top10["score"])
    ax.set_title("Top 10 rotas por score", fontsize=18, fontweight="bold")
    ax.set_ylabel("Score")
    ax.grid(axis="y", linestyle="--", alpha=0.3)
    plt.tight_layout()
    return fig


def build_metrics_comparison_chart(best):
    labels = ["Distância", "Tempo", "Custo", "CO₂"]
    values = [best["distancia_km"], best["tempo_min"], best["custo_rs"], best["co2"]]
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.bar(labels, values)
    ax.set_title("Indicadores da rota escolhida", fontsize=17, fontweight="bold")
    ax.grid(axis="y", linestyle="--", alpha=0.3)
    plt.tight_layout()
    return fig



def render_qaoa_2_module(graph, hub):
    """Renderiza o novo módulo LOGIQ 2.0 sem alterar o módulo operacional 1.0."""
    st.markdown('<div class="section-title">LOGIQ 2.0 | Simulação QAOA</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-subtitle">Este módulo roda uma simulação local de QAOA em um cenário reduzido. Ele não substitui a rota operacional; mostra a ponte técnica para computação quântica aplicada.</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="business-note">
        <b>Leitura honesta:</b> aqui existe sim uma simulação quântica de verdade, feita por statevector local.
        Ela usa uma camada QAOA para testar combinações em um problema pequeno. Ainda não é execução em hardware quântico
        e ainda não promete superar métodos clássicos em rotas reais complexas.
        </div>
        """,
        unsafe_allow_html=True,
    )

    col_a, col_b, col_c = st.columns(3)
    with col_a:
        alpha_q = st.slider(
            "Peso do tempo no QAOA",
            0.0, 1.0, 0.5, 0.05,
            help="Aumente se quiser que a simulação dê mais importância ao tempo de deslocamento.",
        )
    with col_b:
        beta_q = st.slider(
            "Peso da emissão no QAOA",
            0.0, 1.0, 0.5, 0.05,
            help="Aumente se quiser que a simulação dê mais importância à emissão estimada.",
        )
    with col_c:
        p_layers = st.selectbox(
            "Profundidade p",
            [1, 2],
            index=0,
            help="Número de camadas do circuito QAOA. Para MVP local, p=1 é mais rápido e estável.",
        )

    qres = run_qaoa_demo(graph, hub, alpha=alpha_q, beta_weight=beta_q, max_nodes=4, p=int(p_layers), grid_points=15)

    st.markdown("### Cenário reduzido usado na simulação")
    st.write(" → ".join(display_name(n) for n in qres.nodes))
    st.caption("O QAOA foi aplicado em Base + até 3 pontos de entrega para manter a simulação local leve e explicável.")

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Melhor clássico", qres.exact_bitstring, f"nota {qres.exact_cost:.3f}")
    m2.metric("Resultado QAOA", qres.qaoa_bitstring, f"nota {qres.qaoa_cost:.3f}")
    m3.metric("Probabilidade", f"{qres.qaoa_probability*100:.1f}%")
    m4.metric("Proximidade", f"{qres.closeness_percent:.0f}%")

    render_qaoa_speedometer(qres.closeness_percent, qres.exact_cost, qres.qaoa_cost, qres.worst_valid_cost)

    st.markdown(
        f"""
        <div class="big-card">
            <h3 style="font-size:26px;color:#0B1F33;margin-bottom:10px;">O que aconteceu nesta simulação?</h3>
            <p style="font-size:18px;color:#334155;line-height:1.6;">
            O sistema reduziu o problema para poucos pontos, transformou as combinações em estados binários e executou uma busca QAOA simulada.
            A melhor solução clássica para esse recorte foi <b>{qres.exact_bitstring}</b>. O QAOA simulado destacou <b>{qres.qaoa_bitstring}</b>.
            </p>
            <p style="font-size:18px;color:#334155;line-height:1.6;">
            Em linguagem de negócio: esta aba mostra como a LOGIQ pode comparar uma solução clássica com uma camada quântica simulada.
            Isso é uma evolução técnica real, mas ainda em escala reduzida.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    t1, t2 = st.tabs(["Ranking clássico do recorte", "Probabilidades QAOA"])
    with t1:
        st.dataframe(qres.valid_ranking.head(20), width="stretch", hide_index=True)
    with t2:
        st.dataframe(qres.probabilities.head(20), width="stretch", hide_index=True)
        st.pyplot(plot_qaoa_probabilities(qres.probabilities))


def render_qaoa_speedometer(closeness, exact_cost, qaoa_cost, worst_cost):
    """Painel simples em azul para mostrar proximidade do resultado QAOA em relação ao melhor clássico."""
    cx, cy, radius = 220, 190, 145
    needle_angle = 180 - (float(closeness) * 1.8)
    nx_, ny_ = _polar_to_cartesian(cx, cy, radius - 20, needle_angle)
    colors = ["#DBEAFE", "#BFDBFE", "#93C5FD", "#60A5FA", "#38BDF8", "#0EA5E9", "#005CA9"]
    paths = []
    seg_span = 180 / len(colors)
    for idx, color in enumerate(colors):
        start_angle = 180 - (idx * seg_span) - 3
        end_angle = 180 - ((idx + 1) * seg_span) + 3
        paths.append(f'<path d="{_svg_arc_path(cx, cy, radius, start_angle, end_angle)}" fill="none" stroke="{color}" stroke-width="28" stroke-linecap="round"/>')
    svg_segments = "".join(paths)
    st.markdown(
        f"""
        <div class="quality-panel">
            <div class="quality-panel-title">Painel de proximidade do QAOA</div>
            <div class="quality-panel-subtitle">Quanto mais à direita, mais perto o resultado QAOA ficou da melhor solução clássica do recorte.</div>
            <div class="speedometer-wrap">
                <svg class="speedometer-svg" viewBox="0 0 440 245" role="img" aria-label="Proximidade do QAOA">
                    <text x="28" y="224" font-size="14" font-weight="700" fill="#64748B">Longe</text>
                    <text x="190" y="55" font-size="14" font-weight="700" fill="#64748B">Médio</text>
                    <text x="360" y="224" font-size="14" font-weight="700" fill="#64748B">Perto</text>
                    {svg_segments}
                    <line x1="{cx}" y1="{cy}" x2="{nx_:.2f}" y2="{ny_:.2f}" stroke="#0B1F33" stroke-width="8" stroke-linecap="round"/>
                    <circle cx="{cx}" cy="{cy}" r="17" fill="#0B1F33"/>
                    <circle cx="{cx}" cy="{cy}" r="8" fill="#FFFFFF"/>
                    <text x="{cx}" y="{cy+42}" text-anchor="middle" font-size="30" font-weight="900" fill="#0B1F33">{closeness:.0f}%</text>
                </svg>
                <div class="speedometer-text">
                    <span class="quality-badge">QAOA simulado local</span><br><br>
                    <b>Melhor clássico do recorte:</b> {exact_cost:.3f}<br>
                    <b>Resultado QAOA:</b> {qaoa_cost:.3f}<br>
                    <b>Pior válido do recorte:</b> {worst_cost:.3f}<br><br>
                    <b>Regra:</b> aqui a nota menor é melhor. O painel mostra proximidade, não custo em reais.
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def plot_qaoa_probabilities(probabilities_df):
    top = probabilities_df.head(10).copy()
    fig, ax = plt.subplots(figsize=(10, 4.8))
    ax.bar(top["bitstring"], top["probabilidade"] * 100)
    ax.set_title("Estados mais prováveis no QAOA simulado", fontsize=17, fontweight="bold")
    ax.set_xlabel("Bitstring")
    ax.set_ylabel("Probabilidade (%)")
    ax.grid(axis="y", linestyle="--", alpha=0.3)
    plt.tight_layout()
    return fig

# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.markdown("## Decisão da rota")
st.sidebar.markdown(
    """
    <div class="sidebar-callout">
    <b>Escolha o foco da entrega.</b><br><br>
    A LOGIQ compara as rotas e mostra o caminho mais adequado para a operação: mais rápido, mais barato, mais curto, mais sustentável ou equilibrado.<br><br>
    Você não precisa entender de programação nem de computação quântica. O painel traduz os dados em uma decisão simples.
    </div>
    """,
    unsafe_allow_html=True,
)

with st.sidebar.expander("ℹ️ O que este painel faz?", expanded=False):
    st.write(
        """
        Ele transforma uma pergunta técnica em uma escolha simples de negócio.

        Você escolhe a prioridade da operação. A LOGIQ compara as rotas possíveis,
        calcula os impactos e mostra a recomendação de forma explicável.

        A ideia é que uma pessoa de negócios entenda a decisão sem precisar saber programar.
        """
    )

app_module = st.sidebar.radio(
    "Módulo do sistema",
    ["LOGIQ 1.0 | Rotas operacionais", "LOGIQ 2.0 | QAOA simulado"],
    help=(
        "Escolha o modo de uso. O módulo 1.0 mantém a rota operacional. "
        "O módulo 2.0 roda uma simulação QAOA local em cenário reduzido, sem substituir a rota principal."
    ),
)

if "upload_key" not in st.session_state:
    st.session_state.upload_key = 0

source_mode = st.sidebar.radio(
    "Fonte dos dados",
    ["Usar base de demonstração", "Usar minha planilha"],
    help="Escolha se quer testar com a base pronta do MVP ou enviar uma planilha própria.",
)

uploaded_file = None
if source_mode == "Usar minha planilha":
    uploaded_file = st.sidebar.file_uploader(
        "Subir planilha Excel",
        type=["xlsx", "xls"],
        key=f"uploaded_excel_{st.session_state.upload_key}",
        help="Envie uma base real de rotas. A planilha precisa ter uma aba com origem, destino, distância, tempo, custo e CO₂.",
    )

    if st.sidebar.button("Limpar planilha enviada", help="Remove a planilha carregada e permite testar outra."):
        st.session_state.upload_key += 1
        st.rerun()
else:
    st.sidebar.info("Você está usando a base simulada. Para testar outro arquivo, escolha 'Usar minha planilha'.")

criterion = st.sidebar.selectbox(
    "O que você quer melhorar hoje?",
    ["Equilibrar tudo", "Andar menos", "Chegar mais rápido", "Gastar menos", "Emitir menos CO₂"],
    help=(
        "Esta escolha orienta a recomendação da rota. "
        "Por exemplo: se você escolher 'Gastar menos', o sistema favorece rotas de menor custo."
    ),
)

st.sidebar.markdown("### Ajuste fino")
st.sidebar.caption("Use os pesos quando quiser calibrar a decisão com mais detalhe.")

peso_distancia = st.sidebar.slider("Distância", 0.0, 1.0, 0.25, 0.05, help="Aumente se quiser favorecer trajetos mais curtos.")
peso_tempo = st.sidebar.slider("Tempo", 0.0, 1.0, 0.25, 0.05, help="Aumente se quiser favorecer entregas mais rápidas.")
peso_custo = st.sidebar.slider("Custo", 0.0, 1.0, 0.25, 0.05, help="Aumente se quiser favorecer menor custo operacional.")
peso_co2 = st.sidebar.slider("CO₂", 0.0, 1.0, 0.25, 0.05, help="Aumente se quiser favorecer menor emissão estimada.")

peso_total = peso_distancia + peso_tempo + peso_custo + peso_co2
if peso_total == 0:
    weights = {"distancia_km": 0.25, "tempo_min": 0.25, "custo_rs": 0.25, "co2": 0.25}
else:
    weights = {
        "distancia_km": peso_distancia / peso_total,
        "tempo_min": peso_tempo / peso_total,
        "custo_rs": peso_custo / peso_total,
        "co2": peso_co2 / peso_total,
    }

# ============================================================
# EXECUÇÃO
# ============================================================

try:
    routes, sheet_name, source_name = load_routes(uploaded_file)
    points_meta = load_points_meta(uploaded_file)
    graph = build_graph(routes)
    nodes = list(graph.nodes)
    default_hub = "Hub" if "Hub" in nodes else nodes[0]

    hub = st.sidebar.selectbox(
        "Base de saída e retorno",
        nodes,
        index=nodes.index(default_hub),
        format_func=display_name_full,
        help="É o ponto onde a rota começa e termina. Em logística, também pode ser chamado de hub.",
    )

    best, ranking = find_best_route(graph, hub, criterion, weights)
    # Header mais limpo e alinhado
    van_b64 = image_to_base64(DEFAULT_VAN_IMAGE)
    if van_b64:
        van_html = f'<div class="hero-van-wrap"><img src="data:image/png;base64,{van_b64}" alt="Van LOGIQ"></div>'
    else:
        van_html = '<div class="hero-van-wrap"><div style="color:#0B1F33;font-weight:800;text-align:center;">Adicione<br>assets/van_logiq.png</div></div>'

    st.markdown(
        f"""
        <div class="hero-card">
            {van_html}
            <div class="hero-content">
                <div class="hero-title">LOGIQ</div>
                <div class="hero-subtitle">Rotas mais claras para quem decide, acompanha e executa a operação.</div>
                <span class="chip">Rota explicável</span>
                <span class="chip">Menos custo</span>
                <span class="chip">Menos emissão</span>
                <span class="chip">Quantum-inspired</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if app_module == "LOGIQ 2.0 | QAOA simulado":
        render_qaoa_2_module(graph, hub)
        st.stop()

    tabs = st.tabs([
        "Visão da solução",
        "Rota do motorista",
        "Resumo executivo",
        "Dados usados",
        "Lógica quântica",
    ])

    # Tab 1
    with tabs[0]:
        st.markdown('<div class="section-title">Visão gráfica da solução</div>', unsafe_allow_html=True)
        st.markdown(
            '<div class="section-subtitle">Aqui a LOGIQ traduz o cálculo em uma recomendação de rota clara, com indicadores que fazem sentido para o negócio.</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            f"""
            <div class="route-card">
                <h3 style="font-size:30px;color:#0B1F33;margin-bottom:10px;">Melhor decisão: {best['opcao']}</h3>
                <p style="font-size:20px;color:#475569;margin-bottom:8px;"><b>Prioridade escolhida:</b> {criterion}</p>
                <p style="font-size:20px;color:#0B1F33;margin-bottom:8px;"><b>Ordem da rota:</b></p>
                <div class="route-sequence">{format_sequence(best['rota_lista'])}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        c1, c2, c3, c4 = st.columns(4)
        c1.markdown(f'<div class="metric-card"><div class="metric-label">Distância</div><div class="metric-value">{best["distancia_km"]:.2f} km</div></div>', unsafe_allow_html=True)
        c2.markdown(f'<div class="metric-card"><div class="metric-label">Tempo</div><div class="metric-value">{best["tempo_min"]:.1f} min</div></div>', unsafe_allow_html=True)
        c3.markdown(f'<div class="metric-card"><div class="metric-label">Custo</div><div class="metric-value">R$ {best["custo_rs"]:.2f}</div></div>', unsafe_allow_html=True)
        c4.markdown(f'<div class="metric-card"><div class="metric-label">Emissão</div><div class="metric-value">{best["co2"]:.2f}</div></div>', unsafe_allow_html=True)

        # Bloco 2 — Ciclo de decisão LOGIQ
        render_cycle_image_block()

    # Tab 2
    with tabs[1]:
        st.markdown('<div class="section-title">Painel do operador</div>', unsafe_allow_html=True)
        st.markdown(
            '<div class="section-subtitle">Esta é a tela para bater o olho e entender a sequência da viagem. Sem rede completa, sem ruído: apenas a rota recomendada.</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            f"""
            <div class="route-card">
                <h3 style="font-size:32px;color:#0B1F33;margin-bottom:12px;">{best['opcao']}</h3>
                <p style="font-size:20px;color:#475569;margin-bottom:8px;"><b>Comece na base, siga as paradas e retorne à base.</b></p>
                <div class="route-sequence">{format_sequence(best['rota_lista'])}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        op1, op2, op3, op4 = st.columns(4)
        op1.metric("Distância", f"{best['distancia_km']:.2f} km")
        op2.metric("Tempo", f"{best['tempo_min']:.1f} min")
        op3.metric("Custo", f"R$ {best['custo_rs']:.2f}")
        op4.metric("Emissão", f"{best['co2']:.2f}")

        st.pyplot(draw_operator_route(graph, best["rota_lista"]))

        st.markdown("### Trecho a trecho")
        segments_df = build_segments_table(graph, best["rota_lista"])
        st.dataframe(segments_df, width="stretch", hide_index=True)

        st.markdown(
            f"""
            <div class="gmaps-button">
                <a href="{google_maps_url(best['rota_lista'], points_meta)}" target="_blank">Abrir rota no Google Maps</a>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.caption("Para o Google Maps funcionar bem, a aba Pontos precisa ter endereço real ou latitude/longitude. Se o Maps mostrar 'Cliente A' em vez de endereço, confira a aba Pontos da planilha enviada.")

    # Tab 3
    with tabs[2]:
        st.markdown('<div class="section-title">Dashboard executivo</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-subtitle">Resumo para decisão: qual rota usar, por que ela venceu e quais indicadores sustentam a escolha.</div>', unsafe_allow_html=True)
        st.markdown(
            f"""
            <div class="big-card">
                <h3 style="font-size:30px;color:#0B1F33;">Decisão recomendada</h3>
                <p style="font-size:20px;color:#475569;"><b>{best['opcao']}</b> é a melhor alternativa para a prioridade <b>{criterion}</b>.</p>
                <p style="font-size:19px;color:#475569;"><b>Caminho:</b> {best['rota']}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        e1, e2 = st.columns(2)
        with e1:
            st.pyplot(build_top_routes_chart(ranking))
        with e2:
            st.pyplot(build_metrics_comparison_chart(best))
        st.markdown(
            """
            <div class="business-note">
            <b>Leitura de negócio:</b> a LOGIQ transforma dados de rota em recomendação prática. O gestor consegue defender a decisão com números e o operador entende a sequência da entrega.
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown("### Top 10 rotas")
        st.dataframe(ranking[["opcao", "rota", "distancia_km", "tempo_min", "custo_rs", "co2", "score"]].head(10), width="stretch", hide_index=True)

    # Tab 4
    with tabs[3]:
        st.markdown('<div class="section-title">Dados</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-subtitle">Transparência da base usada no cálculo.</div>', unsafe_allow_html=True)
        st.dataframe(routes, width="stretch", hide_index=True)
        st.markdown("### Pesos aplicados")
        st.markdown(
            """
            <div class="explain-box">
            <b>O que são pesos?</b><br>
            Peso é a importância que você dá para cada fator. Se todos estão em 0,25, o sistema está tratando distância, tempo, custo e emissão com a mesma importância.
            Se você aumentar o peso de custo, por exemplo, a LOGIQ passa a favorecer rotas mais baratas.
            </div>
            """,
            unsafe_allow_html=True,
        )
        pesos_df = pd.DataFrame([
            {"fator": "Distância", "peso": round(weights["distancia_km"], 4)},
            {"fator": "Tempo", "peso": round(weights["tempo_min"], 4)},
            {"fator": "Custo", "peso": round(weights["custo_rs"], 4)},
            {"fator": "CO₂", "peso": round(weights["co2"], 4)},
        ])
        st.dataframe(pesos_df, width="stretch", hide_index=True)

    # Tab 5
    with tabs[4]:
        st.markdown('<div class="section-title">Camada quantum-inspired</div>', unsafe_allow_html=True)
        st.markdown(
            '<div class="section-subtitle">Aqui a lógica quântica é traduzida para negócios: combinações, pesos e custo de decisão.</div>',
            unsafe_allow_html=True,
        )

        q1, q2 = st.columns(2)
        with q1:
            alpha = st.slider(
                "Peso do tempo",
                0.0,
                1.0,
                0.5,
                0.05,
                help="Quanto maior, mais a simulação demonstrativa favorece rapidez.",
            )
        with q2:
            beta = st.slider(
                "Peso da emissão",
                0.0,
                1.0,
                0.5,
                0.05,
                help="Quanto maior, mais a simulação demonstrativa favorece menor emissão.",
            )

        total_q = alpha + beta
        alpha_norm, beta_norm = (0.5, 0.5) if total_q == 0 else (alpha / total_q, beta / total_q)
        q_df = quantum_inspired_demo(graph, alpha_norm, beta_norm)
        q_best = q_df.iloc[0]

        render_quality_panel(q_df, q_best)

        with st.expander("ℹ️ O que esta aba quer mostrar?", expanded=False):
            st.write(
                """
                Esta aba é uma demonstração da camada quantum-inspired da LOGIQ.

                Em português simples, ela mostra como várias combinações possíveis podem ser testadas, comparadas e ranqueadas por uma nota de decisão.

                Essa parte não substitui a rota operacional. Ela mostra como a arquitetura pode evoluir para modelos QUBO, Ising e QAOA.
                """
            )

        st.markdown("### Ranking demonstrativo")
        st.dataframe(
            q_df[["opcao_quantica", "bitstring", "custo_ponderado", "arestas_ativadas"]].head(20),
            width="stretch",
            hide_index=True,
        )

        st.markdown(
            f"""
            <div class="big-card">
                <h3 style="font-size:28px;color:#0B1F33;margin-bottom:14px;">Melhor configuração demonstrativa</h3>
                <p style="font-size:18px;margin-bottom:10px;"><b>{q_best['opcao_quantica']}</b></p>
                <p style="font-size:18px;margin-bottom:10px;">
                    <b>Bitstring</b><span class="info-dot" title="É uma sequência de zeros e uns usada para representar uma combinação possível. Para negócios, pense como uma hipótese que o sistema testou.">i</span>: {q_best['bitstring']}
                </p>
                <p style="font-size:18px;margin-bottom:10px;">
                    <b>Custo ponderado</b><span class="info-dot" title="É uma nota calculada pelo sistema com base nos pesos escolhidos. Não é dinheiro. Quanto menor a nota, melhor a combinação dentro daquela prioridade.">i</span>: {q_best['custo_ponderado']}
                </p>
                <p style="font-size:17px;color:#475569;line-height:1.6;margin-top:12px;">
                    Em português simples: esta foi a combinação demonstrativa com <b>menor nota</b> dentro dos pesos escolhidos.
                    Ela não substitui a rota operacional; serve para mostrar como a solução pode evoluir para modelos quantum-inspired.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            """
            <div class="quantum-mini-note">
                <b>Quanto menor, melhor.</b> O custo ponderado é uma nota de comparação, não um valor em reais.
                Ele serve para ordenar as combinações e mostrar qual ficou mais adequada dentro dos pesos escolhidos.
            </div>
            """,
            unsafe_allow_html=True,
        )


except Exception as e:
    st.error("Erro ao executar o sistema.")
    st.exception(e)
    st.markdown(
        """
        Verifique:
        1. Se a planilha existe em `data/logiq_planilha_completa_mvp.xlsx`.
        2. Se a imagem existe em `assets/van_logiq.png`.
        3. Se as dependências foram instaladas com `pip install -r requirements.txt`.
        4. Se você está rodando o comando dentro da pasta correta.
        """
    )
