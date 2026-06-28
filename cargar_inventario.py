"""
cargar_inventario.py
--------------------
Inserta el inventario de bodega en la base de datos del sistema Caja (inventario.db).
Los productos se organizan con prefijo de categoría para que aparezcan agrupados.

USO:
  1. Copia este archivo a la carpeta del proyecto (inventario_caja/)
  2. Abre CMD en esa carpeta
  3. Ejecuta: python cargar_inventario.py
"""

import sqlite3
import os

# ── Ruta de la base de datos ────────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "inventario.db")

# ── Productos organizados por categoría ─────────────────────────────────────
# Formato: (codigo, nombre, tipo, precio, stock)
# El prefijo [CATEGORÍA] agrupa los productos al ordenar alfabéticamente.

productos = [

    # ── BOMBAS ──────────────────────────────────────────────────────────────
    (None,              "BOMBAS · Auxiliar de frenos VR (par)",                 "producto", 0, 8),
    (None,              "BOMBAS · Auxiliar de frenos VR (individual)",           "producto", 0, 1),
    (None,              "BOMBAS · Clutch camiones",                              "producto", 0, 6),
    (None,              "BOMBAS · Clutch FAW principal",                         "producto", 0, 3),
    (None,              "BOMBAS · Clutch general",                               "producto", 0, 6),
    (None,              "BOMBAS · Freno principal",                              "producto", 0, 3),
    (None,              "BOMBAS · Freno retroexcavadora principal",              "producto", 0, 3),
    (None,              "BOMBAS · Freno retroexcavadora SD 25-30",              "producto", 0, 1),
    ("1002389847",      "BOMBAS · Agua Weichai",                                "producto", 0, 6),
    ("D0305-130720B",   "BOMBAS · Agua Yuchai",                                 "producto", 0, 4),
    (None,              "BOMBAS · Agua retroexcavadora",                        "producto", 0, 1),
    (None,              "BOMBAS · Hidráulica principal retroexcavadora",        "producto", 0, 1),
    (None,              "BOMBAS · Hidráulica flexible minicargador (completa)", "producto", 0, 1),
    (None,              "BOMBAS · Inyección diesel camiones",                   "producto", 0, 1),
    (None,              "BOMBAS · Inyección gasolina Yuchai",                   "producto", 0, 1),
    (None,              "BOMBAS · Inyección Kangda",                            "producto", 0, 1),
    (None,              "BOMBAS · Transmisión manual",                          "producto", 0, 1),
    (None,              "BOMBAS · Transferencia manual",                        "producto", 0, 1),

    # ── BUJES RETROEXCAVADORA ────────────────────────────────────────────────
    (None, "BUJES RETRO · B 46mm x 53mm",      "producto", 0, 2),
    (None, "BUJES RETRO · B 57mm x 44mm",      "producto", 0, 4),
    (None, "BUJES RETRO · B 38mm x 38mm",      "producto", 0, 8),
    (None, "BUJES RETRO · B 45mm x 34mm",      "producto", 0, 16),
    (None, "BUJES RETRO · B 62mm x 57mm",      "producto", 0, 12),
    (None, "BUJES RETRO · B 2p x 45mm",        "producto", 0, 2),
    (None, "BUJES RETRO · B 1-3/8p x 35mm",   "producto", 0, 2),
    (None, "BUJES RETRO · B 1-7/8p x 40mm",   "producto", 0, 1),
    # Retroexcavadora 388
    (None, "BUJES RETRO 388 · B 2-3/4p x 49mm", "producto", 0, 6),
    (None, "BUJES RETRO 388 · B 4p x 50mm",      "producto", 0, 4),
    (None, "BUJES RETRO 388 · B 3-1/8p x 61mm",  "producto", 0, 1),
    (None, "BUJES RETRO 388 · B 2-1/2p x 62mm",  "producto", 0, 2),
    (None, "BUJES RETRO 388 · B 4-1/4p x 45mm",  "producto", 0, 6),
    (None, "BUJES RETRO 388 · B 2-1/2p x 52mm",  "producto", 0, 1),
    (None, "BUJES RETRO 388 · B 3p x 52mm",       "producto", 0, 1),
    (None, "BUJES RETRO 388 · B 3-1/4p x 60mm",  "producto", 0, 2),
    (None, "BUJES RETRO 388 · B 2-3/4p x 65mm",  "producto", 0, 2),
    (None, "BUJES RETRO 388 · B 4p x 45mm",       "producto", 0, 2),
    (None, "BUJES RETRO 388 · B 2-3/4p x 55mm",  "producto", 0, 2),
    (None, "BUJES RETRO 388 · B 4-1/8p x 45mm",  "producto", 0, 2),

    # ── CARROCERÍA FAW ──────────────────────────────────────────────────────
    (None,                  "CARROCERÍA FAW · Lodera delantera izquierda",   "producto", 0, 1),
    (None,                  "CARROCERÍA FAW · Lodera delantera derecha",     "producto", 0, 1),
    (None,                  "CARROCERÍA FAW · Lodera trasera izquierda",     "producto", 0, 1),
    (None,                  "CARROCERÍA FAW · Lodera trasera derecha",       "producto", 0, 1),
    (None,                  "CARROCERÍA FAW · Grada delantera izquierda",    "producto", 0, 1),
    (None,                  "CARROCERÍA FAW · Grada delantera derecha",      "producto", 0, 1),
    (None,                  "CARROCERÍA FAW · Grada trasera izquierda",      "producto", 0, 1),
    (None,                  "CARROCERÍA FAW · Grada trasera derecha",        "producto", 0, 2),
    (None,                  "CARROCERÍA FAW · Lodera de puerta frontal",     "producto", 0, 6),
    (None,                  "CARROCERÍA FAW · Bumper metálico (2 piezas)",   "producto", 0, 1),
    ("21E6A",               "CARROCERÍA FAW · Parrilla frontal verde",       "producto", 0, 1),
    ("21E6A",               "CARROCERÍA FAW · Parrilla frontal blanca",      "producto", 0, 1),
    (None,                  "CARROCERÍA FAW · Bumper verde",                 "producto", 0, 1),
    (None,                  "CARROCERÍA FAW · Parrilla front",               "producto", 0, 1),
    (None,                  "CARROCERÍA FAW · Estribo de camión",            "producto", 0, 4),
    (None,                  "CARROCERÍA FAW · Bumper defensa frontal",       "producto", 0, 3),

    # ── CILINDROS HIDRÁULICOS ────────────────────────────────────────────────
    (None, "CILINDROS HIDRÁULICOS · C 41-3/8mm",          "producto", 0, 1),
    (None, "CILINDROS HIDRÁULICOS · C 40-5/8mm",          "producto", 0, 2),
    (None, "CILINDROS HIDRÁULICOS · Estabilizadores",     "producto", 0, 8),
    (None, "CILINDROS HIDRÁULICOS · Cucharón",            "producto", 0, 2),
    (None, "CILINDROS HIDRÁULICOS · Transmisión",         "producto", 0, 1),
    (None, "CILINDROS HIDRÁULICOS · Estabilizadores (2)", "producto", 0, 2),
    (None, "CILINDROS HIDRÁULICOS · Cucharón frontal",    "producto", 0, 2),
    (None, "CILINDROS HIDRÁULICOS · Secon Boon",          "producto", 0, 1),
    (None, "CILINDROS HIDRÁULICOS · Brazo de cucharón frontal", "producto", 0, 2),
    (None, "CILINDROS HIDRÁULICOS · Boon",                "producto", 0, 1),
    (None, "CILINDROS HIDRÁULICOS · Swing",               "producto", 0, 8),
    (None, "CILINDROS HIDRÁULICOS · Garra",               "producto", 0, 1),

    # ── CLUTCH / EMBRAGUE ────────────────────────────────────────────────────
    ("1001669266",      "CLUTCH · Prensa Weichai",     "producto", 0, 10),
    ("241110-245901",   "CLUTCH · Disco Weichai",      "producto", 0, 10),
    ("C325T000-0G01-3", "CLUTCH · Disco Yuchai",       "producto", 0, 6),
    ("Y325T150-10P1-3", "CLUTCH · Prensa Yuchai",      "producto", 0, 6),
    ("1601310-x090*A",  "CLUTCH · Prensa FAW",         "producto", 0, 10),
    ("1601210-X090*A",  "CLUTCH · Disco FAW",          "producto", 0, 10),

    # ── ELÉCTRICO / ARRANQUE / ALTERNADOR ───────────────────────────────────
    ("443FE200309",     "ELÉCTRICO · Motor de arranque Yuchai",                    "producto", 0, 1),
    (None,              "ELÉCTRICO · Motor de arranque Yuchai retro 24V",          "producto", 0, 1),
    (None,              "ELÉCTRICO · Motor de arranque FAW",                       "producto", 0, 4),
    ("A1H4-5D1",        "ELÉCTRICO · Motor de arranque Weichai",                   "producto", 0, 1),
    (None,              "ELÉCTRICO · Motor de arranque (general)",                 "producto", 0, 4),
    ("D5K52-3707100B",  "ELÉCTRICO · Motor de arranque Yuchai (repuesto)",        "producto", 0, 1),
    ("D12Y1-3701100",   "ELÉCTRICO · Alternador Yuchai",                          "producto", 0, 1),
    ("D36Y5-3724270",   "ELÉCTRICO · Arnés de alternador Yuchai",                "producto", 0, 1),
    (None,              "ELÉCTRICO · Electroválvula",                             "producto", 0, 2),
    (None,              "ELÉCTRICO · Sensores (general)",                         "producto", 0, 4),
    (None,              "ELÉCTRICO · Frenos de compresión electrónicos",          "producto", 0, 4),
    (None,              "ELÉCTRICO · Switch retroexcavadora",                     "producto", 0, 2),
    (None,              "ELÉCTRICO · Apagador retroexcavadora",                   "producto", 0, 1),
    (None,              "ELÉCTRICO · Cable apagador",                             "producto", 0, 2),
    (None,              "ELÉCTRICO · Cable acelerador",                           "producto", 0, 1),
    (None,              "ELÉCTRICO · Luz piloto minicargador",                    "producto", 0, 2),
    (None,              "ELÉCTRICO · Luz de trabajo",                             "producto", 0, 3),

    # ── FILTROS DE ACEITE ────────────────────────────────────────────────────
    ("D25TC1-132241",       "FILTRO ACEITE · Motor FAW (casa)",               "producto", 0, 75),
    ("D25TC1-13224-1 SAB",  "FILTRO ACEITE · Motor 10,000 km",               "producto", 0, 50),
    ("D20TCID-110082",      "FILTRO ACEITE · Diesel 20,000 km",              "producto", 0, 25),
    ("530-1012240",         "FILTRO ACEITE · Motor (general)",                "producto", 0, 52),
    ("1012010-X2",          "FILTRO ACEITE · FAW",                           "producto", 0, 167),
    ("150-1012240",         "FILTRO ACEITE · Yuchai",                        "producto", 0, 125),
    ("186-1012240",         "FILTRO ACEITE · Yuchai 20,000 km",              "producto", 0, 20),
    ("YJX-0818-IN",         "FILTRO ACEITE · Retroexcavadora Yuchai",        "producto", 0, 14),
    ("1012160TA",           "FILTRO ACEITE · ISUZU",                         "producto", 0, 59),
    ("1000491060A",         "FILTRO ACEITE · Weichai VR",                    "producto", 0, 65),
    ("JX0810Y",             "FILTRO ACEITE · Kafu Long",                     "producto", 0, 50),
    ("JX0810Y",             "FILTRO ACEITE · Biaumeng",                      "producto", 0, 9),
    ("JX0810D2",            "FILTRO ACEITE · Wecan",                         "producto", 0, 61),
    ("JX0814D",             "FILTRO ACEITE · Yangdong",                      "producto", 0, 21),
    ("JX1010",              "FILTRO ACEITE · Concretera",                    "producto", 0, 1),
    ("CX 0713",             "FILTRO ACEITE · Motor diesel 10,000 km FAW",   "producto", 0, 18),
    ("HA11383",             "FILTRO ACEITE · Yunnei",                        "producto", 0, 2),

    # ── FILTROS DE AIRE ──────────────────────────────────────────────────────
    ("1109060DD051AA",  "FILTRO AIRE · Yunei (FAW) frenos de compresión",   "producto", 0, 4),
    ("1109060-Q1040",   "FILTRO AIRE · Yuchai grande",                      "producto", 0, 2),
    ("-YK2036",         "FILTRO AIRE · Retroexcavadora Yuchai 388 (ext)",   "producto", 0, 22),
    ("00002036",        "FILTRO AIRE · Retroexcavadora Yuchai 388 (int)",   "producto", 0, 2),
    ("107999015",       "FILTRO AIRE · Motor Huanghai",                     "producto", 0, 10),
    (None,              "FILTRO AIRE · Camiones (general)",                  "producto", 0, 24),
    (None,              "FILTRO AIRE · SD 25-30",                           "producto", 0, 39),
    (None,              "FILTRO AIRE · Concretera trompo",                  "producto", 0, 3),
    (None,              "FILTRO AIRE · Tang Niu concretera",                "producto", 0, 2),
    (None,              "FILTRO AIRE · Mini cargador",                      "producto", 0, 3),
    (None,              "FILTRO AIRE · Super grande",                       "producto", 0, 6),

    # ── FILTROS DE COMBUSTIBLE / DIESEL ──────────────────────────────────────
    (None,                  "FILTRO DIESEL · FAW (casa)",                        "producto", 0, 12),
    ("F0155-000 SAE211107", "FILTRO DIESEL · Crudo J6F 10T",                    "producto", 0, 24),
    ("231-1105020",         "FILTRO DIESEL · Motor J6F",                        "producto", 0, 52),
    ("812253220084-000",    "FILTRO DIESEL · Crudo (general)",                  "producto", 0, 24),
    ("231-1105020",         "FILTRO DIESEL · Combustible (general)",            "producto", 0, 119),
    ("1117012AX21",         "FILTRO DIESEL · FAW 4T a 6T",                     "producto", 0, 127),
    ("1105050-6K9",         "FILTRO DIESEL · Combustible Weichai VR",          "producto", 0, 147),
    ("107003005",           "FILTRO DIESEL · Combustible Huanghai Pick Up",    "producto", 0, 30),
    ("1105010-DD05-AAA",    "FILTRO DIESEL · Combustible FAW",                 "producto", 0, 6),
    ("CX0708",              "FILTRO DIESEL · Wecan",                            "producto", 0, 91),
    ("Z20140023",           "FILTRO DIESEL · Weichai VR",                      "producto", 0, 37),
    ("CX0710B",             "FILTRO DIESEL · Motor volqueta",                  "producto", 0, 22),
    (None,                  "FILTRO DIESEL · Combustible bolqueta",             "producto", 0, 22),
    ("YN33CRD-11501-1",     "FILTRO DIESEL · Separador agua/aceite",           "producto", 0, 12),
    ("WG972555131",         "FILTRO DIESEL · Combustible y separador de agua", "producto", 0, 5),
    ("WU-100180-J",         "FILTRO DIESEL · Tanque de combustible",           "producto", 0, 2),
    (None,                  "FILTRO DIESEL · Separador agua Mannfilter",       "producto", 0, 4),
    ("B7604-1105240",       "FILTRO DIESEL · Núcleo Yuchai",                   "producto", 0, 21),
    ("B76041105240",        "FILTRO DIESEL · Pre-combustible Yuchai",          "producto", 0, 4),
    (None,                  "FILTRO DIESEL · Tanque hidráulico retroexcavadora","producto", 0, 7),

    # ── FRENOS ──────────────────────────────────────────────────────────────
    ("410-200-16",  "FRENOS · Zapata J6F 10T",                       "producto", 97,  15),
    (None,          "FRENOS · Zapata FAW (zapatas)",                  "producto", 97,   8),
    (None,          "FRENOS · Zapata VR delantera (fricciones)",      "producto", 0,    8),
    (None,          "FRENOS · Zapata VR trasera (fricciones)",        "producto", 0,   20),
    (None,          "FRENOS · Zapata J6F trasera (fricciones)",       "producto", 0,   15),
    (None,          "FRENOS · Tambor VR",                             "producto", 0,   10),
    (None,          "FRENOS · Tambor VR (J6F)",                      "producto", 0,   12),
    (None,          "FRENOS · Remache para zapatas (bolsa)",          "producto", 0,    4),
    (None,          "FRENOS · Chancleta de frenos de aire camiones",  "producto", 0,    5),
    (None,          "FRENOS · Servofreno",                            "producto", 0,    1),
    (None,          "FRENOS · Tubo retroexcavadora",                  "producto", 0,    5),
    (None,          "FRENOS · Hidrobac con bomba",                    "producto", 0,    1),
    (None,          "FRENOS · Válvula de prioridad",                  "producto", 0,    2),

    # ── INYECTORES ───────────────────────────────────────────────────────────
    ("D0800-1112100B-005",  "INYECTOR · Yuchai",               "producto", 0, 5),
    ("B938",                "INYECTOR · Caja Yuchai",           "producto", 0, 6),
    ("A3H1-2A",             "INYECTOR · Weichai",               "producto", 0, 4),
    (None,                  "INYECTOR · Weichai electrónico",   "producto", 0, 0),
    (None,                  "INYECTOR · Herramienta calibrador","producto", 0, 1),
    (None,                  "INYECTOR · Bomba de inyección",    "producto", 0, 1),

    # ── INTER COOLER ─────────────────────────────────────────────────────────
    ("1119010-5539E",   "INTER COOLER · FAW (mod. 5539E)", "producto", 0, 2),
    ("1119010-DR052",   "INTER COOLER · FAW (mod. DR052)", "producto", 0, 3),
    ("1119010-6K9",     "INTER COOLER · FAW (mod. 6K9)",   "producto", 0, 2),

    # ── LUCES Y FAROS ────────────────────────────────────────────────────────
    ("LLB78",           "LUCES · Traseras camiones 4T y 4x4",                  "producto", 0, 16),
    ("LHB91",           "LUCES · Faro delantero izquierdo 5T",                 "producto", 0, 4),
    ("LHB91",           "LUCES · Faro delantero derecho 5T",                   "producto", 0, 5),
    (None,              "LUCES · Luz trasera derecha Tiger VR",                "producto", 0, 7),
    (None,              "LUCES · Luz trasera izquierda Tiger VR",              "producto", 0, 8),
    ("3732015-6K9AA",   "LUCES · Farol antiniebla izquierdo J6F",             "producto", 0, 2),
    ("3732015-6K9AA",   "LUCES · Farol antiniebla derecho J6F",               "producto", 0, 2),
    (None,              "LUCES · Antiniebla izquierda VR",                    "producto", 0, 4),
    (None,              "LUCES · Antiniebla derecha VR",                      "producto", 0, 2),
    ("LLB78",           "LUCES · Faro derecho VR y 4T",                       "producto", 0, 3),
    ("LLB78",           "LUCES · Faro izquierdo VR y 4T",                     "producto", 0, 4),
    ("LB43",            "LUCES · Farol izquierdo 4x4",                        "producto", 0, 2),
    ("LB43",            "LUCES · Farol derecho 4x4",                          "producto", 0, 3),
    (None,              "LUCES · Antiniebla derecha camión 6T",               "producto", 0, 4),
    (None,              "LUCES · Antiniebla izquierda camión 6T",             "producto", 0, 4),
    (None,              "LUCES · Antiniebla y vía FAW derecha 10T",           "producto", 0, 8),
    (None,              "LUCES · Antiniebla y vía FAW izquierda 10T",         "producto", 0, 8),
    (None,              "LUCES · Espejo minicargador",                        "producto", 0, 2),

    # ── MANGUERAS Y TUBOS ────────────────────────────────────────────────────
    (None,          "MANGUERAS · Hidráulicas para concreteras",    "producto", 0, 8),
    ("SD30-25",     "MANGUERAS · Hidráulica SD 30-25",             "producto", 0, 1),
    (None,          "MANGUERAS · Tubos líquido hidráulico",        "producto", 0, 4),

    # ── MOTOR Y MECÁNICA MAYOR ───────────────────────────────────────────────
    ("1003020AX2",  "MOTOR · Culata de motor",                    "producto", 0, 2),
    (None,          "MOTOR · Juego de empaque de motor",          "producto", 0, 2),
    (None,          "MOTOR · Tapa de puntería Yunnei",            "producto", 0, 1),
    ("313942R92",   "MOTOR · Termostato tractor internacional",   "producto", 0, 1),
    (None,          "MOTOR · Pedal acelerador retroexcavadora",   "producto", 0, 1),
    (None,          "MOTOR · Pedal acelerador retroexcavadora (2)","producto", 0, 1),

    # ── PINES RETROEXCAVADORA ────────────────────────────────────────────────
    (None, "PINES RETRO · Doble 4p x 27mm",     "producto", 0, 1),
    (None, "PINES RETRO · P 3p x 35mm",         "producto", 0, 2),
    (None, "PINES RETRO · P 3-1/8p x 35mm",    "producto", 0, 1),
    (None, "PINES RETRO · P 3-3/4p x 35mm",    "producto", 0, 1),
    (None, "PINES RETRO · P 3-7/8p x 31mm",    "producto", 0, 1),
    (None, "PINES RETRO · P 3-7/8p x 35mm",    "producto", 0, 1),
    (None, "PINES RETRO · P 4-1/4p x 40mm",    "producto", 0, 2),
    (None, "PINES RETRO · P 4-1/4p x 45mm",    "producto", 0, 1),
    (None, "PINES RETRO · P 4-5/8p x 45mm",    "producto", 0, 2),
    (None, "PINES RETRO · P 4-3/4p x 37mm",    "producto", 0, 2),
    (None, "PINES RETRO · P 4-3/4p x 40mm",    "producto", 0, 2),
    (None, "PINES RETRO · P 4-7/8p x 45mm",    "producto", 0, 1),
    (None, "PINES RETRO · P 5p x 40mm",         "producto", 0, 1),
    (None, "PINES RETRO · P 5p x 45mm",         "producto", 0, 1),
    (None, "PINES RETRO · P 5-1/4p x 45mm",    "producto", 0, 1),
    (None, "PINES RETRO · P 5-7/8p x 40mm",    "producto", 0, 2),
    (None, "PINES RETRO · P 5-7/8p x 45mm",    "producto", 0, 3),
    (None, "PINES RETRO · P 6p x 40mm",         "producto", 0, 1),
    (None, "PINES RETRO · P 6-1/8p x 37mm",    "producto", 0, 3),
    (None, "PINES RETRO · P 6-1/8p x 40mm",    "producto", 0, 2),
    (None, "PINES RETRO · P 6-1/8p x 45mm",    "producto", 0, 2),
    (None, "PINES RETRO · P 6-1/4p x 47mm",    "producto", 0, 1),
    (None, "PINES RETRO · P 6-2/2p x 37mm",    "producto", 0, 11),
    (None, "PINES RETRO · P 6-3/8p x 47mm",    "producto", 0, 1),
    (None, "PINES RETRO · P 6-5/8p x 40mm",    "producto", 0, 1),
    (None, "PINES RETRO · P 6-3/4p x 27mm",    "producto", 0, 1),
    (None, "PINES RETRO · P 6-3/4p x 37mm",    "producto", 0, 6),
    (None, "PINES RETRO · P 7p x 37mm",         "producto", 0, 1),
    (None, "PINES RETRO · P 7-1/8p x 45mm",    "producto", 0, 4),
    (None, "PINES RETRO · P 7-1/4p x 49mm",    "producto", 0, 1),
    (None, "PINES RETRO · P 7-3/8p x 50mm",    "producto", 0, 1),
    (None, "PINES RETRO · P 8-1/8p x 40mm",    "producto", 0, 1),
    (None, "PINES RETRO · P 8-1/4p x 40mm",    "producto", 0, 2),
    (None, "PINES RETRO · P 8-1/4p x 50mm",    "producto", 0, 2),
    (None, "PINES RETRO · P 9p x 39mm",         "producto", 0, 1),
    (None, "PINES RETRO · P 9-1/2p x 50mm",    "producto", 0, 2),
    (None, "PINES RETRO · P 10-1/4p x 50mm",   "producto", 0, 3),
    (None, "PINES RETRO · P 10-3/8p x 47mm",   "producto", 0, 1),
    (None, "PINES RETRO · P 10-1/2p x 53mm",   "producto", 0, 2),
    (None, "PINES RETRO · P 10-1/2p x 55mm",   "producto", 0, 1),
    (None, "PINES RETRO · P 10-1/2p x 58mm",   "producto", 0, 1),
    (None, "PINES RETRO · P 11p x 47mm",        "producto", 0, 1),
    (None, "PINES RETRO · P 11-1/4p x 50mm",   "producto", 0, 3),
    (None, "PINES RETRO · P 11-1/2p x 50mm",   "producto", 0, 1),
    (None, "PINES RETRO · P 12-1/2p x 65mm",   "producto", 0, 1),
    (None, "PINES RETRO · P 13p x 58mm (NO DISPONIBLE)", "producto", 0, 0),
    (None, "PINES RETRO · P 16-7/8p x 60mm",   "producto", 0, 2),

    # ── RADIADORES ───────────────────────────────────────────────────────────
    ("8448-130101Q1120AA",  "RADIADOR · FAW camiones",              "producto", 0, 1),
    ("QDXY",                "RADIADOR · Aire Núm 704",              "producto", 0, 1),
    ("GB/T85772005",        "RADIADOR · General",                   "producto", 0, 1),
    (None,                  "RADIADOR · Retroexcavadora",           "producto", 0, 2),

    # ── REPUESTOS VARIOS ─────────────────────────────────────────────────────
    (None,          "VARIOS · Cardán completo",                     "producto", 0, 1),
    ("REF4035",     "VARIOS · Cuerpo de válvula",                   "producto", 0, 1),
    ("LEI SHENG",   "VARIOS · Válvula Lei Sheng",                   "producto", 0, 1),
    (None,          "VARIOS · Torre de dirección",                  "producto", 0, 1),
    (None,          "VARIOS · Obitro (masa de dirección)",          "producto", 0, 1),
    (None,          "VARIOS · Torre joystick retroexcavadora",      "producto", 0, 1),

    # ── RETROVISORES Y ESPEJOS ───────────────────────────────────────────────
    (None, "RETROVISORES · Espejo puerta camión 10T y 2.5T",       "producto", 0, 5),
    (None, "RETROVISORES · Espejo puerta camión 4T",               "producto", 0, 11),
    (None, "RETROVISORES · Retrovisor superior camión 10T",        "producto", 0, 6),
    (None, "RETROVISORES · Retrovisor doble camión 10T",           "producto", 0, 10),
    (None, "RETROVISORES · Retrovisor doble camión 2.5T",          "producto", 0, 11),
    (None, "RETROVISORES · Retrovisor camión (general)",           "producto", 0, 3),

    # ── RINES ────────────────────────────────────────────────────────────────
    (None, "RINES · Tiger VR",    "producto", 0, 17),
    (None, "RINES · Camión VR",   "producto", 0, 18),
    (None, "RINES · Aro para rin","producto", 0, 18),

]

# ── Insertar en la base de datos ─────────────────────────────────────────────
def main():
    if not os.path.exists(DB_PATH):
        print(f"❌ No se encontró la base de datos en: {DB_PATH}")
        print("   Asegúrate de correr este script desde la carpeta del proyecto.")
        return

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row

    # Verificar cuántos productos hay actualmente
    existing = conn.execute("SELECT COUNT(*) FROM productos").fetchone()[0]
    if existing > 0:
        resp = input(f"⚠️  Ya hay {existing} producto(s) en la base de datos.\n"
                     f"   ¿Deseas agregar los nuevos sin borrar los existentes? (s/n): ")
        if resp.strip().lower() != "s":
            print("Operación cancelada.")
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
    print(f"\n✅ Se insertaron {insertados} productos correctamente.")
    print("   Abre el sistema en 127.0.0.1:5000 → Productos para verificar.")

if __name__ == "__main__":
    main()
