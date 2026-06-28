# -*- coding: utf-8 -*-
"""Genera un PDF con la descripción y el avance del proyecto Inventario y Caja."""
import os
from fpdf import FPDF

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SALIDA = os.path.join(BASE_DIR, "Inventario_y_Caja - Resumen del proyecto.pdf")

AZUL = (30, 60, 114)
GRIS = (90, 90, 90)
VERDE = (40, 130, 80)


class PDF(FPDF):
    def header(self):
        if self.page_no() == 1:
            return
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(*GRIS)
        self.cell(0, 8, "Inventario y Caja - Resumen del proyecto", align="L")
        self.cell(0, 8, f"Página {self.page_no()}", align="R")
        self.ln(12)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(*GRIS)
        self.cell(0, 10, "Documento generado con Claude Code - 2026-06-07", align="C")


pdf = PDF()
pdf.set_auto_page_break(auto=True, margin=20)
pdf.add_page()

# ---------- Portada ----------
pdf.set_font("Helvetica", "B", 26)
pdf.set_text_color(*AZUL)
pdf.ln(50)
pdf.cell(0, 14, "Sistema de Inventario y Caja", align="C", new_x="LMARGIN", new_y="NEXT")
pdf.set_font("Helvetica", "", 16)
pdf.set_text_color(*GRIS)
pdf.cell(0, 10, "Resumen del proyecto y avances realizados", align="C", new_x="LMARGIN", new_y="NEXT")
pdf.ln(10)
pdf.set_font("Helvetica", "", 12)
pdf.cell(0, 8, "Aplicación web local (Python / Flask) para catálogo de productos", align="C", new_x="LMARGIN", new_y="NEXT")
pdf.cell(0, 8, "y punto de venta (caja), hecha a la medida del negocio.", align="C", new_x="LMARGIN", new_y="NEXT")
pdf.ln(20)
pdf.set_font("Helvetica", "I", 11)
pdf.cell(0, 8, "Fecha del documento: 7 de junio de 2026", align="C", new_x="LMARGIN", new_y="NEXT")

pdf.add_page()


def titulo(texto):
    pdf.set_font("Helvetica", "B", 15)
    pdf.set_text_color(*AZUL)
    pdf.ln(4)
    pdf.cell(0, 10, texto, new_x="LMARGIN", new_y="NEXT")
    pdf.set_draw_color(*AZUL)
    pdf.set_line_width(0.6)
    y = pdf.get_y()
    pdf.line(pdf.l_margin, y, pdf.w - pdf.r_margin, y)
    pdf.ln(4)
    pdf.set_text_color(0, 0, 0)


def subtitulo(texto):
    pdf.set_font("Helvetica", "B", 12)
    pdf.set_text_color(*VERDE)
    pdf.ln(2)
    pdf.cell(0, 8, texto, new_x="LMARGIN", new_y="NEXT")
    pdf.set_text_color(0, 0, 0)


def parrafo(texto):
    pdf.set_font("Helvetica", "", 11)
    pdf.set_text_color(0, 0, 0)
    pdf.multi_cell(0, 6.5, texto)
    pdf.ln(1)


def viñeta(texto):
    pdf.set_font("Helvetica", "", 11)
    pdf.set_text_color(0, 0, 0)
    pdf.set_x(pdf.l_margin + 4)
    pdf.multi_cell(0, 6.2, f"-  {texto}")


# ---------- 1. Qué es el sistema ----------
titulo("1. ¿Qué es este sistema?")
parrafo(
    "Es una aplicacion web que corre de forma local (en la propia computadora del "
    "negocio, sin depender de internet) y que permite administrar el inventario de "
    "productos y servicios, asi como realizar ventas desde una caja registradora "
    "digital (punto de venta). Fue disenada a la medida, pensando en el flujo de "
    "trabajo real del negocio: busqueda rapida de productos, control de stock, "
    "cortes de caja, cancelacion de ventas con autorizacion, y reportes."
)
parrafo(
    "Tecnologias utilizadas: Python (Flask) para la logica del programa, "
    "SQLite como base de datos local, y Bootstrap para una interfaz sencilla "
    "y agradable que funciona en cualquier navegador (Chrome, Edge, etc.)."
)

# ---------- 2. Funciones completadas ----------
titulo("2. Funciones completadas hasta el momento")

subtitulo("2.1 Catalogo de productos y servicios")
viñeta("Alta, edicion y eliminacion de productos y servicios (CRUD completo).")
viñeta("Cada producto puede tener codigo/SKU, nombre, tipo (producto o servicio), precio y stock.")
viñeta("Los servicios no afectan el inventario (no controlan stock).")
viñeta("Indicadores visuales de stock bajo o agotado.")

subtitulo("2.2 Buscador inteligente de productos")
viñeta("Busqueda por palabras (no es necesario escribir el nombre completo ni en orden exacto).")
viñeta("Sugerencias en vivo mientras se escribe, mostrando precio y disponibilidad.")
viñeta(
    "Ejemplo: buscar 'filtro camion 5080' encuentra "
    "'Filtro de combustible para camion 5080 KXY' aunque el orden de las palabras sea distinto."
)

subtitulo("2.3 Punto de venta (Caja)")
viñeta("Interfaz tipo carrito: se buscan productos, se agregan, se ajustan cantidades y se cobra.")
viñeta("Calculo automatico del total de la venta.")
viñeta("Validacion de stock disponible antes de completar la venta.")
viñeta("Generacion automatica de un recibo de venta imprimible.")

subtitulo("2.4 Efectivo recibido y cambio (vuelto)")
viñeta("Campo para indicar cuanto efectivo entrega el cliente.")
viñeta("Calculo automatico y en tiempo real del cambio a entregar.")
viñeta("El sistema bloquea el cobro si el cliente paga menos del total (evita errores de caja).")
viñeta("El recibo de venta muestra el total, el efectivo recibido y el cambio entregado.")

subtitulo("2.5 Cancelacion / anulacion de ventas (con autorizacion)")
viñeta("Las ventas se pueden cancelar solo con la contrasena de administrador.")
viñeta("Se debe indicar un motivo de cancelacion, que queda registrado junto con la fecha y hora.")
viñeta("Al cancelar, el stock de los productos se devuelve automaticamente al inventario (los servicios no se ven afectados).")
viñeta("Las ventas canceladas se excluyen de los totales y estadisticas de los reportes, pero quedan visibles en el historial, marcadas claramente, para mantener un registro completo.")

subtitulo("2.6 Apertura y cierre de caja (cortes de caja)")
viñeta("Antes de vender, se debe 'abrir caja' indicando el fondo inicial (efectivo con el que se inicia el turno).")
viñeta("El sistema no permite registrar ventas si la caja esta cerrada.")
viñeta("Al cerrar caja, se genera un resumen automatico: numero de ventas, total vendido y efectivo esperado (fondo inicial + ventas).")
viñeta("Se solicita contar el efectivo fisico real, y el sistema calcula automaticamente la diferencia (sobrante o faltante).")
viñeta("Historial de todos los cortes de caja realizados, con sus diferencias resaltadas (exacto, sobrante o faltante).")

subtitulo("2.7 Seguridad y permisos de administrador")
viñeta("Contrasena de administrador configurable, almacenada de forma segura (con cifrado/hash, no en texto plano).")
viñeta("La seccion de Productos es exclusiva del administrador: se pide la contrasena para entrar.")
viñeta("Al editar o eliminar un producto se vuelve a pedir la contrasena, como confirmacion adicional.")
viñeta("Pagina de Configuracion para cambiar la contrasena de administrador cuando se desee.")

subtitulo("2.8 Reportes y estadisticas")
viñeta("Resumen de ventas totales e ingresos totales (sin contar ventas canceladas).")
viñeta("Productos y servicios mas vendidos, con cantidades e ingresos generados.")
viñeta("Ventas por dia, para ver tendencias.")
viñeta("Historial de ventas (ultimas 100), con estado (valida o cancelada) y acceso al recibo de cada una.")

# ---------- 3. Lo que falta / próximos pasos ----------
pdf.add_page()
titulo("3. Posibles mejoras futuras (a discutir)")
parrafo(
    "Durante el desarrollo se identificaron varias funciones adicionales que se "
    "podrian agregar mas adelante, segun las necesidades del negocio:"
)
viñeta("Metodos de pago (efectivo, tarjeta, transferencia) y registro de cada uno.")
viñeta("Descuentos y promociones en las ventas.")
viñeta("Conexion con impresora de tickets (se investigo el modelo Epson TM-T20III como opcion recomendada).")
viñeta("Categorias de productos para organizar mejor el catalogo.")
viñeta("Alertas automaticas de stock bajo.")
viñeta("Registro de proveedores y compras.")
viñeta("Historial de movimientos de inventario (entradas y salidas).")
viñeta("Registro de clientes y cuentas por cobrar (fiados).")
viñeta("Calculo de ganancias (costo vs. precio de venta).")
viñeta("Exportacion de reportes a Excel o PDF, y graficas visuales.")
viñeta("Soporte para lector de codigos de barras.")
viñeta("Acceso desde varias computadoras en red local, o desde la nube (para varias sucursales).")
viñeta("Cuentas de usuario por cajero, con permisos diferenciados.")

# ---------- 4. Posibilidades a futuro ----------
titulo("4. Crecimiento a futuro: red local y nube")
parrafo(
    "Actualmente el sistema corre en una sola computadora, con su propia base de "
    "datos local. Si en el futuro se requiere que varias cajas o sucursales usen "
    "el mismo sistema al mismo tiempo, existen dos caminos:"
)
subtitulo("Opcion A: Red local (LAN)")
parrafo(
    "El programa corre en una computadora 'servidor' dentro del negocio, y las "
    "demas computadoras se conectan a traves de la red local (sin necesidad de "
    "internet). Es gratis, rapido y mantiene los datos dentro del negocio. "
    "Ideal si todo opera en un mismo local."
)
subtitulo("Opcion B: Nube (acceso remoto / multiples sucursales)")
parrafo(
    "El sistema se aloja en un servidor en internet, permitiendo el acceso desde "
    "cualquier lugar con conexion (incluyendo celulares). Esto requeriria cambios "
    "importantes: una base de datos mas robusta (en lugar de SQLite), cuentas de "
    "usuario por cajero, refuerzos de seguridad (HTTPS, respaldos automaticos) y "
    "un costo mensual de hospedaje (aproximadamente entre 5 y 25 dolares al mes)."
)

# ---------- 5. Cierre ----------
titulo("5. Estado actual")
parrafo(
    "El sistema se encuentra funcional y en uso, con todas las funciones descritas "
    "en la seccion 2 implementadas y probadas de extremo a extremo: creacion de "
    "ventas, devolucion de stock al cancelar, calculo de cambio, cortes de caja "
    "con deteccion de diferencias, control de acceso por contrasena, y reportes "
    "que excluyen automaticamente las ventas canceladas."
)
parrafo(
    "Se cuenta ademas con un acceso directo en el escritorio para iniciar el "
    "programa facilmente, sin necesidad de conocimientos tecnicos."
)

pdf.output(SALIDA)
print(f"PDF generado en: {SALIDA}")
