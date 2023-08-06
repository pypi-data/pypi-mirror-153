from geezlit.style.base import BaseLit


class IPALit(BaseLit):
    """Ge'ez transliteration based IPA"""

    NAME = "ipa"

    def __init__(self):
        super().__init__()
