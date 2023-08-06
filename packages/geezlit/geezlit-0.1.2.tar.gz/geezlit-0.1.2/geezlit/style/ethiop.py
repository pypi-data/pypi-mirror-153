from geezlit.style.base import BaseLit


class EthiopLit(BaseLit):
    """Ge'ez transliteration for `ethiop` the `babel` package for Latex"""

    NAME = "ethiop"

    def __init__(self):
        super().__init__()
        self.ascii_rows = [
            "h",
            "l",
            ".h",
            "m",
            "’s",
            "r",
            "s",
            "^s",
            "q",
            "q",
            ".q",
            ".q",
            "b",
            "v",
            "t",
            "^c",
            "_h",
            "_h",
            "n",
            "~n",
            "’",
            "k",
            "k",
            "_k",
            "_k",
            "w",
            "‘",
            "z",
            "^z",
            "y",
            "d",
            ".d",
            "^g",
            "g",
            "g",
            ".g",
            ".t",
            "^C",
            ".p",
            ".s",
            ".c",
            "f",
            "p",
            "’q",
            "’k",
            "’h",
            "’g",
        ]
        self.ascii_cols = ["a", "u", "i", "A", "E", "e", "o"]
        self.ascii_cols_labial = ["ua", "=", "ui", "uA", "uuE", "ue", "="]
        self.geez_rows_labial = {9, 11, 17, 22, 24, 34, 36}
        self.geez_puncs = {
            "።": "::",
            "፡": ":",
            "፣": ",",
            "፤": ";",
            "፥": ":=",
            "፦": ":-",
            "፧": "|",
        }
