LOGIQ MVP V5.0

Esta versão mantém tudo que já existia no LOGIQ 1.0 e adiciona um novo módulo opcional:

1) LOGIQ 1.0 | Rotas operacionais
- Mantém o motor clássico de rota.
- Mostra melhor rota, painel do motorista, resumo executivo, dados usados e camada quantum-inspired.
- Continua usando planilhas Excel com base, pontos, distâncias, tempo, custo e CO2.

2) LOGIQ 2.0 | QAOA simulado
- Novo módulo selecionável no menu lateral.
- Roda uma simulação QAOA local em cenário reduzido, usando statevector.
- Usa Base + até 3 pontos de entrega para manter a simulação leve e explicável.
- Compara o melhor resultado clássico do recorte com o resultado QAOA simulado.
- Mostra painel de proximidade em azul, ranking clássico do recorte e probabilidades do QAOA.

Leitura honesta:
- O LOGIQ 2.0 executa uma simulação QAOA local, ou seja, já há uma camada quântica simulada real.
- Ele ainda não roda em hardware quântico de nuvem.
- Ele ainda não promete superar algoritmos clássicos em rotas reais complexas.
- O valor está em demonstrar a ponte técnica entre logística, otimização clássica e algoritmos quânticos.

Como rodar localmente:
1. Abrir o PowerShell na pasta do projeto.
2. Ativar o ambiente virtual:
   .\.venv\Scripts\Activate.ps1
3. Instalar dependências:
   pip install -r requirements.txt
4. Rodar o sistema:
   streamlit run app.py

Como usar:
- No menu lateral, escolha "Módulo do sistema".
- Use "LOGIQ 1.0 | Rotas operacionais" para a solução de rota.
- Use "LOGIQ 2.0 | QAOA simulado" para testar a camada quântica simulada.

Observações:
- Para o Google Maps funcionar bem, a aba Pontos da planilha precisa trazer endereço real ou latitude/longitude.
- Para o QAOA simulado, o sistema usa um recorte pequeno de pontos, porque simulação quântica cresce rapidamente em complexidade.
