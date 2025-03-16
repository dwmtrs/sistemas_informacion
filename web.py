from flask import Flask, render_template_string, request, jsonify
import traceback
import sys
import io
import os
from contextlib import redirect_stdout

app = Flask(__name__)

# Definir rutas de los scripts
scripts = {
    "script1": {
        "name": "Crear Base de Datos",
        "description": "Script para crear la base de datos",
        "file_path": "CrearBBDD.py"
    },
    "script2": {
        "name": "Ejercicio 2",
        "description": "Sistema ETL",
        "file_path": "Ejercicio2.py"
    },
    "script3": {
        "name": "Ejercicio 3",
        "description": "Agrupaciones",
        "file_path": "Ejercicio3.py"
    },
    "script4": {
        "name": "Ejercicio 4",
        "description": "Imagenes",
        "file_path": "Ejercicio4.py"
    }
}

def get_script_content(script_id):
    """Lee el contenido del archivo del script."""
    script_info = scripts.get(script_id)
    if script_info and "file_path" in script_info:
        file_path = script_info["file_path"]
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as file:
                return file.read()
        else:
            return None
    return None

# Plantilla HTML directamente en el código
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Ejecutor de Scripts Python</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
        }
        .script-container {
            border: 1px solid #ddd;
            border-radius: 5px;
            padding: 15px;
            margin-bottom: 20px;
        }
        .output {
            background-color: #f5f5f5;
            border: 1px solid #ddd;
            border-radius: 3px;
            padding: 10px;
            font-family: monospace;
            white-space: pre-wrap;
            margin-top: 10px;
            display: none;
        }
        button {
            background-color: #4CAF50;
            border: none;
            color: white;
            padding: 10px 15px;
            text-align: center;
            text-decoration: none;
            display: inline-block;
            font-size: 16px;
            margin: 4px 2px;
            cursor: pointer;
            border-radius: 4px;
        }
        h1 {
            color: #333;
        }
        .error {
            color: red;
        }
    </style>
</head>
<body>
    <h1>Ejecutor de Scripts Python</h1>
    <p>Selecciona un script para ejecutar:</p>

    <div id="scripts-container">
        <!-- Los scripts se cargarán aquí -->
    </div>

    <script>
        // Datos de los scripts
        const scripts = {
            {% for id, script in scripts.items() %}
            "{{ id }}": {
                "name": "{{ script.name }}",
                "description": "{{ script.description }}"
            },
            {% endfor %}
        };

        // Crear elementos HTML para cada script
        const scriptsContainer = document.getElementById('scripts-container');

        for (const [id, script] of Object.entries(scripts)) {
            const scriptDiv = document.createElement('div');
            scriptDiv.className = 'script-container';

            const title = document.createElement('h2');
            title.textContent = script.name;

            const description = document.createElement('p');
            description.textContent = script.description;

            const button = document.createElement('button');
            button.textContent = 'Ejecutar';
            button.onclick = function() { ejecutarScript(id); };

            const output = document.createElement('div');
            output.className = 'output';
            output.id = `output-${id}`;

            scriptDiv.appendChild(title);
            scriptDiv.appendChild(description);
            scriptDiv.appendChild(button);
            scriptDiv.appendChild(output);

            scriptsContainer.appendChild(scriptDiv);
        }

        // Función para ejecutar el script
        function ejecutarScript(scriptId) {
            const outputDiv = document.getElementById(`output-${scriptId}`);
            outputDiv.style.display = 'block';
            outputDiv.innerHTML = 'Ejecutando...';

            fetch(`/ejecutar/${scriptId}`, {
                method: 'POST'
            })
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    outputDiv.innerHTML = `<div class="error">Error: ${data.error}</div><pre>${data.traceback}</pre>`;
                } else {
                    outputDiv.innerHTML = data.output;
                    outputDiv.innerHTML += `<br><strong>${data.resultado}</strong>`;
                }
            })
            .catch(error => {
                outputDiv.innerHTML = `<div class="error">Error de conexión: ${error}</div>`;
            });
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE, scripts=scripts)


@app.route('/ejecutar/<script_id>', methods=['POST'])
def ejecutar_script(script_id):
    if script_id not in scripts:
        return jsonify({"error": "Script no encontrado"}), 404

    script_code = get_script_content(script_id)
    if script_code is None:
        return jsonify({"error": "Archivo de script no encontrado"}), 404

    try:
        f = io.StringIO()
        with redirect_stdout(f):
            namespace = {}
            exec(script_code, namespace)
            # Si el script no tiene una función 'ejecutar', simplemente ejecuta el código
            resultado = "Script ejecutado correctamente"

        output = f.getvalue()

        return jsonify({
            "resultado": resultado,
            "output": output
        })
    except Exception as e:
        error_traceback = traceback.format_exc()
        return jsonify({
            "error": str(e),
            "traceback": error_traceback
        }), 500



if __name__ == '__main__':
    app.run(debug=True)