import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import linregress

# 1. Carga de datos experimentales reales de la Práctica P8 (Mateo Cano & Claudia Sarabia)
# Reemplazar con la ruta de tu archivo CSV si es necesario
csv_path = 'P8- Mateo Cano y Claudia Sarabia.csv'
df = pd.read_csv(csv_path, sep=';', decimal=',', on_bad_lines='skip')

# Limpieza de columnas clave
df_clean = df[['kelvin', 'kelvin^4', 'p (mW)', 'ln(T)', 'Ln(P+p0)']].dropna()

T_kelvin = df_clean['kelvin'].values
T4 = df_clean['kelvin^4'].values
P_mW = df_clean['p (mW)'].values
ln_T = df_clean['ln(T)'].values
ln_P = df_clean['Ln(P+p0)'].values

# 2. Regresión Lineal 1: P vs T^4 (Verificación de Stefan-Boltzmann)
res_linear = linregress(T4, P_mW)
slope_lin = res_linear.slope
intercept_lin = res_linear.intercept
r2_lin = res_linear.rvalue**2

# 3. Regresión Lineal 2: ln(P) vs ln(T) (Determinación del exponente n ~ 4)
res_log = linregress(ln_T, ln_P)
exponent_n = res_log.slope
intercept_log = res_log.intercept
r2_log = res_log.rvalue**2

print("--- RESULTADOS EXPERIMENTALES (PRÁCTICA P8) ---")
print(f"Pendiente (P vs T^4): {slope_lin:.3e} mW/K^4 (R² = {r2_lin:.4f})")
print(f"Exponente de Temperatura n: {exponent_n:.4f} (Teórico: 4.000, R² = {r2_log:.4f})")

# 4. Generación de figura con estándar de publicación (2 paneles)
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5))

# Panel A: P vs T^4
ax1.scatter(T4 / 1e10, P_mW, color='#1f77b4', alpha=0.7, edgecolors='k', label='Experimental Data (Lab P8)')
ax1.plot(T4 / 1e10, (slope_lin * T4 + intercept_lin), color='red', linewidth=2, 
         label=f'Fit: $y = {slope_lin:.2e}x {intercept_lin:+.2f}$\n$R^2 = {r2_lin:.4f}$')
ax1.set_xlabel(r'Temperature $T^4$ ($10^{10} \text{ K}^4$)', fontsize=11)
ax1.set_ylabel(r'Power $P$ (mW)', fontsize=11)
ax1.set_title(r'Stefan-Boltzmann Law: $P \propto T^4$', fontsize=12, fontweight='bold')
ax1.grid(True, linestyle='--', alpha=0.6)
ax1.legend(frameon=True)

# Panel B: Log-Log Fit para verificar el exponente 4
ax2.scatter(ln_T, ln_P, color='#2ca02c', alpha=0.7, edgecolors='k', label='Experimental Data (Lab P8)')
ax2.plot(ln_T, res_log.slope * ln_T + res_log.intercept, color='darkgreen', linewidth=2, 
         label=f'Fit: $n = {exponent_n:.4f}$\n$R^2 = {r2_log:.4f}$')
ax2.set_xlabel(r'$\ln(T)$', fontsize=11)
ax2.set_ylabel(r'$\ln(P - P_0)$', fontsize=11)
ax2.set_title(r'Temperature Exponent Validation ($P \propto T^n$)', fontsize=12, fontweight='bold')
ax2.grid(True, linestyle='--', alpha=0.6)
ax2.legend(frameon=True)

plt.suptitle('Experimental Validation of Stefan-Boltzmann Law (P8 - Physics & Chemistry Lab)', fontsize=14, fontweight='bold', y=1.02)
plt.tight_layout()
plt.savefig('stefan_boltzmann_lab_results.png', dpi=300, bbox_inches='tight')
plt.show()
