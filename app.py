import streamlit as st

from grafo import LOCAIS, RUAS, alterar_rua, criar_grafo, dijkstra
from mapa import desenhar_grafo


def nome_local(codigo):
    return f"{codigo} | {LOCAIS[codigo]}"


def texto_rota(caminho):
    return " → ".join(caminho)


st.set_page_config(page_title="Central de rotas", layout="wide")
st.caption("CHECKPOINT 5 / GRAFOS E CAMINHO MÍNIMO")
st.title("Central de rotas")
st.write("Escolha os pontos da entrega e encontre o menor percurso pela cidade.")

original = criar_grafo()
controles, mapa = st.columns([1, 2.1], gap="large")

with controles:
    with st.container(border=True):
        st.header("Planejar viagem")
        origem = st.selectbox("Origem", list(LOCAIS), format_func=nome_local)
        destino = st.selectbox("Destino", list(LOCAIS), index=6, format_func=nome_local)
        simular = st.checkbox("Simular mudança em uma rua")
        rua = None
        peso = None
        interditada = False
        if simular:
            with st.expander("Condição da rua", expanded=True):
                rua = st.selectbox(
                    "Rua", [(a, b) for a, b, _ in RUAS], index=9,
                    format_func=lambda par: f"{par[0]} ↔ {par[1]}",
                )
                acao = st.radio("Mudança", ["Interditar", "Alterar distância"], horizontal=True)
                interditada = acao == "Interditar"
                if not interditada:
                    peso = st.number_input(
                        "Nova distância (km)", min_value=0.1, max_value=1000.0,
                        value=float(original[rua[0]][rua[1]]), step=0.5,
                        key=f"peso_{rua[0]}_{rua[1]}",
                    )
                st.caption("A mudança vale nos dois sentidos. Desmarque a simulação para restaurar o mapa.")
        calcular = st.button("Calcular rota", type="primary", width="stretch")

grafo = alterar_rua(original, *rua, novo_peso=peso, interditada=interditada) if simular else original
pedido = (origem, destino, simular, rua, peso, interditada)
if calcular:
    if origem == destino:
        st.session_state.pop("resultado", None)
    else:
        distancia, caminho = dijkstra(grafo, origem, destino)
        st.session_state.resultado = (pedido, distancia, caminho)

resultado = st.session_state.get("resultado")
atualizado = resultado is not None and resultado[0] == pedido
caminho = resultado[2] if atualizado else []

with controles:
    if origem == destino:
        st.warning("Escolha pontos diferentes para origem e destino.")
    elif atualizado:
        distancia = resultado[1]
        if not caminho:
            st.error("Não existe caminho entre os pontos selecionados.")
        else:
            st.header("Percurso encontrado")
            st.metric("Distância total", f"{distancia:g} km")
            st.markdown(f"**{texto_rota(caminho)}**")
            st.caption(f"{len(caminho) - 1} ruas percorridas")
            st.table([
                {"Trecho": f"{a} → {b}", "Distância": f"{grafo[a][b]:g} km"}
                for a, b in zip(caminho, caminho[1:])
            ])
    else:
        st.info("Selecione os pontos e clique em Calcular rota.")

with mapa:
    st.header("Mapa da cidade")
    st.caption("7 pontos / 12 ruas no mapa original / distâncias em quilômetros")
    figura = desenhar_grafo(grafo, caminho, rua if simular and interditada else None)
    st.pyplot(figura, width="stretch")
    figura.clear()
    st.caption("Mapa esquemático. As posições dos pontos não estão em escala.")
    if simular:
        if interditada:
            st.warning(f"Rua {rua[0]} ↔ {rua[1]} interditada nos dois sentidos.")
        else:
            st.info(f"Rua {rua[0]} ↔ {rua[1]}: {original[rua[0]][rua[1]]:g} km no mapa original, {peso:g} km na simulação.")
        if atualizado and caminho:
            distancia_original, caminho_original = dijkstra(original, origem, destino)
            st.write(f"**Sem a mudança:** {texto_rota(caminho_original)} ({distancia_original:g} km).")
            diferenca = resultado[1] - distancia_original
            if diferenca > 0:
                st.write(f"A mudança acrescentou {diferenca:g} km à menor rota disponível.")
            elif diferenca < 0:
                st.write(f"A mudança reduziu a menor distância em {abs(diferenca):g} km.")
            else:
                st.write("A menor distância permaneceu igual, mesmo com a mudança na rua.")

st.divider()
with st.expander("Consultar ruas e funcionamento"):
    st.write("As ruas são bidirecionais. O algoritmo soma as distâncias dos trechos para escolher o caminho de menor custo.")
    st.table([{"Origem": a, "Destino": b, "Distância (km)": p} for a, b, p in RUAS])
