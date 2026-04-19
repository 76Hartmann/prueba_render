from flask import Flask, jsonify, request

app = Flask(__name__)

# Base de datos en memoria (diccionario)
usuarios = [
    {"id": 1, "nombre": "Ana", "correo": "ana@example.com"},
    {"id": 2, "nombre": "Carlos", "correo": "carlos@example.com"},
    {"id": 3, "nombre": "Laura", "correo": "laura@example.com"}
]

API_KEY = '123456'

@app.before_request
def verificar():
    key_recibida = request.headers.get("x-apy-key")
    if key_recibida != API_KEY:
        return jsonify({"error": "Acceso negado, API KEY incorrecta"}), 403

# (C) - Crear un usuario
# Acepta tanto /usuarios como /usuarios/
@app.route('/usuarios', methods=['POST'])
@app.route('/usuarios/', methods=['POST'])
def crear_usuario():
    # Si el cliente manda JSON
    if request.is_json:
        datos = request.get_json()
    else:
        # request.form funciona para form-data y x-www-form-urlencoded
        datos = request.form.to_dict()
    nombre = datos.get('nombre')
    correo = datos.get('correo')

    if not nombre or not correo:
        return jsonify({"error": "Faltan campos. Enviar 'nombre' y 'correo'."}), 400
    nuevo_usuario = {
        "id": len(usuarios) + 1,
        "nombre": nombre,
        "correo": correo
    }
    usuarios.append(nuevo_usuario)
    return jsonify({"mensaje": "Usuario creado correctamente", "usuario": nuevo_usuario}), 201

# (C-Alternativo) Crear usuario por GET (para probar en el navegador)
@app.route('/crear', methods=['GET'])
def crear_usuario_get():
    nombre = request.args.get('usuario')
    correo = request.args.get('correo')
    if not nombre or not correo:
        return jsonify({"error": "Enviar 'usuario' y 'correo' en la URL"}), 400
    nuevo_usuario = {
        "id": len(usuarios) + 1,
        "nombre": nombre,
        "correo": correo
    }
    usuarios.append(nuevo_usuario)
    return jsonify({
        "mensaje": "Usuario creado correctamente (por GET)",
        "usuario": nuevo_usuario
    })

# (R) - Leer todos los usuarios
@app.route('/usuarios', methods=['GET'])
def obtener_usuarios():
    return jsonify(usuarios)

# (R) - Leer un usuario por ID
@app.route('/usuarios/<int:id>', methods=['GET'])
def obtener_usuario(id):
    usuario = next((u for u in usuarios if u["id"] == id), None)
    if usuario:
        return jsonify(usuario)
    return jsonify({"error": "Usuario no encontrado"}), 404

# (U) - Actualizar un usuario
@app.route('/usuarios/<int:id>', methods=['PUT'])
def actualizar_usuario(id):
    usuario = next((u for u in usuarios if u["id"] == id), None)
    if not usuario:
        return jsonify({"error": "Usuario no encontrado"}), 404
    datos = request.get_json()
    usuario.update({
        "nombre": datos.get("nombre", usuario["nombre"]),
        "correo": datos.get("correo", usuario["correo"])
    })
    return jsonify({"mensaje": "Usuario actualizado", "usuario": usuario})

# (D) - Eliminar un usuario
@app.route('/usuarios/<int:id>', methods=['DELETE'])
def eliminar_usuario(id):
    global usuarios
    usuarios = [u for u in usuarios if u["id"] != id]
    return jsonify({"mensaje": f"Usuario con ID {id} eliminado"})

if __name__ == '__main__':
    app.run(debug=True)
