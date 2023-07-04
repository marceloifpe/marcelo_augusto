#Aluno: Marcelo Augusto de Barros Araújo.
#Disciplina: Matemática Discreta 2.
#Professor: Marcos Maia.
import matplotlib.pyplot as plt
import numpy as np

# Pontos de controle x e y
x0, y0 = 100, 300
x1, y1 = 200, 50
x2, y2 = 300, 250
x3, y3 = 400, 200

# variando de 0 a 1
t = np.linspace(0, 1, 100)

# Fórmula da curva de Bézier
B_x = (1 - t)**3 * x0 + 3 * (1 - t)**2 * t * x1 + 3 * (1 - t) * t**2 * x2 + t**3 * x3
B_y = (1 - t)**3 * y0 + 3 * (1 - t)**2 * t * y1 + 3 * (1 - t) * t**2 * y2 + t**3 * y3

# Geração da curva no gráfico
plt.plot(B_x, B_y, color='blue', linewidth=2)
plt.scatter([x0, x1, x2, x3], [y0, y1, y2, y3], color='red', marker='o')

plt.title("Curva Cúbica de Bézier(Triângulo de Pascal)")
plt.xlabel("Eixo X")
plt.ylabel("Eixo Y")
plt.grid(True)
plt.show()
