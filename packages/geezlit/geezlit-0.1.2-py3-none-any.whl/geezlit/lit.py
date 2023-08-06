from .style.base import BaseLit
from .style.ethiop import EthiopLit


def get_liter(name):
    lit_classes = {BaseLit, EthiopLit}
    for cls in lit_classes:
        if name == cls.NAME:
            return cls()
    raise TypeError("Unkown GeezLit style: " + name)


def geezlit(text, style="ethiop"):
    lit = get_liter(name=style)
    return lit.to_ascii(text)
