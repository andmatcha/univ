# n!の計算
def fact(n):
    if n == 0:
        return 1
    else:
        return n * fact(n - 1)

number_list = range(0, 21)

for i in number_list:
    print(str(i) + "! = " + str(fact(i)))

# 最大公約数の計算
def gcd(a, b):
    if b == 0:
        return a
    else:
        return gcd(b, a % b)
