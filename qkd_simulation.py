import numpy as np
import matplotlib.pyplot as plt

def simulate_bb84_protocol(n_bits=100, eavesdropper=True):
    """
    Simulación del protocolo de distribución de clave cuántica BB84.
    Muestra cómo la presencia de un espía (Eve) introduce un porcentaje
    de error (QBER) al intentar medir la polarización de los fotones.
    """
    np.random.seed(42)
    
    # 1. Alice genera bits aleatorios y elige bases de polarización (0: Rectilínea +, 1: Diagonal X)
    alice_bits = np.random.randint(0, 2, n_bits)
    alice_bases = np.random.randint(0, 2, n_bits)
    
    # 2. Transmisión a través del canal cuántico
    bob_bases = np.random.randint(0, 2, n_bits)
    bob_results = np.zeros(n_bits, dtype=int)
    
    if eavesdropper:
        # Eve intercepta las mediciones
        eve_bases = np.random.randint(0, 2, n_bits)
        eve_measured = np.where(eve_bases == alice_bases, alice_bits, np.random.randint(0, 2, n_bits))
        
        # Bob mide los fotones alterados por Eve
        bob_results = np.where(bob_bases == eve_bases, eve_measured, np.random.randint(0, 2, n_bits))
    else:
        # Sin espía: Bob mide exactamente si usa la misma base que Alice
        bob_results = np.where(bob_bases == alice_bases, alice_bits, np.random.randint(0, 2, n_bits))
        
    # 3. Filtrado de claves (Sifting): Solo conservan bits donde coinciden las bases
    matching_bases = (alice_bases == bob_bases)
    alice_key = alice_bits[matching_bases]
    bob_key = bob_results[matching_bases]
    
    # 4. Cálculo de la Tasa de Error de Bits Cuánticos (QBER)
    errors = np.sum(alice_key != bob_key)
    qber = (errors / len(alice_key)) * 100 if len(alice_key) > 0 else 0
    
    return len(alice_key), qber

# Ejecución de simulaciones
_, qber_no_eve = simulate_bb84_protocol(n_bits=1000, eavesdropper=False)
_, qber_with_eve = simulate_bb84_protocol(n_bits=1000, eavesdropper=True)

print(f"QBER sin espía: {qber_no_eve:.2f}%")
print(f"QBER con espía (Eve): {qber_with_eve:.2f}%")

# Generación de la gráfica comparativa
categories = ['Channel without Eavesdropper', 'Channel with Eavesdropper (Eve)']
qber_values = [qber_no_eve, qber_with_eve]
colors = ['#2ca02c', '#d62728']

plt.figure(figsize=(7, 4.5))
bars = plt.bar(categories, qber_values, color=colors, width=0.5)
plt.ylabel('Quantum Bit Error Rate (QBER %)', fontsize=11)
plt.title('BB84 Quantum Key Distribution - Eavesdropping Impact', fontsize=12, fontweight='bold')
plt.ylim(0, 35)

for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, yval + 1, f'{yval:.2f}%', ha='center', va='bottom', fontweight='bold')

plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.savefig('qkd_simulation.py.png', dpi=300)
plt.show()
