LOGIQ MVP V4.5

Esta versão ajusta a interface para ficar menos poluída e mais clara para usuários de negócio.

Principais mudanças:
- Remove o aviso amarelo fixo sobre dados em uso da tela principal.
- Aumenta a fonte dos títulos das abas.
- Renomeia as abas para linguagem mais simples:
  * Visão da solução
  * Rota do motorista
  * Resumo executivo
  * Dados usados
  * Lógica quântica
- Substitui os seis cards fixos de "Como a LOGIQ decide" por um ciclo visual em formato de infinito.
- Os detalhes do ciclo ficam recolhidos em um bloco expansível, para reduzir poluição visual.
- Mantém a visão do operador, a rota por trecho, o link para Google Maps e a camada quantum-inspired.

Como rodar:
1. Abrir o PowerShell na pasta do projeto
2. Ativar o ambiente virtual:
   .\.venv\Scripts\Activate.ps1
3. Instalar dependências:
   pip install -r requirements.txt
4. Rodar:
   streamlit run app.py

Observação:
Para o Google Maps funcionar bem, a aba Pontos da planilha precisa trazer endereço real ou latitude/longitude.


V4.5: Remove textos de segurança pós-quântica, simplifica o ciclo infinito e inclui a rota recomendada dentro do ciclo visual.


V4.7
- Substitui o ciclo visual anterior por uma imagem limpa em formato de fluxo contínuo.
- Separa a melhor decisão e o ciclo de decisão em blocos distintos.
- Mantém o detalhamento operacional da rota apenas nas abas próprias.
