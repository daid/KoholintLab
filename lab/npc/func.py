from annotations import *
from tokenizer import ParseError


@function()
def dialog(generator, state, message):
    message = message.get_string()
    state.append(f"  call_open_dialog {generator.add_dialog(message)}")
    new_state = generator.new_state()
    state.append(new_state)
    new_state.append(f"  ld a, [wDialogState]")
    new_state.append(f"  and a")
    new_state.append(f"  ret nz")
    return new_state

@function()
def giveItem(generator, state, item_id):
    item_id = item_id.get_identifier()
    state.append(f"  ld   d, {item_id}")
    state.append(f"  call GiveInventoryItem_trampoline")