# LOGIQ MVP V2

MVP local em Streamlit para otimização de rotas urbanas sustentáveis.

## Como rodar

```powershell
Set-Location -LiteralPath "C:\Users\vivis\OneDrive\AA - Projetos\11. Quantum\Hackthon\logiq-mvp"
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python gerar_planilha.py
streamlit run app.py
```

## O que mudou na V2

- Dashboard mais executivo.
- Melhor rota indexada como Rota 1, Rota 2 etc.
- Ranking com coluna `opcao`.
- QAOA demonstrativo indexado como Bitstring 1, Bitstring 2 etc.
- Resumo executivo orientado ao negócio.
- Visual com cards, destaque de decisão, gráficos e aviso de base simulada.
