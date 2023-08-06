def russion():
    Lang = ['Корней нет']
def english():
    Lang = ['No roots']
def init(Language):
    if Language == "ru":
        russion()
    if Language == "en":
        english()
        
def Pyth(cathetusX, cathetusY, Hypotenuse):
    if Hypotenuse == 0:
        hypo = cathetusX*cathetusX + cathetusY*cathetusY
        print(hypo ** (0.5))
    elif cathetusX == 0:
        cathetX = Hypotenuse*Hypotenuse - cathetusY*cathetusY
        print(cathetX ** (0.5))
    elif cathetusY == 0:
        cathetY = Hypotenuse*Hypotenuse - cathetusX*cathetusX
        print(cathetY ** (0.5))
def Discr(a,b,c):
    a = float(a)
    b = float(b)
    c = float(c)
    discr = b ** 2 - 4 * a * c
    if discr > 0:
        x1 = (-b + math.sqrt(discr)) / (2 * a)
        x2 = (-b - math.sqrt(discr)) / (2 * a)
        print("x1 = %.2f \nx2 = %.2f" % (x1, x2))
    elif discr == 0:
        x = -b / (2 * a)
        print("x = %.2f" % x)
    else:
        print("Корней нет")
def euler(n):
    r = n
    i = 2
    while i*i <= n:
        if n % i == 0:
            while n % i == 0:
                n //= i
            r -= r//i
        else:
            i += 1
    if n > 1:
        r -= r//n
    return r