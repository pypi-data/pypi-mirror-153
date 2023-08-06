from geezlit.style.base import BaseLit


class MSERALit(BaseLit):
    """Ge'ez transliteration based modified SERA in HornMorpho"""

    NAME = "msera"

    def __init__(self):
        super().__init__()
