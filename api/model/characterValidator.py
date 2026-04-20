class Validator:
    InvalidCharacters = "<>/\\;,.:-_+*~}{[]|°¬!#$%&()=?'¿¡"

    def validateField(self, field: str) -> tuple[bool, str]: # hice esto en vez de any(char in hola for char in InvalidCharacters) por que no sé cómo sacarle el caracter inválido a eso
        for c in field:
            if c in self.InvalidCharacters:
                return (False, c)
        return (True, "")
    
    def validateNum(self, field: int):
        print("hola")
