"""
Script de clasificación temática de logs técnicos usando Gemini API (free version).

Objetivo:
- Leer un archivo de logs
- Dividirlos en bloques optimizados según límites de API
- Enviar cada bloque al modelo
- Obtener etiquetas temáticas abstractas
- Guardar los resultados en un archivo JSON

Restricciones consideradas:
- 5 peticiones por minuto
- 20 peticiones por día
"""

from google import genai
from google.genai.errors import ClientError
import json
import time
import math

# CONFIGURACIÓN GENERAL
MODEL = "gemini-2.5-flash"

ARCHIVO_LOGS = "logs 1.txt"
ARCHIVO_SALIDA = "output.json"

MAX_PETICIONES_DIA = 20
MAX_PETICIONES_MINUTO = 5
MAX_LOGS_POR_BLOQUE = 7

# Tiempo de espera entre peticiones
ESPERA_SEGUNDOS = 15

# Inicialización del cliente Gemini
client = genai.Client(
    api_key="AIzaSyC6eowv3jafsxX8ms6jrkOgTbewXEYCoSA"
)

# FUNCIONES AUXILIARES

def extraer_json(texto: str) -> list:
    """
    Extrae el primer bloque JSON válido contenido en la respuesta del modelo.

    Esto hace al sistema más robusto ante respuestas que incluyan
    texto adicional antes o después del JSON.
    """
    inicio = texto.find("[")
    fin = texto.rfind("]") + 1

    if inicio == -1 or fin == -1:
        raise ValueError("No se encontró JSON válido en la respuesta")

    return json.loads(texto[inicio:fin])


def leer_logs(path: str) -> list:
    """
    Lee el archivo de logs y devuelve una lista limpia de entradas.
    Se descartan líneas vacías.
    """
    with open(path, "r", encoding="utf-8") as f:
        logs = [linea.strip() for linea in f if linea.strip()]

    if not logs:
        raise RuntimeError("El archivo de logs está vacío")

    return logs


def calcular_bloques(total_logs: int) -> int:
    """
    Calcula dinámicamente cuántos logs enviar por petición,
    respetando el máximo diario y el límite por bloque.
    """
    peticiones_necesarias = math.ceil(total_logs / MAX_LOGS_POR_BLOQUE)
    peticiones_a_usar = min(peticiones_necesarias, MAX_PETICIONES_DIA)

    bloque_size = math.ceil(total_logs / peticiones_a_usar)
    bloque_size = min(bloque_size, MAX_LOGS_POR_BLOQUE)

    return bloque_size

# PROCESO PRINCIPAL

# 1. Leer logs
logs = leer_logs(ARCHIVO_LOGS)
total_logs = len(logs)

print(f"Total de logs detectados: {total_logs}")

# 2. Calcular tamaño de bloque óptimo
bloque_size = calcular_bloques(total_logs)

print(f"Logs por bloque: {bloque_size}")

# 3. Inicialización de variables de control
resultados = []
log_id_global = 1
peticiones_realizadas = 0

# 4. Procesamiento por bloques
for i in range(0, total_logs, bloque_size):

    if peticiones_realizadas >= MAX_PETICIONES_DIA:
        print("Límite diario alcanzado. Proceso detenido.")
        break

    bloque = logs[i:i + bloque_size]

    # Construcción del prompt
    prompt = f"""
Eres un sistema de clasificación de logs técnicos.

OBJETIVO:
Asignar ETIQUETAS TEMÁTICAS y GENERALES.
Las etiquetas deben representar categorías técnicas reutilizables,
NO reformular ni traducir el texto del log.

REGLAS OBLIGATORIAS:
- NO reutilices palabras clave del log
- NO describas el evento literal
- Usa categorías técnicas abstractas
  (ej: authentication, database connectivity, timeout error)
- Máximo 3 etiquetas por log
- Responde ÚNICAMENTE con JSON válido
- Sin explicaciones, sin Markdown

FORMATO EXACTO:

[
  {{
     "log_id": 1,
     "texto": "...",
     "etiquetas": ["..."]
  }}
]

LOGS:
"""

    for log in bloque:
        prompt += f"\nLog {log_id_global}: {log}"
        log_id_global += 1

    # Llamada al modelo
    try:
        response = client.models.generate_content(
            model=MODEL,
            contents=prompt
        )

        clasificaciones = extraer_json(response.text)

        # Asociar texto original al resultado
        for item in clasificaciones:
            idx = item["log_id"] - 1
            item["texto"] = logs[idx]
            resultados.append(item)

        peticiones_realizadas += 1
        print(f"Bloque {peticiones_realizadas} procesado")

        # Espera preventiva para evitar rate limit
        time.sleep(ESPERA_SEGUNDOS)

    except ValueError:
        print("Error al interpretar JSON. Bloque omitido.")
        continue

    except ClientError as e:
        if "429" in str(e):
            print("Cuota agotada (429). Proceso detenido.")
            break
        else:
            raise

# GUARDADO DE RESULTADOS EN ARCHIVO JSON

with open(ARCHIVO_SALIDA, "w", encoding="utf-8") as out:
    json.dump(resultados, out, indent=2, ensure_ascii=False)

print("Proceso finalizado. Archivo output.json generado.")