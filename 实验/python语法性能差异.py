

def a():
    """
    三元运算符和条件判断语句。
    """
    def conditional_operator(x:int)->str:
        return "True" if x%2 == 0 else "False"
    
    def conditional_statement(x:int)->str:
        if x%2 == 0:
            return "True"
        else:
            return "False"
        
    