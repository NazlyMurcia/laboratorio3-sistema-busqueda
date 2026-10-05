"""
Demo interactiva: muestra que buscar, insertar y listar funcionan, sobre
un dataset pequeño. No forma parte del análisis estadístico.
Ejecutar: python -m demo.demo_interactiva
"""
import random
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.generador_datos import generar_estudiantes
from src.estructuras import construir_lista


def demo_interactiva():
    estudiantes_demo = generar_estudiantes(12, semilla=1)
    lista_demo = construir_lista(estudiantes_demo)

    print("Estudiantes de prueba cargados:")
    for id_est, nombre, edad, promedio in lista_demo.listar_en_orden():
        print(f"  ID: {id_est}  Nombre: {nombre}  Edad: {edad}  Promedio: {promedio}")

    modo = input("¿Cómo quieres buscar? Escribe 'manual' o 'aleatorio': ").strip().lower()
    if modo == "aleatorio":
        id_buscar = random.choice([e["id"] for e in estudiantes_demo])
        print(f"ID elegido al azar: {id_buscar}")
    else:
        id_buscar = int(input("Ingresa el ID del estudiante a buscar: "))

    resultado = lista_demo.buscar(id_buscar)
    if resultado:
        print(f"Encontrado -> ID: {resultado.id}, Nombre: {resultado.nombre}, "
              f"Edad: {resultado.edad}, Promedio: {resultado.promedio}")
    else:
        print(f"No se encontró un estudiante con ID {id_buscar}")

    nuevo_id = int(input("ID del nuevo estudiante: "))
    nuevo_nombre = input("Nombre: ")
    nueva_edad = int(input("Edad: "))
    nuevo_promedio = float(input("Promedio: "))

    lista_demo.insertar({"id": nuevo_id, "nombre": nuevo_nombre,
                          "edad": nueva_edad, "promedio": nuevo_promedio})
    print(f"Estudiante {nuevo_nombre} (ID {nuevo_id}) insertado correctamente.")

    print("Listado actualizado de estudiantes (ordenado por ID):")
    for id_est, nombre, edad, promedio in lista_demo.listar_en_orden():
        print(f"  ID: {id_est}  Nombre: {nombre}  Edad: {edad}  Promedio: {promedio}")


if __name__ == "__main__":
    demo_interactiva()