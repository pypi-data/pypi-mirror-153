from quickstats.utils.enums import GeneralEnum, DescriptiveEnum

class WSVariables(GeneralEnum):
    VARIABLES                         = 0
    OBSERVABLES                       = 1
    POIS                              = 2
    GLOBAL_OBSERVABLES                = 3
    NUISANCE_PARAMETERS               = 4
    CONSTRAINED_NUISANCE_PARAMETERS   = 5
    UNCONSTRAINED_NUISANCE_PARAMETERS = 6
    CONSTRAINTS                       = 7
    AUXILIARY                         = 8
    CORE                              = 9
    NON_CONSTRAINT_VARIABLES          = 10
    
class WSArgument(DescriptiveEnum):
    WORKSPACE                         = (0, "Workspace", False)
    DATASET                           = (1, "Datasets", False)
    SNAPSHOT                          = (2, "Snapshots", False)
    PDF                               = (3, "PDFs", False)
    FUNCTION                          = (4, "Functions", False)
    VARIABLE                          = (5, "Workspace variables", True)
    OBSERVABLE                        = (6, "Observables", True)
    POI                               = (7, "Parameters of Interest (POI)", True)
    GLOBAL_OBSERVABLE                 = (8, "Global observables", True)
    NUISANCE_PARAMETER                = (9, "Nuisance parameters", True)
    CONSTRAINED_NUISANCE_PARAMETER    = (10, "Nuisance parameters with an associated constraint Pdf", True)
    UNCONSTRAINED_NUISANCE_PARAMETER  = (11, "Nuisance parameters without an associated constraint Pdf", True)
    CONSTRAINT                        = (12, "Tuple of constraint pdf and the associated nuisance parameter and global observable", False)
    AUXILIARY                         = (13, "Auxiliary variables (All variables except POIs, observables, global observables and "
                                             "nuisance parameters)", True)
    CORE                              = (14, "Nuisance parameters, global observables and POIs", True)    
    
    def __init__(self, enum_id:int, description:str="", is_variable:bool=False):
        super().__init__(enum_id=enum_id, description=description)
        self.is_variable = is_variable

class SetValueMode(GeneralEnum):
    UNCHANGED = 0
    FIX       = 1
    FREE      = 2