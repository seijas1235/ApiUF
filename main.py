import requests
from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/uf', methods=['GET'])
def uf():
    try:
        # Obtener la fecha del parámetro
        fecha = request.args.get('fecha')

        # Validar que se ingrese una fecha
        if not fecha:
            return jsonify({'error': 'Se debe ingresar una fecha en formato dd-mm-yyyy.'}), 400

        # Validar que la fecha sea mayor o igual a 01-01-2013
        if fecha < '01-01-2013':
            return jsonify({'error': 'La fecha mínima para consultar es 01-01-2013.'}), 400

        # Realizar la consulta a la API de la UF
        url = f'https://mindicador.cl/api/uf/{fecha.split("-")[2]}-{fecha.split("-")[1]}-{fecha.split("-")[0]}'

        response = requests.get(url)

        # Validar si la respuesta de la API es correcta
        if response.status_code != 200:
            return jsonify({'error': 'No se pudo obtener el valor de la UF.'}), 500

        # Obtener el valor de la UF de la respuesta y devolverla en formato JSON
        uf = response.json()['serie'][0]['valor']
        return jsonify({'fecha': fecha, 'valor': uf})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
