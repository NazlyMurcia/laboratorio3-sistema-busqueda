"""
Medición estadística de tiempos de búsqueda.
"""
import time
import statistics


def medir_repetido(estructura, ids_buscar, repeticiones=10):
    """
    Mide el tiempo de M búsquedas sobre una estructura YA CONSTRUIDA,
    repitiendo la medición `repeticiones` veces.

    Importante: la estructura se construye UNA sola vez fuera de esta
    función (ver experimento.py). Repetir la construcción en cada
    repetición es innecesario (los datos y el orden de inserción no
    cambian) y, para un ABB degenerado, costaría O(n²) por repetición.

    Tratamiento de valores atípicos: se descartan mediciones a más de
    2 desviaciones estándar de la media.
    """
    tiempos = []
    altura_estructura = estructura.altura() if hasattr(estructura, "altura") else None

    for _ in range(repeticiones):
        inicio = time.perf_counter()
        for id_est in ids_buscar:
            estructura.buscar(id_est)
        fin = time.perf_counter()
        tiempos.append(fin - inicio)

    media_cruda = statistics.mean(tiempos)
    std_cruda = statistics.stdev(tiempos) if len(tiempos) > 1 else 0.0

    if std_cruda > 0:
        tiempos_filtrados = [t for t in tiempos if abs(t - media_cruda) <= 2 * std_cruda]
    else:
        tiempos_filtrados = tiempos

    if len(tiempos_filtrados) == 0:
        tiempos_filtrados = tiempos  # salvaguarda

    return {
        "tiempos_crudos": tiempos,
        "media": statistics.mean(tiempos_filtrados),
        "std": statistics.stdev(tiempos_filtrados) if len(tiempos_filtrados) > 1 else 0.0,
        "n_descartados": len(tiempos) - len(tiempos_filtrados),
        "altura": altura_estructura,
    }