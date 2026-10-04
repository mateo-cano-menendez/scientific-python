import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# 1. Definición de perfiles de línea (Perfil Gaussiano)
def gaussian(x, amp, center, sigma):
    return amp * np.exp(-((x - center) ** 2) / (2 * sigma ** 2))

def multi_gaussian(x, *params):
    """Suma de múltiples gaussianas para deconvolución de espectros."""
    y = np.zeros_like(x)
    for i in range(0, len(params), 3):
        amp = params[i]
        center = params[i+1]
        sigma = params[i+2]
        y += gaussian(x, amp, center, sigma)
    return y

# 2. Generación de espectro experimental sintético (e.g., Raman / UV-Vis superpuesto)
np.random.seed(101)
wavenumber = np.linspace(400, 800, 300)

# Dos picos muy juntos (superposición física)
true_peak1 = gaussian(wavenumber, 120, 580, 25)
true_peak2 = gaussian(wavenumber, 85, 625, 20)
baseline = 10 + 0.02 * wavenumber
noise = np.random.normal(0, 3.5, size=wavenumber.shape)

experimental_spectrum = true_peak1 + true_peak2 + baseline + noise

# 3. Estimación inicial y Ajuste de Deconvolución
# Formato: [amp1, center1, sigma1, amp2, center2, sigma2]
initial_guess = [100, 570, 20, 70, 630, 20]
popt, _ = curve_fit(lambda x, *p: multi_gaussian(x, *p) + (10 + 0.02*x), 
                    wavenumber, experimental_spectrum, p0=initial_guess)

# 4. Extracción de componentes ajustadas
fit_peak1 = gaussian(wavenumber, *popt[0:3])
fit_peak2 = gaussian(wavenumber, *popt[3:6])
fitted_total = fit_peak1 + fit_peak2 + (10 + 0.02 * wavenumber)

# 5. Representación visual para publicación
plt.figure(figsize=(8, 5))
plt.scatter(wavenumber, experimental_spectrum, color='black', s=10, alpha=0.6, label='Raw Experimental Data')
plt.plot(wavenumber, fitted_total, color='red', linewidth=2, label='Total Spectral Fit')
plt.plot(wavenumber, fit_peak1, '--', color='blue', linewidth=1.5, label=f'Peak 1 ({popt[1]:.1f} cm⁻¹)')
plt.plot(wavenumber, fit_peak2, '--', color='green', linewidth=1.5, label=f'Peak 2 ({popt[4]:.1f} cm⁻¹)')

plt.xlabel('Wavenumber (cm⁻¹)', fontsize=12)
plt.ylabel('Intensity (a.u.)', fontsize=12)
plt.title('Spectroscopic Peak Deconvolution & Fitting', fontsize=13, fontweight='bold')
plt.legend(frameon=True)
plt.grid(True, linestyle=':', alpha=0.6)
plt.tight_layout()

# Guardar la imagen
plt.savefig('spectroscopy_deconvolution.png', dpi=300)
plt.show()
