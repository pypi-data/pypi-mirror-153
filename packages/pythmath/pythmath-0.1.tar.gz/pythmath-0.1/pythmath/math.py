pi = 3.141592653589793
e = 2.718281828459045


def absolute(x):
    """
    Gets the absolute value of x, if negative it will be positive.

    :param x: Value of x to get its absolute value in positive.
    :return: Returns absolute value of x in positive
    """
    if x <= 0:
        return x * -1
    return x * 1


def area_circle(r):
    """
    Calculate the area of circle from given radius.

    :param r: Radius of a circle.
    :return: Returns the area of a circle.
    """
    return float(pi * power(r, 2))


def area_rect(a, b):
    """
    Calculates the area of rectangle from given points or sides.

    :param a: Side 'a' of a rectangle.
    :param b: Side 'b' of a rectangle.
    :return: Returns the area of a rectangle.
    """
    return float(a * b)


def perimeter_rect(a, b):
    """
    Calculates the perimeter of a rectangle from given points or sides.

    :param a: Side 'a' of a rectangle.
    :param b: Side 'b' of a rectangle.
    :return: Returns the area of a rectangle.
    """
    return float(2 * (a + b))


def area_square(side):
    """
    Calculates the area of a square from given side, a square has four equal sides,
    therefore it takes only one side to calculate its area.

    :param side: Side of a square.
    :return: Area of a square
    """
    return float(side * side)


def area_triangle(a, b, c):
    """
    Calculates the area of a triangle from three sides of a triangle.

    :param a: First side of a triangle.
    :param b: Second side of a triangle.
    :param c: Third side of a triangle.
    :return: Area of a triangle.
    """
    s = (a + b + c) / 2
    return square_root((s*(s-a)*(s-b)*(s-c)))


def power(a, b):
    """
    Calculates the power x**y (x to the power of y).

    :param a: Base number
    :param b: Exponent Number or power value
    :return: Return x**y (x to the power of y).
    """
    return float(pow(a, b))


def square_root(a):
    """
    Calculates the square root of a number

    :param a: Number Value
    :return: Square Root of a number to which the square root will be calculated
    """
    return float(a ** (1 / 2))


def cube_root(a):
    """
    Calculates cube root of a number

    :param a: Number value to which the cube root will be calculated
    :return: Cube root of a number
    """
    return float(a ** (1 / 3))


def calc_lcm(a, b):
    """
    Calculate The Least Common Multiple of two numbers.

    :param a: First Number
    :param b: Second Number
    :return: The Least Common Multiple of two numbers
    """
    if a > b:
        greater = a
    else:
        greater = b

    while True:
        if (greater % a == 0) and (greater % b == 0):
            lcm = greater
            break
        greater += 1

    return float(lcm)


def calc_gcd(a, b):
    """
    Calculate the Greatest Common Divisor of two numbers.

    :param a: First Number
    :param b: Second Number
    :return: Greatest Common Divisor
    """
    if a > b:
        smaller = b
    else:
        smaller = a
    for i in range(1, smaller + 1):
        if (a % i == 0) and (b % i == 0):
            gcd = i
    return float(gcd)


def deg_to_rad(deg):
    """
    Convert angle x from degrees to radians.

    :param deg: angle in degrees.
    :return: Degrees to Radians.
    """
    return deg * pi / 180


def rad_to_deg(rad):
    """
    Convert angle x from radians to degrees.

    :param rad: angle in radians.
    :return: Radians to Degrees.
    """
    return rad * 180 / pi


def cos(x):
    """
    Calculates the cosine of x in radians.

    :param x: Value of x to be passed in cos(x) function.
    :return: Cosine of x in radians form.
    """
    return (e ** (x * 1j)).real


def cosd(x):
    """
    Calculates the cosine of x in degrees.

    :param x: Value of x to be passed in cosd(x) function.
    :return: Cosine of x in degrees form.
    """
    return cos(x * pi / 180)


def cot(x):
    """
    Calculates the cotangent of x in radians.

    :param x: Value of x to be passed in cot(x) function.
    :return: Cotangent of x in radians form.
    """
    return cos(x) / sin(x)


def cotd(x):
    """
    Calculates Cotangent of x in degrees.

    :param x: Value of x to be passed in cotd(x) function.
    :return: Cotangent of x in degrees form.
    """
    return cot(x * pi / 180)


def cosh(x):
    """
    Calculates the hyperbolic cosine of x in radians format.

    :param x: Value of x to be passed in cosh(x) function.
    :return: Hyperbolic cosine of x in radians format.
    """
    return (power(e, x) + power(e, -x)) / 2


def sin(x):
    """
    Calculates the sine of x in radians format.

    :param x: Value of x to be passed in sin(x) function.
    :return: Sine of x in radians.
    """
    return (e ** (x * 1j)).imag


def sind(x):
    """
    Calculates the sine of x in degrees format.

    :param x: Value of x to be passed in sind(x) function.
    :return: Sine of x in degrees.
    """
    return sin(x * pi / 180)


def sec(x):
    """
    Calculates the secant of x in radians format.

    :param x: Value of x to be passed in sec(x) function.
    :return: Secant of x in radians.
    """
    return 1 / cos(x)


def secd(x):
    """
    Calculates the secant of x in degrees format.

    :param x: Value of x to be passed in secd(x) function.
    :return: Secant of x in degrees.
    """
    return sec(x * pi / 180)


def cosec(x):
    """
    Calculates the cosecant of x in radians format.

    :param x: Value of x to be passed in cosec(x) function.
    :return: Cosecant of x in radians format.
    """
    return 1 / sin(x)


def cosecd(x):
    """
    Calculates the cosecant of x in degrees format.

    :param x: Value of x to be passed in cosecd(x) function.
    :return: Cosecant of x in degrees format.
    """
    return cosec(x * pi / 180)


def sinh(x):
    """
    Calculates the hyperbolic sine of x in radians format.

    :param x: Value of x to be passed in sinh(x) function.
    :return: Hyperbolic sine of x in radians.
    """
    return (power(e, x) - power(e, -x)) / 2


def tan(x):
    """
    Calculates the tangent of x in radians format.

    :param x: Value of x to be passed in tan(x) function.
    :return: Tangent of x in radians.
    """
    return sin(x) / cos(x)


def tand(x):
    """
    Calculates the tangent of x in degrees format.

    :param x: Value of x to be passed in tand(x) function.
    :return: Tangent of x in degrees.
    """
    return tan(x * pi / 180)


def tanh(x):
    """
    Calculates the hyperbolic tangent of x in radians format.

    :param x: Value of x to be passed in tanh(x) function.
    :return: Hyperbolic tangent of x in radians.
    """
    return sinh(x) / cosh(x)


def fact(num):
    """
    Find factorial of x.

    Raise a ValueError if x is negative or non-integral.

    :param num: Number of which you want to find it's factorial
    :return: Factorial of a number 'x'.
    """
    fact = 1
    if num < 0:
        raise ValueError("Sorry, factorial does not exist for negative numbers")
    if not isinstance(num, int):
        raise ValueError("Number is non integral")
    else:
        for i in range(1, num + 1):
            fact = fact * i
        return float(fact)


def isinteger(x):
    """
    Check whether the number is integral or non-integral.

    :param x: Number to check integral or non-integral.
    :return: True if number is integral otherwise False.
    """
    return isinstance(x, int)


def iseven(x):
    """
    Check whether the number is an even number.

    :param x: Number to check even or not.
    :return: True if number is even otherwise False.
    """
    if (x % 2) == 0:
        return True
    else:
        return False


def isodd(x):
    """
    Check whether the number is an odd number.

    :param x: Number to check odd or not.
    :return: True if number is odd otherwise False.
    """
    if (x % 2) != 0:
        return True
    else:
        return False


def isprime(x):
    """
    Check whether the number is a prime number.

    :param x: Number to check prime or not.
    :return: True if number is prime otherwise False.
    """
    if x > 1:
        for n in range(2, x):
            if (x % n) == 0:
                return False
        return True
    else:
        return False


def intsqrt(x):
    """
    Gets the integer part of square root from input.

    :param x: Number to calculate its square root.
    :return: Returns the integer part of square root.
    """
    return floor(square_root(x))


def intcbrt(x):
    """
    Gets the integer part of cube root from input.

    :param x: Number to calculate its cube root.
    :return: Returns the integer part of cube root.
    """
    return floor(cube_root(x))


def ispositive(x):
    """
    Checks whether the number is positive or not.

    :param x: Number to check positive or not.
    :return: True if number is positive otherwise False.
    """
    if x > 0:
        return True
    else:
        return False


def isnegative(x):
    """
    Checks whether the number is negative or not.

    :param x: Number to check negative or not.
    :return: True if number is negative otherwise False.
    """
    if x < 0:
        return True
    else:
        return False


def iszero(x):
    """
    Checks whether the number is zero or not.

    :param x: Number to check zero or not.
    :return: True if number is zero otherwise False.
    """
    if x == 0:
        return True
    else:
        return False


def hypotenuse(x, y):
    """
    Calculates the hypotenuse of x and y

    :param x: Value of x
    :param y: Value of y
    :return: Returns the hypotenuse of x and y
    """
    return square_root(x ** 2 + y ** 2)


def floor(n):
    """
    Floors the number.

    :param n: Number you want to be floored.
    :return: Floor of the number
    """
    return int(n // 1)


def floatsum(numbers):
    """
    Calculates the accurate floating sum of values in a sequence or in list

    :param numbers: Numbers to calculate the floating sum
    :return: Accurate Floating Sum of numbers in a list
    """
    a = 0
    for num in numbers:
        a += num
    return float(a)


def floatabs(x):
    """
    Gets the absolute floating value of x.

    :param x: Number to get absolute floating value.
    :return: Absolute floating value of x.
    """
    return (x ** 2) ** 0.5


def ceil(n):
    """
    Find the ceiling of a number

    :param n: Number you want to be ceiled.
    :return: Ceiling of the number
    """
    return int(-1 * n // 1 * -1)


def remainder(num, divisor):
    """
    Find the remainder of two numbers.

    :param num: Number or Dividend
    :param divisor: Value of divisor
    :return: Remainder of two numbers.
    """
    return float(num - divisor * (num // divisor))


def euc_dist(x, y):
    """
    Finds the Euclidean Distance between two points x and y.

    :param x: First Point
    :param y: Second Point
    :return: Euclidean Distance between two points x and y.
    """
    return square_root(sum((px - py) ** 2 for px, py in zip(x, y)))


def exponential(x):
    """
    Finds the exponential of a specific number (e raised to the power of x).

    :param x: Number raise to the power of e
    :return: Exponential of a specific number (e raised to the power of x).
    """
    return power(e, x)
