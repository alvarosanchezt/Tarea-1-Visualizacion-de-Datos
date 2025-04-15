import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
import numpy as np

# Cargar tu DataFrame (reemplaza 'elecciones.csv' por tu archivo real)
df = pd.read_csv("datos/Suma de Votos Totales y Primera fecha Candidato (a) por Año, Mes, Día, Votación Presidencial y Partido.csv")

meses = {
    'enero': 1, 'febrero': 2, 'marzo': 3, 'abril': 4, 'mayo': 5, 'junio': 6,
    'julio': 7, 'agosto': 8, 'septiembre': 9, 'octubre': 10, 'noviembre': 11, 'diciembre': 12
}
df["Mes_Num"] = df["Mes"].str.lower().map(meses)
df_fecha = df.rename(columns={"Año": "year", "Mes_Num": "month", "Día": "day"})
df = df.rename(columns={"Primera fecha: Candidato (a)": "Candidato"})
# Crear columna de fecha para orden cronológico
df["Fecha"] = pd.to_datetime(df_fecha[["year", "month", "day"]])

# Etiqueta para mostrar en el eje X
df["Etiqueta"] = df["Votación Presidencial"] + " " + df["Año"].astype(str)

# Agrupar por fecha y partido
votos_por_fecha = df.groupby(["Fecha", "Partido", "Candidato"])["Suma de Votos Totales"].sum().reset_index()

# Calcular porcentajes
totales_por_fecha = votos_por_fecha.groupby("Fecha")["Suma de Votos Totales"].sum().reset_index()
totales_por_fecha.columns = ["Fecha", "Total Votos"]
votos_por_fecha = pd.merge(votos_por_fecha, totales_por_fecha, on="Fecha")
votos_por_fecha["Porcentaje"] = (votos_por_fecha["Suma de Votos Totales"] / votos_por_fecha["Total Votos"]) * 100

# Ordenar y calcular bordes para las cintas
votos_por_fecha = votos_por_fecha.sort_values(by=["Fecha", "Porcentaje"], ascending=[False, True])
votos_por_fecha["y0"] = votos_por_fecha.groupby("Fecha")["Porcentaje"].cumsum() - votos_por_fecha["Porcentaje"]
votos_por_fecha["y1"] = votos_por_fecha.groupby("Fecha")["Porcentaje"].cumsum()

# Colores por partido
colors = {
    'ALIANZA HUMANISTA VERDE': '#FF5733',
    'COMUNISTA DE CHILE': '#33FF57',
    'DEMOCRATA CRISTIANO': '#3357FF',
    'HUMANISTA': '#F0E68C',
    'INDEPENDIENTE': '#FF8C00',
    'PAIS': '#8B008B',
    'PARTIDO ECOLOGISTA VERDE': '#00FFFF',
    'PARTIDO IGUALDAD': '#FF1493',
    'PARTIDO PROGRESISTA': '#1E90FF',
    'PARTIDO REGIONALISTA DE LOS INDEPENDIENTES': '#32CD32',
    'POR LA DEMOCRACIA': '#FFD700',
    'RENOVACION NACIONAL': '#800080',
    'SOCIALISTA DE CHILE': '#008080',
    'UNION DE CENTRO CENTRO': '#D2691E',
    'UNION DEMOCRATA INDEPENDIENTE': '#A52A2A',
    'UNION PATRIOTICA': '#B8860B',
}

# Preparar coordenadas para el gráfico
fechas_unicas = sorted(votos_por_fecha["Fecha"].unique())
x_vals = list(range(len(fechas_unicas)))
fecha_to_x = dict(zip(fechas_unicas, x_vals))
votos_por_fecha["x"] = votos_por_fecha["Fecha"].map(fecha_to_x)



# Crear gráfico tipo Ribbon
fig = go.Figure()

# Añadir trazas invisibles solo para mostrar leyenda una vez por partido
for partido in votos_por_fecha["Partido"].unique():
    fig.add_trace(go.Scatter(
        x=[None], y=[None],
        mode='markers',
        marker=dict(color=colors.get(partido, '#999999'), size=10),
        name=partido,
        legendgroup=partido,  # 💡 clave para agrupar
        showlegend=True,
        hoverinfo='skip'
    ))

for partido in votos_por_fecha["Partido"].unique():
    subdf = votos_por_fecha[votos_por_fecha["Partido"] == partido].sort_values("x")
    
    # Detectar bloques contiguos
    subdf["x_diff"] = subdf["x"].diff().fillna(1)
    subdf["block"] = (subdf["x_diff"] > 1).cumsum()

    for _, block_df in subdf.groupby("block"):
        if len(block_df) < 2:
            continue  # No se puede hacer una cinta con un solo punto

        x = block_df["x"].tolist()
        x_rev = x[::-1]
        y0 = block_df["y0"].tolist()
        y1 = block_df["y1"].tolist()

        hover_text = [
            f"<b>Partido:</b> {partido}<br>"
            f"<b>Votos:</b> {votos:,}<br>"
            f"<b>Porcentaje:</b> {porc:.1f}%"
            for votos, porc in zip(block_df["Suma de Votos Totales"], block_df["Porcentaje"])
        ]

        fig.add_trace(go.Scatter(
            x=x + x_rev,
            y=y1 + y0[::-1],
            fill='toself',
            mode='lines',
            line=dict(color='rgba(0,0,0,0)'),
            fillcolor=colors.get(partido, '#999999'),
            opacity=0.5,
            line_width=1,
            line_smoothing=0.6,
            name=partido,
            legendgroup=partido,  # 💡 esto agrupa
            hoverinfo='text',
            text=hover_text,
            line_shape='spline',
            showlegend=False,  # Ya está en la leyenda
        ))


fig.update_xaxes(range=[-0.15,11],tickmode = 'array',showticklabels=True,
            ticktext = [fecha.strftime("%d-%b-%Y") for fecha in fechas_unicas],
            tickvals = x_vals)

# Etiquetas del eje X
ticktext = [fecha.strftime("%d-%b-%Y") for fecha in fechas_unicas]
tickvals = x_vals


# Generar barras de referencia para cada elección (tipo stacked bar por fecha)
for i, fecha in enumerate(fechas_unicas):
    subdf = votos_por_fecha[votos_por_fecha["Fecha"] == fecha]
    
    y_base = 0
    for _, row in subdf.iterrows():
        fig.add_trace(go.Bar(
            x=[i], 
            y=[row["Porcentaje"]],
            base=y_base,
            marker=dict(color=colors.get(row["Partido"], "#999999")),
            width=0.5,
            hoverinfo="text",
            text=row["Partido"] + f"<br><b>Votos:</b> {int(row['Suma de Votos Totales']):,}<br><b>Porcentaje:</b> {row['Porcentaje']:.1f}%",
            name=row["Partido"],
            legendgroup=row["Partido"],  # 💡 misma agrupación
            showlegend=False,
        ))
        y_base += row["Porcentaje"]
        
# Configuración final
fig.update_layout(
    barmode='stack',  bargap=0.5,showlegend=True, legend_title_text="Partidos",
    title=dict(
        text="<b>Evolución de participación por partido en elecciones presidenciales de Chile (1989–2017)</b>",
        x=0.5,  # Centrado (0: izquierda, 1: derecha)
        xanchor='center',
        font=dict(size=20), 
    ),
    xaxis=dict(title="Elección", tickmode='array', tickvals=tickvals, ticktext=ticktext),
    yaxis=dict(title="Porcentaje de votos", range=[0, 100]),
    plot_bgcolor='white',
    height=750
)

fig.show()