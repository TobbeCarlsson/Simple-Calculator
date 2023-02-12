import sys

registers = {}

# Supported operations
operations = ["add","subtract","multiply"]

# Register class to store instructions and calculate value of register
class Register:
    
    def __init__(self):
        self.instructionQueue = []
        self.value = 0
    
    # Add operation to queue for register
    def addOperation(self, operation,value):
        self.instructionQueue.append([operation,value])
        
    # Calculate value of register
    def evaluate(self):
        while len(self.instructionQueue) > 0:
            instruction = self.instructionQueue.pop(0)
        
            operation = instruction[0]
            value = instruction[1]
            # If value in operation is a number it is directly calculated
            # else the other register has to be evaluated first
            if value.isdigit():
                self.calculate(operation,value)
            else:
                registers[value].evaluate()
                self.calculate(operation,registers[value].value)
        
    # Calculate value of register
    def calculate(self, operation,value):
        if operation == "add":
            self.value += int(value)
        elif operation == "subtract":
            self.value -= int(value)
        elif operation == "multiply":
            self.value *= int(value)
        else:
            print("Operation %s not supported" % operation)
  
# Validate command and show user error message if command is invalid
def validCommand(command):
    #<register> <operation> <value> command
    if(len(command) == 3):
        if command[1] not in operations:
            print("Operation %s not supported" % command[1])
            return False
        elif command[0].isdigit():
            print("Register name cannot be a number: %s %s %s" % (command[0],command[1],command[2]))
            return False
        else:
            return True
    # print <register> command
    elif(len(command) == 2):
        if command[0] != "print":
            print("Invalid command: %s %s" % (command[0], command[1]))
            return False
        elif command[1] not in registers:
            print("Register %s not initialized in command: print %s" % (command[1],command[1]))
            return False
        else:
            return True
    else:
        print("Invalid command: %s" % command)
        
    
# Add instruction to register  
def addInstruction(instruction):
    command = instruction.split()
    # check if command is valid
    if validCommand(command):
        # print <register> instruction
        if(command[0] == "print") and (len(command) == 2):
            registers[command[1]].evaluate()
            print(registers[command[1]].value)
        # <register> <operation> <value> instruction
        elif (len(command) == 3):
            register,operation,value = command[0],command[1],command[2]
            if register in registers:
                registers[register].addOperation(operation,value)
            else:
                reg = Register()
                reg.addOperation(operation,value)
                registers[register] = reg
    

def calculator():  
    # Read instructions from file if filepath is provided othwerise read from stdin
    instructions = []

    # Read from file
    if(len(sys.argv) > 1):
        try:
            file = open(sys.argv[1], 'r')
            instructions = file.readlines()
            file.close()
        except FileNotFoundError:
            print("File %s not found" % sys.argv[1])
    
    # Read from stdin
    else:
        while True:
            line = input().lower()
            if line == "quit":
                break
            else:
                instructions.append(line)
       
    # Add instructions to register         
    for instruction in instructions:
        if instruction.lower() == "quit":
            break
        else:
            addInstruction(instruction.lower())


calculator()