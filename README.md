# Central de rotas

Aplicação do checkpoint 5: cálculo de caminho mínimo com Dijkstra e interface em Streamlit. O mapa usa os sete pontos e as doze ruas do enunciado.

Além do cálculo normal, dá para interditar uma rua ou alterar sua distância e comparar o resultado com o mapa original.

## Executar no Linux

Requer Python 3.11 ou superior. Abra o terminal nesta pasta e execute:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

Abra o endereço indicado no terminal, normalmente `http://localhost:8501`. A instalação das bibliotecas precisa de internet; o cálculo e o mapa funcionam localmente, sem APIs externas.

## Usar

1. Selecione a origem e o destino.
2. Clique em **Calcular rota**.
3. Confira o percurso, os trechos e a distância total. As ruas da rota aparecem com linha mais grossa no mapa.
4. Para o desafio adicional, marque **Simular mudança em uma rua**. Escolha a rua, a mudança e calcule novamente.
5. Desmarque a simulação e recalcule para voltar ao mapa original.

Exemplo: de A até G, o programa encontra `A -> D -> G`, com 5 km. Interditando D ↔ G, o percurso muda para `A -> D -> F -> G`, com 6 km. Alterar a distância de D ↔ G para 10 km também produz esse desvio.

Se os controles forem alterados, o resultado anterior sai da tela até um novo cálculo. Isso evita mostrar uma rota que não corresponde à seleção atual.

## Arquivos

| Arquivo | Conteúdo |
| --- | --- |
| `app.py` | Controles e resultados no Streamlit |
| `grafo.py` | Dados, alteração de rua e implementação manual de Dijkstra |
| `mapa.py` | Desenho do grafo com Matplotlib |
| `requirements.txt` | Versões das bibliotecas utilizadas |
| `testes.py` | Testes do algoritmo e dos cenários |
| `testes_resultado.txt` | Saída da execução dos testes |
| `relatorio.pdf` | Relatório curto com análise dos resultados |
| `relatorio.md` | Versão editável do texto do relatório |
| `capturas/` | Telas reais da aplicação em execução |
| `.streamlit/config.toml` | Tema e configuração local |

## Testar

```bash
python testes.py
```

Os testes usam somente a biblioteca padrão. São nove métodos de teste, incluindo os quatro percursos do relatório e uma comparação dos 49 pares de pontos com a enumeração de todos os caminhos simples. Essa enumeração serve apenas como conferência no mapa pequeno; a aplicação usa Dijkstra.

Também são verificados: vértice inválido, peso negativo ou não finito, destino desconectado, origem igual ao destino, alteração de distância e interdição nos dois sentidos. A função retorna distância zero para um ponto até ele mesmo; a interface pede pontos diferentes, conforme o enunciado.

## Capturas

| Arquivo | Situação |
| --- | --- |
| `01_interface.png` | Interface antes do cálculo |
| `02_rota_A_G.png` | A até G, 5 km |
| `03_rota_A_C.png` | A até C, 6 km |
| `04_rota_E_C.png` | E até C, 8 km |
| `05_rota_G_A.png` | Percurso inverso, G até A, 5 km |
| `06_rua_D_G_interditada.png` | Interdição de D ↔ G, rota com 6 km |
| `07_distancia_D_G_alterada.png` | D ↔ G com 10 km, rota com 6 km |
| `08_validacao.png` | Origem e destino iguais |

O mapa é esquemático: o tamanho das linhas não representa a distância. O que determina o custo é o número de quilômetros indicado em cada rua.

## Referências

Enunciado fornecido: `cp 5 - Dynamic Programming.pdf`, atividade de grafos e caminho mínimo com Dijkstra.

- [Executar uma aplicação Streamlit](https://docs.streamlit.io/develop/concepts/architecture/run-your-app)
- [Referência de st.pyplot](https://docs.streamlit.io/develop/api-reference/charts/st.pyplot)
