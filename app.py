import os
import sqlite3
from datetime import datetime
from functools import wraps

from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash

CONTRASENA_ADMIN_POR_DEFECTO = "admin123"

# Usamos rutas absolutas basadas en la ubicación de este archivo, así
# la base de datos y el esquema se encuentran sin importar desde dónde
# se ejecute el programa (terminal, VS Code, vista previa, etc.)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.environ.get("DB_PATH", os.path.join(BASE_DIR, "inventario.db"))
SCHEMA_PATH = os.path.join(BASE_DIR, "schema.sql")

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "clave-secreta-local-inventario")


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
        conn.executescript(f.read())
    conn.commit()
    conn.close()


def migrar_db():
    """Actualiza una base de datos ya existente para que tenga las columnas y
    tablas nuevas, sin borrar los datos que ya tiene guardados."""
    conn = get_db()
    columnas_ventas = [fila["name"] for fila in conn.execute("PRAGMA table_info(ventas)").fetchall()]
    if "cancelada" not in columnas_ventas:
        conn.execute("ALTER TABLE ventas ADD COLUMN cancelada INTEGER NOT NULL DEFAULT 0")
    if "motivo_cancelacion" not in columnas_ventas:
        conn.execute("ALTER TABLE ventas ADD COLUMN motivo_cancelacion TEXT")
    if "fecha_cancelacion" not in columnas_ventas:
        conn.execute("ALTER TABLE ventas ADD COLUMN fecha_cancelacion TEXT")
    conn.execute(
        "CREATE TABLE IF NOT EXISTS configuracion (clave TEXT PRIMARY KEY, valor TEXT)"
    )
    conn.execute(
        "CREATE TABLE IF NOT EXISTS turnos_caja ("
        "id INTEGER PRIMARY KEY AUTOINCREMENT, "
        "fecha_apertura TEXT NOT NULL, "
        "monto_inicial REAL NOT NULL DEFAULT 0, "
        "notas_apertura TEXT, "
        "fecha_cierre TEXT, "
        "monto_esperado REAL, "
        "monto_contado REAL, "
        "diferencia REAL, "
        "notas_cierre TEXT, "
        "cerrado INTEGER NOT NULL DEFAULT 0"
        ")"
    )
    if "turno_id" not in columnas_ventas:
        conn.execute("ALTER TABLE ventas ADD COLUMN turno_id INTEGER REFERENCES turnos_caja (id)")
    if "monto_recibido" not in columnas_ventas:
        conn.execute("ALTER TABLE ventas ADD COLUMN monto_recibido REAL")
    if "cambio" not in columnas_ventas:
        conn.execute("ALTER TABLE ventas ADD COLUMN cambio REAL")
    conn.commit()
    conn.close()


def obtener_turno_abierto(conn):
    return conn.execute(
        "SELECT * FROM turnos_caja WHERE cerrado = 0 ORDER BY id DESC LIMIT 1"
    ).fetchone()


def asegurar_db():
    """Crea la base de datos con su esquema si todavía no existe, o la actualiza
    si ya existía pero le faltan columnas/tablas nuevas."""
    nueva = not os.path.exists(DB_PATH)
    if nueva:
        init_db()
    else:
        migrar_db()
    if nueva or obtener_config("admin_password_hash") is None:
        establecer_config("admin_password_hash", generate_password_hash(CONTRASENA_ADMIN_POR_DEFECTO))


def obtener_config(clave):
    conn = get_db()
    fila = conn.execute("SELECT valor FROM configuracion WHERE clave = ?", (clave,)).fetchone()
    conn.close()
    return fila["valor"] if fila else None


def establecer_config(clave, valor):
    conn = get_db()
    conn.execute(
        "INSERT INTO configuracion (clave, valor) VALUES (?, ?) "
        "ON CONFLICT(clave) DO UPDATE SET valor = excluded.valor",
        (clave, valor),
    )
    conn.commit()
    conn.close()


def verificar_contrasena_admin(contrasena):
    hash_guardado = obtener_config("admin_password_hash")
    if not hash_guardado:
        return False
    return check_password_hash(hash_guardado, contrasena or "")


def requiere_admin(vista):
    """Decorador: exige que se haya iniciado sesión como administrador
    (mediante /productos/acceso) antes de poder ver o modificar el catálogo."""
    @wraps(vista)
    def envoltura(*args, **kwargs):
        if not session.get("es_admin"):
            session["destino_tras_acceso"] = request.url
            flash("Esta sección es exclusiva del administrador. Ingresa la contraseña para continuar.", "error")
            return redirect(url_for("acceso_productos"))
        return vista(*args, **kwargs)
    return envoltura


@app.route("/productos/acceso", methods=["GET", "POST"])
def acceso_productos():
    if session.get("es_admin"):
        return redirect(url_for("productos"))

    if request.method == "POST":
        contrasena = request.form.get("contrasena", "")
        if verificar_contrasena_admin(contrasena):
            session["es_admin"] = True
            destino = session.pop("destino_tras_acceso", None)
            flash("Acceso de administrador concedido.", "success")
            return redirect(destino or url_for("productos"))
        flash("Contraseña de administrador incorrecta.", "error")

    return render_template("acceso_productos.html")


@app.route("/productos/salir")
def salir_productos():
    session.pop("es_admin", None)
    flash("Saliste del modo administrador.", "success")
    return redirect(url_for("inicio"))


# Nos aseguramos de que la base de datos exista apenas se carga la app,
# sin importar si se ejecuta con `python app.py` o a través de otra
# herramienta que importe este módulo directamente.
asegurar_db()


def buscar_productos(conn, texto, solo_disponibles=False):
    """Búsqueda inteligente: separa el texto en palabras y ordena los resultados
    por cuántas palabras coinciden con el código o el nombre del producto.
    Así "filtro camion 5080" encuentra "Filtro de combustible para camión 5080 KXY"
    aunque el orden de las palabras sea distinto."""
    palabras = [p for p in texto.lower().split() if p]
    if not palabras:
        return []

    if solo_disponibles:
        filas = conn.execute(
            "SELECT * FROM productos WHERE tipo = 'servicio' OR stock > 0"
        ).fetchall()
    else:
        filas = conn.execute("SELECT * FROM productos").fetchall()

    resultados = []
    for fila in filas:
        texto_producto = f"{fila['codigo'] or ''} {fila['nombre']}".lower()
        coincidencias = sum(1 for palabra in palabras if palabra in texto_producto)
        if coincidencias > 0:
            resultados.append((coincidencias, fila))

    # Más coincidencias primero; a igualdad, orden alfabético por nombre
    resultados.sort(key=lambda par: (-par[0], par[1]["nombre"].lower()))
    return [fila for _, fila in resultados]


@app.route("/api/buscar_productos")
def api_buscar_productos():
    texto = request.args.get("q", "").strip()
    solo_disponibles = request.args.get("disponibles") == "1"
    conn = get_db()
    items = buscar_productos(conn, texto, solo_disponibles=solo_disponibles) if texto else []
    conn.close()

    return {
        "resultados": [
            {
                "id": p["id"],
                "codigo": p["codigo"] or "",
                "nombre": p["nombre"],
                "tipo": p["tipo"],
                "precio": p["precio"],
                "stock": p["stock"],
                "disponible": (p["tipo"] == "servicio" or p["stock"] > 0),
            }
            for p in items[:15]
        ]
    }


# ---------- Inicio ----------

@app.route("/")
def inicio():
    conn = get_db()
    total_productos = conn.execute("SELECT COUNT(*) AS c FROM productos").fetchone()["c"]
    ventas_hoy = conn.execute(
        "SELECT COUNT(*) AS c, COALESCE(SUM(total), 0) AS suma FROM ventas WHERE fecha LIKE ?",
        (datetime.now().strftime("%Y-%m-%d") + "%",),
    ).fetchone()
    conn.close()
    return render_template(
        "inicio.html",
        total_productos=total_productos,
        ventas_hoy=ventas_hoy["c"],
        total_hoy=ventas_hoy["suma"],
    )


# ---------- Catálogo de productos ----------

@app.route("/productos")
@requiere_admin
def productos():
    busqueda = request.args.get("q", "").strip()
    conn = get_db()
    if busqueda:
        items = buscar_productos(conn, busqueda)
    else:
        items = conn.execute("SELECT * FROM productos ORDER BY nombre").fetchall()
    conn.close()
    return render_template("productos.html", productos=items, busqueda=busqueda)


@app.route("/productos/nuevo", methods=["GET", "POST"])
@requiere_admin
def nuevo_producto():
    if request.method == "POST":
        codigo = request.form.get("codigo", "").strip()
        nombre = request.form["nombre"].strip()
        tipo = request.form["tipo"]
        precio = float(request.form["precio"] or 0)
        stock = int(request.form["stock"] or 0) if tipo == "producto" else 0

        if not nombre:
            flash("El nombre es obligatorio.", "error")
            return redirect(url_for("nuevo_producto"))

        conn = get_db()
        conn.execute(
            "INSERT INTO productos (codigo, nombre, tipo, precio, stock) VALUES (?, ?, ?, ?, ?)",
            (codigo, nombre, tipo, precio, stock),
        )
        conn.commit()
        conn.close()
        flash(f'"{nombre}" se agregó al catálogo.', "success")
        return redirect(url_for("productos"))

    return render_template("form_producto.html", producto=None)


@app.route("/productos/<int:producto_id>/editar", methods=["GET", "POST"])
@requiere_admin
def editar_producto(producto_id):
    conn = get_db()
    item = conn.execute("SELECT * FROM productos WHERE id = ?", (producto_id,)).fetchone()
    if item is None:
        conn.close()
        flash("Producto no encontrado.", "error")
        return redirect(url_for("productos"))

    if request.method == "POST":
        contrasena = request.form.get("contrasena", "")
        if not verificar_contrasena_admin(contrasena):
            conn.close()
            flash("Contraseña de administrador incorrecta. No se guardaron los cambios.", "error")
            return redirect(url_for("editar_producto", producto_id=producto_id))

        codigo = request.form.get("codigo", "").strip()
        nombre = request.form["nombre"].strip()
        tipo = request.form["tipo"]
        precio = float(request.form["precio"] or 0)
        stock = int(request.form["stock"] or 0) if tipo == "producto" else 0

        conn.execute(
            "UPDATE productos SET codigo = ?, nombre = ?, tipo = ?, precio = ?, stock = ? WHERE id = ?",
            (codigo, nombre, tipo, precio, stock, producto_id),
        )
        conn.commit()
        conn.close()
        flash(f'"{nombre}" se actualizó.', "success")
        return redirect(url_for("productos"))

    conn.close()
    return render_template("form_producto.html", producto=item)


@app.route("/productos/<int:producto_id>/eliminar", methods=["POST"])
@requiere_admin
def eliminar_producto(producto_id):
    contrasena = request.form.get("contrasena", "")
    if not verificar_contrasena_admin(contrasena):
        flash("Contraseña de administrador incorrecta. El producto no fue eliminado.", "error")
        return redirect(url_for("productos"))

    conn = get_db()
    item = conn.execute("SELECT * FROM productos WHERE id = ?", (producto_id,)).fetchone()
    conn.execute("DELETE FROM productos WHERE id = ?", (producto_id,))
    conn.commit()
    conn.close()
    nombre = item["nombre"] if item else f"#{producto_id}"
    flash(f'"{nombre}" se eliminó del catálogo.', "success")
    return redirect(url_for("productos"))


# ---------- Caja / punto de venta ----------

@app.route("/caja")
def caja():
    conn = get_db()
    turno = obtener_turno_abierto(conn)
    hay_disponibles = conn.execute(
        "SELECT 1 FROM productos WHERE tipo = 'servicio' OR stock > 0 LIMIT 1"
    ).fetchone()
    conn.close()
    return render_template("caja.html", productos_disponibles=hay_disponibles, turno=turno)


@app.route("/caja/abrir", methods=["POST"])
def abrir_caja():
    conn = get_db()
    if obtener_turno_abierto(conn) is not None:
        conn.close()
        flash("Ya hay un turno de caja abierto.", "error")
        return redirect(url_for("caja"))

    try:
        monto_inicial = float(request.form.get("monto_inicial", "0") or 0)
    except ValueError:
        monto_inicial = 0.0
    notas = request.form.get("notas_apertura", "").strip()

    conn.execute(
        "INSERT INTO turnos_caja (fecha_apertura, monto_inicial, notas_apertura) VALUES (?, ?, ?)",
        (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), monto_inicial, notas),
    )
    conn.commit()
    conn.close()
    flash(f"Caja abierta con un fondo inicial de ${monto_inicial:.2f}.", "success")
    return redirect(url_for("caja"))


@app.route("/caja/cerrar", methods=["GET", "POST"])
def cerrar_caja():
    conn = get_db()
    turno = obtener_turno_abierto(conn)
    if turno is None:
        conn.close()
        flash("No hay ningún turno de caja abierto.", "error")
        return redirect(url_for("caja"))

    resumen = conn.execute(
        "SELECT COUNT(*) AS num_ventas, COALESCE(SUM(total), 0) AS total_ventas "
        "FROM ventas WHERE turno_id = ? AND cancelada = 0",
        (turno["id"],),
    ).fetchone()
    monto_esperado = turno["monto_inicial"] + resumen["total_ventas"]

    if request.method == "POST":
        try:
            monto_contado = float(request.form.get("monto_contado", "0") or 0)
        except ValueError:
            monto_contado = 0.0
        notas_cierre = request.form.get("notas_cierre", "").strip()
        diferencia = monto_contado - monto_esperado

        conn.execute(
            "UPDATE turnos_caja SET fecha_cierre = ?, monto_esperado = ?, monto_contado = ?, "
            "diferencia = ?, notas_cierre = ?, cerrado = 1 WHERE id = ?",
            (
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                monto_esperado,
                monto_contado,
                diferencia,
                notas_cierre,
                turno["id"],
            ),
        )
        conn.commit()
        conn.close()
        flash(f"Caja cerrada. Diferencia: ${diferencia:.2f}.", "success")
        return redirect(url_for("turnos"))

    conn.close()
    return render_template(
        "cerrar_caja.html",
        turno=turno,
        resumen=resumen,
        monto_esperado=monto_esperado,
    )


@app.route("/caja/turnos")
def turnos():
    conn = get_db()
    items = conn.execute(
        "SELECT * FROM turnos_caja ORDER BY id DESC LIMIT 50"
    ).fetchall()
    conn.close()
    return render_template("turnos.html", turnos=items)


@app.route("/caja/vender", methods=["POST"])
def vender():
    """Recibe el carrito como listas paralelas: producto_id[] y cantidad[]."""
    conn_turno = get_db()
    turno = obtener_turno_abierto(conn_turno)
    conn_turno.close()
    if turno is None:
        flash("Debes abrir la caja antes de registrar una venta.", "error")
        return redirect(url_for("caja"))

    ids = request.form.getlist("producto_id")
    cantidades = request.form.getlist("cantidad")

    carrito = []
    for pid, cant in zip(ids, cantidades):
        try:
            cantidad = int(cant)
        except ValueError:
            cantidad = 0
        if cantidad > 0:
            carrito.append((int(pid), cantidad))

    if not carrito:
        flash("Agrega al menos un producto con cantidad mayor a 0.", "error")
        return redirect(url_for("caja"))

    try:
        monto_recibido = float(request.form.get("monto_recibido", "") or 0)
    except ValueError:
        monto_recibido = 0.0

    conn = get_db()

    # Validar stock disponible antes de vender
    detalles = []
    total = 0.0
    for pid, cantidad in carrito:
        prod = conn.execute("SELECT * FROM productos WHERE id = ?", (pid,)).fetchone()
        if prod is None:
            continue
        if prod["tipo"] == "producto" and prod["stock"] < cantidad:
            conn.close()
            flash(f'No hay suficiente stock de "{prod["nombre"]}" (disponible: {prod["stock"]}).', "error")
            return redirect(url_for("caja"))
        subtotal = prod["precio"] * cantidad
        total += subtotal
        detalles.append((prod, cantidad, subtotal))

    if monto_recibido < total:
        conn.close()
        flash(
            f"El efectivo recibido (${monto_recibido:.2f}) es menor que el total a cobrar (${total:.2f}). "
            "Verifica el monto entregado por el cliente.",
            "error",
        )
        return redirect(url_for("caja"))

    cambio = monto_recibido - total

    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cur = conn.execute(
        "INSERT INTO ventas (fecha, total, turno_id, monto_recibido, cambio) VALUES (?, ?, ?, ?, ?)",
        (fecha, total, turno["id"], monto_recibido, cambio),
    )
    venta_id = cur.lastrowid

    for prod, cantidad, subtotal in detalles:
        conn.execute(
            "INSERT INTO venta_detalle (venta_id, producto_id, nombre_producto, cantidad, precio_unitario, subtotal) "
            "VALUES (?, ?, ?, ?, ?, ?)",
            (venta_id, prod["id"], prod["nombre"], cantidad, prod["precio"], subtotal),
        )
        if prod["tipo"] == "producto":
            conn.execute(
                "UPDATE productos SET stock = stock - ? WHERE id = ?",
                (cantidad, prod["id"]),
            )

    conn.commit()
    conn.close()
    return redirect(url_for("recibo", venta_id=venta_id))


@app.route("/caja/recibo/<int:venta_id>")
def recibo(venta_id):
    conn = get_db()
    venta = conn.execute("SELECT * FROM ventas WHERE id = ?", (venta_id,)).fetchone()
    detalles = conn.execute(
        "SELECT * FROM venta_detalle WHERE venta_id = ?", (venta_id,)
    ).fetchall()
    conn.close()
    if venta is None:
        flash("Venta no encontrada.", "error")
        return redirect(url_for("caja"))
    return render_template("recibo.html", venta=venta, detalles=detalles)


@app.route("/caja/recibo/<int:venta_id>/cancelar", methods=["POST"])
def cancelar_venta(venta_id):
    contrasena = request.form.get("contrasena", "")
    motivo = request.form.get("motivo", "").strip()

    if not verificar_contrasena_admin(contrasena):
        flash("Contraseña de administrador incorrecta. La venta no fue cancelada.", "error")
        return redirect(url_for("recibo", venta_id=venta_id))

    if not motivo:
        flash("Debes indicar un motivo para cancelar la venta.", "error")
        return redirect(url_for("recibo", venta_id=venta_id))

    conn = get_db()
    venta = conn.execute("SELECT * FROM ventas WHERE id = ?", (venta_id,)).fetchone()
    if venta is None:
        conn.close()
        flash("Venta no encontrada.", "error")
        return redirect(url_for("caja"))

    if venta["cancelada"]:
        conn.close()
        flash("Esta venta ya estaba cancelada.", "error")
        return redirect(url_for("recibo", venta_id=venta_id))

    # Devolver al inventario el stock de los productos vendidos (los servicios no afectan stock)
    detalles = conn.execute(
        "SELECT * FROM venta_detalle WHERE venta_id = ?", (venta_id,)
    ).fetchall()
    for d in detalles:
        producto = conn.execute("SELECT * FROM productos WHERE id = ?", (d["producto_id"],)).fetchone()
        if producto and producto["tipo"] == "producto":
            conn.execute(
                "UPDATE productos SET stock = stock + ? WHERE id = ?",
                (d["cantidad"], d["producto_id"]),
            )

    conn.execute(
        "UPDATE ventas SET cancelada = 1, motivo_cancelacion = ?, fecha_cancelacion = ? WHERE id = ?",
        (motivo, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), venta_id),
    )
    conn.commit()
    conn.close()

    flash(f"La venta #{venta_id} fue cancelada y el stock se devolvió al inventario.", "success")
    return redirect(url_for("recibo", venta_id=venta_id))


# ---------- Configuración ----------

@app.route("/configuracion", methods=["GET", "POST"])
def configuracion():
    if request.method == "POST":
        actual = request.form.get("contrasena_actual", "")
        nueva = request.form.get("contrasena_nueva", "")
        confirmar = request.form.get("contrasena_confirmar", "")

        if not verificar_contrasena_admin(actual):
            flash("La contraseña actual no es correcta.", "error")
        elif len(nueva) < 4:
            flash("La nueva contraseña debe tener al menos 4 caracteres.", "error")
        elif nueva != confirmar:
            flash("La confirmación no coincide con la nueva contraseña.", "error")
        else:
            establecer_config("admin_password_hash", generate_password_hash(nueva))
            flash("La contraseña de administrador se actualizó correctamente.", "success")
            return redirect(url_for("configuracion"))

    return render_template("configuracion.html")


# ---------- Reportes ----------

@app.route("/reportes")
def reportes():
    conn = get_db()
    ventas = conn.execute(
        "SELECT * FROM ventas ORDER BY fecha DESC LIMIT 100"
    ).fetchall()
    # Los totales y estadísticas excluyen las ventas canceladas
    resumen = conn.execute(
        "SELECT COUNT(*) AS num_ventas, COALESCE(SUM(total), 0) AS total_general "
        "FROM ventas WHERE cancelada = 0"
    ).fetchone()
    mas_vendidos = conn.execute(
        "SELECT vd.nombre_producto, SUM(vd.cantidad) AS total_cantidad, SUM(vd.subtotal) AS total_ingresos "
        "FROM venta_detalle vd JOIN ventas v ON v.id = vd.venta_id "
        "WHERE v.cancelada = 0 "
        "GROUP BY vd.nombre_producto ORDER BY total_cantidad DESC LIMIT 10"
    ).fetchall()
    por_dia = conn.execute(
        "SELECT substr(fecha, 1, 10) AS dia, COUNT(*) AS num_ventas, SUM(total) AS total "
        "FROM ventas WHERE cancelada = 0 GROUP BY dia ORDER BY dia DESC LIMIT 30"
    ).fetchall()
    conn.close()
    return render_template(
        "reportes.html",
        ventas=ventas,
        resumen=resumen,
        mas_vendidos=mas_vendidos,
        por_dia=por_dia,
    )


if __name__ == "__main__":
    app.run(debug=True, port=5000)
