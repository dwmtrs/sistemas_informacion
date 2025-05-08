import textwrap

import requests

def ejecutar():
    url = "https://cve.circl.lu/api/last"
    try:
        response = requests.get(url, timeout=20)
        response.raise_for_status()

        cves = response.json()

        if not cves:
            print("No se encontraron vulnerabilidades.")
            return

        # Mostrar las 10 primeras vulnerabilidades
        print("Últimas 10 vulnerabilidades CVE:\n")
        for cve in cves[1:11]:
            metadata = cve.get('cveMetadata', {})
            cve_id = metadata.get('cveId', 'No disponible')
            name = metadata.get('assignerShortName', 'No hay descripción')
            summary_formated = textwrap.fill(name, width=80)
            published = metadata.get('datePublished', 'No disponible')

            print(f"CVE ID: {cve_id}")
            print(f"Fecha de Publicación: {published}")
            print(f"Nombre: {summary_formated}")
            print("-" * 60)

    except requests.RequestException as e:
        print(f"Error al obtener las vulnerabilidades: {e}")

