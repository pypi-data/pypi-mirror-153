

class Iterable:
    def __init__(self, iterable):
        r"""
         Agrega las propiedas de iterables a el objeto usando `iterable` como iterable
        """
        self.iterable = iterable
                    
    def __iter__(self):
        self.__current_index = 0
        return iter(self.iterable)

    def __next__(self):
        if self.__current_index < len(self.iterable):
            self.__current_index += 1
            return self.iterable[self.__current_index]
        else:
            raise StopIteration

    def __getitem__(self, other):
        if isinstance(other, int):
            return self.iterable[other]

        elif isinstance(other, slice):
            return self.__getslice__(other)

        else:
            raise TypeError("Index must be integer or slice")

    def __setitem__(self, other, item):
        if isinstance(other, int):
            self.iterable[other] = item

        elif isinstance(other, slice):
            self.__setslice__(other, item)

        else:
            raise TypeError("Index must be integer or slice")

    def __delitem__(self, other):
        if isinstance(other, int):
            del self.iterable[other]
        elif isinstance(other, slice):
            self.__delslice__(self)
        else:
            raise TypeError("Index must be integer or slice")
            
    def __getslice__(self, other):
        return self.iterable[other.start:other.other]

    def __setslice__(self, other, item):
        self.iterable[other.start:other.stop:other.end] = item

    def __delslice__(self, other):
        del self.iterable[other.start:other.stop:other.step]

              

    def __doc__(self):
        return r"""
        Agrega las propiedas de iterables a el objeto usando `iterable` como iterable
        """
