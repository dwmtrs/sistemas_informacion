from flask import Flask, render_template_string, request, jsonify
import traceback
import sys
import io
import os
from contextlib import redirect_stdout
import pandas as pd

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
        "name": "Top Clientes y Empleados",
        "description": "Muestra el top X de clientes con más incidencias o empleados con más tiempo en resolución",
        "file_path": "top_clientes_incidencias.py"
    },
    "top_incidencias": {
        "name": "Top Tipos de Incidencias por Tiempo",
        "description": "Muestra el top X de tipos de incidencias que han requerido mayor tiempo de resolución",
        "file_path": "top_tipos_incidencias_tiempo.py"
    },
    "ultimos_cves": {
        "name": "Últimas CVEs",
        "description": "Muestra las últimas 10 vulnerabilidades reportadas (CVE)",
        "file_path": "top10_vulnerabilidades.py"
    },
    "metricas_avanzadas": {
        "name": "Métricas Avanzadas",
        "description": "Análisis de tiempos de resolución por tipo de incidencia",
        "file_path": "AnalisisMetricas.py"
    },
    "nvd": {
        "name": "Buscar CVEs por palabra clave",
        "description": "Consulta vulnerabilidades en NVD relacionadas con una palabra clave",
        "file_path": "vulnerabilidades_nvd.py"
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
            flex-direction: column;
        }
        .form-row {
            display: flex;
            align-items: center;
            margin-bottom: 10px;
        }
        input[type=number] {
            width: 60px;
            padding: 5px;
            margin-right: 10px;
        }
        label {
            margin-right: 5px;
        }
        select {
            padding: 5px;
            margin-right: 10px;
        }
        .radio-group {
            display: flex;
            margin-bottom: 10px;
        }
        .radio-option {
            margin-right: 15px;
        }
        .radio-option input {
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

            if (id === 'top_incidencias') {
                paramsForm = document.createElement('div');
                paramsForm.className = 'params-form';
                paramsForm.id = `params-${id}`;
                paramsForm.style.display = 'none';

                const formRow = document.createElement('div');
                formRow.className = 'form-row';

                const label = document.createElement('label');
                label.textContent = 'Top X:';

                const input = document.createElement('input');
                input.type = 'number';
                input.id = `top-n-${id}`;
                input.min = '1';
                input.max = '100';
                input.value = '5';

                const rangeDisplay = document.createElement('div');
                rangeDisplay.id = `range-display-${id}`;
                rangeDisplay.className = 'range-display';
                rangeDisplay.textContent = '5';
                rangeDisplay.style.marginLeft = '5px';
                rangeDisplay.style.fontWeight = 'bold';

                input.addEventListener('input', function() {
                    rangeDisplay.textContent = this.value;
                });

                formRow.appendChild(label);
                formRow.appendChild(input);
                formRow.appendChild(rangeDisplay);

                const executeButton = document.createElement('button');
                executeButton.textContent = 'Aplicar';
                executeButton.onclick = function() {
                    ejecutarScript(id);
                };

                paramsForm.appendChild(formRow);
                paramsForm.appendChild(executeButton);
            }

            if (id === 'top_clientes') {
                paramsForm = document.createElement('div');
                paramsForm.className = 'params-form';
                paramsForm.id = `params-${id}`;
                paramsForm.style.display = 'none';

                // Primera fila: tipo de visualización
                const viewTypeRow = document.createElement('div');
                viewTypeRow.className = 'form-row';

                const viewTypeLabel = document.createElement('label');
                viewTypeLabel.textContent = 'Mostrar:';

                const radioGroup = document.createElement('div');
                radioGroup.className = 'radio-group';

                // Opción Solo Clientes
                const clientesOption = document.createElement('div');
                clientesOption.className = 'radio-option';

                const clientesRadio = document.createElement('input');
                clientesRadio.type = 'radio';
                clientesRadio.name = `view-type-${id}`;
                clientesRadio.id = `view-clientes-${id}`;
                clientesRadio.value = 'solo_clientes';
                clientesRadio.checked = true;

                const clientesLabel = document.createElement('label');
                clientesLabel.htmlFor = `view-clientes-${id}`;
                clientesLabel.textContent = 'Solo clientes';

                clientesOption.appendChild(clientesRadio);
                clientesOption.appendChild(clientesLabel);

                // Opción Ambos
                const ambosOption = document.createElement('div');
                ambosOption.className = 'radio-option';

                const ambosRadio = document.createElement('input');
                ambosRadio.type = 'radio';
                ambosRadio.name = `view-type-${id}`;
                ambosRadio.id = `view-ambos-${id}`;
                ambosRadio.value = 'ambos';

                const ambosLabel = document.createElement('label');
                ambosLabel.htmlFor = `view-ambos-${id}`;
                ambosLabel.textContent = 'Clientes y empleados';

                ambosOption.appendChild(ambosRadio);
                ambosOption.appendChild(ambosLabel);

                radioGroup.appendChild(clientesOption);
                radioGroup.appendChild(ambosOption);

                viewTypeRow.appendChild(viewTypeLabel);
                viewTypeRow.appendChild(radioGroup);

                // Segunda fila: Top X
                const topRow = document.createElement('div');
                topRow.className = 'form-row';

                const topLabel = document.createElement('label');
                topLabel.textContent = 'Top X:';

                const topInput = document.createElement('input');
                topInput.type = 'number';
                topInput.id = `top-n-${id}`;
                topInput.min = '1';
                topInput.max = '100';
                topInput.value = '5';

                const rangeDisplay = document.createElement('div');
                rangeDisplay.id = `range-display-${id}`;
                rangeDisplay.className = 'range-display';
                rangeDisplay.textContent = '5';
                rangeDisplay.style.marginLeft = '5px';
                rangeDisplay.style.fontWeight = 'bold';

                topInput.addEventListener('input', function() {
                    rangeDisplay.textContent = this.value;
                });

                topRow.appendChild(topLabel);
                topRow.appendChild(topInput);
                topRow.appendChild(rangeDisplay);

                // Botón de aplicar
                const executeButton = document.createElement('button');
                executeButton.textContent = 'Aplicar';
                executeButton.onclick = function() {
                    ejecutarScript(id);
                };

                paramsForm.appendChild(viewTypeRow);
                paramsForm.appendChild(topRow);
                paramsForm.appendChild(executeButton);
            }
            
            if (id === 'nvd') {
                paramsForm = document.createElement('div');
                paramsForm.className = 'params-form';
                paramsForm.id = `params-${id}`;
                paramsForm.style.display = 'none';
            
                const formRow = document.createElement('div');
                formRow.className = 'form-row';
            
                const label = document.createElement('label');
                label.textContent = 'Keyword:';
            
                const input = document.createElement('input');
                input.type = 'text';
                input.id = `keyword-${id}`;
                input.value = 'apache';
            
                formRow.appendChild(label);
                formRow.appendChild(input);

                const executeButton = document.createElement('button');
                executeButton.textContent = 'Buscar';
                executeButton.onclick = function() {
                    ejecutarScript(id);
                };

                paramsForm.appendChild(formRow);
                paramsForm.appendChild(executeButton);
            }

            
            const button = document.createElement('button');
            button.textContent = id === 'top_clientes' || id === 'top_incidencias' || id === 'nvd' ? 'Configurar' : 'Ejecutar';
            button.onclick = function() {
                if (id === 'top_clientes' || id === 'top_incidencias' || id === 'nvd') {
                    // Solo mostrar el formulario de parámetros
                    const formElement = document.getElementById(`params-${id}`);
                    formElement.style.display = formElement.style.display === 'none' ? 'flex' : 'none';
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

            // Preparar parámetros según el script
            let params = {};

            if (scriptId === 'top_incidencias') {
                const topN = document.getElementById(`top-n-${scriptId}`).value;
                params = { top_n: topN };
            }
            
            if (scriptId === 'top_clientes') {
                const topN = document.getElementById(`top-n-${scriptId}`).value;
                const viewType = document.querySelector(`input[name="view-type-${scriptId}"]:checked`).value;

                params = { 
                    top_n: topN,
                    view_type: viewType
                };
            }
            if (scriptId === 'nvd') {
                const keyword = document.getElementById(`keyword-${scriptId}`).value;
                params = { keyword };
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
                    if (data.table_data && Array.isArray(data.table_data)) {
                        // Mostrar múltiples tablas
                        data.table_data.forEach(tabla => {
                            if (tabla.title) {
                                outputDiv.innerHTML += `<h3>${tabla.title}</h3>`;
                            }
                            outputDiv.innerHTML += crearTablaHTML(tabla);
                        });
                    } else if (data.table_data) {
                        // Mostrar una sola tabla
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
                if script_id == 'top_incidencias' and 'top_n' in params:
                    top_n = int(params['top_n'])
                    resultado = namespace['ejecutar'](top_n)
                elif script_id == 'top_clientes' and 'top_n' in params:
                    top_n = int(params['top_n'])
                    view_type = params.get('view_type', 'solo_clientes')

                    if view_type == 'solo_clientes':
                        resultado = namespace['ejecutar'](top_n, "clientes")
                        table_data = None
                        if 'pandas' in sys.modules and hasattr(resultado, 'to_dict'):
                            table_data = {
                                'columns': resultado.columns.tolist(),
                                'data': resultado.values.tolist()
                            }
                    else:  # ambos
                        # Ejecutar para clientes
                        resultado_clientes = namespace['ejecutar'](top_n, "clientes")
                        # Ejecutar para empleados
                        resultado_empleados = namespace['ejecutar'](top_n, "empleados")

                        # Crear formato para múltiples tablas
                        table_data = []

                        if 'pandas' in sys.modules and hasattr(resultado_clientes, 'to_dict'):
                            table_data.append({
                                'title': f'Top {top_n} clientes con más incidencias',
                                'columns': resultado_clientes.columns.tolist(),
                                'data': resultado_clientes.values.tolist()
                            })

                        if 'pandas' in sys.modules and hasattr(resultado_empleados, 'to_dict'):
                            table_data.append({
                                'title': f'Top {top_n} empleados con más tiempo en resolución',
                                'columns': resultado_empleados.columns.tolist(),
                                'data': resultado_empleados.values.tolist()
                            })

                elif script_id == 'nvd' and 'keyword' in params:
                    keyword = params['keyword']
                    resultado = namespace['ejecutar'](keyword)

                elif script_id == 'metricas_avanzadas':  # Nuevo caso para métricas
                    resultado = namespace['ejecutar']()
                    # Procesar múltiples DataFrames
                    if isinstance(resultado, list):
                        table_data = [{
                            'columns': df.columns.tolist(),
                            'data': df.values.tolist()
                        } for df in resultado if isinstance(df, pd.DataFrame)]

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
                table_data = None

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