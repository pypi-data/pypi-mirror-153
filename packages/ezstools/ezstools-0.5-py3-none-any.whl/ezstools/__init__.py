from .random_generator import *
from .errorshelp import *
from .funcs import *
from .console import *
from .datastructures import *
from .templates import *
from . import json_tools

for i in dir(json_tools):
    print(i)