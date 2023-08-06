from .util import Position
from .error import gen_error, error
from .generator import Gen, Var
from . import functions

class Node:
    """
    base node class
    """

    def __init__(self, pos: Position):
        self.pos = pos
    
    def get_pos(self) -> Position:
        return self.pos
    
    def generate(self):
        error("Invalid AST")
    
    def get(self):
        error("Invalid AST")
    
    def set(self):
        error("Invalid AST")
    
    def drename(self, vars):
        error("Invalid AST")

class CodeListNode(Node):
    """
    node with a list of code
    """

    def __init__(self, pos: Position, code: list):
        super().__init__(pos)
        
        self.code = code
    
    def get_pos(self) -> Position:
        if len(self.code) > 0:
            return self.pos + self.code[-1].get_pos()
        
        return self.pos
    
    def generate(self):
        return "\n".join([ln for ln in "\n".join([node.generate() for node in self.code]).splitlines() if ln])
    
    def drename(self, vars):
        return CodeListNode(self.pos, [c.drename(vars) for c in self.code])

class ReturnNode(Node):
    """
    function return node
    """

    def __init__(self, pos: Position, func: str, value: Node):
        super().__init__(pos)
        
        self.func = func
        self.value = value
    
    def get_pos(self) -> Position:
        return self.value.get_pos()

    def generate(self):
        return f"set __f_{self.func}_retv {self.value.get()}"
    
    def drename(self, vars):
        return ReturnNode(self.pos, self.func, self.value.drename(vars))

class LoopActionNode(Node):
    ACTIONS = ["break", "continue"]

    def __init__(self, pos: Position, name: str, action: str):
        super().__init__(pos)

        self.name = name
        self.action = action
    
    def get_pos(self) -> Position:
        return self.pos
    
    def generate(self):
        if self.action == "break":
            return f">{self.name}_e"
        elif self.action == "continue":
            return f">{self.name}_s"
    
    def drename(self, vars):
        return self

class ExternNode(Node):
    def __init__(self, pos: Position, name: str):
        super().__init__(pos)

        self.name = name
    
    def get_pos(self) -> Position:
        return self.pos
    
    def generate(self):
        return ""
    
    def drename(self, vars):
        return self

class AssignmentNode(Node):
    def __init__(self, pos: Position, var: Node, op: str, value: Node):
        super().__init__(pos)

        self.var = var
        self.op = op
        self.value = value
    
    def get_pos(self) -> Position:
        return self.pos + self.value.get_pos()
    
    def generate(self):
        if self.op == "=":
            varc, varv = self.var.set()
            valc, valv = self.value.get()
            return f"{valc}\nset {varv} {valv}\n{varc}"

        else:
            # determine operator
            op = "add" if self.op == "+=" else "sub" if self.op == "-=" else "mul" if self.op == "*=" else "div" if self.op == "/=" else ""
            if op == "":
                gen_error(self.get_pos(), f"Invalid operator: \"{self.op}\"")
            
            vasc, vasv = self.var.get()
            varc, varv = self.var.set()
            valc, valv = self.value.get()
            return f"{vasc}\n{valc}\nop {op} {varv} {vasv} {valv}\n{varc}"
    
    def drename(self, vars):
        return AssignmentNode(self.pos, self.var.drename(vars), self.op, self.value.drename(vars))

class CallNode(Node):
    def __init__(self, pos: Position, func: str, args: list):
        super().__init__(pos)

        self.func = func
        self.args = args

        self._ret_var = "_"

    def get_pos(self) -> Position:
        if len(self.args) > 0:
            return self.pos + self.args[-1].get_pos()
        
        return self.pos
    
    def generate(self):
        if self.func in functions.native:
            nargs = functions.native[self.func]
            retvar = "_"
            if self.func in functions.native_ret:
                nargs -= 1
                retvar = Gen.temp_var()
            
            if len(self.args) != nargs:
                gen_error(self.get_pos(), f"Invalid number of arguments to function \"{self.func}\" (expected {nargs}, got {len(self.args)})")
            
            code = ""
            args = []
            for a in self.args:
                ac, av = a.get()
                code += f"{ac}\n"
                args.append(av)
            
            if self.func in functions.native_ret:
                args.insert(functions.native_ret[self.func], retvar)
                self._ret_var = retvar
            else:
                self._ret_var = "_"
            
            code += f"{self.func} {' '.join(map(str, args))}"
            return code
        
        elif self.func in functions.native_sublist:
            spl = self.func.split(".")

            nargs = functions.native_sub[spl[0]][spl[1]]
            retvar = "_"
            if self.func in functions.native_sub_ret:
                nargs -= 1
                retvar = Gen.temp_var()
            self._ret_var = retvar
            
            if len(self.args) != nargs:
                gen_error(self.get_pos(), f"Invalid number of arguments to function \"{self.func}\" (expected {nargs}, got {len(self.args)})")
            
            code = ""
            args = []
            for a in self.args:
                ac, av = a.get()
                code += f"{ac}\n"
                args.append(av)
            
            if retvar != "_":
                args.insert(functions.native_sub_ret[self.func], retvar)
            
            code += f"{spl[0]} {spl[1]} {' '.join(map(str, args))}"
            return code
        
        elif self.func in functions.builtin:
            if len(self.args) != functions.builtin_params.get(self.func, functions.builtin_params_default):
                gen_error(self.get_pos(), f"Invalid number of arguments to function \"{self.func}\" (expected {nargs}, got {len(self.args)})")
            
            retvar = Gen.temp_var()
            self._ret_var = retvar
            
            code = ""
            args = []
            for a in self.args:
                ac, av = a.get()
                code += f"{ac}\n"
                args.append(av)
            
            while len(args) < 2:
                args.append("_")
            
            return f"{code}\nop {self.func} {retvar} {' '.join(map(str, args))}"

        code = ""
        for i, arg in enumerate(self.args):
            valc, valv = arg.get()
            code += f"{valc}\nset __f_{self.func}_a{i} {valv}\n"
            self._ret_var = Var(f"__f_{self.func}_ret", True)

        code += f"op add __f_{self.func}_ret @counter 1\nset @counter __f_{self.func}"

        return code
    
    def get(self):
        return self.generate(), self._ret_var
    
    def drename(self, vars):
        return CallNode(self.pos, self.func, [a.drename(vars) for a in self.args])

class ExpressionNode(Node):
    def __init__(self, pos: Position, left: Node, right: list):
        super().__init__(pos)

        self.left = left
        self.right = right
    
    def get_pos(self) -> Position:
        if len(self.right) > 0:
            return self.pos + self.right[-1][1].get_pos()
        
        return self.pos
    
    def get(self):
        valc, valv = self.left.get()

        if len(self.right) > 0:
            tmpv = Gen.temp_var(valv)
            code = f"{valc}\nset {tmpv} {valv}"

            for r in self.right:
                # determine operator
                op = "land" if r[0] == "&&" else "or" if r[0] == "||" else ""
                if op == "":
                    gen_error(self.get_pos(), f"Invalid operator")
                
                valc, valv = r[1].get()

                tmpv2 = Gen.temp_var()
                code += f"\n{valc}\nop {op} {tmpv2} {tmpv} {valv}"
                tmpv = tmpv2

            return code, tmpv

        else:
            return valc, valv
    
    def drename(self, vars):
        return ExpressionNode(self.pos, self.left.drename(vars), [(r[0], r[1].drename(vars)) for r in self.right])

class CompExpressionNode(Node):
    def __init__(self, pos: Position, left: Node, right: list):
        super().__init__(pos)

        self.left = left
        self.right = right
    
    def get_pos(self) -> Position:
        if len(self.right) > 0:
            return self.pos + self.right[-1][1].get_pos()
        
        return self.pos
    
    def get(self):
        valc, valv = self.left.get()

        if len(self.right) > 0:
            tmpv = Gen.temp_var(valv)
            code = f"{valc}\nset {tmpv} {valv}"

            for r in self.right:
                # determine operator
                op = "equal" if r[0] == "==" else "lessThan" if r[0] == "<" else "greaterThan" if r[0] == ">" else "lessThanEq" if r[0] == "<=" \
                    else "greaterThanEq" if r[0] == ">=" else "notEqual" if r[0] == "!=" else "strictEqual" if r[0] == "===" else ""
                if op == "":
                    gen_error(self.get_pos(), f"Invalid operator")
                
                valc, valv = r[1].get()

                tmpv2 = Gen.temp_var()
                code += f"\n{valc}\nop {op} {tmpv2} {tmpv} {valv}"
                tmpv = tmpv2

            return code, tmpv

        else:
            return valc, valv
    
    def drename(self, vars):
        return CompExpressionNode(self.pos, self.left.drename(vars), [(r[0], r[1].drename(vars)) for r in self.right])

class ArithExpressionNode(Node):
    def __init__(self, pos: Position, left: Node, right: list):
        super().__init__(pos)

        self.left = left
        self.right = right
    
    def get_pos(self) -> Position:
        if len(self.right) > 0:
            return self.pos + self.right[-1][1].get_pos()
        
        return self.pos
    
    def get(self):
        valc, valv = self.left.get()

        if len(self.right) > 0:
            tmpv = Gen.temp_var(valv)
            code = f"{valc}\nset {tmpv} {valv}"

            for r in self.right:
                # determine operator
                op = "add" if r[0] == "+" else "sub" if r[0] == "-" else ""
                if op == "":
                    gen_error(self.get_pos(), f"Invalid operator")
                
                valc, valv = r[1].get()

                tmpv2 = Gen.temp_var()
                code += f"\n{valc}\nop {op} {tmpv2} {tmpv} {valv}"
                tmpv = tmpv2

            return code, tmpv

        else:
            return valc, valv
    
    def drename(self, vars):
        return ArithExpressionNode(self.pos, self.left.drename(vars), [(r[0], r[1].drename(vars)) for r in self.right])

class TermNode(Node):
    def __init__(self, pos: Position, left: Node, right: list):
        super().__init__(pos)

        self.left = left
        self.right = right
    
    def get_pos(self) -> Position:
        if len(self.right) > 0:
            return self.pos + self.right[-1][1].get_pos()
        
        return self.pos
    
    def get(self):
        valc, valv = self.left.get()

        if len(self.right) > 0:
            tmpv = Gen.temp_var(valv)
            code = f"{valc}\nset {tmpv} {valv}"

            for r in self.right:
                # determine operator
                op = "mul" if r[0] == "*" else "div" if r[0] == "/" else "pow" if r[0] == "**" else ""
                if op == "":
                    gen_error(self.get_pos(), f"Invalid operator")
                
                valc, valv = r[1].get()

                tmpv2 = Gen.temp_var()
                code += f"\n{valc}\nop {op} {tmpv2} {tmpv} {valv}"
                tmpv = tmpv2

            return code, tmpv

        else:
            return valc, valv
    
    def drename(self, vars):
        return TermNode(self.pos, self.left.drename(vars), [(r[0], r[1].drename(vars)) for r in self.right])

class FactorNode(Node):
    def __init__(self, pos: Position, value: Node, flags: dict):
        super().__init__(pos)

        self.value = value
        self.flags = flags
    
    def get_pos(self) -> Position:
        return self.pos + self.value.get_pos()
    
    def get(self):
        valc, valv = self.value.get()
        tmpv = Gen.temp_var(valv)
        code = f"{valc}\nset {tmpv} {valv}"

        if not self.flags["sign"]:
            code += f"\nop sub {tmpv} 0 {tmpv}"
        if self.flags["not"]:
            code += f"\nop not {tmpv} {tmpv} 0"
        if self.flags["flip"]:
            code += f"\nop flip {tmpv} {tmpv} _"
        
        return code, tmpv
    
    def drename(self, vars):
        return FactorNode(self.pos, self.value.drename(vars), self.flags)

class ValueNode(Node):
    def __init__(self, pos: Position, value: str):
        super().__init__(pos)

        self.value = value
    
    def get_pos(self) -> Position:
        return self.pos
    
    def get(self):
        if Gen.REGEXES["ATTR"].fullmatch(self.value):
            tmpv = Gen.temp_var()
            return f"sensor {tmpv} {self.value.replace('.', ' @')}", tmpv

        return "", Var(self.value, False)
    
    def set(self):
        if Gen.REGEXES["ATTR"].fullmatch(self.value):
            tmpv = Gen.temp_var()
            spl = self.value.split(".")
            return f"control {spl[1]} {spl[0]} {tmpv} _ _", tmpv

        return "", Var(self.value, False)
    
    def drename(self, vars):
        return ValueNode(self.pos, vars.get(self.value, self.value))

class IndexedValueNode(Node):
    def __init__(self, pos: Position, value: str, idx: Node):
        super().__init__(pos)

        self.value = value
        self.idx = idx
    
    def get_pos(self) -> Position:
        return self.pos + self.idx.get_pos()
    
    def get(self):
        tmpv = Gen.temp_var()
        ic, iv = self.idx.get()
        return f"{ic}\nread {tmpv} {self.value} {iv}", tmpv
    
    def set(self):
        tmpv = Gen.temp_var()
        ic, iv = self.idx.get()
        return f"{ic}\nwrite {tmpv} {self.value} {iv}", tmpv
    
    def drename(self, vars):
        return IndexedValueNode(self.pos, vars.get(self.value, self.value), self.idx.drename(vars))

class IfNode(Node):
    def __init__(self, pos: Position, cond: Node, code: Node, elseCode: Node):
        super().__init__(pos)

        self.cond = cond
        self.code = code
        self.elseCode = elseCode
    
    def get_pos(self) -> Position:
        return self.pos + self.cond.get_pos()
    
    def generate(self):
        condc, condv = self.cond.get()
        code = self.code.generate().strip()
        elseCode = self.elseCode.generate().strip()

        if elseCode:
            ecl = Gen.temp_lab()
            el = Gen.temp_lab()
            return f"{condc}\n>{ecl} {condv} notEqual true\n{code}\n>{el}\n<{ecl}\n{elseCode}\n<{el}"
        
        else:
            el = Gen.temp_lab()
            return f"{condc}\n>{el} {condv} notEqual true\n{code}\n<{el}"
    
    def drename(self, vars):
        return IfNode(self.pos, self.cond.drename(vars), self.code.drename(vars), self.elseCode.drename(vars))

class WhileNode(Node):
    def __init__(self, pos: Position, name: str, cond: Node, code: Node):
        super().__init__(pos)

        self.name = name
        self.cond = cond
        self.code = code
    
    def get_pos(self) -> Position:
        return self.pos + self.cond.get_pos()
    
    def generate(self):
        condc, condv = self.cond.get()
        code = self.code.generate().strip()

        return f"<{self.name}_s\n{condc}\n>{self.name}_e {condv} notEqual true\n{code}\n>{self.name}_s\n<{self.name}_e"
    
    def drename(self, vars):
        return WhileNode(self.pos, self.name, self.cond.drename(vars), self.code.drename(vars))

class ForNode(Node):
    def __init__(self, pos: Position, name: str, init: Node, cond: Node, action: Node, code: Node):
        super().__init__(pos)

        self.name = name
        self.init = init
        self.cond = cond
        self.action = action
        self.code = code
    
    def get_pos(self) -> Position:
        return self.pos + self.action.get_pos()
    
    def generate(self):
        condc, condv = self.cond.get()
        init = self.init.generate()
        action = self.action.generate()
        code = self.code.generate().strip()

        return f"{init}\n<{self.name}_s\n{condc}\n>{self.name}_e {condv} notEqual true\n{code}\n{action}\n>{self.name}_s\n<{self.name}_e"
    
    def drename(self, vars):
        return ForNode(self.pos, self.name, self.init.drename(vars), self.cond.drename(vars), self.action.drename(vars), self.code.drename(vars))

class FunctionNode(Node):
    def __init__(self, pos: Position, name: str, args: list, code: Node):
        super().__init__(pos)

        self.name = name
        self.args = args
        self.code = code
    
    def get_pos(self) -> Position:
        return self.pos
    
    def generate(self):
        args = {arg: f"__f_{self.name}_a{i}" for i, arg in enumerate(self.args)}

        end_label = Gen.temp_lab()
        code = f"op add __f_{self.name} @counter 1\n>{end_label}\n"
        code += self.code.drename(args).generate()
        code += f"\nset @counter __f_{self.name}_ret\n<{end_label}"

        return code
    
    def drename(self, vars):
        return self

class EndNode(Node):
    def __init__(self, pos: Position, reset: bool):
        super().__init__(pos)

        self.reset = reset
    
    def get_pos(self) -> Position:
        return self.pos

    def generate(self):
        if self.reset:
            return "end"

        return "jump 0 always _ _"
