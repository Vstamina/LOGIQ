LOGIQ MVP V4.2

Versão com linguagem mais simples para negócio, operação e demonstração quantum-inspired.

Principais ajustes:
- Explicação clara de pesos aplicados.
- Explicação de bitstring e custo ponderado em linguagem simples.
- Camada futura de criptografia pós-quântica como diferencial de cybersecurity.
- Google Maps usa latitude/longitude da aba Pontos quando disponíveis.
- Painel do operador mantém rota por trecho, cores e sequência visual.
- Menu de decisão permanece no lado direito.

Como rodar:
1. Abra o PowerShell na pasta do projeto.
2. Ative o ambiente virtual:
   .\.venv\Scripts\Activate.ps1
3. Instale dependências:
   pip install -r requirements.txt
4. Rode:
   streamlit run app.py

Para recriar a planilha de demonstração:
   python gerar_planilha.py

Observação:
A aba Quantum-inspired é demonstrativa. Ela traduz a lógica de combinações, pesos e bitstrings para negócios. A rota operacional continua sendo apresentada no Painel do operador.
