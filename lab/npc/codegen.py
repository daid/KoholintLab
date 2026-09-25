from .tokenizer import ParseError
from . import func
from . import annotations
from . import expression
import json


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
    def __init__(self, npc, output_stream):
        self._npc = npc
        self._output_stream = output_stream
        self._states = []
        self._dialogs = []
        
        idle_state = self.new_state()
        if npc.oninit:
            state = self._compile(idle_state, npc.oninit)
            idle_state = self.new_state('Idle')
            state.append(idle_state)
        if npc.onidle:
            post_idle_state = self._compile(idle_state, npc.onidle)
            if post_idle_state != idle_state:
                raise ParseError(npc.onidle[-1], f"onidle scripts do not allow blocking operations")
        if npc.oninteraction:
            idle_state.append(f"  call ShouldLinkTalkToEntity_{npc.bank_nr:02X}")
            idle_state.append(f"  ret nc")
            state = self._compile(idle_state, npc.oninteraction)
            state.append(idle_state)
        else:
            idle_state.append(f"ret")
        
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
                    self.output(f"  ; -> {line.label}")
                    if line == state:
                        self.output(f"  ret")
                    elif line.index == state.index + 1:
                        self.output(f"  jp IncrementEntityState")
                    else:
                        self.output(f"  call IncrementEntityState")
                        self.output(f"  ld   [hl], {line.index}")
                        self.output(f"  ret")
                else:
                    self.output(line)

    @property
    def bank_nr(self):
        return self._npc.bank_nr

    def new_state(self, label=''):
        state = EntityState()
        state.label = f"{self._npc.name}State{len(self._states)}{label}"
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
                    context = expression.Context(state, node.token)
                    result_reg = expression.compile_value(context, state, node.params[1])
                    assert result_reg == "a"
                    result_target = expression.compile_address(context, state, node.params[0])
                    if result_target.startswith("h"):
                        state.append(f"  ldh [{result_target}], {result_reg}")
                    else:
                        state.append(f"  ld [{result_target}], {result_reg}")
                    result_reg.release()
                case "if":
                    condition_label = state.gen_condition_label()
                    condition_result = expression.compile_condition(expression.Context(state, node.token), state, node.params[0])
                    match condition_result: # Turn a "true" condition into a "jump if false"
                        case "z":   # a == x
                            state.append(f"  jr nz, .false{condition_label}")
                        case "!z":  # a != x
                            state.append(f"  jr z, .false{condition_label}")
                        case "c":   # a < x
                            state.append(f"  jr nc, .false{condition_label}")
                        case "!c":  # a >= x
                            state.append(f"  jr c, .false{condition_label}")
                        case "cz":  # a <= x
                            state.append(f"  jr z, :+")
                            state.append(f"  jr nc, .false{condition_label}")
                            state.append(f":")
                        case "!cz": # a > x
                            state.append(f"  jr c, .false{condition_label}")
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

    def output(self, code):
        self._output_stream.write(code + "\n")

    def get_dialog_labels(self):
        return [f"{self._npc.name}Dialog{idx}" for idx, dialog in enumerate(self._dialogs)]
