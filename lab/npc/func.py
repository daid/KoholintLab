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

@function()
def lookAtLink(generator, state):
    state.append(f"  call GetEntityDirectionToLink_{generator.bank_nr:02X}")
    state.append(f"  ld   hl, wEntitiesDirectionTable")
    state.append(f"  add  hl, bc")
    state.append(f"  ld   [hl], e")
    state.append(f"  call SetEntityVariantForDirection_{generator.bank_nr:02X}")

@function()
def destroy(generator, state):
    state.append(f"  call UnloadEntity")

@function()
def spawnEntity(generator, state, entity_type, x, y):
    entity_type = entity_type.get_identifier()
    state.append(f"  ld a, {entity_type}")
    state.append(f"  call SpawnNewEntity_trampoline")
    state.append(f"  jr c, :+")
    state.append(f"  ld   hl, wEntitiesPosXTable")
    state.append(f"  add  hl, de")
    state.append(f"  ld   [hl], {x.get_number()}")
    state.append(f"  ld   hl, wEntitiesPosYTable")
    state.append(f"  add  hl, de")
    state.append(f"  ld   [hl], {y.get_number()}")
    state.append(f":")
