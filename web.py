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
    },
    "top_clientes": {
        "name": "Top Clientes con Incidencias",
        "description": "Muestra el top X de clientes con más incidencias reportadas",
        "file_path": "top_clientes_incidencias.py"
    },
    "top_incidencias": {
        "name": "Top Tipos de Incidencias por Tiempo",
        "description": "Muestra el top X de tipos de incidencias que han requerido mayor tiempo de resolución",
        "file_path": "top_tipos_incidencias_tiempo.py"
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
        .params-form {
            margin-top: 10px;
            margin-bottom: 10px;
            padding: 10px;
            background-color: #f9f9f9;
            border-radius: 5px;
            display: none;
            align-items: center;
        }
        input[type=number] {
            width: 60px;
            padding: 5px;
            margin-right: 10px;
        }
        label {
            margin-right: 5px;
        }
        .success {
            color: green;
            font-weight: bold;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 10px;
        }
        table, th, td {
            border: 1px solid #ddd;
        }
        th, td {
            padding: 8px;
            text-align: left;
        }
        th {
            background-color: #f2f2f2;
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

            let paramsForm = null;
            if (id === 'top_clientes' || id === 'top_incidencias') {
                paramsForm = document.createElement('div');
                paramsForm.className = 'params-form';
                paramsForm.id = `params-${id}`;
                paramsForm.style.display = 'block';

                const label = document.createElement('label');
                label.textContent = 'Top X:';

                const input = document.createElement('input');
                input.type = 'number';
                input.id = `top-n-${id}`;
                input.min = '1';
                input.max = '100';
                input.value = '5';
                // Control de cambio numérico
                const rangeDisplay = document.createElement('div');
                rangeDisplay.id = `range-display-${id}`;
                rangeDisplay.className = 'range-display';
                rangeDisplay.textContent = '5';
                rangeDisplay.style.marginLeft = '5px';
                rangeDisplay.style.fontWeight = 'bold';

                // Actualizar el display cuando cambie el input
                input.addEventListener('input', function() {
                    rangeDisplay.textContent = this.value;
                });

                const executeButton = document.createElement('button');
                executeButton.textContent = 'Aplicar';
                executeButton.onclick = function() {
                    ejecutarScript(id);
                };

                paramsForm.appendChild(label);
                paramsForm.appendChild(input);
                paramsForm.appendChild(rangeDisplay);
                paramsForm.appendChild(executeButton);
            }

            const button = document.createElement('button');
            button.textContent = id === 'top_clientes' || id === 'top_incidencias' ? 'Configurar' : 'Ejecutar';
            button.onclick = function() {
                if (id === 'top_clientes' || id === 'top_incidencias') {
                    // Solo mostrar el formulario de parámetros
                    const formElement = document.getElementById(`params-${id}`);
                    formElement.style.display = formElement.style.display === 'none' ? 'block' : 'none';
                } else {
                    ejecutarScript(id);
                }
            };

            const output = document.createElement('div');
            output.className = 'output';
            output.id = `output-${id}`;

            scriptDiv.appendChild(title);
            scriptDiv.appendChild(description);
            if (paramsForm) {
                scriptDiv.appendChild(paramsForm);
            }
            scriptDiv.appendChild(button);
            scriptDiv.appendChild(output);

            scriptsContainer.appendChild(scriptDiv);
        }

        // Función para ejecutar el script
        function ejecutarScript(scriptId) {
            const outputDiv = document.getElementById(`output-${scriptId}`);
            outputDiv.style.display = 'block';
            outputDiv.innerHTML = 'Ejecutando...';

            // Preparar parámetros si es un script de top
            let params = {};
            if (scriptId === 'top_clientes' || scriptId === 'top_incidencias') {
                const topN = document.getElementById(`top-n-${scriptId}`).value;
                params = { top_n: topN };
            }

            fetch(`/ejecutar/${scriptId}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(params)
            })
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    outputDiv.innerHTML = `<div class="error">Error: ${data.error}</div><pre>${data.traceback}</pre>`;
                } else {
                    outputDiv.innerHTML = `<div class="success">${data.resultado}</div>`;
                    outputDiv.innerHTML += `<pre>${data.output}</pre>`;

                    // Si hay datos de tabla, mostrarlos
                    if (data.table_data) {
                        outputDiv.innerHTML += crearTablaHTML(data.table_data);
                    }
                }
            })
            .catch(error => {
                outputDiv.innerHTML = `<div class="error">Error de conexión: ${error}</div>`;
            });
        }

        // Función para crear una tabla HTML a partir de datos
        function crearTablaHTML(data) {
            if (!data || !data.columns || !data.data || data.data.length === 0) {
                return '';
            }

            let html = '<table>';

            // Encabezados
            html += '<tr>';
            data.columns.forEach(column => {
                html += `<th>${column}</th>`;
            });
            html += '</tr>';

            // Filas de datos
            data.data.forEach(row => {
                html += '<tr>';
                row.forEach(cell => {
                    html += `<td>${cell}</td>`;
                });
                html += '</tr>';
            });

            html += '</table>';
            return html;
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
        # Obtener parámetros si se proporcionan
        params = request.json or {}

        f = io.StringIO()
        with redirect_stdout(f):
            namespace = {}
            exec(script_code, namespace)

            if 'ejecutar' in namespace and callable(namespace['ejecutar']):
                if script_id in ['top_clientes', 'top_incidencias'] and 'top_n' in params:
                    top_n = int(params['top_n'])
                    resultado = namespace['ejecutar'](top_n)
                else:
                    resultado = namespace['ejecutar']()

                table_data = None
                if 'pandas' in sys.modules and hasattr(resultado, 'to_dict'):
                    table_data = {
                        'columns': resultado.columns.tolist(),
                        'data': resultado.values.tolist()
                    }
            else:
                resultado = "Script ejecutado correctamente"

        output = f.getvalue()

        response_data = {
            "resultado": "Script ejecutado correctamente",
            "output": output
        }

        # Añadir datos de tabla si existen
        if 'table_data' in locals() and table_data:
            response_data["table_data"] = table_data

        return jsonify(response_data)
    except Exception as e:
        error_traceback = traceback.format_exc()
        return jsonify({
            "error": str(e),
            "traceback": error_traceback
        }), 500


if __name__ == '__main__':
    app.run(debug=True)