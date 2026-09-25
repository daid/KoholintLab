from .tokenizer import ParseError

CONSTANTS = {
    "swordLevel": "wSwordLevel",
    "shieldLevel": "wShieldLevel",
    "linkX": "hLinkPositionX",
    "linkY": "hLinkPositionY"
}

COMPARE_RESULT_LR = { # Which flags result in a "true" result on "cp L, R"
    "==": "z",
    "!=": "!z",
    "<": "c",
    ">": "!cz",
    "<=": "cz",
    ">=": "!c",
}
COMPARE_RESULT_RL = { # Which flags result in a "true" result on "cp R, L"
    "==": "z",
    "!=": "!z",
    "<": "!cz",
    ">": "c",
    "<=": "!c",
    ">=": "cz",
}

class Context:
    def __init__(self, state, token):
        self._state = state
        self._token = token # For error reporting
        self._regs = {
            "a": None,
            "d": None,
            "e": None,
            "h": None,
            "l": None,
        }
    
    def __del__(self):
        for reg, value in self._regs.items():
            assert value is None, f"Internal compiler error, registers acquired but not released: {reg}"

    def acquire(self, want=None):
        if want is not None:
            if self._regs[want] is not None:
                self._move(want, self._free_reg())
            self._regs[want] = Context._RegRef(self, want)
            return self._regs[want]
        reg = self._free_reg()
        self._regs[reg] = Context._RegRef(self, reg)
        return self._regs[reg]

    def in_use(self, reg_name):
        return self._regs[reg_name] is not None

    def preserve(self, state, *regs):
        return Context._Preserve(self, state, regs)
    
    def free_up(self, reg):
        if self._regs[reg] is not None:
            self._move(reg, self._free_reg())

    def _move(self, src, target):
        self.free_up(target)
        self._regs[src]._value = target
        self._state.append(f"  ld {target}, {src}")
        self._regs[target] = self._regs[src]
        self._regs[src] = None

    def _free_reg(self):
        for reg in "adehl":
            if self._regs[reg] is None:
                return reg
        raise ParseError(self._token, "Ran out of registers to allocate...")

    class _RegRef:
        def __init__(self, context, value):
            self._context = context
            self._value = value
        
        def assure(self, value):
            if self._value == value:
                return
            self._context._move(self._value, value)
        
        def release(self):
            assert self._context._regs[self._value] is self
            self._context._regs[self._value] = None
        
        def __str__(self):
            return self._value

        def __eq__(self, other):
            if isinstance(other, str):
                return self._value == other
            return self is other

        @property
        def value(self):
            return self._value

    class _Preserve:
        def __init__(self, context, state, regs):
            self._context = context
            self._state = state
            self._regs = regs
        def __enter__(self):
            for reg in self._regs:
                if any(self._context.in_use(c) for c in reg):
                    raise ParseError(self._context._token, "Preserve not fully implemented yet")
        def __exit__(self, exc_type, exc_value, traceback):
            pass


def compile_condition(context, state, node):
    if node.kind == "!":
        res = compile_condition(context, state, node.params[0])
        if res.startswith("!"):
            return res[1:]
        return f"!{res}"
    elif node.kind == "call":
        if node.params[0].get_identifier() == "hasItem":
            item_id = node.params[1].get_identifier()
            with context.preserve(state, "a", "de", "hl"):
                state.append(f"  ld hl, wInventoryItems.BButtonSlot")
                state.append(f"  ld d, INVENTORY_SLOT_COUNT")
                state.append(f": ld a, [hl+]")
                state.append(f"  cp {item_id}")
                state.append(f"  jr z, :+")
                state.append(f"  dec d")
                state.append(f"  jr nz, :-")
                state.append(f"  rla ; clear zero flag")
                state.append(f": ; z set if item found")
            return "z"
    elif node.kind in {"<", ">", "<=", ">=", "==", "!="}:
        left_reg = compile_value(context, state, node.params[0])
        assert left_reg == "a"
        if node.params[1].is_number():
            state.append(f"  cp a, {node.params[1].get_number()}")
            left_reg.release()
            return COMPARE_RESULT_LR[node.kind]
        else:
            state.append(f"  ld d, a")
            right_reg = compile_value(context, state, node.params[1])
            assert right_reg == "a"
            state.append(f"  cp a, d")
            left_reg.release()
            right_reg.release()
            return COMPARE_RESULT_RL[node.kind]
    raise ParseError(node.token, f"Do not know how to compile: {node}")


def compile_value(context, state, node):
    if node.kind == "value" and node.token.kind == "NUMBER":
        reg = context.acquire()
        state.append(f"  ld {reg}, {node.token.value}")
        return reg
    if node.kind == "value" and node.token.kind == "ID":
        if node.token.value in CONSTANTS:
            reg = context.acquire("a")
            if CONSTANTS[node.token.value].startswith("h"):
                state.append(f"  ldh {reg}, [{CONSTANTS[node.token.value]}]")
            else:
                state.append(f"  ld {reg}, [{CONSTANTS[node.token.value]}]")
            return reg
    if node.kind == "+":
        left_reg = compile_value(context, state, node.params[0])
        if node.params[1].is_number():
            assert left_reg == "a", f"Got reg: {left_reg} expected 'a'"
            state.append(f"  add {left_reg}, {node.params[1].get_number()}")
        else:
            right_reg = compile_value(context, state, node.params[1])
            assert left_reg == "a" or right_reg == "a", f"Got reg: {left_reg} or {right_reg} expected 'a'"
            if right_reg == "a":
                left_reg, right_reg = right_reg, left_reg
            state.append(f"  add {left_reg}, {right_reg}")
            right_reg.release()
        return left_reg
    if node.kind == "-" and len(node.params) == 2:
        if node.params[1].is_number():
            left_reg = compile_value(context, state, node.params[0])
            assert left_reg == "a", f"Got reg: {left_reg} expected 'a'"
            state.append(f"  sub {left_reg}, {node.params[1].get_number()}")
        else:
            right_reg = compile_value(context, state, node.params[1])
            context.free_up("a")
            left_reg = compile_value(context, state, node.params[0])
            left_reg.assure("a")
            state.append(f"  sub {left_reg}, {right_reg}")
            right_reg.release()
        return left_reg
    if node.kind == "-" and len(node.params) == 1:
        context.free_up("a")
        reg = compile_value(context, state, node.params[0])
        reg.assure("a")
        state.append(f"  cpl")
        state.append(f"  inc {reg}")
        return reg
    raise ParseError(node.token, f"Do not know how to compile: {node}")


def compile_address(context, state, node):
    if node.kind == "value" and node.token.kind == "ID":
        if node.token.value in CONSTANTS:
            return CONSTANTS[node.token.value]
    raise ParseError(node.token, f"Do not know how to compile: {node}")
