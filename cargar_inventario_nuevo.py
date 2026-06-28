"""
cargar_inventario_nuevo.py
--------------------------
Carga el inventario actualizado de ML Motors (repuestos FAW/J6F/TVR/TVH).
Los datos provienen del archivo inventario_organizado.xlsx.

USO EN SERVIDOR (Coolify terminal):
  python cargar_inventario_nuevo.py
"""

import sqlite3
import os

DB_PATH = os.environ.get("DB_PATH", os.path.join(os.path.dirname(os.path.abspath(__file__)), "inventario.db"))

# Formato: (codigo, nombre, tipo, precio, stock)
productos = [

    # ── CAMIÓN TVR  (VIN: LFNA4LB7XPAE24967)
    ("1109060-DD051(Q1100)", "CAMIÓN TVR · Filtro de aire (conjunto)", "producto", 62.00, 1),
    ("5302511-E98A（E100)", "CAMIÓN TVR · Cubierta esquina izquierda de cabina", "producto", 56.00, 4),
    ("5302512-E100", "CAMIÓN TVR · Cubierta esquina derecha de cabina", "producto", 56.00, 4),
    ("1105010-DD051-AAA", "CAMIÓN TVR · Filtro de diesel crudo", "producto", 36.00, 0),
    ("1001993394", "CAMIÓN TVR · Culata de motor", "producto", 1928.00, 2),
    ("GB/T297 30306/GB/T297 32209", "CAMIÓN TVR · Rodamiento delantero de dirección", "producto", 36.00, 20),
    ("3003025-X141B", "CAMIÓN TVR · Rótula delantera", "producto", 44.00, 20),
    ("1039E2-3502332", "CAMIÓN TVR · Pastilla de freno delantera", "producto", 24.00, 20),
    ("Z20140023", "CAMIÓN TVR · Filtro de combustible", "producto", 52.00, 3),
    ("1000000699", "CAMIÓN TVR · Inyector de combustible", "producto", 532.00, 4),
    ("1002335534", "CAMIÓN TVR · Junta de culata", "producto", 60.00, 20),
    ("100000648", "CAMIÓN TVR · Bomba inyectora", "producto", 1572.00, 2),
    ("1119010-DR052", "CAMIÓN TVR · Intercooler", "producto", 280.00, 4),
    ("3732015-DR052", "CAMIÓN TVR · Luz auxiliar delantera izquierda", "producto", 64.00, 2),
    ("3716015-DR052", "CAMIÓN TVR · Luz trasera izquierda (conjunto)", "producto", 32.00, 4),
    ("8202015-E100", "CAMIÓN TVR · Espejo retrovisor exterior izquierdo", "producto", 152.00, 2),
    ("3711015-DR050", "CAMIÓN TVR · Faro delantero izquierdo", "producto", 228.00, 4),
    ("1000491060A", "CAMIÓN TVR · Filtro de aceite", "producto", 32.00, 120),
    ("1301010-D9940M", "CAMIÓN TVR · Radiador", "producto", 452.00, 4),
    ("1303031-D9940M   1303032-D9940M", "CAMIÓN TVR · Mangueras de radiador (entrada y salida)", "producto", 24.00, 8),
    ("JH35011201-YHS128", "CAMIÓN TVR · Pastilla de freno trasera", "producto", 24.00, 20),
    ("3732020-DR052", "CAMIÓN TVR · Luz auxiliar delantera derecha", "producto", 64.00, 2),
    ("3716020-DR052", "CAMIÓN TVR · Luz trasera derecha (conjunto)", "producto", 32.00, 4),
    ("8202020-E100", "CAMIÓN TVR · Espejo retrovisor exterior derecho", "producto", 152.00, 2),
    ("3711020-DR050", "CAMIÓN TVR · Faro delantero derecho", "producto", 228.00, 4),
    ("1004862561", "CAMIÓN TVR · Sensor de presión de aceite", "producto", 72.00, 4),
    ("8219010-E96", "CAMIÓN TVR · Espejo de visión inferior", "producto", 28.00, 6),
    ("1002389847", "CAMIÓN TVR · Bomba de agua", "producto", 240.00, 8),
    ("ML-0003", "CAMIÓN TVR · Parabrisas", "producto", 260.00, 0),
    ("ML-0010", "CAMIÓN TVR · Correa", "producto", 20.00, 20),
    ("ML-0004", "CAMIÓN TVR · Pernos y tuercas", "producto", 16.00, 20),
    ("3539010-DR050", "CAMIÓN TVR · Válvula de freno con accesorios", "producto", 192.00, 4),
    ("1602110-D9940M", "CAMIÓN TVR · Booster del clutch", "producto", 132.00, 4),
    ("ML-0006", "CAMIÓN TVR · Disco de clutch", "producto", 180.00, 10),
    ("1602310-DD033", "CAMIÓN TVR · Cilindro maestro del clutch", "producto", 28.00, 4),
    ("ML-0007", "CAMIÓN TVR · Plato de presión del clutch", "producto", 232.00, 10),
    ("ML-0012", "CAMIÓN TVR · Dinamo", "producto", 492.00, 2),
    ("L2803016-DR061", "CAMIÓN TVR · Defensa delantera", "producto", 376.00, 1),
    ("1703320-D9069M1703220-D9069M", "CAMIÓN TVR · Cable de cambios (selector de marchas)", "producto", 48.00, 2),
    ("QT020BQ0-3003110", "CAMIÓN TVR · Conector de dirección izquierdo", "producto", 60.00, 2),
    ("QT026AQ43-3551010", "CAMIÓN TVR · Brazo ajustador delantero izquierdo", "producto", 260.00, 4),
    ("5302311-E98A-MD", "CAMIÓN TVR · Máscara del radiador", "producto", 132.00, 2),
    ("QT020BQ0-3003120", "CAMIÓN TVR · Conector de dirección derecho", "producto", 60.00, 2),
    ("QT026AQ43-3551020", "CAMIÓN TVR · Brazo ajustador delantero derecho", "producto", 260.00, 3),
    ("ML-0008", "CAMIÓN TVR · Motor de arranque", "producto", 412.00, 4),
    ("1108010-6K9", "CAMIÓN TVR · Cable del acelerador", "producto", 68.00, 6),

    # ── CAMIÓN TVH
    ("1109060-X030", "CAMIÓN TVH · Filtro de aire (conjunto)", "producto", 48.00, 6),
    ("5302511-E91", "CAMIÓN TVH · Cubierta esquina izquierda de cabina", "producto", 60.00, 4),
    ("5302512-E91", "CAMIÓN TVH · Cubierta esquina derecha de cabina", "producto", 60.00, 4),
    ("1105050-X030", "CAMIÓN TVH · Filtro de diesel crudo", "producto", 116.00, 0),
    ("1003040AX2/A", "CAMIÓN TVH · Culata de motor", "producto", 80.00, 2),
    ("7507E  7510E", "CAMIÓN TVH · Rodamiento delantero de dirección", "producto", 32.00, 20),
    ("3003025-D131", "CAMIÓN TVH · Rótula delantera", "producto", 32.00, 20),
    ("ML-0001", "CAMIÓN TVH · Pastilla de freno delantera", "producto", 12.00, 20),
    ("1117010AX21", "CAMIÓN TVH · Filtro de combustible", "producto", 20.00, 6),
    ("1112010-X162", "CAMIÓN TVH · Inyector de combustible", "producto", 76.00, 6),
    ("1003090-C102", "CAMIÓN TVH · Junta de culata", "producto", 28.00, 20),
    ("B1111010-X236", "CAMIÓN TVH · Bomba inyectora", "producto", 1540.00, 4),
    ("1119010-D539E", "CAMIÓN TVH · Intercooler", "producto", 280.00, 4),
    ("3732020-X051", "CAMIÓN TVH · Luz auxiliar delantera izquierda", "producto", 52.00, 4),
    ("3716020-D133", "CAMIÓN TVH · Luz trasera izquierda (conjunto)", "producto", 52.00, 6),
    ("8202015-E91", "CAMIÓN TVH · Espejo retrovisor exterior izquierdo", "producto", 104.00, 4),
    ("3711015-D9000E", "CAMIÓN TVH · Faro delantero izquierdo", "producto", 192.00, 4),
    ("1012010-X2", "CAMIÓN TVH · Filtro de aceite", "producto", 20.00, 160),
    ("1301010-DC99", "CAMIÓN TVH · Radiador", "producto", 276.00, 4),
    ("1303031-DC99  1303034-DC99", "CAMIÓN TVH · Mangueras de radiador (entrada y salida)", "producto", 48.00, 8),
    ("ML-0002", "CAMIÓN TVH · Pastilla de freno trasera", "producto", 12.00, 20),
    ("3732015-X051", "CAMIÓN TVH · Luz auxiliar delantera derecha", "producto", 52.00, 4),
    ("3716020-D133", "CAMIÓN TVH · Luz trasera derecha (conjunto)", "producto", 52.00, 6),
    ("8202020-E91", "CAMIÓN TVH · Espejo retrovisor exterior derecho", "producto", 104.00, 4),
    ("3711020-D9000E", "CAMIÓN TVH · Faro delantero derecho", "producto", 192.00, 4),
    ("3818020-X2", "CAMIÓN TVH · Sensor de presión de aceite", "producto", 12.00, 4),
    ("8219010-A95-C00", "CAMIÓN TVH · Espejo de visión inferior", "producto", 32.00, 6),
    ("1307010-C145", "CAMIÓN TVH · Bomba de agua", "producto", 116.00, 8),
    ("5206015-A95", "CAMIÓN TVH · Parabrisas", "producto", 180.00, 4),
    ("ML-0011", "CAMIÓN TVH · Correa", "producto", 20.00, 20),
    ("ML-0005", "CAMIÓN TVH · Pernos y tuercas", "producto", 20.00, 20),
    ("3514010-D539", "CAMIÓN TVH · Válvula de freno con accesorios", "producto", 92.00, 4),
    ("1602300-D149E", "CAMIÓN TVH · Booster del clutch", "producto", 120.00, 4),
    ("1601210-X090", "CAMIÓN TVH · Disco de clutch", "producto", 136.00, 10),
    ("1602110-D539E", "CAMIÓN TVH · Cilindro maestro del clutch", "producto", 36.00, 4),
    ("1601310-X090", "CAMIÓN TVH · Plato de presión del clutch", "producto", 164.00, 10),
    ("ML-0013", "CAMIÓN TVH · Dinamo", "producto", 300.00, 0),
    ("2803016-D9000E", "CAMIÓN TVH · Defensa delantera", "producto", 168.00, 1),
    ("1703320-D9000T", "CAMIÓN TVH · Cable de cambios (selector de marchas)", "producto", 84.00, 4),
    ("3003025-D131", "CAMIÓN TVH · Conector de dirección izquierdo", "producto", 36.00, 4),
    ("QT1061-3502205", "CAMIÓN TVH · Brazo ajustador delantero izquierdo", "producto", 60.00, 4),
    ("5302311-E91G", "CAMIÓN TVH · Máscara del radiador", "producto", 128.00, 4),
    ("3003025-D131", "CAMIÓN TVH · Conector de dirección derecho", "producto", 36.00, 2),
    ("QT1061-3502205", "CAMIÓN TVH · Brazo ajustador delantero derecho", "producto", 60.00, 4),
    ("ML-0009", "CAMIÓN TVH · Motor de arranque", "producto", 288.00, 4),
    ("1108410A-D9000E", "CAMIÓN TVH · Cable del acelerador", "producto", 20.00, 6),

    # ── CAMIÓN
    ("ML-0021", "CAMIÓN · Cadena de izaje 3 toneladas con cuerdas 3m", "producto", 200.00, 2),
    ("1109060-Q1040", "CAMIÓN · Filtro de aire", "producto", 72.00, 8),
    ("ML-0014", "CAMIÓN · Correa", "producto", 64.00, 20),
    ("3514010-6M7", "CAMIÓN · Válvula de freno con accesorios", "producto", 104.00, 6),
    ("5302511-A95-MD", "CAMIÓN · Cubierta esquina delantera izquierda", "producto", 64.00, 4),
    ("5302512-A95-MD", "CAMIÓN · Cubierta esquina delantera derecha", "producto", 64.00, 4),
    ("1602300-DR575", "CAMIÓN · Booster del clutch", "producto", 88.00, 6),
    ("C350T000-1G02-3", "CAMIÓN · Disco de clutch", "producto", 420.00, 6),
    ("1602110-D9031", "CAMIÓN · Cilindro maestro del clutch", "producto", 32.00, 10),
    ("Y350T150-10P2-3", "CAMIÓN · Plato de presión del clutch", "producto", 336.00, 6),
    ("D12F1-3701100", "CAMIÓN · Dinamo", "producto", 468.00, 0),
    ("QT026AQ43-3501572", "CAMIÓN · Zapatas de freno delanteras", "producto", 12.00, 12),
    ("2803016-6K9-MD", "CAMIÓN · Cubierta de defensa delantera", "producto", 200.00, 4),
    ("3732015-6K9", "CAMIÓN · Neblinero delantero", "producto", 52.00, 10),
    ("3732020-6K9", "CAMIÓN · Neblinero delantero", "producto", 52.00, 10),
    ("5302020-A95-MD", "CAMIÓN · Panel frontal exterior soldado", "producto", 224.00, 2),
    ("8219020-A95-C00", "CAMIÓN · Espejo de visión frontal inferior", "producto", 28.00, 6),
    ("1105050-6K9", "CAMIÓN · Filtro de combustible", "producto", 24.00, 150),
    ("ML-0015", "CAMIÓN · Inyector de combustible", "producto", 68.00, 5),
    ("1703320-D9069M1703220-D9069M", "CAMIÓN · Cable de cambios (selector de marchas)", "producto", 100.00, 10),
    ("ML-0018", "CAMIÓN · Bloque / Liner del motor", "producto", 1200.00, 1),
    ("ML-0017", "CAMIÓN · Junta de culata", "producto", 40.00, 10),
    ("ML-0016", "CAMIÓN · Bomba inyectora", "producto", 1840.00, 1),
    ("1119010-6K9", "CAMIÓN · Intercooler", "producto", 344.00, 2),
    ("QT020BQ0-3003110", "CAMIÓN · Conector de dirección izquierdo", "producto", 60.00, 4),
    ("QT026AQ43-3551010", "CAMIÓN · Brazo ajustador delantero izquierdo", "producto", 248.00, 4),
    ("3711015-6K9", "CAMIÓN · Faro combinado delantero izquierdo", "producto", 152.00, 5),
    ("8202015BA95-C00", "CAMIÓN · Espejo retrovisor izquierdo", "producto", 100.00, 6),
    ("150-1012240", "CAMIÓN · Filtro de aceite", "producto", 24.00, 150),
    ("231-1105020", "CAMIÓN · Filtro primario (diesel)", "producto", 24.00, 60),
    ("1301010-Q1034", "CAMIÓN · Radiador", "producto", 500.00, 2),
    ("5302311-A95-MD", "CAMIÓN · Máscara del radiador", "producto", 84.00, 4),
    ("1303031-D9069M  1303032-D9069M", "CAMIÓN · Mangueras de radiador (entrada y salida)", "producto", 40.00, 8),
    ("QT385D649-3551010", "CAMIÓN · Brazo ajustador trasero automático", "producto", 232.00, 2),
    ("QT310×130Z7-3502572", "CAMIÓN · Zapatas de freno traseras", "producto", 20.00, 12),
    ("QT020BQ0-3003120", "CAMIÓN · Conector de dirección derecho", "producto", 60.00, 4),
    ("3003060-A2N-C01", "CAMIÓN · Acoplamiento de barra de dirección derecho", "producto", 36.00, 5),
    ("QT026AQ43-3551020", "CAMIÓN · Brazo ajustador delantero derecho", "producto", 248.00, 10),
    ("3711020-6K9", "CAMIÓN · Faro combinado delantero derecho", "producto", 152.00, 5),
    ("8202020BA95-C00", "CAMIÓN · Espejo retrovisor derecho", "producto", 100.00, 6),
    ("3101015-8K9-C00", "CAMIÓN · Rines", "producto", 140.00, 4),
    ("QT026AQ43-3501574", "CAMIÓN · Remaches para zapatas de freno", "producto", 0.40, 20),
    ("ML-0020", "CAMIÓN · Sensor de presión de aceite", "producto", 32.00, 2),
    ("8219010-A95-C00", "CAMIÓN · Espejo de visión lateral", "producto", 28.00, 6),
    ("D21YA-3708100", "CAMIÓN · Motor de arranque", "producto", 636.00, 2),
    ("1108410-D9015E", "CAMIÓN · Cable del acelerador", "producto", 16.00, 10),
    ("ML-0019", "CAMIÓN · Bomba de agua", "producto", 220.00, 4),

    # ── FAW
    ("2803016-DD051", "FAW · Bumper grande", "producto", 180.00, 1),
    ("2803030-D9000E", "FAW · Defensa bumper metálico derecho", "producto", 65.00, 1),
    ("2803025-D9000E", "FAW · Defensa bumper metálico izquierdo", "producto", 65.00, 1),
    ("5103512-E96", "FAW · Lodera delantera derecha", "producto", 50.00, 2),
    ("5103511-E96", "FAW · Lodera delantera izquierda", "producto", 50.00, 2),
    ("5302310-E94G", "FAW · Parrilla frontal", "producto", 150.00, 1),

    # ── J6F
    ("F0155-000-SAE211107", "J6F · Filtro de diesel crudo J6F", "producto", 87.00, 24),
    ("231-1105020", "J6F · Filtro diesel motor J6F", "producto", 39.00, 52),
    ("410-200-16", "J6F · Zapatos de freno J6F", "producto", 0.00, 15),

    # ── FILTROS
    ("X251313", "FILTROS · Filtro de aceite 10K km", "producto", 24.00, 50),
    ("530-1012240", "FILTROS · Filtro de aceite de motor", "producto", 0.00, 52),
    ("812253220084-000", "FILTROS · Filtro de diesel crudo (genérico)", "producto", 0.00, 24),
    ("D25TC1-132241", "FILTROS · Filtro de motor (casa FAW)", "producto", 0.00, 75),
    ("X10010167", "FILTROS · Filtro diesel 20K km", "producto", 84.00, 25),
    ("HA110045", "FILTROS · Separador de aceite y agua", "producto", 84.00, 12),

    # ── RETROEXCAVADORA
    ("YK2036", "RETROEXCAVADORA · Filtro aire Yuchai retroexcavadora", "producto", 0.00, 22),
    ("00002036", "RETROEXCAVADORA · Filtro aire retroexcavadora 388", "producto", 0.00, 2),
]

def main():
    if not os.path.exists(DB_PATH):
        print(f"❌ No se encontró la base de datos en: {DB_PATH}")
        return

    conn = sqlite3.connect(DB_PATH)
    existing = conn.execute("SELECT COUNT(*) FROM productos").fetchone()[0]
    if existing > 0:
        resp = input(f"⚠️  Ya hay {existing} producto(s) en la BD. ¿Agregar sin borrar existentes? (s/n): ")
        if resp.strip().lower() != "s":
            print("Cancelado.")
            conn.close()
            return

    insertados = 0
    for cod, nombre, tipo, precio, stock in productos:
        conn.execute(
            "INSERT INTO productos (codigo, nombre, tipo, precio, stock) VALUES (?, ?, ?, ?, ?)",
            (cod, nombre, tipo, precio, stock)
        )
        insertados += 1

    conn.commit()
    conn.close()
    print(f"\n✅ {insertados} productos insertados correctamente.")

if __name__ == "__main__":
    main()
