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
python ./codigo/criterios-SB/cr01_sb.py --tipo all
```

2. Para ver todos los continentes:
```bash
python ./codigo/criterios-SB/cr01_sb.py --tipo continents
```

3. Para ver paises por un continente específico (AMERICA, EUROPA, AFRICA, ASIA, OCEANIA): 
```bash
python ./codigo/criterios-SB/cr01_sb.py --tipo continent_detail --continente EUROPA 
```

### Ejecución `cr01_sb.py`   
```bash
python ./codigo/criterios-SB/cr02_sb.py
```

### Ejecución `cr01_bg.ipynb`

Ejecutar la primera caja de código para ver el gráfico con Franco Parisi incluido.

Ejecutar la segunda caja de código para ver el gráfico sin Franco Parisi.

### Ejecución `cr02_bg.ipynb`

Ejecutar la única caja en el archivo para que se abra el gráfico en el navegador predeterminado.