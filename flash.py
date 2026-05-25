# ============================================
# PLANTA DE CONCENTRACIÓN DE MOSTO
# Etapa 1 — Presión de vapor (Antoine)
# ============================================

# Constantes de Antoine para etanol y agua
# Fórmula: log10(P_sat) = A - B/(C+T)
# P en mmHg, T en °C

A_eth, B_eth, C_eth = 8.04494, 1554.3, 222.65    # Etanol
A_wat, B_wat, C_wat = 8.07131, 1730.63, 233.426   # Agua

def presion_vapor(T_C, A, B, C):
    """
    Calcula la presión de vapor de un componente puro.
    Entrada: T_C = temperatura en °C
    Salida : presión en mmHg
    """
    log_P = A - B / (C + T_C)
    return 10 ** log_P

# --- PRUEBA con los datos de tu reporte DWSIM ---
T = 92  # °C — temperatura del separador flash B-410

P_etanol = presion_vapor(T, A_eth, B_eth, C_eth)
P_agua   = presion_vapor(T, A_wat, B_wat, C_wat)

print("=" * 40)
print(f"  Temperatura de prueba: {T} °C")
print("=" * 40)
print(f"  P_vapor etanol : {P_etanol:.1f} mmHg")
print(f"  P_vapor agua   : {P_agua:.1f}  mmHg")
print()
print("  Esperado etanol : ~1280 mmHg")
print("  Esperado agua   :  ~526 mmHg")
print("=" * 40)
# ============================================
# Paso 2 — K-values (¿quién prefiere el vapor?)
# ============================================

# Presión total del separador en mmHg
# (tu reporte dice 1 atm → convertimos: 1 atm = 760 mmHg)
P_total_mmHg = 1 * 760

# Coeficientes de actividad calibrados con DWSIM a 92°C
# (miden cuánto se "rechazan" etanol y agua entre sí en solución)
gamma_etanol = 2.96
gamma_agua   = 1.11

# K_i = (gamma_i × P_sat_i) / P_total
K_etanol = (gamma_etanol * P_etanol) / P_total_mmHg
K_agua   = (gamma_agua   * P_agua)   / P_total_mmHg

print("=" * 40)
print("  K-values a 92°C, 1 atm")
print("=" * 40)
print(f"  K_etanol : {K_etanol:.3f}")
print(f"  K_agua   : {K_agua:.3f}")
print()
print("  K > 1 → prefiere el vapor")
print("  K < 1 → prefiere el líquido")
print("=" * 40)
# ============================================
# Paso 3 — Balance de masa (Rachford-Rice)
# ============================================
from scipy.optimize import brentq

# ← AGREGA ESTAS 3 LÍNEAS SI NO ESTÁN ARRIBA
F_total  = 1000  # kg/h — flujo de alimentación
z_etanol = 0.10  # fracción másica etanol en alimentación
z_agua   = 0.90  # fracción másica agua en alimentación

# Composición de la alimentación
z = [z_etanol, z_agua]  # [0.10, 0.90]
K = [K_etanol, K_agua]  # los que calculamos en el paso 2

def rachford_rice(V_frac, z, K):
    """
    Ecuación de Rachford-Rice.
    Buscamos el V_frac que hace esta función = 0.
    V_frac = fracción del flujo total que se evapora (entre 0 y 1)
    """
    resultado = 0
    for i in range(len(z)):
        resultado += z[i] * (K[i] - 1) / (1 + V_frac * (K[i] - 1))
    return resultado

# scipy encuentra automáticamente el V_frac correcto
# brentq busca entre 0.0001 (casi nada se evapora) y 0.9999 (casi todo)
V_frac = brentq(rachford_rice, 0.0001, 0.9999, args=(z, K))

# Flujos másicos
V = V_frac * F_total   # kg/h de vapor (producto)
L = F_total - V        # kg/h de líquido (vinazas)

# Composiciones de cada fase
y_etanol = z[0] * K[0] / (1 + V_frac * (K[0] - 1))  # fracción en vapor
x_etanol = y_etanol / K[0]                            # fracción en líquido

print("=" * 40)
print("  Balance de masa — Separador B-410")
print("=" * 40)
print(f"  Fracción evaporada : {V_frac:.5f}")
print(f"  Vapor  (producto)  : {V:.2f} kg/h")
print(f"  Líquido (vinazas)  : {L:.2f} kg/h")
print(f"  y_etanol (vapor)   : {y_etanol*100:.1f}%")
print(f"  x_etanol (vinazas) : {x_etanol*100:.1f}%")
print()
print("  Esperado DWSIM:")
print("  Vapor   : 0.29 kg/h")
print("  Vinazas : 999.71 kg/h")
print("  y_etanol: ~40%")
print("=" * 40)
