import textwrap

import requests

def ejecutar():
    url = "https://cve.circl.lu/api/last"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        cves = response.json()

        if not cves:
            print("No se encontraron vulnerabilidades.")
            return

        # Mostrar las 10 primeras vulnerabilidades
        print("Últimas 10 vulnerabilidades CVE:\n")
        for cve in cves[1:11]:
            cve_id = cve.get('aliases', 'No disponible')
            summary = cve.get('details', 'No hay descripción')
            summary_formated = textwrap.fill(summary, width=80)
            published = cve.get('published', 'No disponible')

            print(f"CVE ID: {cve_id}")
            print(f"Fecha de Publicación: {published}")
            print(f"Descripción: {summary_formated}")
            print("-" * 60)

    except requests.RequestException as e:
        print(f"Error al obtener las vulnerabilidades: {e}")


