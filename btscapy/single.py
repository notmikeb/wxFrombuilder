class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)

        return cls._instances[cls]

class csrdongle(object):
    __metaclass__ = Singleton
    h = 0
    def __init__(self):
        self.h = self.h +1
        print ("handle is {}".format(self.h))
    def show(self):
        print ("handle is {}".format(self.h))

csrdongle()
csrdongle()
csrdongle()
csrdongle()
csrdongle().show()
csrdongle().show()
