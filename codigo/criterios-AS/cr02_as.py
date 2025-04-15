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

# Obtener todos los candidatos únicos
candidatos_unicos = votos_agrupados["Candidato"].unique()

# Asignar un color a cada candidato
color_por_candidato = {
    candidato: colors[i % len(colors)]
    for i, candidato in enumerate(candidatos_unicos)
}



# Obtener las fechas únicas de elecciones
fechas = votos_agrupados["Fecha"].unique()
fig, axs = plt.subplots(nrows=1,
                        ncols=len(fechas),
                        figsize=(21, 11.5),
                        squeeze=True,)


# Crear waffle por elección
for i, fecha in enumerate(fechas):
    ax = axs[i]
    
    # Filtrar datos de esa elección
    data_fecha = votos_agrupados[votos_agrupados["Fecha"] == fecha]
    
    # Ordenar por votos descendente
    data_fecha = data_fecha.sort_values(by="Votos", ascending=False)
    
    # Calcular porcentaje (aproximado)
    total_votos = data_fecha["Votos"].sum()
    valores_pct = (data_fecha["Votos"] / total_votos * 100).round().astype(int)
    
    # Eliminar ceros (por si acaso)
    data_fecha = data_fecha[valores_pct > 0]
    valores_pct = valores_pct[valores_pct > 0]

    # Obtener colores según candidato
    colores = [color_por_candidato[cand] for cand in data_fecha["Candidato"]]

    # Crear el waffle
    Waffle.make_waffle(
        ax=ax,
        rows=20,
        columns=5,
        values=valores_pct.tolist(),
        colors=colores,
        starting_location='SW',
        facecolor = 'whitesmoke',
    )

    # Título individual de cada waffle
    ax.set_title(f"{fecha.strftime('%Y')}", fontsize=12, fontweight='bold', y=1.05)

# Título general
fig.suptitle('Distribución porcentual de votos por candidato\nElecciones presidenciales en Chile (1989–2017)',
             fontsize=14, fontweight='bold', y=1)

# Leyenda
legend_elements = [
    mpatches.Patch(color=color_por_candidato[candidato], label=candidato)
    for candidato in candidatos_unicos
]
fig.legend(
    handles=legend_elements,
    loc="upper left",
    bbox_to_anchor=(0.81, 0.95),
    title="Candidatos",
    title_fontsize=12
)


plt.tight_layout()
plt.subplots_adjust(right=0.80, top=0.85)  # Reduce el espacio de los márgenes para acomodar todo
plt.show()
# for i, (ax, fecha) in enumerate(zip(axs, fechas)):
#     # Filtrar solo los datos de esa elección
#     data_fecha = votos_agrupados[votos_agrupados["Fecha"] == fecha]

#     # Crear el diccionario: {candidato: votos} para esa elección
#     values = dict(zip(data_fecha["Candidato"], data_fecha["Votos"]))

#     # Total para convertir a porcentajes (puedes usar valores absolutos si prefieres)
#     total_votos = sum(values.values())
#     values_pct = {k: round(v / total_votos * 100) for k, v in values.items()}

#     # Crear el waffle para esa elección
#     Waffle.make_waffle(
#         ax=ax,
#         rows=20,
#         columns=5,
#         values=values_pct,
#         colors=[colors[i % len(colors)] for i in range(len(values))],
#         starting_location='NW'
#     )

#     ax.set_title(f'{fecha.strftime("%Y-%m-%d")}', fontsize=10, weight='bold')

# # Título general
# fig.suptitle('Distribución de votos por candidato en las elecciones presidenciales de Chile (1989-2017)',
#              fontsize=14, fontweight='bold', y=1.1)

# # Leyenda
# legend_labels = votos_agrupados["Candidato"].unique().tolist()
# legend_elements = [mpatches.Patch(color=colors[i % len(colors)],
#                                   label=legend_labels[i]) for i in range(len(legend_labels))]

# fig.legend(handles=legend_elements,
#            loc="upper right",
#            title="Candidatos",
#            bbox_to_anchor=(1.05, 0.9))

# plt.tight_layout()
# plt.subplots_adjust(right=0.85)
# plt.show()

# # Init the whole figure and axes
# fig, axs = plt.subplots(nrows=1,
#                         ncols= 7,
#                         figsize=(20,20),)

# # Iterate over each bar and create it
# for i,ax in enumerate(axs):
    
#     col_name = df.Fecha[i]
#     values = votos_agrupados["Votos"] # values from the i-th column
    
#     Waffle.make_waffle(
#         ax=ax,  # pass axis to make_waffle 
#         rows=20,
#         columns=5,
#         values=values,
#     )


# fig.suptitle('Distribución de votos por candidato en las elecciones presidenciales de Chile (1989-2017)',
#              fontsize=10, fontweight='bold')

# # Add a legend
# legend_labels = votos_agrupados["Candidato"].unique().tolist()
# print(legend_labels)
# legend_elements = [mpatches.Patch(color=colors[i],
#                                   label=legend_labels[i]) for i in range(len(colors))]
# fig.legend(handles=legend_elements,
#            loc="upper right",
#            title="Candidatos",
#            bbox_to_anchor=(1.04, 0.9))

# plt.subplots_adjust(right=0.85)

# plt.show()
