from random import random


class role:
    hp = 100
    def __init__(self,name:str,e_name:str,q_name:str) -> None:
        self.name = name
        self.e = e_name
        self.q = q_name
    def _attack(self,p,skill_name:str)->None:
        damage = int(10*random())
        p.hp -= damage
        print(self.name+"使用了"+skill_name)
        print("对"+p.name+f"造成了{damage}点伤害！")
    def __sub__(self,p)->None:
        self._attack(p,self.e)
    def __rshift__(self,p)->None:
        self._attack(p,self.q)
#
kq = role("刻晴","星斗归位","天街巡游")
me = role("爷","风压剑","龙卷风")
