from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import os
import json
app = Flask(__name__, template_folder='templates')  # Cambia 'views' al nombre de tu carpeta
CORS(app)  
print(os.path.abspath(str(app.template_folder)))
# Views
@app.route('/d', methods=['GET'])
def index():
    return render_template('/index.html')  # Asegúrate de que tienes un archivo index.html en tu carpeta templates

@app.route('/login/', methods=['GET'])
def login():
    return render_template('Login/indexLGN.html')  # Asegúrate de tener un archivo login.html en la carpeta 'templates'

@app.route('/dashboard/', methods=['GET'])
def dashboard():
    return render_template('Dashboard/indexDS.html')  # Asume que tienes un archivo dashboard.html

#Repository

# Ruta del archivo JSON
json_file_path = os.path.join(os.getcwd(), 'data.json')

# Función para cargar datos desde el archivo JSON
def load_data():
    if not os.path.exists(json_file_path):
        with open(json_file_path, 'w') as file:
            json.dump([], file)

    with open(json_file_path, 'r') as file:
        return json.load(file)

# Función para guardar datos en el archivo JSON
def save_data(data):
    with open(json_file_path, 'w') as file:
        json.dump(data, file, indent=2)

#Controllers

# CREATE - Insertar un nuevo registro
@app.route('/crear', methods=['POST'])
def guardar_json():
    new_data = request.json  # Flask interpreta automáticamente el JSON entrante
    if not new_data:
        return jsonify({"message": "No se han recibido datos"}), 400  # Devuelve un error 400 si no hay datos
    
    data = load_data()
    data.append(new_data)
    save_data(data)
    return jsonify({"message": "Datos guardados exitosamente"}), 200

# READ - Obtener todos los registros o uno específico
@app.route('/registro', methods=['GET'])
@app.route('/registro/<int:id>', methods=['GET'])
def obtener_registro(id=None):
    data = load_data()
    if id is None:
        return jsonify(data), 200
    else:
        registro = next((item for item in data if int(item["id_Registro"]) == id), None)
        if registro:
            return jsonify(registro), 200
        else:
            return jsonify({"message": "Registro no encontrado"}), 404

# UPDATE - Actualizar un registro existente
@app.route('/actualizar-json/<int:id>', methods=['PUT'])
def actualizar_registro(id):
    updated_data = request.json
    data = load_data()
    for i, registro in enumerate(data):
        if int(registro["id_Registro"]) == id:
            data[i] = updated_data
            save_data(data)
            return jsonify({"message": "Registro actualizado exitosamente"}), 200
    return jsonify({"message": "Registro no encontrado"}), 404

# DELETE - Eliminar un registro específico
@app.route('/eliminar-json/<int:id>', methods=['DELETE'])
def eliminar_registro(id):
    data = load_data()
    data = [registro for registro in data if int(registro["id_Registro"]) != id]
    save_data(data)
    return jsonify({"message": "Registro eliminado exitosamente"}), 200


#Metodo de debug
@app.route('/debugJson', methods=['GET'])
@app.route('/debugJson/<int:id>', methods=['GET'])
def obtener_registro_debug(id=None):
    if id is None:
        return jsonify(registros), 200
    else:
        registro = next((item for item in registros if int(item["id_Registro"]) == id), None)
        if registro:
            return jsonify(registro), 200
        else:
            return jsonify({"message": "Registro no encontrado"}), 404



registros = [
  {
    "id_Registro": "1",
    "datepicker": "08/18/2024",
    "Precio_Consulta": "34",
    "Menu_id_paciente": "Paciente 1",
    "Menu_id_cups": "Procedimiento 1",
    "Finalidad_Consulta": "Opción 1",
    "causa_externa": "Opción 1",
    "id_diagnostico_principal": "Opción 1"
  },
  {
    "id_Registro": "2",
    "datepicker": "08/19/2024",
    "Precio_Consulta": "33",
    "Menu_id_paciente": "Paciente 1",
    "Menu_id_cups": "Procedimiento 2",
    "Finalidad_Consulta": "Opción 2",
    "causa_externa": "Opción 1",
    "id_diagnostico_principal": "Opción 2"
  },
  {
    "id_Registro": "3",
    "datepicker": "08/19/2024",
    "Precio_Consulta": "34",
    "Menu_id_paciente": "Paciente 2",
    "Menu_id_cups": "Procedimiento 2",
    "Finalidad_Consulta": "Opción 2",
    "causa_externa": "Opción 1",
    "id_diagnostico_principal": "Opción 1"
  },
  {
    "id_Registro": "4",
    "datepicker": "08/20/2024",
    "Precio_Consulta": "35",
    "Menu_id_paciente": "Paciente 3",
    "Menu_id_cups": "Procedimiento 1",
    "Finalidad_Consulta": "Opción 3",
    "causa_externa": "Opción 2",
    "id_diagnostico_principal": "Opción 2"
  },
  {
    "id_Registro": "5",
    "datepicker": "08/21/2024",
    "Precio_Consulta": "36",
    "Menu_id_paciente": "Paciente 4",
    "Menu_id_cups": "Procedimiento 3",
    "Finalidad_Consulta": "Opción 2",
    "causa_externa": "Opción 1",
    "id_diagnostico_principal": "Opción 3"
  },
  {
    "id_Registro": "6",
    "datepicker": "08/22/2024",
    "Precio_Consulta": "37",
    "Menu_id_paciente": "Paciente 5",
    "Menu_id_cups": "Procedimiento 2",
    "Finalidad_Consulta": "Opción 1",
    "causa_externa": "Opción 3",
    "id_diagnostico_principal": "Opción 1"
  },
  {
    "id_Registro": "7",
    "datepicker": "08/23/2024",
    "Precio_Consulta": "38",
    "Menu_id_paciente": "Paciente 1",
    "Menu_id_cups": "Procedimiento 1",
    "Finalidad_Consulta": "Opción 3",
    "causa_externa": "Opción 2",
    "id_diagnostico_principal": "Opción 4"
  },
  {
    "id_Registro": "8",
    "datepicker": "08/24/2024",
    "Precio_Consulta": "39",
    "Menu_id_paciente": "Paciente 2",
    "Menu_id_cups": "Procedimiento 3",
    "Finalidad_Consulta": "Opción 1",
    "causa_externa": "Opción 1",
    "id_diagnostico_principal": "Opción 2"
  },
  {
    "id_Registro": "9",
    "datepicker": "08/25/2024",
    "Precio_Consulta": "34",
    "Menu_id_paciente": "Paciente 3",
    "Menu_id_cups": "Procedimiento 4",
    "Finalidad_Consulta": "Opción 2",
    "causa_externa": "Opción 3",
    "id_diagnostico_principal": "Opción 5"
  },
  {
    "id_Registro": "10",
    "datepicker": "08/26/2024",
    "Precio_Consulta": "40",
    "Menu_id_paciente": "Paciente 4",
    "Menu_id_cups": "Procedimiento 2",
    "Finalidad_Consulta": "Opción 1",
    "causa_externa": "Opción 2",
    "id_diagnostico_principal": "Opción 4"
  },
  {
    "id_Registro": "11",
    "datepicker": "08/27/2024",
    "Precio_Consulta": "41",
    "Menu_id_paciente": "Paciente 5",
    "Menu_id_cups": "Procedimiento 1",
    "Finalidad_Consulta": "Opción 3",
    "causa_externa": "Opción 3",
    "id_diagnostico_principal": "Opción 1"
  },
  {
    "id_Registro": "12",
    "datepicker": "08/28/2024",
    "Precio_Consulta": "42",
    "Menu_id_paciente": "Paciente 1",
    "Menu_id_cups": "Procedimiento 3",
    "Finalidad_Consulta": "Opción 2",
    "causa_externa": "Opción 1",
    "id_diagnostico_principal": "Opción 2"
  },
  {
    "id_Registro": "13",
    "datepicker": "08/29/2024",
    "Precio_Consulta": "43",
    "Menu_id_paciente": "Paciente 2",
    "Menu_id_cups": "Procedimiento 4",
    "Finalidad_Consulta": "Opción 1",
    "causa_externa": "Opción 3",
    "id_diagnostico_principal": "Opción 3"
  },
  {
    "id_Registro": "14",
    "datepicker": "08/30/2024",
    "Precio_Consulta": "44",
    "Menu_id_paciente": "Paciente 3",
    "Menu_id_cups": "Procedimiento 2",
    "Finalidad_Consulta": "Opción 2",
    "causa_externa": "Opción 2",
    "id_diagnostico_principal": "Opción 4"
  },
  {
    "id_Registro": "15",
    "datepicker": "08/31/2024",
    "Precio_Consulta": "45",
    "Menu_id_paciente": "Paciente 4",
    "Menu_id_cups": "Procedimiento 1",
    "Finalidad_Consulta": "Opción 3",
    "causa_externa": "Opción 1",
    "id_diagnostico_principal": "Opción 5"
  },
  {
    "id_Registro": "16",
    "datepicker": "09/01/2024",
    "Precio_Consulta": "46",
    "Menu_id_paciente": "Paciente 5",
    "Menu_id_cups": "Procedimiento 3",
    "Finalidad_Consulta": "Opción 1",
    "causa_externa": "Opción 2",
    "id_diagnostico_principal": "Opción 4"
  },
  {
    "id_Registro": "17",
    "datepicker": "09/02/2024",
    "Precio_Consulta": "47",
    "Menu_id_paciente": "Paciente 1",
    "Menu_id_cups": "Procedimiento 4",
    "Finalidad_Consulta": "Opción 3",
    "causa_externa": "Opción 3",
    "id_diagnostico_principal": "Opción 1"
  },
  {
    "id_Registro": "18",
    "datepicker": "09/03/2024",
    "Precio_Consulta": "48",
    "Menu_id_paciente": "Paciente 2",
    "Menu_id_cups": "Procedimiento 1",
    "Finalidad_Consulta": "Opción 1",
    "causa_externa": "Opción 2",
    "id_diagnostico_principal": "Opción 5"
  },
  {
    "id_Registro": "19",
    "datepicker": "09/04/2024",
    "Precio_Consulta": "49",
    "Menu_id_paciente": "Paciente 3",
    "Menu_id_cups": "Procedimiento 2",
    "Finalidad_Consulta": "Opción 2",
    "causa_externa": "Opción 3",
    "id_diagnostico_principal": "Opción 4"
  },
  {
    "id_Registro": "20",
    "datepicker": "09/05/2024",
    "Precio_Consulta": "50",
    "Menu_id_paciente": "Paciente 4",
    "Menu_id_cups": "Procedimiento 3",
    "Finalidad_Consulta": "Opción 3",
    "causa_externa": "Opción 2",
    "id_diagnostico_principal": "Opción 1"
  },
  {
    "id_Registro": "21",
    "datepicker": "09/06/2024",
    "Precio_Consulta": "51",
    "Menu_id_paciente": "Paciente 5",
    "Menu_id_cups": "Procedimiento 4",
    "Finalidad_Consulta": "Opción 1",
    "causa_externa": "Opción 3",
    "id_diagnostico_principal": "Opción 5"
  },
  {
    "id_Registro": "22",
    "datepicker": "09/07/2024",
    "Precio_Consulta": "52",
    "Menu_id_paciente": "Paciente 1",
    "Menu_id_cups": "Procedimiento 2",
    "Finalidad_Consulta": "Opción 2",
    "causa_externa": "Opción 2",
    "id_diagnostico_principal": "Opción 4"
  },
  {
    "id_Registro": "23",
    "datepicker": "09/08/2024",
    "Precio_Consulta": "53",
    "Menu_id_paciente": "Paciente 2",
    "Menu_id_cups": "Procedimiento 1",
    "Finalidad_Consulta": "Opción 3",
    "causa_externa": "Opción 1",
    "id_diagnostico_principal": "Opción 5"
  },
  {
    "id_Registro": "24",
    "datepicker": "09/09/2024",
    "Precio_Consulta": "54",
    "Menu_id_paciente": "Paciente 3",
    "Menu_id_cups": "Procedimiento 3",
    "Finalidad_Consulta": "Opción 1",
    "causa_externa": "Opción 3",
    "id_diagnostico_principal": "Opción 1"
  },
  {
    "id_Registro": "25",
    "datepicker": "09/10/2024",
    "Precio_Consulta": "55",
    "Menu_id_paciente": "Paciente 4",
    "Menu_id_cups": "Procedimiento 4",
    "Finalidad_Consulta": "Opción 2",
    "causa_externa": "Opción 2",
    "id_diagnostico_principal": "Opción 2"
  },
  {
    "id_Registro": "26",
    "datepicker": "09/11/2024",
    "Precio_Consulta": "56",
    "Menu_id_paciente": "Paciente 5",
    "Menu_id_cups": "Procedimiento 1",
    "Finalidad_Consulta": "Opción 3",
    "causa_externa": "Opción 1",
    "id_diagnostico_principal": "Opción 3"
  },
  {
    "id_Registro": "27",
    "datepicker": "09/12/2024",
    "Precio_Consulta": "57",
    "Menu_id_paciente": "Paciente 1",
    "Menu_id_cups": "Procedimiento 2",
    "Finalidad_Consulta": "Opción 1",
    "causa_externa": "Opción 3",
    "id_diagnostico_principal": "Opción 4"
  },
  {
    "id_Registro": "28",
    "datepicker": "09/13/2024",
    "Precio_Consulta": "58",
    "Menu_id_paciente": "Paciente 2",
    "Menu_id_cups": "Procedimiento 3",
    "Finalidad_Consulta": "Opción 2",
    "causa_externa": "Opción 2",
    "id_diagnostico_principal": "Opción 1"
  },
  {
    "id_Registro": "29",
    "datepicker": "09/14/2024",
    "Precio_Consulta": "59",
    "Menu_id_paciente": "Paciente 3",
    "Menu_id_cups": "Procedimiento 4",
    "Finalidad_Consulta": "Opción 3",
    "causa_externa": "Opción 1",
    "id_diagnostico_principal": "Opción 5"
  },
  {
    "id_Registro": "30",
    "datepicker": "09/15/2024",
    "Precio_Consulta": "60",
    "Menu_id_paciente": "Paciente 4",
    "Menu_id_cups": "Procedimiento 1",
    "Finalidad_Consulta": "Opción 1",
    "causa_externa": "Opción 3",
    "id_diagnostico_principal": "Opción 2"
  }
]



if __name__ == '__main__':
    app.run(ssl_context='adhoc', debug=True)