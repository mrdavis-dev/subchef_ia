# subchef_ia

App web para generar recetas de cocinas con inteligencia artificial a partir de los ingredientes disponibles.

## 🚀 Comenzando

### 📦 Prerrequisitos

- Python 3.10 (especificado en ) `.python-version`
- pip o uv (gestor de paquetes moderno y ultrarrápido para Python)

### 🏗️ Instalación

Puedes elegir entre pip (tradicional) o uv (recomendado por su rendimiento y reproducibilidad). Para comenzar con uv,
visita: [https://docs.astral.sh/uv/getting-started/](https://docs.astral.sh/uv/getting-started/).

### 🔧 Usando uv (Recomendado)

```bash
# Crear un entorno virtual (lo crea en `.venv`)
uv venv

# Activar el entorno (Unix/macOS)
source .venv/bin/activate

# En Windows (PowerShell)
.venv\Scripts\Activate.ps1

# Instalar dependencias
uv pip install -r requirements.txt
```

### 🧪 Usando pip

```bash
# Crear entorno virtual
python3.10 -m venv .venv

# Activar entorno
source .venv/bin/activate  # O .venv\Scripts\Activate.ps1 en Windows

# Instalar dependencias
pip install -r requirements.txt
```

## 🛠️ Configuración de desarrollo

Instalar herramientas de desarrollo (a través de uv o pip) para linting, empaquetado, etc.:

```bash
uv pip install --group dev
```

## 🏃‍♀️ Ejecutando la aplicación

Iniciar el servidor de desarrollo local:

```bash
streamlit run Homepage.py 
```
