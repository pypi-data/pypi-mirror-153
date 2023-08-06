# PW AuX: The functions for reading, writing, and interpreting PowerWorld auxiliary files
#
# Adam Birchfield, Texas A&M University
# 
# Log:
# 5/25/2022 Initial version
#

# Stages to implement: read, parse, form, write

class PWAuxFormat:

    def __init__(self):
        self.concise = False
        self.script_blocks = []
        self.data_blocks = []

class PWAuxScriptBlock:

    def __init__(self, name):
        self.name = name
        self.statements = []

    def write(self, f):
        f.write("SCRIPT " + self.name + "\n{\n")
        for statement in self.statements:
            f.write(statement + "\n")
        f.write("}\n")

class PWAuxDataBlock:

    def __init__(self, object_type, field_names):
        self.object_type = object_type
        self.field_names = list(field_names)
        self.field_map = {field_names[i]:i for i in range(len(field_names))}
        self.data = []
        self.subdata_headers = []
        self.subdata_data = []

    def add_data_line(self, data_line=None):
        nf = len(self.field_names)
        if data_line is None:
            self.data.append(["" for i in range(nf)])
        else:
            self.data.append(data_line)
        self.subdata_headers.append([])
        self.subdata_data.append([])

    def add_subdata(self, index, subdatatype, subdatadata):
        self.subdata_headers[index].append(subdatatype)
        self.subdata_data[index].append(subdatadata)
    
    def write(self, f):
        f.write("DATA (" + self.object_type + ", [" + ",".join(self.field_names) + "])\n{\n")
        for i in range(len(self.data)):
            f.write(" ".join(self.data[i])+"\n")
            for j in range(len(self.subdata_headers[i])):
                f.write("<SUBDATA " + self.subdata_headers[i][j] + ">\n")
                for k in range(len(self.subdata_data[i][j])):
                    f.write(self.subdata_data[i][j][k]+"\n")
                f.write("</SUBDATA>\n");
        f.write("}\n")

    