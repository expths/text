

class A():

    @property
    def a(self):
        """
        使用property装饰器会产生一个property对象。

        被装饰函数作为getter方法被调用。

        property对象的setter是另一个装饰器，可以将被装饰函数定义为setter方法。
        """
        return "ABC"
    
    @a.setter
    def a(self,a):
        """
        被定义为元素的setter方法。

        注意：被装饰函数的名称必须和property对象一致。
        """
        print(a)


if __name__ == "__main__":
    an = A()
    print(an.a)
    an.a = 1
