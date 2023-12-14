

class Ttype(type):
    """
    类似于枚举类型。用于数据追踪器自动管理数据。
    """
    pass


class Symbol(metaclass = Ttype):
    pass

class exchange(metaclass = Ttype):
    pass
