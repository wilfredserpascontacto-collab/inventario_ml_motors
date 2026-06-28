DROP TABLE IF EXISTS productos;
DROP TABLE IF EXISTS ventas;
DROP TABLE IF EXISTS venta_detalle;
DROP TABLE IF EXISTS configuracion;
DROP TABLE IF EXISTS turnos_caja;

CREATE TABLE productos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    codigo TEXT,                              -- código/SKU/código de barras (opcional)
    nombre TEXT NOT NULL,
    tipo TEXT NOT NULL DEFAULT 'producto',   -- 'producto' o 'servicio'
    precio REAL NOT NULL DEFAULT 0,
    stock INTEGER NOT NULL DEFAULT 0          -- los servicios siempre tienen stock 0 / ilimitado
);

CREATE TABLE ventas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    fecha TEXT NOT NULL,
    total REAL NOT NULL DEFAULT 0,
    cancelada INTEGER NOT NULL DEFAULT 0,
    motivo_cancelacion TEXT,
    fecha_cancelacion TEXT,
    turno_id INTEGER REFERENCES turnos_caja (id),
    monto_recibido REAL,
    cambio REAL
);

-- Turnos de caja: registran la apertura y el cierre (corte) de caja con el
-- monto inicial, lo vendido durante el turno y el conteo final de efectivo.
CREATE TABLE turnos_caja (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    fecha_apertura TEXT NOT NULL,
    monto_inicial REAL NOT NULL DEFAULT 0,
    notas_apertura TEXT,
    fecha_cierre TEXT,
    monto_esperado REAL,
    monto_contado REAL,
    diferencia REAL,
    notas_cierre TEXT,
    cerrado INTEGER NOT NULL DEFAULT 0
);

-- Tabla de configuración general (clave/valor), por ejemplo la contraseña de administrador
CREATE TABLE configuracion (
    clave TEXT PRIMARY KEY,
    valor TEXT
);

-- Historial de cambios en productos (precio, stock, nombre, código, tipo)
CREATE TABLE IF NOT EXISTS historial_productos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    producto_id INTEGER NOT NULL,
    nombre_producto TEXT NOT NULL,
    campo TEXT NOT NULL,
    valor_anterior TEXT,
    valor_nuevo TEXT,
    fecha TEXT NOT NULL,
    FOREIGN KEY (producto_id) REFERENCES productos (id)
);

CREATE TABLE venta_detalle (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    venta_id INTEGER NOT NULL,
    producto_id INTEGER NOT NULL,
    nombre_producto TEXT NOT NULL,
    cantidad INTEGER NOT NULL,
    precio_unitario REAL NOT NULL,
    subtotal REAL NOT NULL,
    FOREIGN KEY (venta_id) REFERENCES ventas (id),
    FOREIGN KEY (producto_id) REFERENCES productos (id)
);
