"""
Generación de datos sintéticos de estudiantes.

Cada estudiante tiene: id (número de matrícula, único), nombre, edad y promedio.
"""
import random


def generar_estudiantes(n=10000, semilla=None):
    """Genera n estudiantes con id único, nombre, edad y promedio."""
    if semilla is not None:
        random.seed(semilla)
    nombres = ["Ana", "Carlos", "María", "Luis", "Sofía", "Pedro",
               "Laura", "Diego", "Valentina", "Andrés"]
    estudiantes = []
    ids_usados = set()
    while len(estudiantes) < n:
        id_est = random.randint(1000, 1000 + n * 3)
        if id_est in ids_usados:
            continue
        ids_usados.add(id_est)
        estudiantes.append({
            "id": id_est,
            "nombre": random.choice(nombres),
            "edad": random.randint(17, 25),
            "promedio": round(random.uniform(5.0, 10.0), 1)
        })
    return estudiantes