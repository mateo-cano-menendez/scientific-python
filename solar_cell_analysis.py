import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# 1. Modelo físico (Ecuación del diodo ideal para celda solar)
def iv_curve(V, I_sc, I_0, n, V_t=0.0259):
    return I_sc - I_0 * (np.exp(V / (n * V_t)) - 1)

# 2. Generación de datos sintéticos con ruido
np.random.seed(42)
voltage_exp = np.linspace(0, 0.8, 50)
ideal_current = iv_curve(voltage_exp, I_sc=0.035, I_0=1e-9, n=1.2)
noise = np.random.normal(0, 0.0008, size=voltage_exp.shape)
current_exp = ideal_current + noise

# 3. Ajuste de curvas (Curve Fitting con SciPy)
popt, _ = curve_fit(iv_curve, voltage_exp, current_exp, p0=[0.03, 1e-8, 1.0])
I_sc_fit, I_0_fit, n_fit = popt

# 4. Cálculo de Potencia Máxima y Fill Factor
power = voltage_exp * current_exp
max_power_idx = np.argmax(power)
P_max = power[max_power_idx]
FF = P_max / (voltage_exp[-1] * I_sc_fit)

print(f"I_sc ajustada: {I_sc_fit*1000:.2f} mA")
print(f"Factor de idealidad (n): {n_fit:.2f}")
print(f"Máxima Potencia (Pmax): {P_max*1000:.2f} mW")
print(f"Fill Factor (FF): {FF*100:.2f}%")

# 5. Generación de la gráfica
fig, ax1 = plt.subplots(figsize=(8, 5))

color = 'tab:blue'
ax1.set_xlabel('Voltage (V)', fontsize=12)
ax1.set_ylabel('Current (A)', color=color, fontsize=12)
ax1.scatter(voltage_exp, current_exp, color='red', label='Experimental Data', s=20)
ax1.plot(voltage_exp, iv_curve(voltage_exp, *popt), color=color, linewidth=2, label='Shockley Model Fit')
ax1.grid(True, linestyle='--', alpha=0.6)

ax2 = ax1.twinx()
color = 'tab:orange'
ax2.set_ylabel('Power (W)', color=color, fontsize=12)
ax2.plot(voltage_exp, power, color=color, linestyle=':', linewidth=2, label='Power Output')

plt.title('Photovoltaic Cell I-V & Power Characterization', fontsize=14, fontweight='bold')
fig.tight_layout()

# Guardar la gráfica
plt.savefig('solar_cell_characterization.png', dpi=300)
plt.show()
