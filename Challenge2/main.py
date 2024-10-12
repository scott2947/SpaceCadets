# Back end
# Memory

class MemoryUnit():
    def __init__(self, identifier, maxSize = 4096):
        self.identifier = identifier
        self.memory = []
        self.deleted = [] # array of deleted cell indices
        self.size = 0
        self.maxSize = maxSize

    def Info(self):
        return self.identifier
    
    def Defragmenter(self):
        for i in self.deleted:
            self.memory.pop(i)
        self.size -= len(self.deleted)
        self.deleted.clear()

    def WriteObject(self, object):
        if self.size < self.maxSize:
            if len(self.deleted) == 0:
                index = self.size
                self.memory.append(object)
            else:
                index = self.deleted.pop(0)
                self.memory[index] = object
            self.size += 1
            return index
        else:
            raise("Error: Memory overflow")
    
    def EditObject(self, object, pointer):
        self.memory[pointer] = object
    
    def ReadObject(self, pointer):
        return self.memory[pointer]

# Literals (for now just integers)

class Literal():
    def __init__(self):
        self.value = None
        self.descriptor = "<Literal>"
    
    def Info(self):
        return self.descriptor
    
    def ReadValue(self):
        return self.value

class Integer(Literal):
    def __init__(self, value):
        if isinstance(value, int):
            self.value = value
            self.descriptor = "<Integer>"
        else:
            raise("Error: Cannot assign non-integer value to integer")

# Data structures (for now just variables)

class Variable():
    def __init__(self, identifier, data, memoryUnit): # data is a defined literal, memoryUnit is the referenced memory block
        self.identifier = identifier
        self.memoryUnit = memoryUnit
        self.pointer = memoryUnit.WriteObject(data)

    def Info(self):
        return "{0} object at index {1} of {2} with value {3}".format(self.memoryUnit.ReadObject(self.pointer).Info(), self.pointer, self.memoryUnit.Info(), self.memoryUnit.ReadObject(self.pointer).ReadValue())
    
## mainMemory = MemoryUnit("system memory", 10000)
## number = Variable("number", Integer(6), mainMemory)
## print(number.Info())

# Front end
# Highest level interpreter class

class Interpreter():
    def __init__(self, filepath):
        self.filepath = filepath

        with open(filepath, "r") as fileObj:
            self.code = [i.replace("\n", "") for i in fileObj.readlines()]

        self.control = 0

    def Execute(self):
        pass # Determine if indents matter

# test = Interpreter("./example.txt")