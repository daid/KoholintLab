from tokenizer import ParseError
import func
import annotations
import json


CONSTANTS = {
    "swordLevel": "wSwordLevel",
    "shieldLevel": "wShieldLevel",
}


class EntityState:
    def __init__(self):
        self.label = None
        self.index = None
        self.code = []
        self._condition_counter = 0
    
    def append(self, code):
        self.code.append(code)
    
    def gen_condition_label(self) -> str:
        self._condition_counter += 1
        return f"{self._condition_counter:02X}"


class CodeGen:
    def __init__(self, npc):
        self._npc = npc
        self._states = []
        self._dialogs = []
        
        initial_state = self.new_state()
        if npc.oninteraction:
            initial_state.append(f"  call ShouldLinkTalkToEntity_{npc.bank_nr:02X}")
            initial_state.append(f"  ret nc")
            state = self._compile(initial_state, npc.oninteraction)
            state.append(initial_state)
        else:
            initial_state.append(f"ret")
        
        self.output("; Generated with KoholintLab Entity generator")
        self.output(f"; {npc.name} in bank {npc.bank_nr:02X}")
        for idx, dialog in enumerate(self._dialogs):
            self.output(f"{self._npc.name}Dialog{idx}:")
            self.output(f"  dialog_text {json.dumps(dialog)}")
        self.output(f"")
        self.output(f"{npc.name}SpriteData:")
        for sprite in npc.sprites:
            self.output(f"  db ${sprite[0]:02X}, ${sprite[2]:02X}, ${sprite[1]:02X}, ${sprite[3]:02X}")
        self.output(f"")
        self.output(f"{npc.entry_point}:")
        self.output(f"  ld   de, {npc.name}SpriteData")
        self.output(f"  call RenderActiveEntitySpritesPair")
        self.output(f"  call ReturnIfNonInteractive_{npc.bank_nr:02X}")
        self.output(f"  call PushLinkOutOfEntity_{npc.bank_nr:02X}")
        self.output(f"  ldh  a, [hActiveEntityState]")
        self.output(f"  JP_TABLE")
        for state in self._states:
            self.output(f"  dw {state.label}")
        for state in self._states:
            self.output(f"")
            self.output(f"{state.label}:")
            for line in state.code:
                if isinstance(line, EntityState):
                    if line == state:
                        self.output(f"  ret")
                    elif line.index == state.index + 1:
                        self.output(f"  jp IncrementEntityState ; {line.label}")
                    else:
                        self.output(f"  call IncrementEntityState")
                        self.output(f"  ld   [hl], {line.index} ; {line.label}")
                        self.output(f"  ret")
                else:
                    self.output(line)

    @property
    def bank_nr(self):
        return self._npc.bank_nr

    def new_state(self):
        state = EntityState()
        state.label = f"{self._npc.name}State{len(self._states)}"
        state.index = len(self._states)
        self._states.append(state)
        return state

    def add_dialog(self, message: str) -> str:
        self._dialogs.append(message)
        return f"{self._npc.name}Dialog{len(self._dialogs)-1}"

    def _compile(self, state, nodes):
        start_state = state
        for node in nodes:
            state.append(f"  ; {node}")
            match node.kind:
                case "call":
                    function = annotations.function_mapping.get(node.params[0].get_identifier().lower())
                    if not function:
                        raise ParseError(node.token, f"Do not know how to compile: {node}")
                    new_state = function(self, state, *node.params[1:])
                    if new_state:
                        state = new_state
                case "=":
                    result_reg = self._compile_value(state, node.params[1])
                    result_target = self._compile_address(state, node.params[0])
                    state.append(f"  ld [{result_target}], {result_reg}")
                case "if":
                    condition_label = state.gen_condition_label()
                    condition_result = self._compile_condition(state, node.params[0])
                    match condition_result:
                        case "z":
                            state.append(f"  jr nz, .false{condition_label}")
                        case "!z":
                            state.append(f"  jr z, .false{condition_label}")
                        case _:
                            raise ParseError(node.token, f"Internal compiler error: {condition_result} {node}")
                    true_end_state = self._compile(state, node.params[1])
                    if len(node.params) == 2:
                        state.append(f".false{condition_label}:")
                        if true_end_state != state:
                            new_state = self.new_state()
                            state.append(new_state)
                            true_end_state.append(new_state)
                            state = new_state
                    else:
                        if true_end_state == state:
                            state.append(f"  jr .true{condition_label}")
                        state.append(f".false{condition_label}:")
                        false_end_state = self._compile(state, node.params[2])
                        if true_end_state == state:
                            state.append(f".true{condition_label}:")
                        if true_end_state != state or false_end_state != state:
                            state = self.new_state()
                            true_end_state.append(state)
                            false_end_state.append(state)
                case _:
                    raise ParseError(node.token, f"Do not know how to compile: {node}")
        return state

    def _compile_condition(self, state, node):
        if node.kind == "!":
            res = self._compile_condition(state, node.params[0])
            if res.startswith("!"):
                return res[1:]
            return f"!{res}"
        elif node.kind == "call":
            if node.params[0].get_identifier() == "hasItem":
                item_id = node.params[1].get_identifier()
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
        raise ParseError(node.token, f"Do not know how to compile: {node}")

    def _compile_value(self, state, node):
        if node.kind == "value" and node.token.kind == "NUMBER":
            state.append(f"  ld a, {node.token.value}")
            return "a"
        raise ParseError(node.token, f"Do not know how to compile: {node}")

    def _compile_address(self, state, node):
        if node.kind == "value" and node.token.kind == "ID":
            if node.token.value in CONSTANTS:
                return CONSTANTS[node.token.value]
        raise ParseError(node.token, f"Do not know how to compile: {node}")

    def output(self, code):
        print(code)
