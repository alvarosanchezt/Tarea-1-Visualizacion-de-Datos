import matplotlib.pyplot as plt
import matplotlib.patches as mpatches # for the legend
from pywaffle import Waffle
import pandas as pd

# Leer el archivo
df = pd.read_excel("datos/resultados_elecciones_presidenciales_ce_1989_2017_Chile.xlsx")

# Renombrar columnas por claridad
df = df.rename(columns={
    "Candidato (a)": "Candidato",
    "Votos Totales": "Votos",
    "Fecha de Elección": "Fecha",
    "Votación Presidencial": "Votacion"
})

# Filtrar elecciones presidenciales - primera vuelta o única
df_pres = df[
    (df["Tipo de Elección"] == "PRESIDENCIAL") &
    (df["Votacion"].str.upper().str.contains("PRIMERA|UNICA"))
]
# Agrupar votos por candidato y año
votos_agrupados = df_pres.groupby(["Fecha", "Candidato"])["Votos"].sum().reset_index()

colors = [
    "darkred", "red", "salmon", "orangered", "tomato",
    "darkorange", "orange", "gold", "khaki", "peachpuff",
    "yellowgreen", "greenyellow", "chartreuse", "lawngreen", "limegreen",
    "seagreen", "mediumseagreen", "forestgreen", "darkgreen", "teal",
    "cadetblue", "darkcyan", "lightseagreen", "turquoise", "mediumturquoise",
    "skyblue", "deepskyblue", "dodgerblue", "cornflowerblue", "royalblue",
    "blue", "mediumblue", "darkblue", "navy", "slateblue",
    "darkslateblue"
]


# Init the whole figure and axes
fig, axs = plt.subplots(nrows=1,
                        ncols= 7,
                        figsize=(20,20),)

# Iterate over each bar and create it
for i,ax in enumerate(axs):
    
    col_name = df.Fecha[i]
    values = votos_agrupados["Votos"] # values from the i-th column
    
    Waffle.make_waffle(
        ax=ax,  # pass axis to make_waffle 
        rows=20,
        columns=5,
        values=values,
    )


fig.suptitle('Distribución de votos por candidato en las elecciones presidenciales de Chile (1989-2017)',
             fontsize=10, fontweight='bold')

# Add a legend
legend_labels = votos_agrupados["Candidato"].unique().tolist()
print(legend_labels)
legend_elements = [mpatches.Patch(color=colors[i],
                                  label=legend_labels[i]) for i in range(len(colors))]
fig.legend(handles=legend_elements,
           loc="upper right",
           title="Candidatos",
           bbox_to_anchor=(1.04, 0.9))

plt.subplots_adjust(right=0.85)

plt.show()
