import requests
import textwrap

def ejecutar(keyword="apache"):
    url = f"https://services.nvd.nist.gov/rest/json/cves/2.0?keywordSearch={keyword}&resultsPerPage=5"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()

        cves = data.get("vulnerabilities", [])

        if not cves:
            print("No se encontraron vulnerabilidades.")
            return

        print(f"Vulnerabilidades relacionadas con: {keyword}\n")

        for cve in cves:
            id_cve = cve["cve"]["id"]
            descripcion = cve["cve"]["descriptions"][0]["value"]
            descripcion_formateada = textwrap.fill(descripcion, width=80)

            print(f"CVE ID: {id_cve}")
            print("Descripción:")
            print(descripcion_formateada)
            print("-" * 60)

    except Exception as e:
        print(f"Error al obtener datos de NVD: {e}")

