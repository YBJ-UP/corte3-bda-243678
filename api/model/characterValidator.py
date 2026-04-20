def validateField(field: str) -> tuple[bool, str]: # hice esto en vez de any(char in hola for char in InvalidCharacters) por que no sé cómo sacarle el caracter inválido a eso
    InvalidCharacters = "<>/\;,.:-_+*~}{[]|°¬!#$%&()=?'¿¡"
    for c in field:
        if c in InvalidCharacters:
            return (False, c)
    return (True, "")