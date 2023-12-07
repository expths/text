def A(cls:type):
    def B(b):
        if type(b)==cls:
            return b
        return cls(b)
    B.type = cls
    for key in cls.__dict__:
        if type(cls.__dict__[key])==staticmethod:
            B.__dict__[key] = cls.__dict__[key]
    return B
@A
class B:
    def __init__(self,a) -> None:
        print("class B")
        self.a = a
    @staticmethod
    def func():
        print("func")

a = B(123)
b = B(a)
B.func()
