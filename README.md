# ☀️ Scientific Python

Scientific computing projects and numerical methods applied to physics and materials science.

## Topics
- **NumPy**
- **SciPy**
- **Matplotlib**

---

## 📌 Projects Included

### 1. Solar Cell I-V Curve Fitting & Power Analysis (`solar_cell_analysis.py`)
A Python implementation for analyzing experimental Current-Voltage (I-V) characteristics of photovoltaic devices (e.g., Perovskites).

* **Physics Model:** Shockley diode equation for solar cells.
* **Key Features:**
  * Curve fitting with `scipy.optimize.curve_fit` to extract physical parameters ($I_{sc}$, $I_0$, $n$).
  * Maximum Power Point ($P_{max}$) and Fill Factor ($FF$) calculation.
  * Dual-axis data visualization using `Matplotlib`.

### 📊 Generated Results & Visualization
![Solar Cell Characterization](solar_cell_characterization.png)

---

### 2. Quantum Key Distribution (QKD) Simulator (`qkd_simulation.py`)
A simulation of the BB84 protocol for quantum cryptography, demonstrating the impact of photon interception and Quantum Bit Error Rate (QBER) detection.

* **Quantum Principles:** Photon polarization state measurement and base mismatch.
* **Key Features:**
  * Sifting process algorithm comparing random Alice/Bob measurement bases.
  * Eavesdropper (Eve) detection through QBER calculation.
  * Comparative statistical plotting of security metrics.

### 📊 Results & Visualization
![QKD Simulation](qkd_simulation.png)


## 🛠️ Tech Stack & Dependencies
* **Python 3.x**
* **NumPy** - Numerical operations & synthetic data generation
* **SciPy** - Nonlinear least-squares curve fitting
* **Matplotlib** - Publication-ready scientific plotting
