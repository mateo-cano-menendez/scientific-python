import numpy as np
import matplotlib.pyplot as plt

# 1. Parámetros físicos del Potencial de Lennard-Jones (Unidades reducidas)
epsilon = 1.0   # Profundidad del pozo de potencial
sigma = 1.0     # Distancia a la cual el potencial es cero
mass = 1.0      # Masa de las partículas
dt = 0.005      # Paso de tiempo (Time step)
n_steps = 1000  # Número de pasos de simulación

# 2. Función de Fuerza de Lennard-Jones (Derivada del potencial: F = -dV/dr)
def lj_force(r):
    r6 = (sigma / r) ** 6
    r12 = r6 ** 2
    force_magnitude = 24 * epsilon * (2 * r12 - r6) / (r ** 2)
    potential_energy = 4 * epsilon * (r12 - r6)
    return force_magnitude, potential_energy

# 3. Condición inicial: 2 partículas interactuando
r_pos = 1.2  # Distancia inicial entre partículas (cerca del mínimo de energía r ~ 1.12*sigma)
v_1 = np.array([0.1, 0.0])
v_2 = np.array([-0.1, 0.0])

pos_1 = np.array([0.0, 0.0])
pos_2 = np.array([r_pos, 0.0])

# Contenedores para almacenar la trayectoria y energías
e_kin_list, e_pot_list, e_tot_list = [], [], []

# 4. Bucle de Simulación de Dinámica Molecular (Integración de Velocity-Verlet)
f_mag, epot = lj_force(np.linalg.norm(pos_2 - pos_1))
force_vec = f_mag * (pos_2 - pos_1) / np.linalg.norm(pos_2 - pos_1)

for step in range(n_steps):
    r_vec = pos_2 - pos_1
    dist = np.linalg.norm(r_vec)
    f_mag, epot = lj_force(dist)
    f_vec = f_mag * (r_vec / dist)
    
    # Actualización de velocidades y posiciones (Velocity Verlet)
    v_1 += 0.5 * (-f_vec / mass) * dt
    v_2 += 0.5 * (f_vec / mass) * dt
    
    pos_1 += v_1 * dt
    pos_2 += v_2 * dt
    
    # Cálculo de energías
    ekin = 0.5 * mass * (np.linalg.norm(v_1)**2 + np.linalg.norm(v_2)**2)
    
    e_kin_list.append(ekin)
    e_pot_list.append(epot)
    e_tot_list.append(ekin + epot)

# 5. Visualización para publicación (Conservación de Energía en Biofísica)
time = np.arange(n_steps) * dt

plt.figure(figsize=(8, 5))
plt.plot(time, e_kin_list, label='Kinetic Energy ($E_{kin}$)', color='tab:red', linestyle='--')
plt.plot(time, e_pot_list, label='Potential Energy ($E_{pot}$)', color='tab:blue', linestyle='--')
plt.plot(time, e_tot_list, label='Total Energy ($E_{tot}$)', color='black', linewidth=2)

plt.xlabel('Time (reduced units)', fontsize=12)
plt.ylabel('Energy (reduced units)', fontsize=12)
plt.title('Lennard-Jones Molecular Dynamics: Energy Conservation', fontsize=13, fontweight='bold')
plt.legend(frameon=True, loc='right')
plt.grid(True, linestyle=':', alpha=0.6)
plt.tight_layout()

plt.savefig('lennard_jones_energy.png', dpi=300)
plt.show()
