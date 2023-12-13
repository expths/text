class layer:
    # 图层类
    def __init__(self,level:int=0) -> None:
        self.level = level
    def set_level(self,level:int) -> None:
        self.level = level
    def get_level(self) -> int:
        return self.level
    def draw(self) -> None:
        pass
    def behavior(self) -> None:
        return None

def group(iter=[]) -> tuple:
    # 图层组 闭包
    li = list(iter)
    def draw() -> None:
        li.sort(key=lambda x:x.level)
        for layer in li:
            if layer.behavior():
                li.remove(layer)
                continue
            layer.draw()
    return (li,draw)

if __name__ == "__main__":
    pass