import numpy as np
import decimal

decimal.getcontext().prec = 50
dec_one = decimal.Decimal(1)
dec_hundred = decimal.Decimal(100)
dec_x = dec_one / dec_hundred

def one_divided_by(N):
    return np.float64(1.0 / N)


def loop_multiply(x, N):
    sum = np.float64(0)
    for _ in range(N):
        sum += x
    return sum


def main(N):
    x = one_divided_by(N)
    sum = loop_multiply(x, N)
    is_equal = x == sum

    print(f"Nの数値: {N}")
    print(f"sumの数値: {sum}")
    print(f"判定結果: {is_equal}")


main(10)
main(30)
main(50)
main(100)
main(200)
