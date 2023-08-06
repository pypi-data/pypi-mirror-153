# BG Engine: Capability to connect with low-level Brontogrid Engine for solving power
# flow and contingency analysis and OPF
#
# Adam Birchfield, Texas A&M University
# 
# Log:
# 4/1/2022 ABB Initial version
#
from cmath import pi
from ctypes import *
from ..containers import Region, Area, Sub, Bus, Node
from ..devices import Gen, Load, Shunt, Branch

BGE_ERR_BAD_ID_LOW =101
BGE_ERR_BAD_ID_HIGH =102
BGE_ERR_BAD_ID_FREED =103
BGE_ERR_RAW_FILE_NOT_OPENED =1100
BGE_ERR_RAW_FILE_TOO_FEW_LINE_PARTS =1101
BGE_ERR_RAW_FILE_BUS_LINK_NOT_FOUND =1102
BGE_ERR_INL_FILE_NOT_OPENED =1103
BGE_ERR_INL_VALIDATION =1104
BGE_ERR_INL_GEN_LINK_NOT_FOUND =1105
BGE_ERR_CON_UNKNOWN_CTG_ACTION =1106
ENGINE_LOG_SIZE =1000000
OBJ_BUS =0x0001
OBJ_BRANCH =0x0002
BRANCH_STATUS_OPEN =0x0000
BRANCH_STATUS_CLOSED =0x0001
OBJ_GEN =0x0003
GEN_STATUS_OPEN =0x0000
GEN_STATUS_FIXED_P_Q =0x0001
GEN_STATUS_FIXED_P =0x0002
GEN_STATUS_FIXED_Q =0x0003
GEN_STATUS_VAR_PQ =0x0004
GEN_STATUS_SHUNT_OPEN =0x000A
GEN_STATUS_SHUNT_CONTINUOUS =0x000D
OBJ_AREA =0x0008
OBJ_SUB =0x0009
OBJ_CTG = 0x0005
OBJ_CTGELEM =0x0004
CTGELEM_CODE_PFIXED =0x0000
CTGELEM_CODE_QFIXED =0x0001
CTGELEM_CODE_QSHUNT =0x0002
CTGELEM_CODE_GEN_OPEN =0x0003
CTGELEM_CODE_BRANCH_OPEN =0x0004
OBJ_CTGVIO =0x0006
CTGVIO_CODE_NOT_SOLVED =0x0000
CTGVIO_CODE_BRANCH_MVA =0x0001
CTGVIO_CODE_BUS_HIGHV =0x0002
CTGVIO_CODE_BUS_LOWV =0x0003
STEADY_MODELING_AC =0x0000
STEADY_MODELING_DC_KLU =0x0001
STEADY_MODELING_DC_CHOLMOD =0x0002
OBJ_LINCOST =0x0007
LP_MAX_BREAKS =10
LP_TOL =1e-8
LP_EXIT_MAX_ITERATIONS =0
LP_EXIT_OPTIMUM_REACHED =1
LP_EXIT_INFEASIBLE =2
LP_EXIT_UNBOUNDED =3

class BG_Bus(Structure):
    _fields_ = [("del", c_char), ("id", c_int), ("area", c_int), ("label", c_int), 
    ("sub", c_int), ("mag", c_double), ("angle", c_double), ("psload", c_double), 
    ("qsload", c_double), ("qshunt", c_double), ("basekv", c_double), 
    ("lmp", c_double)]

c_char3 = c_char*3
class BG_Branch(Structure):
    _fields_ = [("del", c_char), ("bus1", c_int), ("bus2", c_int), ("status", c_int), 
    ("label", c_int), ("x", c_double), ("r", c_double), ("b", c_double), 
    ("g", c_double), ("tap", c_double), ("phase", c_double), ("p1", c_double), 
    ("q1", c_double), ("p2", c_double), ("q2", c_double), ("slimit", c_double),
     ("smaxctg", c_double), ("ckt", c_char3)]
    
class BG_Gen(Structure):
    _fields_ = [("del", c_char), ("id", c_char3), ("bus", c_int), 
    ("status", c_int), ("busreg", c_int), ("costtable", c_int), ("label", c_int), 
    ("p", c_double), ("q", c_double), ("pmin", c_double), ("pmax", c_double), 
    ("qmin", c_double), ("qmax", c_double), ("vset", c_double), 
    ("partfac", c_double), ("regfac", c_double)]
    
class BG_Area(Structure):
    _fields_ = [("del", c_char), ("id", c_int), ("label", c_int)]
    
class BG_Sub(Structure):
    _fields_ = [("del", c_char), ("id", c_int), ("label", c_int), 
    ("latitude", c_double), ("longitude", c_double)]
    
class BG_Network(Structure):
    _fields_ = [("mva_base", c_double), ("buses", POINTER(BG_Bus)), 
    ("branches", POINTER(BG_Branch)), ("gens", POINTER(BG_Gen)), 
    ("areas", POINTER(BG_Area)), ("subs", POINTER(BG_Sub))]
    
class BG_Ctgelem(Structure):
    _fields_ = [("del", c_char), ("code", c_int), ("id", c_int), ("ctg", c_int), 
    ("label", c_int), ("val", c_double)]

class BG_Ctg(Structure):
    _fields_ = [("del", c_char), ("pce", c_int), ("nvios", c_int), ("solved", c_int), 
    ("nislands", c_int), ("rebuild_flag", c_int), ("regulation_stuck_flag", c_int), 
    ("label", c_int), ("unserved_load", c_double)]
    
class BG_Ctgvio(Structure):
    _fields_ = [("del", c_char), ("code", c_int), ("id", c_int), ("ctg", c_int), 
    ("label", c_int), ("value", c_double)]
    
class BG_Steadystate(Structure):
    _fields_ = [("modeling", c_int), ("dcslack", c_int), 
    ("max_nr_iterations", c_int), ("max_avr_iterations", c_int), 
    ("max_agc_iterations", c_int), ("dishonest_iterations", c_int), 
    ("enforce_limits", c_int), ("agc_max_hit_limit", c_int), ("log_detail", c_int), 
    ("nvmax", c_int), ("nr_tolerance", c_double), ("agc_tolerance = 1e-2", c_double), 
    ("ctgelems", POINTER(BG_Ctgelem)), ("ctgs", POINTER(BG_Ctg)), 
    ("ctgvios", POINTER(BG_Ctgvio))]
    
c_double10 = c_double*10
class BG_Lincost(Structure):
    _fields_ = [("del", c_char), ("npoints", c_int), ("label", c_int), 
    ("x", c_double10), ("y", c_double10)]

class BG_Optimization(Structure):
    _fields_ = [("talk_detail", c_int), ("max_ctg_run", c_int), 
    ("do_sequential", c_int), ("ignore_ctg", c_int), ("ignore_violations", c_int), 
    ("ctg_maintain_base_voltage", c_int), ("save_stats", c_int), 
    ("total_ctgs", c_int), ("tableau_ctgs", c_int), ("binding_ctgs", c_int), 
    ("niterations", c_int), ("nr_iteration_count", c_int), ("lmp_min", c_double), 
    ("lmp_avg", c_double), ("lmp_max", c_double), ("lincosts", POINTER(BG_Lincost))]

class BG_Workbench(Structure):
    _fields_ = [("eng", POINTER(None)), ("net", BG_Network), 
    ("steady", BG_Steadystate), ("opt", BG_Optimization)]

class BG_LP_Variable(Structure):
    _fields_ = [("nsegs", c_int), ("basis_index", c_int), 
    ("marginal_cost", c_double), ("vals", c_double10), ("costs", c_double10), 
    ("val", c_double)]

class Bge():
    def __init__(self, gwb, engine_dll_fname):
        self.gwb = gwb
        self.bgwb = None
        self.lib = CDLL(engine_dll_fname)
        self.lib.create_workbench.argtypes = []
        self.lib.create_workbench.restype = POINTER(BG_Workbench)
        self.lib.destroy_workbench.argtypes = [POINTER(BG_Workbench)]
        self.lib.destroy_workbench.restype = POINTER(BG_Workbench)
        self.lib.count_object.argtypes = [POINTER(BG_Workbench), c_int]
        self.lib.count_object.restype = c_int
        self.lib.add_object.argtypes = [POINTER(BG_Workbench), c_int]
        self.lib.add_object.restype = c_bool
        self.lib.clear_object.argtypes = [POINTER(BG_Workbench), c_int]
        self.lib.clear_object.restype = c_bool
        self.lib.delete_object.argtypes = [POINTER(BG_Workbench), c_int]
        self.lib.delete_object.restype = c_bool
        self.lib.set_label.argtypes = [POINTER(BG_Workbench), c_int, c_int, c_char_p]
        self.lib.set_label.restype = None
        self.lib.get_label.argtypes = [POINTER(BG_Workbench), c_int, c_int]
        self.lib.get_label.restype = c_char_p
        self.lib.steadystate_solve_base.argtypes = [POINTER(BG_Workbench)]
        self.lib.steadystate_solve_base.restype = c_int
        self.lib.steadystate_solve_single_ctg.argtypes = [POINTER(BG_Workbench), c_int]
        self.lib.steadystate_solve_single_ctg.restype = c_int
        self.lib.steadystate_solve_all_ctg.argtypes = [POINTER(BG_Workbench)]
        self.lib.steadystate_solve_all_ctg.restype = c_int
        self.lib.solve_linear_program_simplex.argtypes = [POINTER(BG_Workbench), c_int,
            c_int, POINTER(BG_LP_Variable), POINTER(c_double), POINTER(c_double)]
        self.lib.solve_linear_program_simplex.restype = c_int
        self.lib.do_scopf.argtypes = [POINTER(BG_Workbench), c_char_p]
        self.lib.do_scopf.restype = c_int
        self.lib.do_planning_sensitivity.argtypes = [POINTER(BG_Workbench), c_int,
            c_int, POINTER(c_int), c_int, POINTER(c_int), POINTER(c_int), 
            POINTER(c_double)]
        self.lib.do_planning_sensitivity.restype = c_int
        self.lib.get_planning_limits.argtypes = [POINTER(BG_Workbench), POINTER(c_double),
            POINTER(c_double)]
        self.lib.get_planning_limits.restype = c_int
        self.lib.read_engine_log.argtypes = [POINTER(BG_Workbench), c_char_p,
            c_int]
        self.lib.read_engine_log.restype = c_int
        self.lib.flat_system.argtypes = [POINTER(BG_Workbench)]
        self.lib.flat_system.restype = None
        self.lib.write_dcpf_matrix.argtypes = [POINTER(BG_Workbench), c_char_p]
        self.lib.write_dcpf_matrix.restype = c_int
        self.lib.do_delaunay.argtypes = [c_int, POINTER(c_double), POINTER(c_double),
            c_int, POINTER(c_int), POINTER(c_int)]
        self.lib.do_delaunay.restype = c_int

    def initialize(self):
        if self.bgwb is not None:
            self.lib.destroy_workbench(self.bgwb)
            self.bgwb = None
        self.bgwb = self.lib.create_workbench()
        for i, bus in enumerate(self.gwb.buses):
            bus.bg_idx = i
            self.lib.add_object(self.bgwb, OBJ_BUS)
        for i, branch in enumerate(self.gwb.branches):
            branch.bg_idx = i
            self.lib.add_object(self.bgwb, OBJ_BRANCH)
        for i, gen in enumerate(self.gwb.gens):
            gen.bg_idx = i
            self.lib.add_object(self.bgwb, OBJ_GEN)
        for i, area in enumerate(self.gwb.areas):
            area.bg_idx = i
            self.lib.add_object(self.bgwb, OBJ_AREA)
        for i, sub in enumerate(self.gwb.subs):
            sub.bg_idx = i
            self.lib.add_object(self.bgwb, OBJ_SUB)
        if hasattr(self.gwb, "ctg_set"):
            ielem = 0
            for i, ctg in enumerate(self.gwb.ctg_set.contingencies):
                ctg.bg_idx = i
                self.lib.add_object(self.bgwb, OBJ_CTG)
                for action in ctg.actions:
                    action.bg_idx = ielem
                    ielem += 1
                    self.lib.add_object(self.bgwb, OBJ_CTGELEM)

    def send_data(self):
        if self.bgwb == None:
            return
        
        na = self.lib.count_object(self.bgwb, OBJ_AREA)
        for area in self.gwb.areas:
            if hasattr(area, "bg_idx") and 0 <= area.bg_idx < na:
                self.bgwb.contents.net.areas[area.bg_idx].id = area.number

        nsu = self.lib.count_object(self.bgwb, OBJ_SUB)
        for sub in self.gwb.subs:
            if hasattr(sub, "bg_idx") and 0 <= sub.bg_idx < nsu:
                bg_sub = self.bgwb.contents.net.subs[sub.bg_idx]
                bg_sub.id = sub.number
                bg_sub.latitude = sub.latitude
                bg_sub.longitude = sub.longitude

        nb = self.lib.count_object(self.bgwb, OBJ_BUS)
        for bus in self.gwb.buses:
            if hasattr(bus, "bg_idx") and 0 <= bus.bg_idx < nb:
                bg_bus = self.bgwb.contents.net.buses[bus.bg_idx]
                bg_bus.id = bus.number
                bg_bus.angle = bus.vang * pi / 180.0
                bg_bus.mag = bus.vpu
                bg_bus.area = bus.area.bg_idx
                bg_bus.psload = sum(ld.ps for ld in bus.loads) / 100.0
                bg_bus.qsload = sum(ld.qs for ld in bus.loads) / 100.0
                bg_bus.qshunt = sum(sh.qnom for sh in bus.shunts) / 100.0
                bg_bus.basekv = bus.nominal_kv
                bg_bus.lmp = 0
        
        nbr = self.lib.count_object(self.bgwb, OBJ_BRANCH)
        for br in self.gwb.branches:
            if hasattr(br, "bg_idx") and 0 <= br.bg_idx < nbr:
                bg_br = self.bgwb.contents.net.branches[br.bg_idx]
                bg_br.bus1 = br.from_bus.bg_idx
                bg_br.bus2 = br.to_bus.bg_idx
                bg_br.status = 1 if br.status else 0
                bg_br.x = br.X
                bg_br.r = br.R
                bg_br.b = br.B
                bg_br.g = br.G
                bg_br.tap = br.tap
                bg_br.phase = br.phase / 180.0 * pi
                bg_br.slimit = br.MVA_Limit_A
                bg_br.ckt = br.id.encode("ascii")

        ng = self.lib.count_object(self.bgwb, OBJ_GEN)
        for gen in self.gwb.gens:
            if hasattr(gen, "bg_idx") and 0 <= gen.bg_idx < ng:
                bg_gen = self.bgwb.contents.net.gens[gen.bg_idx]
                bg_gen.id = gen.id.encode("ascii")
                bg_gen.bus = gen.bus.bg_idx
                bg_gen.status = GEN_STATUS_VAR_PQ if gen.status else GEN_STATUS_OPEN
                bg_gen.busreg = self.gwb.bus(gen.reg_bus_num).bg_idx
                bg_gen.p = gen.p / 100.0
                bg_gen.q = gen.q / 100.0
                bg_gen.pmin = gen.pmin / 100.0
                bg_gen.pmax = gen.pmax / 100.0
                bg_gen.qmin = gen.qmin / 100.0
                bg_gen.qmax = gen.qmax / 100.0
                bg_gen.vset = gen.reg_pu_v
                bg_gen.partfac = gen.sbase
                bg_gen.costtable = -1
                bg_gen.regfac = 1

        nc = self.lib.count_object(self.bgwb, OBJ_CTG)
        nce = self.lib.count_object(self.bgwb, OBJ_CTGELEM)
        ice = 0
        if hasattr(self.gwb, "ctg_set"):
            for ic in range(nc):
                bg_ctg = self.bgwb.contents.steady.ctgs[ic]
                gwb_ctg = self.gwb.ctg_set.contingencies[ic]
                bg_ctg.nislands = -1
                bg_ctg.nvios = 0
                bg_ctg.rebuild_flag = -1
                bg_ctg.regulation_stuck_flag = -1
                bg_ctg.solved = -1
                bg_ctg.unserved_load = 0;
                for action in gwb_ctg.actions:
                    command = action.command.split()
                    obj = action.object.split()
                    bg_ctg_elem = self.bgwb.contents.steady.ctgelems[ice]
                    bg_ctg_elem.ctg = ic
                    if command[0] == "OPEN" and obj[0] == "BRANCH":
                        bg_ctg_elem.code = 4
                        bg_ctg_elem.id = self.gwb.branch(int(obj[1]), int(obj[2]), obj[3]).bg_idx
                        bg_ctg_elem.val = 0
                    elif command[0] == "OPEN" and obj[0] == "GEN":
                        bg_ctg_elem.code = 3
                        bg_ctg_elem.id = self.gwb.gen(int(obj[1]), obj[2]).bg_idx
                        bg_ctg_elem.val = 0
                    else:
                        bg_ctg_elem.code = 0
                        bg_ctg_elem.id = 0
                        bg_ctg_elem.val = 0
                    ice += 1
            
        

    def get_data(self):
        if self.bgwb == None:
            return
        
        na = self.lib.count_object(self.bgwb, OBJ_AREA)
        for area in self.gwb.areas:
            if hasattr(area, "bg_idx") and 0 <= area.bg_idx < na:
                #self.bgwb.contents.net.areas[area.bg_idx].id = area.number
                pass # No data to retrieve from areas

        nsu = self.lib.count_object(self.bgwb, OBJ_SUB)
        for sub in self.gwb.subs:
            if hasattr(sub, "bg_idx") and 0 <= sub.bg_idx < nsu:
                bg_sub = self.bgwb.contents.net.subs[sub.bg_idx]
                #bg_sub.id = sub.number
                #bg_sub.latitude = sub.latitude
                #bg_sub.longitude = sub.longitude

        nb = self.lib.count_object(self.bgwb, OBJ_BUS)
        for bus in self.gwb.buses:
            if hasattr(bus, "bg_idx") and 0 <= bus.bg_idx < nb:
                bg_bus = self.bgwb.contents.net.buses[bus.bg_idx]
                #bg_bus.id = bus.number
                bus.vang = 180.0 / pi * bg_bus.angle
                bus.vpu = bg_bus.mag
                #bg_bus.area = bus.area.bg_idx
                #bg_bus.psload = sum(ld.ps for ld in bus.loads) / 100.0
                #bg_bus.qsload = sum(ld.qs for ld in bus.loads) / 100.0
                #bg_bus.qshunt = sum(sh.qnom for sh in bus.shunts) / 100.0
                #bg_bus.basekv = bus.nominal_kv
                bus.lmp = bg_bus.lmp
        
        nbr = self.lib.count_object(self.bgwb, OBJ_BRANCH)
        for br in self.gwb.branches:
            if hasattr(br, "bg_idx") and 0 <= br.bg_idx < nbr:
                bg_br = self.bgwb.contents.net.branches[br.bg_idx]
                br.p1 = bg_br.p1 * 100.0
                br.q1 = bg_br.q1 * 100.0
                br.p2 = bg_br.p2 * 100.0
                br.q2 = bg_br.q2 * 100.0
                br.smaxctg = bg_br.smaxctg * 100.0
                #bg_br.bus1 = br.from_bus.bg_idx
                #bg_br.bus2 = br.to_bus.bg_idx
                #bg_br.status = 1 if br.status else 0
                #bg_br.x = br.X
                #bg_br.r = br.R
                #bg_br.b = br.B
                #bg_br.g = br.G
                #bg_br.tap = br.tap
                #bg_br.phase = br.phase / 180.0 * pi
                #bg_br.slimit = br.MVA_Limit_A
                #bg_br.ckt = br.id.encode("ascii")

        ng = self.lib.count_object(self.bgwb, OBJ_GEN)
        for gen in self.gwb.gens:
            if hasattr(gen, "bg_idx") and 0 <= gen.bg_idx < ng:
                bg_gen = self.bgwb.contents.net.gens[gen.bg_idx]
                #bg_gen.id = gen.id.encode("ascii")
                #bg_gen.bus = gen.bus.bg_idx
                #bg_gen.status = GEN_STATUS_VAR_PQ if gen.status else GEN_STATUS_OPEN
                #bg_gen.busreg = self.gwb.bus(gen.reg_bus_num).bg_idx
                gen.p = 100.0*bg_gen.p
                gen.q = 100.0*bg_gen.q
                #bg_gen.pmin = gen.pmin / 100.0
                #bg_gen.pmax = gen.pmax / 100.0
                #bg_gen.qmin = gen.qmin / 100.0
                #bg_gen.qmax = gen.qmax / 100.0
                #bg_gen.vset = gen.reg_pu_v
                #bg_gen.partfac = gen.sbase
                #bg_gen.costtable = -1
                #bg_gen.regfac = 1

    # Need to implement shunts with continuous control capability
    # Still need to implement solution tools as nice functions
    # Still need to implement contingencies -- need them in GWB first

    def __del__(self):
        if self.bgwb is not None:
            self.lib.destroy_workbench(self.bgwb)
            self.bgwb = None

def setup_bge(self, engine_dll_fname):
    self.bge = Bge(self, engine_dll_fname)
    

    