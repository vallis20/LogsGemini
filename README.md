# Clasificación Automática de Logs Técnicos con Gemini
Este proyecto implementa un script en Python que utiliza un modelo LLM de Google Gemini en su nivel gratuito (Gemini 2.5 Flash) para identificar el tema de un conjunto de logs y etiquetarlos automáticamente según su contenido.

El sistema procesa registros de interacción entre agentes y bases de datos, identifica su temática principal (por ejemplo: consultas, errores, autenticación, conectividad, etc.) y genera un archivo de salida estructurado en formato JSON.

La solución está diseñada considerando restricciones reales de cuota, limite de peticiones.
## Comenzando 🚀

Estas instrucciones te permitirán obtener una copia del proyecto en funcionamiento en tu máquina local para propósitos de desarrollo y pruebas.

El proyecto está diseñado para ejecutarse localmente utilizando Python y la API de Google Gemini.

Mira **Deployment** para conocer como desplegar el proyecto.


### Pre-requisitos 📋

- Python 3.10 o superior 
- API Key google gemini 
- Archivo logs.txt

### Instalación 🔧
1.  Clonar repositorio 
git clone https://github.com/vallis20/LogsGemini.git
cd LogsGemini

2. Instalación de dependencias 
pip install -r requirements.txt

3. Editar APIKey de google AI Studio
Link para obtener el API Key:
https://www.google.com/url?sa=t&source=web&rct=j&opi=89978449&url=https://aistudio.google.com/app/apikey&ved=2ahUKEwiYhrHbv8uSAxWBnCYFHXZKJXIQFnoECBkQAQ&usg=AOvVaw1WWenMsZaHnCnN4FhYRAe9

4. Ejecutar el script:
python main.py


## Despliegue 📦

Este proyecto está pensado para ejecución local como script de línea de comandos.
No requiere despliegue en servidores ni contenedores.

## Construido con 🛠️

Herramientas utilizadas para construir el proyecto:
	•	Python – Lenguaje principal
	•	Google Gemini API – Modelo LLM utilizado para clasificación
	•	JSON – Formato de salida
	•	Control de tasa (rate limiting) – Para respetar límites de cuota del modelo gratuito


## Autores ✒️

* **Estivalis Navarrete Guerrero**  [vallis20](https://github.com/vallis20)
