"""
modular.py

Matemática Discreta - IMAT
ICAI, Universidad Pontificia Comillas

Grupo: GP23A
Integrantes:
    - María Caballo Calderón
    - Lucas García Cucala

Descripción:
Librería para la realización de cálculos y resolución de problemas de aritmética modular.
"""

from typing import Tuple, List, Dict

class IncompatibleEquationError(Exception):
    pass

# EJERCICIO 1
def es_primo(n: int) -> bool:
    """ Reciba un entero n y devuelva verdadero si es un número primo y falso en caso contrario
    Args:
        n (int): Entero
    
    Returns:
        true si el entero es un número primo.
        false en caso contrario.

    Raises: None

    Examples:
        es_primo(5)=True
        es_primo(4)=False
    """

    # los números menores que 2 no son primos
    if n < 2:
        return False

    # primero comprobamos algunos primos pequeños
    lista_primos = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41]

    for primo in lista_primos:
        if n % primo == 0:
            return n == primo

    # separamos numero - 1 en una parte impar y una potencia de 2
    parte_impar = n - 1
    veces_divisible_entre_dos = 0

    while parte_impar % 2 == 0:
        parte_impar = parte_impar // 2
        veces_divisible_entre_dos += 1

    # aplicamos Miller-Rabin
    for base in lista_primos:
        resultado = potencia_mod_p(base, parte_impar, n)

        # comprobamos si esta base pasa directamente la prueba
        pasa_prueba = (resultado == 1 or resultado == n - 1)
        contador = 0

        # vamos elevando al cuadrado hasta comprobar si aparece numero - 1
        while contador < veces_divisible_entre_dos - 1 and not pasa_prueba:
            resultado = (resultado * resultado) % n

            # si obtenemos numero - 1, esta base pasa la prueba
            if resultado == n - 1:
                pasa_prueba = True

            contador += 1
        # si alguna base no pasa la prueba, el número no es primo
        if not pasa_prueba:
            return False
    # si supera todas las pruebas, es primo
    return True


# EJERCICIO 2
def lista_primos(a, b) -> List[int]:
    """ Recibe dos enteros a y b y devuelva la lista de números primos en el intervalo [a, b)

    Args:
        a (int): Elemento inicial del intervalo (incluido)
        b (int): Elemento final del intervalo (no incluido)
    
    Returns:
        List[int]: lista ordenada de primos mayores o iguales que a y menores que b.

    Raises: None
    
    Examples:
        lista_primos(1,11)=[2,3,5,7]
    """
    primos_encontrados = []

    # añadimos el 2 aparte porque es el único primo par
    if a <= 2 and 2 < b:
        primos_encontrados.append(2)
        a = 3

    # si empezamos en un número par, pasamos al siguiente impar
    if a % 2 == 0:
        a += 1

    # recorremos solo los números impares del intervalo
    for numero in range(a, b, 2):
        if es_primo(numero):
            primos_encontrados.append(numero)

    return primos_encontrados


# EJERCICIO 3
def factorizar(n: int) -> Dict[int, int]:
    """ Recibe  un entero n y devuelve un diccionario cuyas claves son los primos que dividen a n y sus valores los
    correspondientes exponentes en la descomposición en producto de factores primos de n.

    Args:
        n (int): Entero que se desea factorizar.
    
    Returns:
        Dict[int,int]: Diccionario en el que las claves son primos positivos p_i que dividen a n y, para cada p_i,
            su valor asociado es el máximo exponente e_i tal que p_i^(e_i) divide a n. Si n=0, devuelve un diccionario vacío.

    Raises: None

    Examples:
        factorizar(12)={2: 2, 3: 1}
        factorizar(0)={}
    """
    # casos especiales de factorización
    if n in (-1, 0, 1):
        return {}
    numero_restante = abs(n)
    factores = {}

    # si el número ya es primo, no hace falta seguir buscando
    if es_primo(numero_restante):
        factores[numero_restante] = 1
        return factores

    # comprobamos primero los factores 2 y 3
    for primo in (2, 3):
        exponente = 0

        while numero_restante % primo == 0:
            exponente += 1
            numero_restante = numero_restante // primo

        if exponente > 0:
            factores[primo] = exponente

    # después probamos posibles factores de la forma 6k - 1 y 6k + 1
    posible_factor = 5

    while posible_factor * posible_factor <= numero_restante:
        for divisor in (posible_factor, posible_factor + 2):
            exponente = 0

            while numero_restante % divisor == 0:
                exponente += 1
                numero_restante = numero_restante // divisor

            if exponente > 0:
                factores[divisor] = exponente

        posible_factor += 6

    # si al final queda un número mayor que 1, también es un factor primo
    if numero_restante > 1:
        factores[numero_restante] = 1

    return factores


# EJERCICIO 4
def mcd(a: int, b: int) -> int:
    """ Calcula el máximo común divisor de dos enteros a y b.

    Args:
        a (int): Primer entero.
        b (int): Segundo entero.
    
    Returns:
        int: devuelve el máximo común divisor de a y b

    Raises: None

    Examples:
        mcd(10,15)=5
    """
    # usar Bézout no sería lo suficientemente rápido debido a los altos niveles de recursividad
    #
    a = abs(a)
    b = abs(b)
    
    # empleamos el algoritmo de Euclides clásico por divisiones sucesivas (empleado en clase)
    while b != 0:
        resto = a % b
        a = b
        b = resto

    return a

def bezout(n:int, m:int) -> Tuple[int,int,int]:
    """ Calcula el máximo común divisor d de dos enteros a y b junto con dos enteros x e y tales que
            d=ax+by

    Args:
        a (int): Primer entero.
        b (int): Segundo entero.
    
    Returns: (d,x,y)
        d (int): Máximo común divisor.
        x (int): Coeficiente de a.
        y (int): Coeficiente de b.

    Raises: None

    Examples:
        bezout(6,10)=(2,2,-1)
    """

    # caso base (cuando el segundo número es 0)
    if m == 0:
        if n >= 0:
            return n, 1, 0
        else:
            return -n, -1, 0

    # aplicamos Bézout con el resto de la división
    mcd_resultado, coeficiente1_anterior, coeficiente2_anterior = bezout(m, n % m)

    # calculamos los coeficientes correspondientes a n y m
    coeficiente1 = coeficiente2_anterior
    coeficiente2 = coeficiente1_anterior - (n // m) * coeficiente2_anterior

    return mcd_resultado, coeficiente1, coeficiente2

# EJERCICIO 5, OPCIONAL
def mcd_n(nlist: List[int]) -> int:
    """ Dados una lista de enteros, devuelve el máximo divisor común a todos ellos.

    Args:
        nList (List[int]): Lista de enteros.        
    
    Returns:
        int: devuelve el máximo entero que divide a todos los enteros de la lista.

    Raises: None

    Examples:
        mcd([4,10,14])=2
    """
    # si la lista está vacía, devolvemos 0
    if len(nlist) == 0:
        return 0
    # empezamos tomando como mcd el primer número de la lista
    resultado_mcd = nlist[0]

    # vamos calculando el mcd con cada número de la lista
    for numero in nlist[1:]:
        resultado_mcd = mcd(resultado_mcd, numero)
    return resultado_mcd


def bezout_n(nlist:List[int])->Tuple[int,List[int]]:
    #Opcional
    """ Dada una lista de enteros [a_1,...,a_n], devuelve el máximo divisor común d a todos ellos y una
    lista de coeficientes [x_1,...,x_n] tal que
        d=a_1*x_1+...a_n*x_n

    Args:
        nList (List[int]): Lista de enteros.        
    
    Returns: (d,X)
        d (int): Máximo entero que divide a todos los enteros de la lista.
        X (List[int]): Lista de coeficientes [x_1,...,x_n].

    Raises: None

    Examples
        bezout_n([4,10,14])=(2,[-2,1,0])
    """
    if len(nlist) == 0:
        return 0, []

    d = nlist[0]
    coeficientes = [1]

    for n in nlist[1:]:
        d_nuevo, x, y = bezout(d, n)

        for i in range(len(coeficientes)):
            coeficientes[i] = coeficientes[i] * x

        coeficientes.append(y)
        d = d_nuevo

    return d, coeficientes


# EJERCICIO 6
def coprimos(n: int, m: int) -> bool:
    """ Determina si dos enteros son coprimos.

    Args:
        a (int): Primer entero.
        b (int): Segundo entero.
    
    Returns:
        bool: Verdadero si son coprimos y falso si no.

    Raises: None

    Examples:
        coprimos(14,20)=False
        coprimos(14,15)=True
    """
    divisor = mcd(n,m)

    # si el mcd es 1, los dos números son coprimos
    return divisor == 1


def potencia_mod_p(base: int, exp: int, p: int) -> int:
    """ Calcula potencias módulo p.

    Args:
        base (int): Base de la potencia.
        exp (int): Exponente al que se eleva la base.
        p (int): Módulo.
    
    Returns:
        int: Resto de dividir base^exp módulo p.

    Raises:
        ZeroDivisionError: Si el módulo es 0 o si la base y el exponente
        son ambos 0 al mismo tiempo.

    Examples:
        potencia_mod_p(2,3,7)=1
    """
    # el módulo no puede ser 0
    if p == 0:
        raise ZeroDivisionError("El módulo no puede ser 0")
    # 0 elevado a 0 no está definido
    if base == 0 and exp == 0:
        raise ZeroDivisionError("0^0 no está definido")
    resultado = 1
    base_reducida = base % p

    # vamos reduciendo el exponente 
    while exp > 0:

        # si el exponente es impar, multiplicamos por la base
        # exponente & 1 equivale a exponente % 2 == 1 pero más rápido
        if exp & 1:
            resultado = (resultado * base_reducida) % p

        # elevamos la base al cuadrado y dividimos el exponente entre 2
        base_reducida = (base_reducida * base_reducida) % p
        # exp >> 1 equivale a exp // 2 pero más rápido a nivel de bits
        exp = exp >> 1

    return resultado % p

# EJERCICIO 8
def inversa_mod_p(n: int, p: int) -> int:
    """ Calcula la inversa de un número n módulo p.

    Args:
        n (int): Número que se desea invertir
        p (int): Módulo.
    
    Returns:
        int: Entero x entre 0 y p-1 tal que n*x es congruente con 1 módulo p.

    Raises:
        ZeroDivisionError: Si el módulo es 0 o si n no es invertible módulo p.
    
    Examples:
        inversa_mod_p(2,7)=4
    """

    # el módulo no puede ser 0
    if p == 0:
        raise ZeroDivisionError("El módulo no puede ser 0")
    # calculamos el mcd y los coeficietnes de Bézout
    divisor, coeficiente_n, coeficiente_p = bezout(n, p)

    # solo existe inversa si el mcd de n y p es 1
    if divisor != 1:
        raise ZeroDivisionError("n no es invertible módulo p")
    # el coeficiente de n es su inversa módulo p
    return coeficiente_n % p


# EJERCICIO 9
def euler(n: int) -> int:
    """ Calcula la función phi de Euler de un entero positivo n, es decir, cuenta cúantos enteros positivos
    menores que n son coprimos con n.

    Args:
        n (int): Número entero positivo.
    
    Returns:
        int: Función phi de Euler de n.

    Raises: None

    Examples:
        euler(7)=6
        euler(15)=8
    """
    # recorremos los factores primos distintos de n
    for primo in factorizar(n):
        # aplicamos la fórmula de Euler para cada factor primo
        n = n // primo * (primo - 1)
    return n


# EJERCICIO 10
def legendre(n: int, p: int) -> int:
    """ Dado un entero n y un número primo p, calcula el símbolo de Legendre de n módulo p.

    Args:
        n (int): Número entero.
        p (int): Número primo.
    
    Returns:
        int: Símbolo de Legendre de Euler de n módulo p:
            0 si es múltiplo de p
            1 si es un cuadrado perfecto (distinto de 0), módulo p
            -1 en caso contrario.

    Raises:
        ZeroDivisionError: Si el módulo p es 0.

    Examples:
        legendre(2,5)=-1
        legendre(2,7)=1
        legendre(10,5)=0
    """
    # el módulo no puede ser 0
    if p == 0:
        raise ZeroDivisionError("El módulo no puede ser 0")
    # si n es múltiplo de p Legendre vale 0
    if n % p == 0:
        return 0
    # si el módulo es 2 y n es impar el resultado es 1
    if p == 2:
        return 1

    # aplicamos el criterio de Euler
    resultado = potencia_mod_p(n, (p - 1) // 2, p)

    # comprobamos si n tiene raíz cuadrada módulo p
    if resultado == 1:
        return 1
    return -1


# EJERCICIO 11
def resolver_sistema_congruencias(alist: List[int], blist: List[int], plist: List[int]) -> Tuple[int, int]:
    """ Dadas tres listas de números enteros [a_1,...,a_n], [b_1,...,b_n] y [p_1,...,p_n], resuelve el sistema de congruencias

    a_i * x = b_i (mod p_i)   i=1,...,n

    devolviendo un entero r y un módulo m tales que las soluciones del sistema corresponden a todos los enteros

    x congruentes con r módulo m.

    Raises:
        IncompatibleEquationError: Si el sistema no tiene solución.
    """
    # comprobamos que las tres listas tengan la misma longitud
    if len(alist) != len(blist) or len(alist) != len(plist):
        raise ValueError("Las tres listas deben tener la misma longitud")
    # el sistema debe tener al menos una ecuación
    if len(alist) == 0:
        raise ValueError("El sistema no puede estar vacío")

    restos = []
    modulos = []
    # resolvemos cada ecuación del sistema por separado
    for posicion in range(len(alist)):
        coeficiente = alist[posicion]
        termino = blist[posicion]
        modulo = plist[posicion]

        if modulo == 0:
            raise ValueError("El módulo no puede ser 0")

        modulo = abs(modulo)# trabajamos siempre con módulos positivos
        divisor = mcd(coeficiente, modulo)

        if termino % divisor != 0: # si el mcd no divide al término independiente, no hay solución
            raise IncompatibleEquationError

        coeficiente = coeficiente // divisor
        termino = termino // divisor
        modulo = modulo // divisor

        if modulo != 1: # si el módulo es 1, esta ecuación no añade ninguna condición
            inversa = inversa_mod_p(coeficiente, modulo)
            resto = (termino * inversa) % modulo
            restos.append(resto)
            modulos.append(modulo)

    if len(modulos) == 0:
        return 0, 1

    # empezamos con la primera congruencia
    resto_actual = restos[0]
    modulo_actual = modulos[0]
    posicion = 1

    # juntamos las congruencias usando el Teorema Chino del Resto
    # los módulos se suponen coprimos dos a dos
    while posicion < len(modulos):
        siguiente_resto = restos[posicion]
        siguiente_modulo = modulos[posicion]

        inversa = inversa_mod_p(modulo_actual, siguiente_modulo)
        diferencia = siguiente_resto - resto_actual
        multiplicador = (diferencia * inversa) % siguiente_modulo
        nuevo_modulo = modulo_actual * siguiente_modulo
        resto_actual = (resto_actual + modulo_actual * multiplicador) % nuevo_modulo

        modulo_actual = nuevo_modulo
        posicion += 1
    return resto_actual, modulo_actual