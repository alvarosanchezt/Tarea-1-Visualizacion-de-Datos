import pandas as pd
import matplotlib.pyplot as plt
import argparse
import joypy

# Leer el archivo Excel
voters_df = pd.read_excel(
    'datos/2021_11_Presidencial_1V_Datos_Eleccion.xlsx', 
    sheet_name='Descripción votantes extranjero',
    usecols='A:I', 
    skiprows=6
)

def get_age_middle(age_range):
    # Manejo especial para rangos que terminan en '+'
    if '+' in age_range:
        start = int(age_range.replace('+', ''))
        end = start + 4  # Asumimos un rango de 5 años como los otros rangos
    else:
        start, end = map(int, age_range.split('-'))
    return (start + end) / 2

def plot_age_ridgeline(df, view_type='all', selected_continent=None):
    df['Edad_Media'] = df['Rango etario'].apply(get_age_middle)
    
    if view_type == 'all':
        plot_data = df
        group_by = 'País'
        title = "Distribución de edades de votantes por País"
    elif view_type == 'continents':
        plot_data = df
        group_by = 'Continente'
        title = "Distribución de edades de votantes por Continente"
    elif view_type == 'continent_detail':
        if selected_continent is None:
            raise ValueError("Se requiere especificar un continente para esta vista")
        plot_data = df[df['Continente'] == selected_continent]
        group_by = 'País'
        title = f"Distribución de edades de votantes en {selected_continent}"
    else:
        raise ValueError("Tipo de vista no válido")

    plt.figure(figsize=(12, 10))
    joypy.joyplot(
        data=plot_data,
        by=group_by,
        column="Edad_Media",
        colormap=plt.cm.viridis,
        title=title,
        labels=plot_data[group_by].unique(),
        overlap=0.4,
        range_style='all',
        tails=0.2,
        grid=True,
        ylim='max',
        fill=True,
        linewidth=0.5,
    )

    plt.xlabel("Edad")
    plt.show()

def main():
    # Configurar el parser de argumentos
    parser = argparse.ArgumentParser(description='Visualizar distribución de edades de votantes')
    parser.add_argument(
        '--tipo', 
        choices=['all', 'continents', 'continent_detail'],
        default='all',
        help='Tipo de visualización: todos los países, continentes, o detalle de continente'
    )
    parser.add_argument(
        '--continente',
        help='Continente a visualizar (requerido si tipo=continent_detail)',
        default=None
    )
    
    args = parser.parse_args()
    
    # Cargar datos
    voters_df = pd.read_excel(
        'datos/2021_11_Presidencial_1V_Datos_Eleccion.xlsx', 
        sheet_name='Descripción votantes extranjero',
        usecols='A:I', 
        skiprows=6
    )
    
    # Validar argumentos
    if args.tipo == 'continent_detail' and args.continente is None:
        parser.error("--continente es requerido cuando --tipo=continent_detail")
    
    # Generar visualización
    plot_age_ridgeline(voters_df, view_type=args.tipo, selected_continent=args.continente)

if __name__ == '__main__':
    main()