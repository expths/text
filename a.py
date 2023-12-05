
def is_prime_number(x: int) -> bool:
    """检查输入的大于等于2的整数是否为质数"""
    if (x == 2) or (x == 3):
        return True
    if (x % 6 != 1) and (x % 6 != 5):
        return False
    for i in range(5, int(x ** 0.5) + 1, 6):
        if (x % i == 0) or (x % (i + 2) == 0):
            return False
    return True
         
def a(nl:list[int],exponent:int)->list:
    for a_number in nl:
        print(a_number)
        if (next_nl:=[number for number in [a_number + n * (10 ** exponent) for n in range(1,10)] if is_prime_number(number)]):
            a(next_nl,exponent+1)
    return None

print(a([5,7],1))