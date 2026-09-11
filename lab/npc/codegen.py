from tokenizer import ParseError
import json


class EntityState:
    def __init__(self):
        self.label = None
        self.index = None
        self.code = []
    
    def append(self, code):
        self.code.append(code)


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
                    function = node.params[0].get_identifier()
                    if function == "dialog":
                        message = node.params[1].get_string()
                        state.append(f"  call_open_dialog {self.add_dialog(message)}")
                        new_state = self.new_state()
                        state.append(new_state)
                        new_state.append(f"  ld a, [wDialogState]")
                        new_state.append(f"  and a")
                        new_state.append(f"  ret nz")
                        state = new_state
                    elif function == "giveItem":
                        state.append("...")
                    else:
                        raise ParseError(node.token, f"Do not know how to compile: {node}")
                case "if":
                    state.append(f"IF {node.params[0]}")
                    true_end_state = self._compile(state, node.params[1])
                    state.append("ELSE")
                    false_end_state = self._compile(state, node.params[2])
                    state.append(f"END {true_end_state} {false_end_state}")
                    if true_end_state != state or false_end_state != state:
                        state = self.new_state()
                        true_end_state.append(state)
                        false_end_state.append(state)
                    # raise ParseError(node.token, f"Do not know how to compile: {node}")
                case _:
                    raise ParseError(node.token, f"Do not know how to compile: {node}")
        return state

    def output(self, code):
        print(code)
