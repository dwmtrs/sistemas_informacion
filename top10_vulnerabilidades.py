import requests


def ejecutar():
    url = "https://cve.circl.lu/api/last"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Levanta un error si el código de estado no es 200

        cves = response.json()

        # Verificar que se hayan obtenido datos válidos
        if not cves:
            print("No se encontraron vulnerabilidades.")
            return

        # Limitar a las primeras 10 vulnerabilidades
        cves = cves[:10]
        print("Últimas 10 vulnerabilidades CVE:\n")

        for cve in cves:
            cve_metadata = cve.get('cveMetadata', {})
            cve_id = cve_metadata.get('cveId', 'No disponible')
            published = cve_metadata.get('datePublished', 'No disponible')
            cvss = cve_metadata.get('cvss',
                                    'N/A')  # Este campo no estaba en el fragmento que me diste, pero lo puedes añadir si existe

            # Asegúrate de que los datos no sean None
            print(f"CVE ID: {cve_id}")
            print(f"Fecha de Publicación: {published}")
            print(f"CVSS Score: {cvss}")
            print("-" * 60)

    except requests.RequestException as e:
        print(f"Error al obtener las vulnerabilidades: {e}")


# Ejecutar la función
ejecutar()
