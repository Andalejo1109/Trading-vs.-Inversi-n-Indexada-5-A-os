---

## 2. 🐍 El archivo de código: `trading_vs_passive.py`
*Este script automatiza el cálculo matemático y exporta los gráficos con alta calidad visual dentro de la carpeta `img/`.*

```python
import numpy as np
import matplotlib.pyplot as plt
import os

# Crear carpeta de imágenes si no existe
if not os.path.exists('img'):
    os.makedirs('img')

months = 60
time_years = np.arange(0, months + 1) / 12
rates = [0.10, 0.15, 0.20]
labels = ['10% Anual', '15% Anual', '20% Anual']

trader_histories = {}
inv50_histories = {}
inv100_histories = {}

# Ejecución de simulación temporal
for r in rates:
    r_m = r / 12
    
    # Trader ($1,000 inicial, $15/mes comisión)
    bal_trader = 1000
    h_trader = [bal_trader]
    for m in range(1, months + 1):
        bal_trader = bal_trader * (1 + r_m) - 15
        h_trader.append(max(0, bal_trader))
    trader_histories[r] = h_trader
    
    # Inversor Pasivo ($200 inicial, $50/mes)
    bal_50 = 200
    h_50 = [bal_50]
    for m in range(1, months + 1):
        bal_50 = bal_50 * (1 + r_m) + 50
        h_50.append(bal_50)
    inv50_histories[r] = h_50

    # Inversor Pasivo ($200 inicial, $100/mes)
    bal_100 = 200
    h_100 = [bal_100]
    for m in range(1, months + 1):
        bal_100 = bal_100 * (1 + r_m) + 100
        h_100.append(bal_100)
    inv100_histories[r] = h_100

# ---- GRÁFICO 1: BARRAS COMPARATIVAS FINALES ----
final_trader = [trader_histories[r][-1] for r in rates]
final_inv50 = [inv50_histories[r][-1] for r in rates]
final_inv100 = [inv100_histories[r][-1] for r in rates]

x = np.arange(len(rates))
width = 0.25

fig, ax = plt.subplots(figsize=(10, 6))
rects1 = ax.bar(x - width, final_trader, width, label='Trader ($1,000 Inicial, -$15/mes)', color='#e74c3c')
rects2 = ax.bar(x, final_inv50, width, label='Inversor Pasivo ($200 + $50/mes)', color='#3498db')
rects3 = ax.bar(x + width, final_inv100, width, label='Inversor Pasivo ($200 + $100/mes)', color='#2ecc71')

ax.set_ylabel('Resultado Final en 5 Años (USD)', fontsize=12)
ax.set_title('Comparativa Final: Trader vs Inversor Pasivo (A 5 Años)', fontsize=14, fontweight='bold', pad=15)
ax.set_xticks(x)
ax.set_xticklabels(labels, fontsize=11)
ax.legend(fontsize=11)
ax.grid(axis='y', linestyle='--', alpha=0.5)

def autolabel(rects):
    for rect in rects:
        height = rect.get_height()
        ax.annotate(f'${height:,.0f}',
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3), textcoords="offset points",
                    ha='center', va='bottom', fontsize=9, fontweight='bold')

autolabel(rects1)
autolabel(rects2)
autolabel(rects3)

plt.tight_layout()
plt.savefig('img/comparativa_trader_vs_inversor.png', dpi=150)
plt.close()

# ---- GRÁFICO 2: EVOLUCIÓN TEMPORAL EN ESCENARIO 15% ----
fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(time_years, trader_histories[0.15], label='Trader (15% Bruto, -$15/mes com.)', color='#e74c3c', linewidth=2.5)
ax.plot(time_years, inv50_histories[0.15], label='Inversor Pasivo ($50/mes al 15%)', color='#3498db', linewidth=2.5)
ax.plot(time_years, inv100_histories[0.15], label='Inversor Pasivo ($100/mes al 15%)', color='#2ecc71', linewidth=2.5)

ax.set_title('Evolución del Capital a lo largo de 5 Años (Rendimiento del 15% Anual)', fontsize=13, fontweight='bold', pad=15)
ax.set_xlabel('Años', fontsize=12)
ax.set_ylabel('Balance del Portafolio (USD)', fontsize=12)
ax.grid(True, linestyle='--', alpha=0.5)
ax.legend(fontsize=11, loc='upper left')
ax.set_xlim(0, 5)

ax.text(5, trader_histories[0.15][-1], f' ${trader_histories[0.15][-1]:,.2f}', va='center', ha='left', color='#e74c3c', fontweight='bold')
ax.text(5, inv50_histories[0.15][-1], f' ${inv50_histories[0.15][-1]:,.2f}', va='center', ha='left', color='#3498db', fontweight='bold')
ax.text(5, inv100_histories[0.15][-1], f' ${inv100_histories[0.15][-1]:,.2f}', va='center', ha='left', color='#2ecc71', fontweight='bold')

plt.tight_layout()
plt.savefig('img/evolucion_capital_15porciento.png', dpi=150)
plt.close()

print("Gráficos generados de manera exitosa dentro de la carpeta /img.")
