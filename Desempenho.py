import numpy as np
import matplotlib.pyplot as plt
import skfuzzy as fuzz
from skfuzzy import control as ctrl

nota = ctrl.Antecedent(np.arange(0, 101, 1), 'nota')
falta = ctrl.Antecedent(np.arange(0, 31, 1), 'falta')

desempenho = ctrl.Consequent(np.arange(0, 101, 1), 'desempenho')

desempenho.defuzzify_method = 'lom'

nota['baixo'] = fuzz.trimf(nota.universe, [0, 0, 50])
nota['medio'] = fuzz.trimf(nota.universe, [40, 60, 80])
nota['alto'] = fuzz.trimf(nota.universe, [70, 90, 100])
nota['perfeita'] = fuzz.trimf(nota.universe, [99, 100, 100])

falta['baixo'] = fuzz.trimf(falta.universe, [0, 0, 5])
falta['medio'] = fuzz.trimf(falta.universe, [4, 7, 10])
falta['alto'] = fuzz.trimf(falta.universe, [8, 30, 30])
falta['zero'] = fuzz.trimf(falta.universe, [0, 0, 1])

desempenho['ruim'] = fuzz.trimf(desempenho.universe, [0, 0, 50])
desempenho['regular'] = fuzz.trimf(desempenho.universe, [40, 55, 90])
desempenho['excelente'] = fuzz.trapmf(desempenho.universe, [90, 98, 100, 100]
)

regra1 = ctrl.Rule(nota['baixo'] & falta['alto'], desempenho['ruim'])
regra2 = ctrl.Rule(nota['alto'] & falta['baixo'], desempenho['excelente'])
regra3 = ctrl.Rule(nota['medio'] | falta['medio'], desempenho['regular'])
regra4 = ctrl.Rule(nota['perfeita'] & falta['zero'], desempenho['excelente'])

controle_desempenho = ctrl.ControlSystem([regra1, regra2, regra3, regra4])

simulacao = ctrl.ControlSystemSimulation(controle_desempenho)

simulacao.input['nota'] = 100
simulacao.input['falta'] = 0

simulacao.compute()

print(f"Desempenho do aluno: {simulacao.output['desempenho']:.2f}%")

desempenho.view(sim=simulacao)
plt.show(block=True)

input("Pressione ENTER para sair...")