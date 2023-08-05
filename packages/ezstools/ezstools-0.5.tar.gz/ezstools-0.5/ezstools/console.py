from typing import *
import asyncio

# replica of console Javascript
class Console():
    def __init__(self):
        self.buffer = []
        self.history = []
        self.counts = []
        self.times = []
        self.history_index = 0
        self.history_max = 10
        self.history_save = True
    
    def log(self, *message : Any) -> None:
        message = " ".join([str(i)  for i in message])
        self.buffer.append(message)
        print(message)
     
    def error(self, message : Any) -> None:
        self.buffer.append(message)
        raise Exception("❗ : " + message)
    
    def warn(self, message : Any) -> None:
        self.buffer.append(message)
        raise Warning("⚠ : " + message)
    
    def clear(self : Any) -> None:
        self.buffer = []
        self.execute("cls")

    def get(self, property) -> Any:
        return self.__dict__[property]

    def time(self, message : str) -> None:
        self.times.append({message : asyncio.get_event_loop().time()})
    
    def timeEnd(self, message : Any, round_to : int = 2) -> Union[float, None]:
        if round_to < 1:
            round_to = 2
        if message in self.times[-1]:
            self.times[-1][message] = asyncio.get_event_loop().time() - self.times[-1][message]  
            print(f"{message} : {str(round(self.times[-1][message], round_to))}'s' ")
            return self.times[-1][message]
        else:
            self.warn(f"{message} not found in times")
            return None

    def table(self, data : List[List[Any]], headers : List[str] = None) -> None:
        if headers is  not None:
            print(f"{' '.join(headers)}")
            print("-" * len(headers) * 2)
            for row in data:
                print(f"{' '.join([str(i) for i in row])}")    
        else:
            for row in data:
                print(f"{' '.join([str(i) for i in row])}")

    def count(self, message : Any) -> Union[int, None]:
        if message in self.counts:
            self.counts[message] += 1
        else:
            self.counts[message] = 1
            
        print(f"{message} : {self.counts[message]}")
        return self.counts[message] if message in self.counts else None
