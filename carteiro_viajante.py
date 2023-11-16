from pulp import *
import numpy as np

#dados de entrada
cust = np.genfromtxt("amostra_.csv", delimiter = ";")

#parametros
n = len(cust)
arcos = [(i,j) for i in range(n) for j in range (n) if cust[i, j] != 999]

#inicializar
tsp = LpProblem("carteiro_viajante", LpMinimize)

#variaveis
#x ij : 1, se a rota do carteiro passar pela cidade j logo depois da i 0 caso contrario
x = LpVariable.dicts("x", arcos, cat = "Binary")
u = LpVariable.dicts("u", [ i for i in range(n)], lowBound = 1, upBound = n, cat = "Coninuous")

#função
tsp += lpSum([cust[i,j] * x[i,j] for (i,j) in arcos])

#restriçao 1
for j in range (n):
    tsp += lpSum([x[i,j] for (i,m) in arcos if m==j]) == 1

#restrição 2
for i in range(n):
    tsp += lpSum([x[i,j] for (m,j) in arcos if m==i]) == 1

#restrição 3
for (i,j) in arcos:
    if i > 0 and i != j:
        tsp += u[i] - u[j] + n*x[i,j] <= n-1

#modelo resolvido
solve_model = tsp.solve()
print(f"problema: {LpStatus[solve_model]}")

#display var
for var in tsp.variables():
    if var.varValue > 0:
        print(f"{var.name} = {var.varValue}")

#display funcao
print(f"custo total = ${value(tsp.objective)}")