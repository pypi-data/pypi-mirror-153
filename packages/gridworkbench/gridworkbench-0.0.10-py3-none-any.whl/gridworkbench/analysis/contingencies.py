# Contingencies: classes to hold contingency set definition data
#
# Adam Birchfield, Texas A&M University
# 
# Log:
# 4/28/2022 ABB Initial version, stub for now
#
from src.gridworkbench.containers import Bus
from src.gridworkbench.devices import Branch, Gen, Load

class ContingencyAction:

    def __init__(self):
        self.command = "NONE"
        self.object = "NONE"
        self.value = 0.0

class Contingency:

    def __init__(self):
        self.label = ""
        self.actions = []

class ContingencyViolation:

    def __init__(self):
        self.type = "NONE"
        self.obj = None
        self.value = 0.0

class ContingencySet:

    def __init__(self):
        self.contingencies = []
        self.violations = []