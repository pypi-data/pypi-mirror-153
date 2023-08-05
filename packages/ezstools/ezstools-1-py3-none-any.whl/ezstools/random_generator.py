import random
from typing import *

#random password generator
def get_random_password(min_length :int = 8, max_length :int = 8, numbers :bool = True, letters :bool = True, special_characters :bool = True, caps :bool = True) -> str:
    # docstring for get_random_password
    """
    Genera una contraseña aleatoria de longitud aleatoria entre min_length y max_length
    numbers : Sirve para incluir numeros en la contraseña
    letters : Sirve para incluir letras en la contraseña
    special_characters : Sirve para incluir caracteres especiales en la contraseña
    caps : Sirve para incluir mayusculas en la contraseña
    """
    
    if min_length > max_length:
        max_length = min_length

    if numbers == False and letters == False and special_characters == False:
        raise "RG0 : Necesitas al menos un parametro activo - 'numbers', 'letters', 'symbols' "
    elif  min_length <= 0 or max_length <= 0:
        raise "RG1 : La longitud debe ser mayor a cero"

    _numbers = []
    _letters = []
    _symbols = []
    _caps = []
    
    if numbers == True:
        _numbers = list("1234567890")
    elif numbers == False:
        _numbers == list("")

    if letters == True:
        _letters = list("abcdefghijklmnñopqrstuvwyz")
    elif letters == False:
        _letters == list("")

    if special_characters == True:
        symbols = list("~!@#$%^&*()_+-=[]{}|;:<>,./")
    elif special_characters == False:
        symbols == list("")

    if caps == True:
        _caps = list("ABCDEFGHIJKLMNÑOPQRSTUVWXYZ")
    elif caps == False or _letters == False:
        _caps = list("")

    all_chars = _numbers + _letters + symbols + _caps

    #generate random password
    password = []
    for i in range(random.randint(min_length, max_length)):
        password.append(all_chars[random.randint(0, len(all_chars)-1)])
    
    password = ''.join(password)
    return password
