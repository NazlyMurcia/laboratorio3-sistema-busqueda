"""
Gráficas de escalabilidad a partir del CSV (no requiere re-correr el experimento).
Ejecutar: python -m src.graficas
"""
import csv
import os


def graficar_resultados(ruta_csv="resultados/resultados_experimento.csv",
                         m_fijo=None,
                         ruta_salida="resultados/graficas/escalabilidad.png"):
    import matplotlib.pyplot as plt

    filas = []
    with open(ruta_csv, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for fila in reader:
            fila["n"] = int(fila["n"])
            fila["m"] = int(fila["m"])
            fila["media_segundos"] = float(fila["media_segundos"])
            fila["std_segundos"] = float(fila["std_segundos"])
            filas.append(fila)

    if m_fijo is not None:
        filas = [f for f in filas if f["m"] == m_fijo]

    grupos = {}
    for f in filas:
        clave = f"{f['estructura']} ({f['orden_insercion']})"
        grupos.setdefault(clave, {"n": [], "media": [], "std": []})
        grupos[clave]["n"].append(f["n"])
        grupos[clave]["media"].append(f["media_segundos"])
        grupos[clave]["std"].append(f["std_segundos"])

    fig, axs = plt.subplots(1, 2, figsize=(14, 5))

    for nombre, datos in grupos.items():
        axs[0].errorbar(datos["n"], datos["media"], yerr=datos["std"],
                         marker='o', label=nombre, capsize=3)
    axs[0].set_xlabel("Número de estudiantes (N)")
    axs[0].set_ylabel("Tiempo de búsqueda (segundos)")
    axs[0].set_title(f"Escalabilidad — escala lineal (M={m_fijo if m_fijo else 'varios'})")
    axs[0].legend()
    axs[0].grid(True, alpha=0.3)

    for nombre, datos in grupos.items():
        axs[1].plot(datos["n"], datos["media"], marker='o', label=nombre)
    axs[1].set_xscale('log')
    axs[1].set_yscale('log')
    axs[1].set_xlabel("Número de estudiantes (N)")
    axs[1].set_ylabel("Tiempo de búsqueda (segundos)")
    axs[1].set_title("Escalabilidad — escala log-log")
    axs[1].legend()
    axs[1].grid(True, alpha=0.3, which="both")

    plt.tight_layout()
    os.makedirs(os.path.dirname(ruta_salida), exist_ok=True)
    plt.savefig(ruta_salida, dpi=150)
    print(f"Gráfica guardada en: {os.path.abspath(ruta_salida)}")
    plt.show()


if __name__ == "__main__":
    graficar_resultados(m_fijo=100)