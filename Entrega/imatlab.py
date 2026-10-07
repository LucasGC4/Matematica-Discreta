"""
imatlab.py

Matemática Discreta - IMAT
ICAI, Universidad Pontificia Comillas

Grupo: GP23A
Integrantes:
    - María Caballo Calderón
    - Lucas García Cucala

Descripción:
Sistema interactivo IMAT-LAB de resolución de ecuaciones en aritmética modular.

Interfaz de acceso interactivo o por lotes a la librería modular.py. Si este
script se ejecuta sin parámetros, lanza la interfaz en modo interactivo.
"""

from typing import List, Optional, TextIO, Tuple
import sys

import modular


def separar_nombre_y_datos(linea: str) -> Tuple[str, str]:
    #Separa el nombre del comando y sus argumentos

    linea = linea.strip()
    posicion = linea.find("(")

    if posicion <= 0:
        raise ValueError

    if linea[-1] != ")":
        raise ValueError

    nombre = linea[:posicion].strip() 
    argumentos = linea[posicion + 1:-1].strip()

    return nombre, argumentos


def leer_enteros(argumentos: str, cantidad=None) -> List[int]:
    #Convietre los argumentos separados por comas en una lista de enteros
    valores = []
    partes = argumentos.split(",")

    i = 0
    while i < len(partes):
        parte = partes[i].strip()

        if parte == "":
            raise ValueError

        valores.append(int(parte))
        i += 1

    if cantidad is not None and len(valores) != cantidad:
        raise ValueError

    return valores


def leer_sistema(argumentos: str) -> Tuple[List[int], List[int], List[int]]:
    #Convierte [a;b;p],[a;b;p],... en las tres listas del sistema

    if argumentos.strip() == "":
        raise ValueError

    ecuaciones = argumentos.split(",")

    lista_1 = []
    lista_2 = []
    lista_3 = []

    i = 0

    while i < len(ecuaciones):
        ecuacion = ecuaciones[i].strip()

        if ecuacion[0] != "[" or ecuacion[-1] != "]":
            raise ValueError

        ecuacion = ecuacion[1:-1] # para quitar los corchetes de la ecuación
        partes = ecuacion.split(";")

        if len(partes) != 3:
            raise ValueError

        if partes[0].strip() == "" or partes[1].strip() == "" or partes[2].strip() == "":
            raise ValueError

        a = int(partes[0].strip())
        b = int(partes[1].strip())
        p = int(partes[2].strip())

        lista_1.append(a)
        lista_2.append(b)
        lista_3.append(p)

        i += 1

    return lista_1, lista_2, lista_3


def comando_primo(argumentos: str) -> str:
    n = leer_enteros(argumentos, 1)[0]
    if modular.es_primo(n):
        return "Sí"
    else:
        return "No" 
    

def comando_primos(argumentos: str) -> str:
    a, b = leer_enteros(argumentos, 2)
    primos = modular.lista_primos(a, b)
    if not primos:
        return "NE"
    
    textos = []
    for p in primos: # pasa los primos a texto y los une separados por comas
        textos.append(str(p))
    return ", ".join(textos)


def comando_factorizar(argumentos: str) -> str:
    n = leer_enteros(argumentos, 1)[0]

    if n in (-1, 0, 1): # casos especiales a factorizar, devuelve directamnete el str
        return str(n)

    factores = modular.factorizar(n)
    textos = []

    for p in sorted(factores):
        texto = str(p) + ": " + str(factores[p])
        textos.append(texto)
    return ", ".join(textos)


def comando_mcd(argumentos: str) -> str:
    valores = leer_enteros(argumentos)

    if len(valores) == 1:
        return str(abs(valores[0])) # si solo hay un número, devuelve su valor absoluto

    if len(valores) == 2: # si hay dos, calcula el mcd entre los dos
        return str(modular.mcd(valores[0], valores[1]))

    # parte opcional, si hay más de dos números, calcula el mcd de todos
    return str(modular.mcd_n(valores))


def comando_coprimos(argumentos: str) -> str:
    a, b = leer_enteros(argumentos, 2)
    if modular.coprimos(a, b):
        return "Sí" 
    else:
        return "No"


def comando_pow(argumentos: str) -> str:
    base, exp, modulo = leer_enteros(argumentos, 3)

    if modulo == 0: # no se puede calcular módulo 0, devuelve No Existe
        return "NE"

    # si el exponente es >= 0, se calcula directamnete
    if exp >= 0:
        return str(modular.potencia_mod_p(base, exp, modulo))

    # para exponente negativo usamos la inversa modular
    if not modular.coprimos(base, modulo): # comprobamos si existe la inversa modular
        return "NE"

    inversa = modular.inversa_mod_p(base, modulo)
    return str(modular.potencia_mod_p(inversa, -exp, modulo))


def comando_inv(argumentos: str) -> str:
    n, p = leer_enteros(argumentos, 2)

    if p == 0: # si el módulo es 0, devuelve No Existe
        return "NE"

    if not modular.coprimos(n, p): # si n y p no son coprimos, tampoco tiene inversa modular
        return "NE"

    return str(modular.inversa_mod_p(n, p)) # en caso de ser posible, la calculamos


def comando_euler(argumentos: str) -> str:
    n = leer_enteros(argumentos, 1)[0]

    if n <= 0: # comprueba que sea positivo porque Euler no se puede hacer para enteros negativos
        raise ValueError("Euler necesita un entero positivo")

    return str(modular.euler(n))


def comando_legendre(argumentos: str) -> str:
    n, p = leer_enteros(argumentos, 2)

    if p == 0: # si p es 0, devuelve No Existe porque no tiene sentido trabajar con módulo 0
        return "NE"

    if not modular.es_primo(p): # como Legendre se define para módulos primos, comprueba que p lo sea, sino lanza un error
        raise ValueError("p debe ser primo")

    return str(modular.legendre(n, p))


def comando_resolver_sistema(argumentos: str) -> str:
    lista_1, lista_2, lista_3 = leer_sistema(argumentos)
    solucion, modulo = modular.resolver_sistema_congruencias(lista_1, lista_2, lista_3)
    return f"{solucion} (mod {modulo})"


def ejecutar_comando(linea: str) -> str:
    """Ejecuta un único comando de IMAT-LAB y devuelve su salida."""
    nombre, argumentos = separar_nombre_y_datos(linea)

    if nombre == "primo":
        return comando_primo(argumentos)
    if nombre == "primos":
        return comando_primos(argumentos)
    if nombre == "factorizar":
        return comando_factorizar(argumentos)
    if nombre == "mcd":
        return comando_mcd(argumentos)
    if nombre == "coprimos":
        return comando_coprimos(argumentos)
    if nombre == "pow":
        return comando_pow(argumentos)
    if nombre == "inv":
        return comando_inv(argumentos)
    if nombre == "euler":
        return comando_euler(argumentos)
    if nombre == "legendre":
        return comando_legendre(argumentos)
    if nombre == "resolverSistema":
        return comando_resolver_sistema(argumentos)

    return "NOP"


# ----------------
def run_commands(fin: TextIO, fout: TextIO):
    """Ejecuta, línea a línea, los comandos leídos de ``fin``.

    La ejecución termina al encontrar una línea vacía. Cada resultado se
    escribe en ``fout``. Una llamada incorrecta produce ``NOP`` y un problema
    correctamente planteado pero sin solución produce ``NE``.
    """
    interactivo = fin is sys.stdin and fout is sys.stdout

    for linea in fin:
        linea = linea.strip()

        if linea == "":
            break
        try:
            salida = ejecutar_comando(linea)
        except modular.IncompatibleEquationError:
            salida = "NE"
        except (ValueError, TypeError, ZeroDivisionError, OverflowError):
            salida = "NOP"

        fout.write(salida + "\n")

        if interactivo:
            fout.flush()


if __name__ == "__main__":
    if len(sys.argv) == 1:
        run_commands(sys.stdin, sys.stdout)

    elif len(sys.argv) == 3:
        try:
            with open(sys.argv[1], "r", encoding="utf-8") as fin:
                with open(sys.argv[2], "w", encoding="utf-8") as fout:
                    run_commands(fin, fout)
        except OSError as error:
            print(f"Error de fichero: {error}", file=sys.stderr)

    else:
        print(
            "Uso: python imatlab.py [fichero_entrada fichero_salida]",
            file=sys.stderr,
        )
