from . import tokenizer
from . import parser


class NPC:
    def __init__(self, filename):
        self.name = None
        self.npc_id = None
        self.assembly_file = None
        self.bank_nr = None
        self.entry_point = None
        self.graphics = []
        self.sprites = []
        self.oninit = None
        self.onidle = None
        self.oninteraction = None
        self.read_file(filename)

    def read_file(self, filename):
        tok = tokenizer.Tokenizer(filename)
        while tok.peek().kind != "EOF":
            while tok.match("NEWLINE"):
                pass
            if tok.match("EOF"):
                break
            key = tok.expect("ID")
            tok.expect(":")
            match key.value.lower():
                case "name": self.name = tok.expect("ID").value
                case "id": self.npc_id = tok.expect("NUMBER").value
                case "file": self.assembly_file = tok.expect("STRING").value
                case "bank": self.bank_nr = tok.expect("NUMBER").value
                case "entry": self.entry_point = tok.expect("STRING").value
                case "type": self.entity_type = tok.expect("ID").value
                case "graphics":
                    while tok.peek().kind != "NEWLINE":
                        slot = tok.expect("NUMBER").value
                        tok.expect(":")
                        value = tok.expect("NUMBER").value
                        self.graphics.append((slot, value))
                case "sprite":
                    tile_a = tok.expect("NUMBER").value
                    tile_b = tok.expect("NUMBER").value
                    attr_a = tok.expect("NUMBER").value
                    attr_b = tok.expect("NUMBER").value
                    self.sprites.append((tile_a, tile_b, attr_a, attr_b))
                case "oninit":
                    self.oninit = parser.parse_block(tok)
                case "onidle":
                    self.onidle = parser.parse_block(tok)
                case "oninteraction":
                    self.oninteraction = parser.parse_block(tok)
                case _:
                    print(f"Warning: Unknown top level key: {key.value}")
                    while (tok.peek().kind != "NEWLINE" or tok.peek().value != 0) and tok.peek().kind != "EOF":
                        tok.pop()
            if tok.match("EOF"):
                break
            tok.expect("NEWLINE")
        
        if self.name is None:
            self.name = f"Entity_{self.npc_id:02X}"


if __name__ == "__main__":
    import sys, os
    from . import codegen
    for arg in sys.argv[1:]:
        try:
            npc = NPC(arg)
            codegen.CodeGen(npc, sys.stdout)
        except tokenizer.ParseError as e:
            print(f"Error: {e.message}")
            if e.token:
                print(f" at: {arg}:{e.token.line}")
                if os.path.isfile(arg):
                    lines = open(arg).readlines()
                    print("-----")
                    for n in range(max(0, e.token.line - 3), min(len(lines), e.token.line + 2)):
                        if n == e.token.line - 1:
                            print(f">{lines[n].rstrip()}")
                        else:
                            print(f" {lines[n].rstrip()}")
                    print("-----")
            exit(1)
