import time
from typing import *

def Print(content :Any , color:Union[int, str, hex]='white', end : Any ='\n', flush :bool =False, times :int =1, add :Union[int, float] =False, enumerate :bool =False) -> Any :
    # docstring for ezs_print
    """
    Printea un mensaje en la consola.
    color : Color del contenido (int : hexadecimal en int, str : "blue", hex : 0xFF0000)
    end : Caracter de fin de linea
    end : Final del contenido
    flush : Limpiar buffer interno
    times : Veces que se printea
    add : Suma al contenido (para contenido numerico)
    enumerate : Enumerar Las veces que se printea 
    """
    ezs_colors = {
        'red': '\033[91m',
        'green': '\033[92m',
        'yellow': '\033[93m',
        'blue': '\033[94m',
        'magenta': '\033[95m',
        'cyan': '\033[96m',
        'white': '\033[97m',
        'end': '\033[0m',
        'pink' : '\033[95m',
        'orange' : '\033[93m',
        'light_blue' : '\033[94m',
        'brown' : '\033[33m',
        'black' : '\033[30m',
        'gray' : '\033[37m',
        'light_green' : '\033[92m',
        'light_yellow' : '\033[93m',
        'light_magenta' : '\033[95m',
        'light_red': '\033[91m'
    }

    # check if color is hex

    # convert color from string to integer
    if color is not None:
        # check if is a string    
        if isinstance(color, str):
            # check if is a valid color
            if color in ezs_colors:
                color = ezs_colors[color]
                            
            else:
                color = ezs_colors['white']
                            
        # if is not a string, check if is an integer
        elif isinstance(color, int):       
            # convert from integer to hex (0x)
            color = hex(color)
            # remove 0x from hex
            color = color[2:]            
            # convert to rgb
            color = tuple(int(color[i:i+2], 16) for i in (0, 2, 4))
            color = f'\033[38;2;{color[0]};{color[1]};{color[2]}m'
            
    else:
        # set color to white
        color = ezs_colors['white']

    for i in range(times):
        if enumerate:
            print(f'{i+1} - ', end='')
        print(f'{color}{content}{ezs_colors["end"]}', end=end, flush=flush)
        if add != False:
            # if content is numeric, add
            if isinstance(content, int) or isinstance(content, float):
                content += add
                
    return content

# convert number to str but format number to roman
def convert_num(number : Union[float, int], type="simple") -> Union[str, int, float]:
    """
    Convierte un numero a una o otro tipo.
    type : Tipo de conversion
    number : Numero a convertir
     
    Tipos de conversion:
    simple : Convierte a simple (10000 -> 10K)
    binary : Convierte a binario (10 -> 0b1010)
    hex : Convierte a hexadecimal (10 -> 0x0A)
    """
    type = type.lower()
    try:
        number = float(number) 
    except ValueError:
        raise "F1 : El numero no es valido"
    
    if type == "simple":
        number = int(number)
        if number < 1000:
            return number
        elif number < 1000000:
            return f'{number//1000}K'
        elif number < 1000000000:
            return f'{number//1000000}M'
        else:
            return f'{number//1000000000}B'

    elif type == "binary":
        return bin(int(number))[2:]

    elif type == "hex":
        return hex(int(number))[2:]
    
    else:
        raise "F3 : Tipo de conversion no valida"
        
# decorator to check time of function execution
def time_it(func):
    """
    Decorador para medir el tiempo de ejecucion de una funcion.
    """
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f'{func.__name__} : Tiempo de ejecucion: {end - start}')
        return end - start
    return wrapper


