from geezlit.style.base import BaseLit


class GeezIMELit(BaseLit):
    """Ge'ez transliteration based on the GeezIME keyboard"""

    NAME = "geezime"

    def __init__(self):
        super().__init__()
