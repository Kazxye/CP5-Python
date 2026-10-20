from matplotlib.figure import Figure
from matplotlib.lines import Line2D
from matplotlib.patches import Circle

from grafo import LOCAIS, RUAS


POSICOES = {
    "A": (0, 0), "B": (1.5, 1.2), "C": (3.7, 1.2),
    "D": (2.2, 0), "E": (1.5, -1.2), "F": (3.7, -1.2),
    "G": (5.2, 0),
}


def desenhar_grafo(grafo, caminho=None, rua_interditada=None):
    caminho = caminho or []
    trechos = {frozenset(par) for par in zip(caminho, caminho[1:])}
    bloqueada = frozenset(rua_interditada or ())
    figura = Figure(figsize=(9, 5.7), facecolor="#faf9f5")
    eixo = figura.subplots()
    eixo.set_facecolor("#faf9f5")

    for origem, destino, _ in RUAS:
        x1, y1 = POSICOES[origem]
        x2, y2 = POSICOES[destino]
        par = frozenset((origem, destino))
        destaque = par in trechos
        interditada = par == bloqueada
        cor = "#b45309" if interditada else "#12675d" if destaque else "#a5afb4"
        eixo.plot(
            [x1, x2], [y1, y2], color=cor,
            linewidth=4 if destaque else 1.5,
            linestyle="--" if interditada else "-", zorder=1,
        )
        peso = grafo[origem].get(destino)
        rotulo = "X" if interditada else f"{peso:g}"
        eixo.text(
            (x1 + x2) / 2, (y1 + y2) / 2, rotulo,
            ha="center", va="center", fontsize=11,
            color=cor if destaque or interditada else "#374151",
            fontweight="bold" if destaque else "normal", zorder=3,
            bbox={"facecolor": "#faf9f5", "edgecolor": "none", "pad": 3},
        )

    for local, (x, y) in POSICOES.items():
        selecionado = local in caminho
        eixo.add_patch(Circle(
            (x, y), radius=0.18, facecolor="#12675d" if selecionado else "#fffefa",
            edgecolor="#12675d" if selecionado else "#65767d", linewidth=2, zorder=4,
        ))
        eixo.text(
            x, y, local, ha="center", va="center", fontsize=12, fontweight="bold",
            color="white" if selecionado else "#253941", zorder=5,
        )
        if local in ("A", "G"):
            eixo.text(x, y - 0.34, LOCAIS[local], ha="center", fontsize=10, color="#52626a")

    legenda = [Line2D([0], [0], color="#a5afb4", lw=1.5, label="Rua disponível")]
    if caminho:
        legenda.append(Line2D([0], [0], color="#12675d", lw=4, label="Caminho mínimo"))
    if rua_interditada:
        legenda.append(Line2D([0], [0], color="#b45309", lw=1.5, ls="--", label="Rua interditada"))
    eixo.legend(handles=legenda, loc="lower center", bbox_to_anchor=(0.5, -0.08),
                ncol=len(legenda), frameon=False, fontsize=10)
    eixo.set(xlim=(-0.55, 5.75), ylim=(-1.8, 1.8), aspect="equal")
    eixo.axis("off")
    figura.tight_layout(pad=1.8)
    return figura
