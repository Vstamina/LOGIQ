import itertools
from pathlib import Path

import pandas as pd

Path("data").mkdir(exist_ok=True)
output_path = Path("data") / "logiq_planilha_completa_mvp.xlsx"

pontos = pd.DataFrame([
    {"id": "Hub", "tipo": "Base", "nome": "Base operacional LOGIQ", "latitude": -11.8600, "longitude": -55.5000, "prioridade": "Alta", "janela_inicio": "08:00", "janela_fim": "18:00", "lucro_estimado_rs": 0, "observacao": "Ponto de saída e retorno"},
    {"id": "Cliente A", "tipo": "Entrega", "nome": "Cliente A", "latitude": -11.8525, "longitude": -55.4940, "prioridade": "Alta", "janela_inicio": "09:00", "janela_fim": "12:00", "lucro_estimado_rs": 120, "observacao": "Entrega prioritária"},
    {"id": "Cliente B", "tipo": "Entrega", "nome": "Cliente B", "latitude": -11.8680, "longitude": -55.5120, "prioridade": "Média", "janela_inicio": "10:00", "janela_fim": "15:00", "lucro_estimado_rs": 95, "observacao": "Cliente residencial"},
    {"id": "Cliente C", "tipo": "Entrega", "nome": "Cliente C", "latitude": -11.8450, "longitude": -55.5075, "prioridade": "Alta", "janela_inicio": "08:30", "janela_fim": "13:00", "lucro_estimado_rs": 110, "observacao": "Cliente comercial"},
    {"id": "Cliente D", "tipo": "Entrega", "nome": "Cliente D", "latitude": -11.8750, "longitude": -55.4925, "prioridade": "Baixa", "janela_inicio": "13:00", "janela_fim": "17:30", "lucro_estimado_rs": 80, "observacao": "Entrega flexível"},
    {"id": "Cliente E", "tipo": "Entrega", "nome": "Cliente E", "latitude": -11.8580, "longitude": -55.4820, "prioridade": "Média", "janela_inicio": "09:30", "janela_fim": "16:00", "lucro_estimado_rs": 100, "observacao": "Cliente recorrente"},
    {"id": "Cliente F", "tipo": "Entrega", "nome": "Cliente F", "latitude": -11.8820, "longitude": -55.5225, "prioridade": "Alta", "janela_inicio": "11:00", "janela_fim": "17:00", "lucro_estimado_rs": 130, "observacao": "Entrega volumosa"},
])

rotas = pd.DataFrame([
    ["Hub", "Cliente A", 5.2, 13, 9.80, 1.4],
    ["Hub", "Cliente B", 8.7, 21, 15.10, 2.2],
    ["Hub", "Cliente C", 6.1, 16, 11.30, 1.7],
    ["Hub", "Cliente D", 10.5, 27, 18.90, 2.9],
    ["Hub", "Cliente E", 7.4, 19, 13.20, 2.0],
    ["Hub", "Cliente F", 11.2, 31, 21.50, 3.3],
    ["Cliente A", "Cliente B", 4.4, 11, 7.60, 1.1],
    ["Cliente A", "Cliente C", 3.1, 9, 5.70, 0.8],
    ["Cliente A", "Cliente D", 8.3, 22, 15.20, 2.3],
    ["Cliente A", "Cliente E", 5.8, 15, 10.40, 1.5],
    ["Cliente A", "Cliente F", 9.6, 26, 18.00, 2.7],
    ["Cliente B", "Cliente C", 5.0, 14, 9.10, 1.4],
    ["Cliente B", "Cliente D", 4.2, 12, 7.90, 1.2],
    ["Cliente B", "Cliente E", 6.7, 18, 12.10, 1.9],
    ["Cliente B", "Cliente F", 7.9, 23, 15.80, 2.4],
    ["Cliente C", "Cliente D", 6.4, 17, 11.90, 1.8],
    ["Cliente C", "Cliente E", 3.6, 10, 6.60, 1.0],
    ["Cliente C", "Cliente F", 8.1, 24, 16.50, 2.5],
    ["Cliente D", "Cliente E", 5.5, 16, 10.30, 1.6],
    ["Cliente D", "Cliente F", 4.7, 15, 9.80, 1.5],
    ["Cliente E", "Cliente F", 6.2, 18, 12.40, 1.9],
], columns=["origem", "destino", "distancia_km", "tempo_min", "custo_rs", "co2_estimado"])

cenarios = pd.DataFrame([
    {"cenario": "Equilibrar tudo", "distancia": 0.25, "tempo": 0.25, "custo": 0.25, "co2": 0.25},
    {"cenario": "Andar menos", "distancia": 1.0, "tempo": 0.0, "custo": 0.0, "co2": 0.0},
    {"cenario": "Chegar mais rápido", "distancia": 0.0, "tempo": 1.0, "custo": 0.0, "co2": 0.0},
    {"cenario": "Gastar menos", "distancia": 0.0, "tempo": 0.0, "custo": 1.0, "co2": 0.0},
    {"cenario": "Emitir menos CO2", "distancia": 0.0, "tempo": 0.0, "custo": 0.0, "co2": 1.0},
])

dicionario = pd.DataFrame([
    {"campo": "id", "explicacao": "Nome curto usado pelo sistema para identificar cada ponto."},
    {"campo": "latitude/longitude", "explicacao": "Coordenadas usadas para abrir a rota no Google Maps."},
    {"campo": "origem/destino", "explicacao": "Trecho da malha de deslocamento."},
    {"campo": "distancia_km", "explicacao": "Distância estimada entre origem e destino."},
    {"campo": "tempo_min", "explicacao": "Tempo estimado em minutos."},
    {"campo": "custo_rs", "explicacao": "Custo operacional estimado."},
    {"campo": "co2_estimado", "explicacao": "Emissão estimada no trecho."},
    {"campo": "bitstring", "explicacao": "Código de 0 e 1 usado na demonstração quantum-inspired para representar uma combinação testada."},
    {"campo": "criptografia pós-quântica", "explicacao": "Camada futura de segurança para proteger dados logísticos contra ameaças associadas à computação quântica."},
])

parametros = pd.DataFrame([
    {"parametro": "Objetivo", "valor": "Escolher a melhor rota com leitura simples para operação, gestão e negócios."},
    {"parametro": "Base", "valor": "Demonstração simulada com coordenadas para Google Maps."},
    {"parametro": "Camada quântica", "valor": "Quantum-inspired, com evolução possível para QUBO, Ising e QAOA."},
    {"parametro": "Segurança futura", "valor": "Prever criptografia pós-quântica como diferencial de cybersecurity."},
])

# Ranking simples de rotas para inspeção da planilha
records = []
clients = [x for x in pontos["id"].tolist() if x != "Hub"]
edge_map = {}
for _, r in rotas.iterrows():
    edge_map[frozenset([r["origem"], r["destino"]])] = r
for perm in itertools.permutations(clients):
    route = ["Hub"] + list(perm) + ["Hub"]
    dist = tempo = custo = co2 = 0
    ok = True
    for a, b in zip(route[:-1], route[1:]):
        edge = edge_map.get(frozenset([a, b]))
        if edge is None:
            ok = False
            break
        dist += float(edge["distancia_km"])
        tempo += float(edge["tempo_min"])
        custo += float(edge["custo_rs"])
        co2 += float(edge["co2_estimado"])
    if ok:
        records.append({"rota": " → ".join(route), "distancia_km": dist, "tempo_min": tempo, "custo_rs": custo, "co2": co2})
rotas_calculadas = pd.DataFrame(records)
rotas_calculadas["score_demo"] = (
    rotas_calculadas["distancia_km"] / rotas_calculadas["distancia_km"].max() * 0.25 +
    rotas_calculadas["tempo_min"] / rotas_calculadas["tempo_min"].max() * 0.25 +
    rotas_calculadas["custo_rs"] / rotas_calculadas["custo_rs"].max() * 0.25 +
    rotas_calculadas["co2"] / rotas_calculadas["co2"].max() * 0.25
)
rotas_calculadas = rotas_calculadas.sort_values("score_demo").reset_index(drop=True)
rotas_calculadas.insert(0, "opcao", [f"Rota {i+1}" for i in range(len(rotas_calculadas))])

with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
    pontos.to_excel(writer, sheet_name="Pontos", index=False)
    rotas.to_excel(writer, sheet_name="Rotas", index=False)
    cenarios.to_excel(writer, sheet_name="Cenarios", index=False)
    parametros.to_excel(writer, sheet_name="Parametros", index=False)
    rotas_calculadas.to_excel(writer, sheet_name="Rotas_Calculadas", index=False)
    dicionario.to_excel(writer, sheet_name="Dicionario", index=False)

print(f"Planilha criada em: {output_path.resolve()}")
