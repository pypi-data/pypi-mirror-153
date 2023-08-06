# PWB Dyn: The functions for sending PowerWorld Dynamics data to and from the GridWorkbench using Easy SimAuto
#
# Adam Birchfield, Texas A&M University
# 
# Log:
# 2/14/2022 Ability to read in GENCLS data
# 3/12/2022 Reading in GENROU fields as well
#
import pandas as pd
from ..dyn import *

def setup_dyn_fields():
    models = []
    fields = {}
    models = [("gencls", "MachineModel_GENCLS"),("genrou", "MachineModel_GENROU")]
    fields["gencls"] = [ ("node_num", "BusNum"), ("gen_id", "GenID"),
        ("H", "TSH"), ("D", "TSD"), ("Ra", "TSRa"), ("Xdp", "TSXd:1"),
        ("Rcomp", "TSRcomp"), ("Xcomp", "TSXcomp")]
    fields["genrou"] = [ ("node_num", "BusNum"), ("gen_id", "GenID"),
        ("H", "TSH"), ("D", "TSD"), ("Ra", "TSRa"), ("Xd", "TSXd"), ("Xq", "TSXq"), ("Xdp", "TSXd:1"), ("Xqp", "TSXq:1"), ("Xdpp", "TSXd:2"), ("Xl", "TSXl"), ("Tdop", "TSTdo"), ("Tqop", "TSTqo"), ("Tdopp", "TSTdo:1"), ("Tqopp", "TSTqo:1"), ("S1", "TSS1"), ("S12", "TSS1:1"), ("Rcomp", "TSRcomp"), ("Xcomp", "TSXcomp")]
    return models, fields

def pwb_read_dyn(self, s=None):
    if s is None:
        s = self.esa

    self.dyn_models = []

    models, fields = setup_dyn_fields()
    
    for mod, mpw in models:
        print(f"Reading {mod}")
        df = s.GetParametersMultipleElement(mpw,
            [f[1] for f in fields[mod]])
        if df is not None:
            df = df.to_dict("records")
            for i in range(len(df)):
                model_info = df[i]
                model_class = globals()[mod]
                model_obj = model_class()
                for field_wb, field_pw in fields[mod]:
                    setattr(model_obj, field_wb, model_info[field_pw])
                self.dyn_models.append(model_obj)
    