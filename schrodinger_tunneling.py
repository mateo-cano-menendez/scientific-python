import numpy as np
import matplotlib.pyplot as plt

# 1. Parámetros del sistema cuántico (Unidades atómicas / reducidas)
dx = 0.01
x = np.arange(-10, 10, dx)
N = len(x)

# 2. Definición del Potencial: Barrera de Potencial Finito
V0 = 8.0          # Altura de la barrera de potencial
barrier_width = 1.0
V = np.zeros(N)
V[(x >= -barrier_width/2) & (x <= barrier_width/2)] = V0

# 3. Construcción del Operador Hamiltoniano H = T + V (Método de Diferencias Finitas)
# Segunda derivada discreta para la energía cinética T = -1/2 * d^2/dx^2
T = np.zeros((N, N))
for i in range(N):
    T[i, i] = -2.0
    if i > 0:
        T[i, i-1] = 1.0
    if i < N - 1:
        T[i, i+1] = 1.0
T = -0.5 * T / (dx**2)

H = T + np.diag(V)

# 4. Cálculo de Autovalores (Energías E) y Autofunciones (Psi)
eigenvalues, eigenvectors = np.linalg.eigh(H)

# 5. Selección de un estado cuántico con energía cercana o inferior a la barrera
state_idx = 15  # Estado estacionario representativo
psi = eigenvectors[:, state_idx]
energy = eigenvalues[state_idx]

# Normalización de la función de onda
prob_density = np.abs(psi)**2
prob_density = prob_density / np.max(prob_density) * (energy * 0.4)  # Escalado visual

# 6. Representación gráfica para publicación
plt.figure(figsize=(8, 5))
plt.plot(x, V, color='black', linewidth=2, label='Potential Barrier $V(x)$')
plt.axhline(energy, color='tab:red', linestyle='--', linewidth=1.5, label=f'Particle Energy $E = {energy:.2f}$')
plt.fill_between(x, energy, energy + prob_density, color='tab:blue', alpha=0.5, label='Probability Density $|\Psi(x)|^2$')
plt.plot(x, energy + prob_density, color='tab:blue', linewidth=1)

plt.xlabel('Position $x$ (a.u.)', fontsize=12)
plt.ylabel('Energy / Probability (a.u.)', fontsize=12)
plt.title('Quantum Tunneling through a Finite Potential Barrier', fontsize=13, fontweight='bold')
plt.xlim(-6, 6)
plt.ylim(-1, V0 + 3)
plt.legend(frameon=True, loc='upper right')
plt.grid(True, linestyle=':', alpha=0.6)
plt.tight_layout()

plt.savefig('quantum_tunneling.png', dpi=300)
plt.show()
