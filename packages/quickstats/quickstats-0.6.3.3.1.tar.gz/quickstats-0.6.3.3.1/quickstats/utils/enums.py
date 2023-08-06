from enum import Enum

class GeneralEnum(Enum):
    
    @classmethod
    def on_parse_exception(cls, expr:str):
        options = cls.get_members()
        raise RuntimeError(f"invalid option \"{expr}\" for the enum class \"{cls.__name__}\" "
                           f"(allowed options: {', '.join(options)})")
    
    @classmethod
    def parse(cls, expr:str):
        if isinstance(expr, cls):
            return expr
        _expr = expr.strip().upper()
        if _expr in cls.__members__:
            return cls[_expr]
        else:
            cls.on_parse_exception(expr)
            
    @classmethod
    def get_members(cls):
        return [i.lower() for i in cls.__members__]
    
    
class DescriptiveEnum(GeneralEnum):
    def __init__(self, enum_id:int, description:str=""):
        self.enum_id = enum_id
        self.description = description
        
    @classmethod
    def on_parse_exception(cls, expr:str):
        enum_descriptions = "".join([f"    {key.lower()} - {val.description}\n" \
                                     for key, val in cls.__members__.items()])
        raise RuntimeError(f"invalid option \"{expr}\" for the enum class \"{cls.__name__}\"\n"
                           f"  Allowed options:\n{enum_descriptions}")