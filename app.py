from flask import Flask, render_template, request, redirect, url_for, session, flash, send_file
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from generador_pdf import generate_ticket_pdf
import os
from email_sender import enviar_correo
from datetime import timedelta

BASE_DATOS_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "wuALdi34",
    "database": "bd_eventos",
    "port": 3306
}

app = Flask(__name__)
app.secret_key = "wuALdi34"
app.config["DEBUG"] = True


@app.route('/')
def home():
    try:
        conn = mysql.connector.connect(**BASE_DATOS_CONFIG)
        cursor = conn.cursor(dictionary=True)
        
        # Consulta para extraer los eventos junto con el nombre de su categoría y ubicación
        query_events = """
            SELECT e.*, c.nombre AS categoria, u.nombre AS ubicacion
            FROM eventos e
            JOIN categoria c ON e.id_categoria = c.id
            JOIN ubicacion u ON e.id_ubicacion = u.id
        """
        cursor.execute(query_events)
        eventos = cursor.fetchall()
        
        # Consulta para obtener todas las categorías
        query_categorias = "SELECT * FROM categoria"
        cursor.execute(query_categorias)
        categorias = cursor.fetchall()
        
        # Consulta para obtener todas las ubicaciones
        query_ubicaciones = "SELECT * FROM ubicacion"
        cursor.execute(query_ubicaciones)
        ubicaciones = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        # Se pasan los datos a la plantilla home.html
        return render_template("home.html", eventos=eventos, categorias=categorias, ubicaciones=ubicaciones)
    except mysql.connector.Error as err:
        return f"Error en la conexión a MySQL: {err}"

@app.route('/register', methods=['POST'])
def register():
    nombre = request.form.get("registerName")
    email = request.form.get("registerEmail")
    password = request.form.get("registerPassword")
    
    if not nombre or not email or not password:
        return "Faltan datos en el formulario"

    rol = "asistente"
    fecha_actual = datetime.now().strftime("%Y-%m-%d")
    password_codificada = generate_password_hash(password)
    
    try:
        conn = mysql.connector.connect(**BASE_DATOS_CONFIG)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO usuarios (nombre, email, contra, rol, fecha_registro) VALUES (%s, %s, %s, %s, %s)",
            (nombre, email, password_codificada, rol, fecha_actual)
        )
        conn.commit()
        cursor.close()
        conn.close()
        # Se redirige a home enviando parámetros para abrir el modal de login con un mensaje
        return redirect(url_for('home', modal='login', message='Ya has sido registrado, inicia sesión para comprar tus tickets.'))
    except mysql.connector.Error as err:
        return f"Error en la conexión a MySQL: {err}"

@app.route('/login', methods=['POST'])
def login():
    email = request.form.get("loginEmail")
    password = request.form.get("loginPassword")
    if not email or not password:
        flash("Faltan datos en el formulario", "danger")
        return redirect(url_for('home', modal='login'))

    try:
        conn = mysql.connector.connect(**BASE_DATOS_CONFIG)
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute("SELECT * FROM usuarios WHERE email = %s", (email,))
        usuario = cursor.fetchone()
        
        cursor.close()
        conn.close()

        if usuario and check_password_hash(usuario["contra"], password):
            session["user_id"] = usuario["id"]
            session["user_name"] = usuario["nombre"]
            session["user_email"] = usuario["email"]
            session["user_role"] = usuario["rol"]
            flash("Inicio de sesión exitoso", "success")
            if session["user_role"] == "organizador":
               
                return redirect(url_for('admin_seccion'))
            else:
                return redirect(url_for('home'))
        else:
            flash("Correo o contraseña incorrectos", "danger")
            return redirect(url_for('home', modal='login'))
    except mysql.connector.Error as err:
        return f"Error en la conexión a MySQL: {err}"

@app.route('/logout')
def logout():
    session.clear()
    flash("Has cerrado sesión", "info")
    return redirect(url_for('home'))

@app.route('/buy-ticket/<int:event_id>')
def buy_ticket(event_id):
    try:
        conn = mysql.connector.connect(**BASE_DATOS_CONFIG)
        cursor = conn.cursor(dictionary=True)
        query = """
            SELECT e.*, c.nombre AS categoria, u.nombre AS ubicacion
            FROM eventos e
            JOIN categoria c ON e.id_categoria = c.id
            JOIN ubicacion u ON e.id_ubicacion = u.id
            WHERE e.id = %s
        """
        cursor.execute(query, (event_id,))
        evento = cursor.fetchone()
        cursor.close()
        conn.close()
        if evento:
            return render_template("buy_ticket.html", evento=evento)
        else:
            return "Evento no encontrado", 404
    except mysql.connector.Error as err:
        return f"Error en la conexión a MySQL: {err}"


import uuid
import os

@app.route('/procesar-compra', methods=['POST'])
def procesar_compra():
    # Verificar que el usuario haya iniciado sesión
    if "user_email" not in session:
        flash("Debe iniciar sesión para comprar tickets", "danger")
        return redirect(url_for('home', modal='login'))
    
    # Obtener datos del formulario
    event_id = request.form.get("event_id")
    quantity = request.form.get("quantity")
    event_price = request.form.get("event_price")
    try:
        quantity = int(quantity)
        event_price = float(event_price.strip())
    except ValueError:
        return "Datos de compra inválidos", 400

    feePerTicket = 3.50
    subtotal = quantity * event_price
    fees = feePerTicket  # Según tu lógica
    total = subtotal + fees

    # Obtener detalles del evento de la base de datos
    try:
        conn = mysql.connector.connect(**BASE_DATOS_CONFIG)
        cursor = conn.cursor(dictionary=True)
        query = """
            SELECT e.*, c.nombre AS categoria, u.nombre AS ubicacion
            FROM eventos e
            JOIN categoria c ON e.id_categoria = c.id
            JOIN ubicacion u ON e.id_ubicacion = u.id
            WHERE e.id = %s
        """
        cursor.execute(query, (event_id,))
        evento = cursor.fetchone()
        cursor.close()
        conn.close()
    except mysql.connector.Error as err:
        return f"Error en la conexión a MySQL: {err}"
    
    if not evento:
        return "Evento no encontrado", 404

    # Generar el PDF (se asume que generate_ticket_pdf devuelve un objeto BytesIO)
    pdf_buffer = generate_ticket_pdf(evento, quantity, event_price, subtotal, fees, total, session.get('user_email'))
    pdf_buffer.seek(0)

    # Guardar el PDF en un archivo temporal
    tmp_filename = str(uuid.uuid4()) + ".pdf"
    tmp_path = os.path.join("tmp", tmp_filename)
    if not os.path.exists("tmp"):
        os.makedirs("tmp")
    with open(tmp_path, "wb") as f:
        f.write(pdf_buffer.getbuffer())

    # Reiniciar el puntero para enviar el correo
    pdf_buffer.seek(0)

    # Enviar el correo adjuntando el PDF
    enviar_correo(
        session.get('user_email'),
        "Usted ha comprado tickets de EventHub",
        "Felicidades, sus tickets han llegado exitosamente!.",
        pdf_buffer
    )

    # Mostrar mensaje de agradecimiento y redirigir a una página que inicie la descarga
    flash("Gracias por su compra. Su ticket se descargara en breve.", "success")
    return render_template("descargar_ticket.html", filename=tmp_filename)

    
@app.route('/enviar-correo-contacto', methods=['POST'])
def enviar_correo_contacto():
    nombre = request.form.get("name")
    correo = request.form.get("email")
    asunto = request.form.get("subject")
    mensaje = request.form.get("message")
    print("llega todo")
    enviar_correo("eventhub.oficial@gmail.com", asunto, mensaje + " - Correo enviado por: " + correo + ". La persona se llama "+nombre, None)
    flash("Gracias por su Consulta, en breve nos comunicaremos con usted", "success")
    
    return render_template("contacto.html")
    
@app.route('/contacto')
def contacto():
    return render_template("contacto.html")

@app.route('/descargar-ticket/<filename>')
def descargar_ticket(filename):
    tmp_path = os.path.join("tmp", filename)
    # Puedes optar por eliminar el archivo después de enviarlo, si lo deseas.
    return send_file(tmp_path, as_attachment=True, download_name="ticket.pdf", mimetype='application/pdf')

@app.route('/admin_seccion')
def admin_seccion():
    conn = mysql.connector.connect(**BASE_DATOS_CONFIG)
    cursor = conn.cursor(dictionary=True)
    
    # Consulta para obtener todas las categorías
    query_categorias = "SELECT * FROM categoria"
    cursor.execute(query_categorias)
    categorias = cursor.fetchall()
    
    # Consulta para obtener todas las ubicaciones
    query_ubicaciones = "SELECT * FROM ubicacion"
    cursor.execute(query_ubicaciones)
    ubicaciones = cursor.fetchall()
    
    # Consulta para obtener todos los eventos
    query_eventos = "SELECT * FROM eventos"
    cursor.execute(query_eventos)
    eventos = cursor.fetchall()
    
    # Consulta para obtener todos los eventos
    query_usuarios = "SELECT * FROM usuarios"
    cursor.execute(query_usuarios)
    usuarios = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    # Convertir campos que no son JSON serializables
    for evento in eventos:
        # Si "hora_inicio" es un timedelta, formatearlo a "HH:MM:SS"
        if isinstance(evento.get('hora_inicio'), timedelta):
            total_seconds = int(evento['hora_inicio'].total_seconds())
            hours = total_seconds // 3600
            minutes = (total_seconds % 3600) // 60
    
            evento['hora_inicio'] = f"{hours:02d}:{minutes:02d}"
    
    return render_template("admin_section.html", categorias=categorias, ubicaciones=ubicaciones, eventos=eventos, usuarios = usuarios)
def test_db_connection():
    try:
        conn = mysql.connector.connect(**BASE_DATOS_CONFIG)
        if conn.is_connected():
            return "Conexión exitosa a MySQL"
    except mysql.connector.Error as err:
        return f"Error en la conexión a MySQL: {err}"
    finally:
        if 'conn' in locals() and conn.is_connected():
            conn.close()

@app.route('/conexion')
def conexion():
    mensaje = test_db_connection()
    return f"<h1>{mensaje}</h1>"

@app.route('/procesar-compra')
def procesarCompra():
    #mensaje = "Le hemos enviado un correo con sus tickets. Felicidades por su compra "
    return redirect(url_for('home'))

@app.route('/nuevo-evento-creado', methods=['POST'])
def nuevo_evento_creado():
    print("Llegan los datos 1")
    # Verificar que el usuario esté autenticado y sea organizador
    if 'user_id' not in session or session.get('user_role') != 'organizador':
        flash("Acceso no autorizado.", "danger")
        return redirect(url_for('home'))
    
    # Recoger datos del formulario
    nombre = request.form.get("nombre")
    descripcion = request.form.get("descripcion")
    duracion = request.form.get("duracion")
    hora_inicio = request.form.get("hora_inicio")
    precio = request.form.get("precio")
    fecha = request.form.get("fecha")
    capacidad = request.form.get("capacidad")
    tickets_disponibles = request.form.get("tickets_disponibles")
    url_imagen = request.form.get("url_imagen")
    id_categoria = request.form.get("id_categoria")
    id_ubicacion = request.form.get("id_ubicacion")
    
    # Asumir que el organizador es el usuario logueado
    id_organizador = session.get("user_id")
    print("Llegan los datos 2")
    # Validar que los campos obligatorios estén completos
    if not all([nombre, duracion, hora_inicio, precio, fecha, capacidad, tickets_disponibles, url_imagen, id_categoria, id_ubicacion]):
        flash("Faltan datos obligatorios", "danger")
        return redirect(url_for('admin_seccion'))
    
    try:
        conn = mysql.connector.connect(**BASE_DATOS_CONFIG)
        cursor = conn.cursor()
        query = """
            INSERT INTO eventos (nombre, descripcion, duracion, hora_inicio, precio, fecha, capacidad, tickets_disponibles, url_imagen, id_organizador, id_categoria, id_ubicacion)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        data = (
            nombre,
            descripcion,
            int(duracion),
            hora_inicio,
            int(precio),
            fecha,
            int(capacidad),
            int(tickets_disponibles),
            url_imagen,
            id_organizador,
            int(id_categoria),
            int(id_ubicacion)
        )
        print("Guardando: ", data)
        cursor.execute(query, data)
        conn.commit()
        cursor.close()
        conn.close()
        flash("Evento creado exitosamente", "success")
        return redirect(url_for('admin_seccion'))
    except mysql.connector.Error as err:
        flash(f"Error al crear el evento: {err}", "danger")
        return redirect(url_for('admin_seccion'))

@app.route('/eliminar-evento/<int:evento_id>', methods=['POST'])
def eliminar_evento(evento_id):
    # Verificar que el usuario esté autenticado y sea organizador
    if 'user_id' not in session or session.get('user_role') != 'organizador':
        flash("Acceso no autorizado.", "danger")
        return redirect(url_for('home'))
    
    try:
        conn = mysql.connector.connect(**BASE_DATOS_CONFIG)
        cursor = conn.cursor()
        query = "DELETE FROM eventos WHERE id = %s"
        cursor.execute(query, (evento_id,))
        conn.commit()
        cursor.close()
        conn.close()
        flash("Evento eliminado correctamente", "success")
    except mysql.connector.Error as err:
        flash(f"Error al eliminar el evento: {err}", "danger")
    return redirect(url_for('admin_seccion'))

@app.route('/editar-evento', methods=['POST'])
def editar_evento():
    # Verificar que el usuario esté autenticado y sea organizador
    if 'user_id' not in session or session.get('user_role') != 'organizador':
        flash("Acceso no autorizado.", "danger")
        return redirect(url_for('home'))
    
    # Recoger datos del formulario
    evento_id = request.form.get("eventoId")
    nombre = request.form.get("nombre")
    descripcion = request.form.get("descripcion")
    duracion = request.form.get("duracion")
    hora_inicio = request.form.get("hora_inicio")
    precio = request.form.get("precio")
    fecha = request.form.get("fecha")
    capacidad = request.form.get("capacidad")
    tickets_disponibles = request.form.get("tickets_disponibles")
    url_imagen = request.form.get("url_imagen")
    id_categoria = request.form.get("id_categoria")
    id_ubicacion = request.form.get("id_ubicacion")
    
    # Validar que el ID del evento exista
    if not evento_id:
        flash("No se encontró el ID del evento.", "danger")
        return redirect(url_for('admin_seccion'))
    
    # Validar que los campos obligatorios estén completos
    if not all([nombre, duracion, hora_inicio, precio, fecha, capacidad, tickets_disponibles, url_imagen, id_categoria, id_ubicacion]):
        flash("Faltan datos obligatorios", "danger")
        return redirect(url_for('admin_seccion'))
    
    try:
        conn = mysql.connector.connect(**BASE_DATOS_CONFIG)
        cursor = conn.cursor()
        query = """
            UPDATE eventos 
            SET nombre = %s, descripcion = %s, duracion = %s, hora_inicio = %s, precio = %s, 
                fecha = %s, capacidad = %s, tickets_disponibles = %s, url_imagen = %s, 
                id_categoria = %s, id_ubicacion = %s 
            WHERE id = %s
        """
        data = (
            nombre,
            descripcion,
            int(duracion),
            hora_inicio,
            int(precio),
            fecha,
            int(capacidad),
            int(tickets_disponibles),
            url_imagen,
            int(id_categoria),
            int(id_ubicacion),
            int(evento_id)
        )
        cursor.execute(query, data)
        conn.commit()
        cursor.close()
        conn.close()
        flash("Evento actualizado exitosamente", "success")
        return redirect(url_for('admin_seccion'))
    except mysql.connector.Error as err:
        flash(f"Error al actualizar el evento: {err}", "danger")
        return redirect(url_for('admin_seccion'))

@app.route('/nueva-categoria', methods=['POST'])
def nueva_categoria():
    # Verificar si el usuario tiene permiso (puedes ajustar la lógica según tu caso)
    if 'user_id' not in session or session.get('user_role') != 'organizador':
        flash("Acceso no autorizado.", "danger")
        return redirect(url_for('home'))
    nombre_categoria = request.form.get("nombre_categoria")
    if not nombre_categoria:
        flash("El nombre de la categoría es obligatorio", "danger")
        return redirect(url_for('admin_seccion'))
    try:
        conn = mysql.connector.connect(**BASE_DATOS_CONFIG)
        cursor = conn.cursor()
        query = "INSERT INTO categoria (nombre) VALUES (%s)"
        cursor.execute(query, (nombre_categoria,))
        conn.commit()
        cursor.close()
        conn.close()
        flash("Categoría creada exitosamente", "success")
    except mysql.connector.Error as err:
        flash(f"Error al crear la categoría: {err}", "danger")
    return redirect(url_for('admin_seccion'))

@app.route('/editar-categoria', methods=['POST'])
def editar_categoria():
    if 'user_id' not in session or session.get('user_role') != 'organizador':
        flash("Acceso no autorizado.", "danger")
        return redirect(url_for('home'))
    categoria_id = request.form.get("categoriaId")
    nombre_categoria = request.form.get("nombre_categoria")
    if not categoria_id or not nombre_categoria:
        flash("Datos insuficientes para editar la categoría", "danger")
        return redirect(url_for('admin_seccion'))
    try:
        conn = mysql.connector.connect(**BASE_DATOS_CONFIG)
        cursor = conn.cursor()
        query = "UPDATE categoria SET nombre = %s WHERE id = %s"
        cursor.execute(query, (nombre_categoria, int(categoria_id)))
        conn.commit()
        cursor.close()
        conn.close()
        flash("Categoría actualizada exitosamente", "success")
    except mysql.connector.Error as err:
        flash(f"Error al actualizar la categoría: {err}", "danger")
    return redirect(url_for('admin_seccion'))

@app.route('/eliminar-categoria/<int:categoria_id>', methods=['POST'])
def eliminar_categoria(categoria_id):
    if 'user_id' not in session or session.get('user_role') != 'organizador':
        flash("Acceso no autorizado.", "danger")
        return redirect(url_for('home'))
    try:
        conn = mysql.connector.connect(**BASE_DATOS_CONFIG)
        cursor = conn.cursor()
        query = "DELETE FROM categoria WHERE id = %s"
        cursor.execute(query, (categoria_id,))
        conn.commit()
        cursor.close()
        conn.close()
        flash("Categoría eliminada exitosamente", "success")
    except mysql.connector.Error as err:
        flash(f"Error al eliminar la categoría: {err}", "danger")
    return redirect(url_for('admin_seccion'))

@app.route('/nueva-ubicacion', methods=['POST'])
def nueva_ubicacion():
    # Verificar permisos (ajusta según tu lógica de roles)
    if 'user_id' not in session or session.get('user_role') != 'organizador':
        flash("Acceso no autorizado.", "danger")
        return redirect(url_for('home'))
    nombre_ubicacion = request.form.get("nombre_ubicacion")
    if not nombre_ubicacion:
        flash("El nombre de la ubicación es obligatorio", "danger")
        return redirect(url_for('admin_seccion'))
    try:
        conn = mysql.connector.connect(**BASE_DATOS_CONFIG)
        cursor = conn.cursor()
        query = "INSERT INTO ubicacion (nombre) VALUES (%s)"
        cursor.execute(query, (nombre_ubicacion,))
        conn.commit()
        cursor.close()
        conn.close()
        flash("Ubicación creada exitosamente", "success")
    except mysql.connector.Error as err:
        flash(f"Error al crear la ubicación: {err}", "danger")
    return redirect(url_for('admin_seccion'))

@app.route('/editar-ubicacion', methods=['POST'])
def editar_ubicacion():
    if 'user_id' not in session or session.get('user_role') != 'organizador':
        flash("Acceso no autorizado.", "danger")
        return redirect(url_for('home'))
    ubicacion_id = request.form.get("ubicacionId")
    nombre_ubicacion = request.form.get("nombre_ubicacion")
    if not ubicacion_id or not nombre_ubicacion:
        flash("Datos insuficientes para editar la ubicación", "danger")
        return redirect(url_for('admin_seccion'))
    try:
        conn = mysql.connector.connect(**BASE_DATOS_CONFIG)
        cursor = conn.cursor()
        query = "UPDATE ubicacion SET nombre = %s WHERE id = %s"
        cursor.execute(query, (nombre_ubicacion, int(ubicacion_id)))
        conn.commit()
        cursor.close()
        conn.close()
        flash("Ubicación actualizada exitosamente", "success")
    except mysql.connector.Error as err:
        flash(f"Error al actualizar la ubicación: {err}", "danger")
    return redirect(url_for('admin_seccion'))

@app.route('/eliminar-ubicacion/<int:ubicacion_id>', methods=['POST'])
def eliminar_ubicacion(ubicacion_id):
    if 'user_id' not in session or session.get('user_role') != 'organizador':
        flash("Acceso no autorizado.", "danger")
        return redirect(url_for('home'))
    try:
        conn = mysql.connector.connect(**BASE_DATOS_CONFIG)
        cursor = conn.cursor()
        query = "DELETE FROM ubicacion WHERE id = %s"
        cursor.execute(query, (ubicacion_id,))
        conn.commit()
        cursor.close()
        conn.close()
        flash("Ubicación eliminada exitosamente", "success")
    except mysql.connector.Error as err:
        flash(f"Error al eliminar la ubicación: {err}", "danger")
    return redirect(url_for('admin_seccion'))

@app.route('/nuevo-usuario', methods=['POST'])
def nuevo_usuario():
    # Verificar permisos (solo organizadores pueden gestionar usuarios)
    if 'user_id' not in session or session.get('user_role') != 'organizador':
        flash("Acceso no autorizado.", "danger")
        return redirect(url_for('home'))
    nombre_usuario = request.form.get("nombre_usuario")
    email_usuario = request.form.get("email_usuario")
    rol_usuario = request.form.get("rol_usuario", "").lower()

    if not nombre_usuario or not email_usuario or not rol_usuario:
        flash("Faltan datos obligatorios", "danger")
        return redirect(url_for('admin_seccion'))
    try:
        conn = mysql.connector.connect(**BASE_DATOS_CONFIG)
        cursor = conn.cursor()
        query = "INSERT INTO usuarios (nombre, email, contra, rol, fecha_registro) VALUES (%s, %s, %s, %s, %s)"
        # Establecemos una contraseña por defecto (en producción, se debe gestionar adecuadamente)
        default_password = generate_password_hash("password123")
        fecha_actual = datetime.now().strftime("%Y-%m-%d")
        cursor.execute(query, (nombre_usuario, email_usuario, default_password, rol_usuario, fecha_actual))
        conn.commit()
        cursor.close()
        conn.close()
        flash("Usuario creado exitosamente", "success")
    except mysql.connector.Error as err:
        flash(f"Error al crear el usuario: {err}", "danger")
        print("Ha ocurrido error!")
    return redirect(url_for('admin_seccion'))

@app.route('/editar-usuario', methods=['POST'])
def editar_usuario():
    if 'user_id' not in session or session.get('user_role') != 'organizador':
        flash("Acceso no autorizado.", "danger")
        return redirect(url_for('home'))
    usuario_id = request.form.get("usuarioId")
    nombre_usuario = request.form.get("nombre_usuario")
    email_usuario = request.form.get("email_usuario")
    rol_usuario = request.form.get("rol_usuario","").lower()
    if not usuario_id or not nombre_usuario or not email_usuario or not rol_usuario:
        flash("Datos insuficientes para editar el usuario", "danger")
        return redirect(url_for('admin_seccion'))
    try:
        conn = mysql.connector.connect(**BASE_DATOS_CONFIG)
        cursor = conn.cursor()
        query = "UPDATE usuarios SET nombre = %s, email = %s, rol = %s WHERE id = %s"
        cursor.execute(query, (nombre_usuario, email_usuario, rol_usuario, int(usuario_id)))
        conn.commit()
        cursor.close()
        conn.close()
        flash("Usuario actualizado exitosamente", "success")
    except mysql.connector.Error as err:
        flash(f"Error al actualizar el usuario: {err}", "danger")
    return redirect(url_for('admin_seccion'))

@app.route('/cookie-policy')
def cookie_policy():
    return render_template('cookie_policy.html')


@app.route('/eliminar-usuario/<int:usuario_id>', methods=['POST'])
def eliminar_usuario(usuario_id):
    if 'user_id' not in session or session.get('user_role') != 'organizador':
        flash("Acceso no autorizado.", "danger")
        return redirect(url_for('home'))
    try:
        conn = mysql.connector.connect(**BASE_DATOS_CONFIG)
        cursor = conn.cursor()
        query = "DELETE FROM usuarios WHERE id = %s"
        cursor.execute(query, (usuario_id,))
        conn.commit()
        cursor.close()
        conn.close()
        flash("Usuario eliminado exitosamente", "success")
    except mysql.connector.Error as err:
        flash(f"Error al eliminar el usuario: {err}", "danger")
    return redirect(url_for('admin_seccion'))


if __name__ == '__main__':
    app.run(debug=True)

