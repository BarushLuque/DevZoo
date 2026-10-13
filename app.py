from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector

app = Flask(__name__)

db_config = {
    'host': 'localhost',
    'port': 3307,
    'user': 'root',
    'password': 'Admin',
    'database': 'wildland_zoo'
}


def get_db_connection():
    return mysql.connector.connect(**db_config)


def leer_formulario():
    nombre = request.form.get('nombre', '').strip()
    color = request.form.get('color', '').strip()
    especie = request.form.get('especie', '').strip()
    if not (nombre and color and especie):
        return None
    return nombre, color, especie


# READ
@app.route('/')
def index():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id, nombre, color, especie FROM animales ORDER BY id")
        animales = cursor.fetchall()
        cursor.close()
        conn.close()
        return render_template('index.html', animales=animales)
    except mysql.connector.Error as err:
        return f"Error al conectar con la base de datos: {err}", 500


# CREATE
@app.route('/agregar', methods=['POST'])
def agregar():
    datos = leer_formulario()
    if datos is None:
        flash('Todos los campos son obligatorios.')
        return redirect(url_for('index'))

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO animales (nombre, color, especie) VALUES (%s, %s, %s)",
            datos
        )
        conn.commit()
        cursor.close()
        conn.close()
        flash('Animal agregado correctamente.')
    except mysql.connector.Error as err:
        flash(f'Error al agregar: {err}')
    return redirect(url_for('index'))


# UPDATE
@app.route('/editar/<int:id>', methods=['POST'])
def editar(id):
    datos = leer_formulario()
    if datos is None:
        flash('Todos los campos son obligatorios.')
        return redirect(url_for('index'))

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE animales SET nombre = %s, color = %s, especie = %s WHERE id = %s",
            datos + (id,)
        )
        conn.commit()
        cursor.close()
        conn.close()
        flash('Animal actualizado correctamente.')
    except mysql.connector.Error as err:
        flash(f'Error al actualizar: {err}')
    return redirect(url_for('index'))


# DELETE
@app.route('/eliminar/<int:id>', methods=['POST'])
def eliminar(id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM animales WHERE id = %s", (id,))
        conn.commit()
        cursor.close()
        conn.close()
        flash('Animal eliminado correctamente.')
    except mysql.connector.Error as err:
        flash(f'Error al eliminar: {err}')
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=False)