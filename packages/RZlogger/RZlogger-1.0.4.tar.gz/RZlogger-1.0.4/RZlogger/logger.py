

class logger:
    def __init__(self, type, filename = ""):
        self.type = type
        if filename == "":
            self.filename = "RZlogger.txt"
        else:
            self.filename =  filename


    def log(self , data):
        if self.type == "console":
            print(data)
        elif self.type == "file":
            f = open(self.filename, "a")
            f.write(data)
            f.close()
        else:
            print(data)

