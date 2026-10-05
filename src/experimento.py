"""
Diseño y ejecución del experimento de escalabilidad.
Ejecutar: python -m src.experimento   (desde la raíz del proyecto)
"""
import csv
import os
import random

from src.generador_datos import generar_estudiantes
from src.estructuras import construir_lista, construir_abb, construir_bplus
from src.medicion import medir_repetido

TAMANOS_N_PRUEBA = [100, 1000, 5000, 20000, 50000]
VALORES_M = [100, 500]
REPETICIONES = 10

ESTRUCTURAS = [
    ("Lista", construir_lista),
    ("ABB", construir_abb),
    ("B+", construir_bplus),
]


def correr_experimento(tamanos_n, valores_m, repeticiones, estructuras):
    resultados = []
    for n in tamanos_n:
        datos_ordenados = sorted(generar_estudiantes(n, semilla=n), key=lambda e: e["id"])
        datos_aleatorios = datos_ordenados.copy()
        random.shuffle(datos_aleatorios)

        for nombre_orden, datos in [("ordenado", datos_ordenados), ("aleatorio", datos_aleatorios)]:
            for nombre_estructura, builder in estructuras:
                print(f"  Construyendo {nombre_estructura} (n={n}, {nombre_orden})...")
                estructura = builder(datos)  # <- se construye UNA sola vez aquí

                for m in valores_m:
                    if m > n:
                        continue
                    ids_prueba = [e["id"] for e in random.sample(datos, m)]
                    r = medir_repetido(estructura, ids_prueba, repeticiones)
                    resultados.append({
                        "estructura": nombre_estructura,
                        "orden_insercion": nombre_orden,
                        "n": n,
                        "m": m,
                        "repeticiones": repeticiones,
                        "media_segundos": r["media"],
                        "std_segundos": r["std"],
                        "outliers_descartados": r["n_descartados"],
                        "altura_estructura": r["altura"],
                    })
                    print(f"    n={n}, m={m}, {nombre_estructura} ({nombre_orden}) completado")
    return resultados


def guardar_csv(resultados, ruta="resultados/resultados_experimento.csv"):
    campos = ["estructura", "orden_insercion", "n", "m", "repeticiones",
              "media_segundos", "std_segundos", "outliers_descartados", "altura_estructura"]
    os.makedirs(os.path.dirname(ruta), exist_ok=True)
    with open(ruta, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=campos)
        writer.writeheader()
        writer.writerows(resultados)
    print(f"Resultados guardados en: {os.path.abspath(ruta)}")


if __name__ == "__main__":
    resultados = correr_experimento(TAMANOS_N_PRUEBA, VALORES_M, REPETICIONES, ESTRUCTURAS)
    guardar_csv(resultados)