from operator import truediv
import re


def validar_rut(rut: str) -> bool:
    #Funcion para validar el RUT
    # 1. Limpiar el RUT: quitar puntos, guiones y pasar a mayúsculas
    rut_limpio = rut.replace(".", "").replace("-", "").upper()

    # 2. Validaciones básicas
    if len(rut_limpio) < 2:
        raise Exception("El rut ingresado es muy corto.")

    cuerpo = rut_limpio[:-1]  # La parte numérica
    dv_ingresado = rut_limpio[-1]  # El dígito verificador

    # El cuerpo debe contener solo números
    if not cuerpo.isdigit():
        raise Exception("Recuerda que el rut tiene que tener digitos...")

    # 3. Calcular el Dígito Verificador (Algoritmo Módulo 11)
    suma = 0
    multiplo = 2

    # Recorremos el cuerpo de derecha a izquierda
    for c in reversed(cuerpo):
        suma += int(c) * multiplo
        multiplo += 1
        if multiplo == 8:
            multiplo = 2

    resto = suma % 11
    resultado = 11 - resto

    # 4. Convertir el resultado al formato del DV
    if resultado == 11:
        dv_calculado = '0'
    elif resultado == 10:
        dv_calculado = 'K'
    else:
        dv_calculado = str(resultado)

    # 5. Comparar
    if dv_calculado == dv_ingresado:
        return True
    else:
        raise Exception("El rut ingresado no es valido.")


def validar_email(email: str) -> bool:
    patron = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if re.match(patron, email):
        return True
    else:
        raise Exception("El email ingresado no es valido.")