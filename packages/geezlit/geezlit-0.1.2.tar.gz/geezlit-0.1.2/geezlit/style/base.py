class BaseLit(object):
    """Base Ge'ez transliteration class"""

    NAME = "base"

    def __init__(self):
        self.he_int = 4608
        self.po_int = 4950
        self.ascii_rows = list(range(47))
        self.ascii_cols = list(range(8))
        self.ascii_cols_labial = list(range(8))
        self.geez_rows_labial = {9, 11, 17, 22, 24, 34, 36}
        self.geez_puncs = dict()

    def char_is_geez(self, char):
        """
        char must bee of length 1,
        else this will throw TypeError
        """
        return self.he_int <= ord(char) <= self.po_int

    def get_geez_row_col(self, char):
        cint = ord(char)
        assert self.he_int <= cint <= self.po_int
        col = cint % 8
        row = ((cint - col) - self.he_int) // 8
        return row, col

    def to_ascii(self, text):
        result = list()
        for char in text:
            try:
                if not self.char_is_geez(char):
                    result.append(self.geez_puncs.get(char, char))
                    continue
                row, col = self.get_geez_row_col(char)
                rtex = self.ascii_rows[row]
                if row in self.geez_rows_labial:
                    ctex = self.ascii_cols_labial[col]
                else:
                    ctex = self.ascii_cols[col]
                result.append(f"{rtex}{ctex}")
            except Exception as ex:
                print(f"Couldn't convert: '{char}'! {ex}")
                result.append(":|:")
        return "".join(result)
