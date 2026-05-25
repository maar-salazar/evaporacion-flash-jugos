# ============================================
# modelo.py — Motor de cálculo de la planta
# ============================================
from scipy.optimize import brentq

# Constantes de Antoine
A_eth, B_eth, C_eth = 8.04494, 1554.3,  222.65
A_wat, B_wat, C_wat = 8.07131, 1730.63, 233.426

def calcular_proceso(T_flash, P_flash_atm, T_feed, F_total=1000, z_etanol=0.10):
    """
    Calcula el balance completo del separador flash.

    Parámetros:
      T_flash     : temperatura del separador (°C)
      P_flash_atm : presión del separador (atm)
      T_feed      : temperatura de alimentación (°C)
      F_total     : flujo total de alimentación (kg/h)
      z_etanol    : fracción másica de etanol en la alimentación

    Retorna un diccionario con todos los resultados.
    """

    z_agua = 1 - z_etanol

    # --- Antoine: presión de vapor ---
    P_sat_eth = 10 ** (A_eth - B_eth / (C_eth + T_flash))  # mmHg
    P_sat_wat = 10 ** (A_wat - B_wat / (C_wat + T_flash))  # mmHg

    # --- Conversión de presión total ---
    P_total_mmHg = P_flash_atm * 760

    # --- Coeficientes de actividad (calibrados con DWSIM) ---
    gamma_eth = 2.96 
    gamma_wat = 1.11 

    # --- K-values ---
    K_eth = (gamma_eth * P_sat_eth) / P_total_mmHg
    K_wat = (gamma_wat * P_sat_wat) / P_total_mmHg

    # --- Rachford-Rice ---
    z = [z_etanol, z_agua]
    K = [K_eth,    K_wat]

    def rr(V_frac):
        return sum(z[i] * (K[i] - 1) / (1 + V_frac * (K[i] - 1)) for i in range(2))

    # --- Rachford-Rice ---
    def rr(V_frac):
        return sum(z[i] * (K[i] - 1) / (1 + V_frac * (K[i] - 1)) for i in range(2))

    # Verificamos si la mezcla está fuera del rango bifásico
    if rr(0.0001) < 0:
        # Todo quiere ser líquido
        V_frac = 0.0001
    elif rr(0.9999) > 0:
        # Todo quiere ser vapor
        V_frac = 0.9999
    else:
        # Hay dos fases — resolvemos normalmente
        V_frac = brentq(rr, 0.0001, 0.9999)

    # --- Flujos ---
    V = V_frac * F_total   # kg/h vapor (producto)
    L = F_total - V        # kg/h líquido (vinazas)

    # --- Composiciones ---
    y_eth = z_etanol * K_eth / (1 + V_frac * (K_eth - 1))
    x_eth = y_eth / K_eth
    y_wat = 1 - y_eth
    x_wat = 1 - x_eth

    # --- Balance de energía (calibrado con DWSIM) ---
    Q_calentador = 96.06 * ((T_flash - T_feed) / (92 - 25)) * (F_total / 1000)
    Q_condensador = V / 3600 * (y_eth * 855 + y_wat * 2260) * 1000 / 1000
    W_bombas = 0.114 + 0.08  # kW — bombas P-210 y P-410

    return {
        # Corrientes
        "V_kg_h"       : round(V, 4),
        "L_kg_h"       : round(L, 4),
        "y_etanol"     : round(y_eth, 4),
        "x_etanol"     : round(x_eth, 4),
        # Energía
        "Q_calentador" : round(Q_calentador, 2),
        "Q_condensador": round(Q_condensador, 2),
        "W_bombas"     : round(W_bombas, 3),
        # K-values (útiles para mostrar en la app)
        "K_etanol"     : round(K_eth, 3),
        "K_agua"       : round(K_wat, 3),
    }


# ============================================
# PRUEBA — borramos esto cuando conectemos
# con Streamlit
# ============================================
if __name__ == "__main__":
    r = calcular_proceso(T_flash=92, P_flash_atm=1, T_feed=25)

    print("=" * 45)
    print("  CASO BASE (debe coincidir con DWSIM)")
    print("=" * 45)
    print(f"  Vapor (producto)  : {r['V_kg_h']} kg/h")
    print(f"  Vinazas           : {r['L_kg_h']} kg/h")
    print(f"  Etanol en vapor   : {r['y_etanol']*100:.1f}%")
    print(f"  Etanol en vinazas : {r['x_etanol']*100:.1f}%")
    print(f"  Q calentador      : {r['Q_calentador']} kW")
    print("=" * 45)
    if __name__ == "__main__":
         r = calcular_proceso(T_flash=92, P_flash_atm=1, T_feed=25)

    print("=" * 45)
    print("  CASO BASE — modelo calibrado")
    print("=" * 45)
    print(f"  Vapor (producto)  : {r['V_kg_h']} kg/h")
    print(f"  Vinazas           : {r['L_kg_h']} kg/h")
    print(f"  Etanol en vapor   : {r['y_etanol']*100:.1f}%")
    print(f"  Etanol en vinazas : {r['x_etanol']*100:.1f}%")
    print(f"  Q calentador      : {r['Q_calentador']} kW")
    print(f"  K etanol          : {r['K_etanol']}")
    print(f"  K agua            : {r['K_agua']}")
    print("=" * 45)

    # Prueba: ¿qué pasa si subimos la temperatura?
    print("\n  ¿Qué pasa a 95°C?")
    r2 = calcular_proceso(T_flash=95, P_flash_atm=1, T_feed=25)
    print(f"  Vapor   : {r2['V_kg_h']} kg/h")
    print(f"  Etanol  : {r2['y_etanol']*100:.1f}%")
    print(f"  Q cal   : {r2['Q_calentador']} kW")