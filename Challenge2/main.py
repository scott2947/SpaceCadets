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
        
    def ReadObject(self, pointer):
        return self.memory[pointer]

# Literals (for now just integers)

class Literal():
    def __init__(self):
        self.value = None
        self.descriptor = "<Literal>"
    
    def Info(self):
        return self.descriptor
    
    def GetValue(self):
        return self.value

class Integer(Literal):
    def __init__(self, value):
        if isinstance(value, int):
            self.value = value
            self.descriptor = "<Integer>"
        else:
            raise("Error: Cannot assign non-integer value to integer")
        
    def Increment(self):
        self.value += 1
    
    def Decrement(self):
        self.value -= 1

# Data structures (for now just variables)

class Variable():
    def __init__(self, identifier, data, memoryUnit): # data is a defined literal, memoryUnit is the referenced memory block
        self.identifier = identifier
        self.memoryUnit = memoryUnit
        self.pointer = memoryUnit.WriteObject(data)

    def Info(self):
        return "{0} object at index {1} of {2} with value {3}".format(self.memoryUnit.ReadObject(self.pointer).Info(), self.pointer, self.memoryUnit.Info(), self.memoryUnit.ReadObject(self.pointer).GetValue())

    def GetObject(self):
        return self.memoryUnit.ReadObject(self.pointer)
    
    def GetValue(self):
        return self.GetObject().GetValue()

# Front end
# Highest level interpreter class

class Interpreter():
    def __init__(self, filepath):
        self.filepath = filepath

        self.control = 0
        self.dataStructures = {}
        self.lookup = {
            "clear": self.Clear,
            "incr": self.Incr,
            "decr": self.Decr,
            "while": self.While,
            "end": self.End
        }
        self.controlFlows = ["while"]

        with open(filepath, "r") as fileObj:
            self.rawCode = [i.replace(";\n", "").replace(";", "").strip() for i in fileObj.readlines()]

        self.splitCode = []
        for i in self.rawCode:
            splitPoint = i.find(" ")
            opcode = i[:splitPoint]
            operands = i[splitPoint + 1:]
            if operands == "end":
                self.splitCode.append([operands, ""])
            else:
                self.splitCode.append([opcode, operands])

        self.linkLines = {}
        for i in range(len(self.splitCode)):
            if self.splitCode[i][0] not in self.controlFlows and self.splitCode[i][0] != "end":
                self.linkLines[i] = i + 1
            else:
                if self.splitCode[i][0] in self.controlFlows:
                    counter = 1
                    j = i + 1
                    while counter != 0:
                        if self.splitCode[j][0] in self.controlFlows:
                            counter += 1
                        elif self.splitCode[j][0] == "end":
                            counter -= 1
                        j += 1
                    self.linkLines[i] = j
                else:
                    counter = 1
                    j = i - 1
                    while counter != 0:
                        if self.splitCode[j][0] == "end":
                            counter += 1
                        elif self.splitCode[j][0] in self.controlFlows:
                            counter -= 1
                        j -= 1
                    self.linkLines[i] = j + 1
    
    def Clear(self, operands):
        self.dataStructures[operands] = Variable(operands, Integer(0), mainMemory)
        return False

    def Incr(self, operands):
        obj = self.dataStructures[operands]
        obj.GetObject().Increment()
        return False

    def Decr(self, operands):
        obj = self.dataStructures[operands]
        obj.GetObject().Decrement()
        return False

    def While(self, operands):
        varName = operands[:operands.find(" ")]
        testValue = self.dataStructures[varName].GetObject().GetValue()
        if testValue == 0:
            return False
        else:
            return True

    def End(self, operands):
        return False

    def Execute(self):
        while self.control != len(self.splitCode):
            currentLine = self.splitCode[self.control]
            routine = self.lookup[currentLine[0]]
            increment = routine(currentLine[1])
            if not increment:
                self.control = self.linkLines[self.control]
            else:
                self.control += 1

            for i in self.dataStructures.keys():
                print(str(i) + ": " + str(self.dataStructures[i].GetValue()), end = " ")
            print()

mainMemory = MemoryUnit("system memory", 10000)
test = Interpreter("./example2.txt")
test.Execute()