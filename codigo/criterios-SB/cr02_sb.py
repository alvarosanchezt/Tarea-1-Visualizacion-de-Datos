import pandas as pd
import matplotlib.pyplot as plt

regions = {
    "DE ANTOFAGASTA": "Antofagasta",
    "DE ARICA Y PARINACOTA": "Arica y Parinacota",
    "DE ATACAMA": "Atacama",
    "DE AYSEN DEL GENERAL CARLOS IBAÑEZ DEL CAMPO": "Aysén",
    "DE COQUIMBO": "Coquimbo",
    "DE LA ARAUCANIA": "La Araucanía",
    "DE LOS LAGOS": "Los Lagos",
    "DE LOS RIOS": "Los Ríos",
    "DE MAGALLANES Y DE LA ANTARTICA CHILENA": "Magallanes",
    "DE TARAPACA": "Tarapacá",
    "DE VALPARAISO": "Valparaíso",
    "DE ÑUBLE": "Ñuble",
    "DEL BIOBIO": "Bio Bio",
    "DEL LIBERTADOR GENERAL BERNARDO O'HIGGINS": "O'Higgins",
    "DEL MAULE": "Maule",
    "METROPOLITANA DE SANTIAGO": "Metropolitana",
}

participation_df  = pd.read_excel(
    'datos/2021_11_Presidencial_1V_Datos_Eleccion.xlsx', 
    sheet_name='Participación en Chile', 
    usecols='A:J',
    skiprows=6
)

region_resume = participation_df.groupby('Región')[['Inscritos', 'Votación']].sum().reset_index()
region_resume['Porcentaje Votación'] = (region_resume['Votación'] / region_resume['Inscritos']) * 100
region_resume['Región'] = region_resume['Región'].replace(regions)

def get_poverty_resume(file_path, sheet_name, usecols, skiprows, nrows, title, label):
    poverty_extreme_df  = pd.read_excel(
        file_path, 
        sheet_name=sheet_name, 
        usecols=usecols, 
        skiprows=skiprows, 
        nrows=nrows
    )
    poverty_filtered = poverty_extreme_df[poverty_extreme_df['Unnamed: 1'] == 'Estimación'].copy()
    poverty_filtered = poverty_filtered.rename(columns={title: 'Región'})
    poverty_resume = poverty_filtered[['Región', 2020]].copy()
    poverty_resume = poverty_resume.rename(columns={2020: f'Porcentaje Pobreza {label}'})
    return poverty_resume

resume_xtrm_poverty = get_poverty_resume(
        'datos/Pobreza_por_Ingreso_Casen_en_Pandemia_2020_revisado2022_09.xlsx', 
        sheet_name='8', 
        usecols='A:I', 
        skiprows=6, 
        nrows=33,
        title='Pobres extremos',
        label='Extrema'
    )

resume_no_xtrm_poverty = get_poverty_resume(
        'datos/Pobreza_por_Ingreso_Casen_en_Pandemia_2020_revisado2022_09.xlsx', 
        sheet_name='8', 
        usecols='A:I', 
        skiprows=43, 
        nrows=33,
        title='Pobres no extremos',
        label='No Extrema'
    )

resume_total_poverty = get_poverty_resume(
        'datos/Pobreza_por_Ingreso_Casen_en_Pandemia_2020_revisado2022_09.xlsx', 
        sheet_name='8', 
        usecols='A:I', 
        skiprows=80, 
        nrows=33,
        title='Total pobres1',
        label='Total'
    )

df = region_resume.merge(resume_total_poverty, on="Región")

pobreza_min = df["Porcentaje Pobreza Total"].min()
pobreza_max = df["Porcentaje Pobreza Total"].max()
votacion_min = df["Porcentaje Votación"].min()
votacion_max = df["Porcentaje Votación"].max()

pobreza_corte = pobreza_min + (pobreza_max - pobreza_min) / 2
votacion_corte = votacion_min + (votacion_max - votacion_min) / 2

# normalizar puntois
min_size, max_size = 60, 800
vot_min = df["Votación"].min()
vot_max = df["Votación"].max()
df["Tamaño Punto"] = df["Votación"].apply(lambda x: min_size + (max_size - min_size) * (x - vot_min) / (vot_max - vot_min))

fig, ax = plt.subplots(figsize=(11, 8))
ax.axhline(votacion_corte, color='gray', linestyle='--', linewidth=1)
ax.axvline(pobreza_corte, color='gray', linestyle='--', linewidth=1)

for _, row in df.iterrows(): # setear colores
    if row["Porcentaje Votación"] > votacion_corte and row["Porcentaje Pobreza Total"] > pobreza_corte:
        color = "orange"
    elif row["Porcentaje Votación"] > votacion_corte and row["Porcentaje Pobreza Total"] <= pobreza_corte:
        color = "green"
    elif row["Porcentaje Votación"] <= votacion_corte and row["Porcentaje Pobreza Total"] > pobreza_corte:
        color = "red"
    else:
        color = "blue"

    ax.scatter(
        row["Porcentaje Pobreza Total"],
        row["Porcentaje Votación"],
        s=row["Tamaño Punto"],
        color=color,
        alpha=0.7,
        edgecolor='black',
        linewidth=0.5
    )

    ax.annotate(
        row["Región"],
        (row["Porcentaje Pobreza Total"], row["Porcentaje Votación"]),
        xytext=(5, 5),
        textcoords='offset points',
        fontsize=9,
        ha='left',
        bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="black", lw=0.5),
        arrowprops=dict(arrowstyle="->", lw=0.5, color='gray', alpha=0.5)
    )

ax.set_title("Pobreza Total vs Participación", fontsize=15)
ax.set_xlabel("Porcentaje de pobreza Total (%)", fontsize=12)
ax.set_ylabel("Porcentaje de votación (%)", fontsize=12)
ax.grid(True, linestyle="--", alpha=0.4)
plt.tight_layout()
plt.show()