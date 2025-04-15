# Tarea-1-Visualizacion-de-Datos

### **Recomendaciones**

Una vez clonado el repositorio creamos un entorno de ejecución virtual para python usando **virtualenv**

1) instalar virtualenv

   ```
   pip install virtualenv
   ```
2) Crear un entorno virtual de python, una vez clonado el proyecto nos dirigimos a la raiz y ejecutamos

   ```
   virtualenv -p python3.12 venv
   ```
3) Activar el entorno vitual (git bash no requiere cambiar permisos)

   ```
   source ./venv/Scripts/activate
   ```
4) Instalar dependencias

   ```
   pip install -r ./requirements.txt
   ```
### Comando útil.  
 - Termina sesión en entorno virtual.   

```
deactivate  
```

## Criterios
Desde ruta raiz. ```../Tarea-1-Visualizacion-de-Datos```  

### Ejecución `cr01_sb.py`  

1. Para ver todos los países:
```bash
python ./codigo/cr01_sb.py --tipo all
```

2. Para ver todos los continentes:
```bash
python ./codigo/cr01_sb.py --tipo continents
```

3. Para ver paises por un continente específico (AMERICA, EUROPA, AFRICA, ASIA, OCEANIA): 
```bash
python ./codigo/cr01_sb.py --tipo continent_detail --continente EUROPA 
```

### Ejecución `cr01_sb.py`   
```bash
python ./codigo/cr02_sb.py
```
## Datasets

-  `2021_11_Presidencial_1V_Datos_Eleccion.xlsx`  
   - Referencia: [Registro Servel Elecciones 2021](https://app.powerbi.com/view?r=eyJrIjoiYTkyYjBjMTAtN2NiMC00ZWQ5LTg4MDMtYzc5MWNiYWFjZGRhIiwidCI6IjI0ODMxZWJlLWQyNmQtNGQzMC05ZmE4LWVmM2MwMjQzYjMyZSIsImMiOjR9)  
   - Usado en: `cr01_sb.py`
   - Usado en: `cr02_sb.py`

-  `Pobreza_por_Ingreso_Casen_en_Pandemia_2020_revisado2022_09.xlsx`  
   - Referencia: [Encuesta Casen Pandemia 2020](https://observatorio.ministeriodesarrollosocial.gob.cl/encuesta-casen-en-pandemia-2020)  
   -Usado en: `cr02_sb.py`  