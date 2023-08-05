import json, os, datetime
import concurrent.futures as cf

# mason = Muchos archivos, JSON
class Mason:
    def __init__(self, max_lines:int=20, data_path="data"):
        self.max_lines = max_lines
        self.data_path = data_path
        self.file_index = 0
        self.last_item_index = 0

        # if data folder doesn't exist, create it
        if not os.path.exists(self.data_path):
            os.makedirs(self.data_path)
            self.__update_current()
        else:
            self.__get_current_file()
                
      
    def __get_current_file(self):
        got_file = False
        
        for file in os.listdir(self.data_path):
            if file.endswith(".json"):
                with open(os.path.join(self.data_path, file), "r") as f:
                    data = json.load(f)
                    lines = len(f.readlines())
                    
                    if lines < self.max_lines:
                        self.current_file = os.path.join(self.data_path, file)

                        self.last_item_index = data["__file_data"]["indexes"][1]
                        self.file_index = int(file.split(" ")[0])

                        got_file = True
                    
        if not got_file:
            self.__update_current()
                                      
    def __update_current(self):
        # create new file
        self.file_index += 1
        self.current_file = f"{self.data_path}/{self.file_index} {datetime.datetime.now().strftime('%Y-%m-%d %H-%M-%S')}.json"
        with open(self.current_file, "w") as f:            
            json.dump({"__file_data": {"indexes": [self.last_item_index, self.last_item_index-1]} }, f, indent=4)
                    
    # adders
    def add(self, data:dict):
        if isinstance(data, dict):
            key = list(data.keys())[0]
            value = data[key]
            
        elif isinstance(data, list) or isinstance(data, tuple):
            key = data[0]
            value = data[1]
        
        # check if key exists
        if self.get( (key) ):
            raise KeyError(f"Duplicate key: {key}")
            
        with open(self.current_file, "r") as f:
            file = json.load(f)
            
            file[key] = value
            
            # update indexes
            file["__file_data"]["indexes"][1] += 1
            self.last_item_index += 1
        
        with open(self.current_file, "w") as f:
            json.dump(file, f, indent=4)
            
        # calculate lines
        with open(self.current_file, "r") as f:
            lines = len(f.readlines())
        
        if lines > self.max_lines:
            self.__update_current()
                    
                    
    # getters
    def exists(self, key:str):
        def _look_for_key(file, key):
            with open(file, "r") as f:
                data = json.load(f)
                if key in data:
                    return file
                else:
                    return None
                
        with cf.ThreadPoolExecutor() as executor:
            files = [f for f in os.listdir(self.data_path) if f.endswith(".json")]
            
            threads  = [executor.submit(_look_for_key, os.path.join(self.data_path, f), key) for f in files]
           
            for t in cf.as_completed(threads):
                if t.result():
                    return t.result()
    
    def get(self, key:str): 
        def _look_for_key(file, key):
            with open(file, "r") as f:
                file = json.load(f)
                if key in file:
                    return file[key]
                else:
                    return None
                
        with cf.ThreadPoolExecutor() as executor:
            files = [f for f in os.listdir(self.data_path) if f.endswith(".json")]
            
            threads  = [executor.submit(_look_for_key, os.path.join(self.data_path, f), key) for f in files]
           
            for t in cf.as_completed(threads):
                if t.result():
                    return t.result()
                
    def __getitem__(self, key:str):
        return self.get(key)
            
    # setters
    def set(self, key:str, value):
        file = self.exists(key)
        if file:
            with open(file, "r") as f:
                file = json.load(f)
                file[key] = value
                
            with open(file, "w") as f:
                json.dump(file, f, indent=4)
                
        else:
            self.add({key:value})
            
    def __setitem__(self, key:str, value):
        self.set(key, value)
    
    # removers
    def remove(self, key:str):
        file = self.exists(key)
        if file:
            with open(file, "r") as f:
                file = json.load(f)
                del file[key]
                
            with open(file, "w") as f:
                json.dump(file, f, indent=4)
                
        else:
            raise KeyError(f"Key {key} not found")
        
    def __delitem__(self, key:str):
        self.remove(key)
    
    # get by index
    def get_by_index(self, index:int):
        def _look_for_index(file, index):
            with open(file, "r") as f:
                data = json.load(f)
                
                indexes = data["__file_data"]["indexes"]
                
                del data["__file_data"]
                
                if index >= indexes[0] and index <= indexes[1]:
                    for real_index, obj in zip(range(indexes[0], indexes[1]+1), data.values()):
                        if real_index == index:
                            return obj
                    
                else:
                    return None
                
        with cf.ThreadPoolExecutor() as executor:     
            files = [f for f in os.listdir(self.data_path) if f.endswith(".json")]
            
            threads  = [executor.submit(_look_for_index, os.path.join(self.data_path, f), index) for f in files]
            
            for t in cf.as_completed(threads):
                if t.result():
                    return t.result()

    # iterators
    def __iter__(self):
        self.__index = 0
        return self

    def __next__(self):
        if self.__index < self.last_item_index:
            self.__index += 1
            return self.get_by_index(self.__index)
        else:
            raise StopIteration
             
open_files = {}
# maneja la entrada y salida de datos en un archivo json
class JsonData:
    def __init__(self, file:str, encoding:str="utf-8"):   
        self.file = file
        self.encoding = encoding
        self.data = {}

        with open(self.file, "r", encoding=self.encoding) as f:
            self.data = json.load(f)
        
    def get(self):
        try:
            with open(self.file, "r", encoding=self.encoding) as f:
                self.data = json.load(f)
            
        except:
            # desplega un hilo para continuar con proceso sin interrupcion
            with cf.ThreadPoolExecutor() as executor:
                executor.submit(self.get)
                
        return {**self.data}
    
    def set(self, data):
        if self.data == data or not data:
            return
    
        self.save(data)
        
    def save(self, data):
        try:
            with open(self.file, "w", encoding=self.encoding) as f:
                json.dump(data, f, indent=4)
                self.data = data
            
        except:
            # desplega un hilo para continuar con proceso sin interrupcion
            with cf.ThreadPoolExecutor() as executor:
                executor.submit(self.save)

# No hay cambios en el archivo, los pasa a JSON_DATA para que los maneje
class open_json:
    def __init__(self, file:str, mode:str="r", encoding:str="utf-8", save_on_exit:bool=True, create=True):        
        self.file = file
        self.mode = mode
        self.encoding = encoding
        self.save_on_exit = save_on_exit
        self.create = create
        
    def __enter__(self):
        global open_files
        
        if self.create:
            # if file doesn't exist, create it
            if not os.path.exists(self.file):
                with open(self.file, "w", encoding=self.encoding) as f:
                    json.dump({}, f, indent=4)
                    
        if self.file  not in open_files:
            open_files[self.file] = JsonData(self.file, self.encoding)
    
        self.data = open_files[self.file].get()
        return self.data
                
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.save_on_exit:
            open_files[self.file].set(self.data)
        
        if exc_type:
            raise exc_type(exc_val)
    
    
    