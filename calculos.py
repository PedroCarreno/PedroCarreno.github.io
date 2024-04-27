import math
import random


# Función para simular el ausentismo durante un período de tiempo
# En el archivo calculos.py
def simular_ausentismo(N_dias, valores_tabla_ausentados, venta, costos, remuneracion, i, j, nomina):
    resultados_simulacion = []

    OPERADORES_MAX = nomina
    OPERADORES_MIN = 20
    BENEFICIO_MAX = venta - costos
    COSTO_X_OPERADOR = remuneracion

    beneficio_acum = 0
    cant_dias_operados = 0

    for k in range(N_dias):
        obreros_ausentes, rnd = generarCantObrerosAusentesRND(valores_tabla_ausentados)

        if (OPERADORES_MAX - obreros_ausentes) >= OPERADORES_MIN:
            cant_dias_operados += 1
            beneficio_x_dia = BENEFICIO_MAX - (COSTO_X_OPERADOR * (OPERADORES_MAX - obreros_ausentes))
            beneficio_acum += beneficio_x_dia
            beneficio_promedio = beneficio_acum / (k + 1)

        else:
            beneficio_x_dia = 0
            beneficio_acum += beneficio_x_dia
            beneficio_promedio = beneficio_acum / (k + 1)

        # Doy formato para que se lea 1.000.000,50 sino es muy complicado de leer 1000000
        beneficio_total_formateado = '{:,.2f}'.format(beneficio_acum).replace(",", "*").replace(".", ",").replace("*",
                                                                                                                   ".")
        # Redondear el beneficio promedio a dos decimales
        beneficio_promedio_redondeado = round(beneficio_promedio, 2)

        if (i - 1) <= k < j or k == (N_dias - 1):
            resultados_simulacion.append({
                'reloj': (k + 1),  # Aquí deberías poner el valor correspondiente para cada columna
                'rnd': rnd,
                'CantObrerosAusentes': obreros_ausentes,
                'CantOperadores': (OPERADORES_MAX - obreros_ausentes),
                'Beneficio': beneficio_x_dia,
                'BeneficioAcum': beneficio_total_formateado,
                'BeneficioPromedio': beneficio_promedio_redondeado
            })

    indice_productividad = (cant_dias_operados / N_dias) * 100
    return resultados_simulacion, indice_productividad


def generarCantObrerosAusentesRND(ls):
    rnd = random.random()
    cant = rnd * 100

    for i in range(5, 0, -1):
        if cant >= sum(ls[:i]):
            return i, round(rnd, 2)

    return 0, round(rnd, 2)


    """if (cant >= sum(ls[0:5])):
        return 5, round(rnd,2)
    elif (cant >= sum(ls[0:4])):
        return 4, round(rnd,2)
    elif (cant >= sum(ls[0:3])):
        return 3, round(rnd,2)
    elif (cant >= sum(ls[0:2])):
        return 2, round(rnd,2)
    elif (cant >= sum(ls[0:1])):
        return 1, round(rnd,2)
    else:
        return 0, round(rnd,2)
    """
