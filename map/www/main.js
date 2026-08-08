"use strict";
var current_room;
var current_room_image;
var tileset_image;
var tileset_info;
var entities_image;
var entities_info;
var selected_tile;
var selected_entity;
async function save() {
    await fetch(`/save`);
    console.log("Saved");
}
async function doroomcopy() {
    var target = parseInt(prompt("which room to copy to?"), 16);
    await fetch(`/room_copy?source=${current_room.id}&target=${target}`)
}
async function load_room_edit(room_id) {
    current_room = await(await fetch(`/room_info?${room_id}`)).json();

    document.getElementById("content").innerHTML = "";

    var top_canvas = canvasElement(160, 16, 2);
    var left_canvas = canvasElement(16, 128, 2);
    var bottom_canvas = canvasElement(160, 16, 2);
    var right_canvas = canvasElement(16, 128, 2);
    var canvas = canvasElement(160, 128, 2);
    canvas.id = "map";
    document.getElementById("content").appendChild(createTable([
        [null, top_canvas, null],
        [left_canvas, canvas, right_canvas],
        [null, bottom_canvas, null],
    ]));

    canvas = canvasElement(256, 256+16, 2);
    canvas.id = "tileset";
    document.getElementById("content").appendChild(canvas);
    canvas = canvasElement(256, 256, 2);
    canvas.id = "entities";
    document.getElementById("content").appendChild(canvas);
    document.getElementById("header").innerHTML = `<button onclick='load_map(${current_room.map_id})'>To map</button><button onclick='save()'>Save</button>${to_hex(current_room.num, 3)}<button onclick='doroomcopy()'>Copy to...</button>`;

    entities_info = await(await fetch(`/get_entities_info`)).json();
    var image = await fetch(`/render_entities?${current_room.id}`);
    entities_image = new ImageData(new Uint8ClampedArray(await image.bytes()), 256, 256);
    draw_entities_image();

    var image = await fetch(`/render_room?${current_room.id}`);
    current_room_image = new ImageData(new Uint8ClampedArray(await image.bytes()), 160, 128);
    draw_current_room();
    await update_tileset_image();

    var map_info = await (await fetch(`/map_info?${current_room.map_id}`)).json();
    for(var info of map_info) {
        if (info.x == current_room.x - 1 && info.y == current_room.y) {
            var image = await fetch(`/render_room?${info.id}`);
            var image_data = new ImageData(new Uint8ClampedArray(await image.bytes()), 160, 128);
            left_canvas.getContext("2d").putImageData(image_data, 16-160, 0);
            left_canvas.room_id = info.id;
        }
        if (info.x == current_room.x + 1 && info.y == current_room.y) {
            var image = await fetch(`/render_room?${info.id}`);
            var image_data = new ImageData(new Uint8ClampedArray(await image.bytes()), 160, 128);
            right_canvas.getContext("2d").putImageData(image_data, 0, 0);
            right_canvas.room_id = info.id;
        }
        if (info.x == current_room.x && info.y == current_room.y - 1) {
            var image = await fetch(`/render_room?${info.id}`);
            var image_data = new ImageData(new Uint8ClampedArray(await image.bytes()), 160, 128);
            top_canvas.getContext("2d").putImageData(image_data, 0, 16-128);
            top_canvas.room_id = info.id;
        }
        if (info.x == current_room.x && info.y == current_room.y + 1) {
            var image = await fetch(`/render_room?${info.id}`);
            var image_data = new ImageData(new Uint8ClampedArray(await image.bytes()), 160, 128);
            bottom_canvas.getContext("2d").putImageData(image_data, 0, 0);
            bottom_canvas.room_id = info.id;
        }
    }
    left_canvas.onclick = right_canvas.onclick = top_canvas.onclick = bottom_canvas.onclick = function(e) {
        if (e.target.room_id === undefined) return;
        load_room_edit(e.target.room_id);
    };

    document.getElementById(`tileset`).onmousedown = function(e) {
        var [x, y] = get_tile_clicked(e);
        selected_tile = tileset_info[x + y * 16];
        selected_entity = undefined;
        document.getElementById("tile_attr").value = selected_tile.attr
        info.innerText = JSON.stringify(selected_tile);
        draw_tileset_image();
        draw_entities_image();
    };
    document.getElementById(`entities`).onmousedown = function(e) {
        var [x, y] = get_tile_clicked(e);
        selected_tile = undefined;
        document.getElementById("tile_attr").value = ""
        selected_entity = entities_info[x + y * 16];
        info.innerText = JSON.stringify(selected_entity);
        draw_tileset_image();
        draw_entities_image();
    };
    document.getElementById(`map`).onmousedown = async function(e) {
        var [x, y] = get_tile_clicked(e);
        if (selected_tile !== undefined) {
            var image = await fetch(`/update_room_tile?room=${current_room.id}&x=${x}&y=${y}&tile=${selected_tile.id}`);
            current_room_image = new ImageData(new Uint8ClampedArray(await image.bytes()), 160, 128);
            draw_current_room();
        }
        if (selected_entity !== undefined) {
            var image = await fetch(`/update_room_entity?room=${current_room.id}&x=${x}&y=${y}&entity=${selected_entity.id}`);
            current_room_image = new ImageData(new Uint8ClampedArray(await image.bytes()), 160, 128);
            draw_current_room();
        }
    };
    document.getElementById(`map`).oncontextmenu = function(e) { e.preventDefault(); return false; };
    document.getElementById(`map`).onmousemove = function(e) { if (e.buttons != 0) e.target.onmousedown(e); };
    var info = document.createElement("div");
    info.id = "info";
    document.getElementById("content").appendChild(info);
    var tile_attr = document.createElement("input");
    tile_attr.id = "tile_attr";
    tile_attr.oninput = async function() {
        if (tile_attr.value.length == 8 && selected_tile) {
            var image = await fetch(`/update_tile_attr?room=${current_room.id}&tile=${selected_tile.id}&attr=${tile_attr.value}`);
            current_room_image = new ImageData(new Uint8ClampedArray(await image.bytes()), 160, 128);
            draw_current_room();
            await update_tileset_image();
        }
    }
    document.getElementById("content").appendChild(tile_attr);

    if (current_room.num < 0x100) {
        document.getElementById("content").appendChild(roomDataSelector("Tileset", "tileset", overworld_tileset_table));
        document.getElementById("content").appendChild(roomDataSelector("Animation", "animation", animation_table));
        document.getElementById("content").appendChild(roomDataSelector("Attrib", "attribute_table", overworld_attr_table));
        document.getElementById("content").appendChild(roomDataSelector("Palette", "palette_index", palette_index_table));
    } else {
        document.getElementById("content").appendChild(roomDataSelector("Tileset", "tileset", underworld_tileset_table));
        document.getElementById("content").appendChild(roomDataSelector("Animation", "animation", animation_table));
        document.getElementById("content").appendChild(roomDataSelector("Event", "event", event_table));
        if (current_room.palette_index !== null)
            document.getElementById("content").appendChild(roomDataSelector("Palette", "palette_index", underworld_palette_index_table));
    }
    document.getElementById("content").appendChild(roomDataSelector("ChestItem", "chestitem", item_table));
    for(var n=0; n<4; n++) {
        var div = document.createElement("div");
        div.innerText = "Warp:";
        var target_room = document.createElement("input");
        target_room.id = `warp${n}_target`
        target_room.style.width = "30px";
        target_room.oninput = update_warp_data
        div.appendChild(target_room);
        var target_x = document.createElement("input");
        target_x.id = `warp${n}_x`
        target_x.style.width = "30px";
        target_x.oninput = update_warp_data
        div.appendChild(target_x);
        var target_y = document.createElement("input");
        target_y.id = `warp${n}_y`
        target_y.style.width = "30px";
        target_y.oninput = update_warp_data
        div.appendChild(target_y);
        var goto = document.createElement("button");
        goto.innerText = "go";
        goto.my_index = n;
        goto.onclick = function(e) {
            var target = document.getElementById(`warp${e.target.my_index}_target`).value;
            target = parseInt(target, 16);
            if (isNaN(target)) return;
            load_room_edit(target);
        };
        div.appendChild(goto)
        document.getElementById("content").appendChild(div);
        if (current_room.warpdata[n]) {
            target_room.value = to_hex(current_room.warpdata[n].target, 3);
            target_x.value = to_hex(current_room.warpdata[n].target_x, 2);
            target_y.value = to_hex(current_room.warpdata[n].target_y, 2);
        }
    }
}

async function update_warp_data() {
    var warps = []
    for(var n=0; n<4; n++) {
        var room = parseInt(document.getElementById(`warp${n}_target`).value, 16);
        var x = parseInt(document.getElementById(`warp${n}_x`).value, 16);
        var y = parseInt(document.getElementById(`warp${n}_y`).value, 16);
        if (!isNaN(room) && !isNaN(x) && !isNaN(y)) {
            warps.push({target: room, target_x: x, target_y: y});
        }
    }
    await fetch(`/update_room_data?room=${current_room.id}&key=warpdata&value=${JSON.stringify(warps)}`)
}

async function load_map(map_id) {
    var info = await (await fetch(`/map_info?${map_id}`)).json();
    var span = document.createElement("span");
    span.style.display = "inline-grid";
    var xmin = 16;
    var ymin = 16;
    for(var room of info) { if (room.x < xmin) xmin = room.x; if (room.y < ymin) ymin = room.y; }
    info.forEach((room) => {
        var canvas = canvasElement(160, 128, 1);
        canvas.style.gridColumn = room.x-xmin+1;
        canvas.style.gridRow = room.y-ymin+1;
        span.appendChild(canvas);

        fetch(`/render_room?${room.id}`).then(async function (image) {
            canvas.onmousedown = async function(e) {
                if (e.button == 0)
                    load_room_edit(room.id);
                if (e.button == 2) {
                    var target = prompt(`Move to x,y (current: ${room.x},${room.y})`).split(",");
                    if (target.length == 2) {
                        var x = parseInt(target[0]);
                        var y = parseInt(target[1]);
                        await fetch(`/move_room?room=${room.id}&x=${x}&y=${y}`);
                        await load_map(map_id);
                    }
                }
            };
            canvas.oncontextmenu = function(e) { return false; };
            var ctx = canvas.getContext("2d");
            var img = new ImageData(new Uint8ClampedArray(await image.bytes()), 160, 128);
            ctx.putImageData(img, 0, 0);
        });
    });
    document.getElementById("content").innerHTML = "";
    document.getElementById("content").appendChild(span);
    document.getElementById("header").innerHTML = `<button onclick='load_map_selection()'>Select map</button><button onclick='save()'>Save</button>`;
}
async function load_map_selection() {
    var info = await (await fetch(`/maps`)).json();
    var html = "";
    for(var map of info) {
        html += `<button onclick='load_map(${map.id})'>${map.name}</button><br>`;
    }
    document.getElementById("content").innerHTML = html;
    document.getElementById("header").innerHTML = `<button onclick='save()'>Save</button>`;
}
load_map_selection();


function draw_current_room() {
    var canvas = document.getElementById(`map`);
    var ctx = canvas.getContext("2d");
    ctx.putImageData(current_room_image, 0, 0);
}

function draw_tileset_image() {
    var canvas = document.getElementById(`tileset`);
    var ctx = canvas.getContext("2d");
    ctx.putImageData(tileset_image, 0, 0);
    for(var idx=0; idx<tileset_info.length; idx++) {
        if (tileset_info[idx] == selected_tile) {
            var x = idx % 16;
            var y = ~~(idx / 16);
            ctx.strokeStyle = "red";
            ctx.lineWidth = 2;
            ctx.beginPath();
            ctx.rect(x*16, y*16, 16, 16);
            ctx.stroke();
        }
    }
}

function draw_entities_image() {
    var canvas = document.getElementById(`entities`);
    var ctx = canvas.getContext("2d");
    ctx.putImageData(entities_image, 0, 0);
    for(var idx=0; idx<entities_info.length; idx++) {
        if (entities_info[idx] == selected_entity) {
            var x = idx % 16;
            var y = ~~(idx / 16);
            ctx.strokeStyle = "red";
            ctx.lineWidth = 2;
            ctx.beginPath();
            ctx.rect(x*16, y*16, 16, 16);
            ctx.stroke();
        }
    }
}

async function update_tileset_image()
{
    var image = await fetch(`/render_tileset?${current_room.id}`);
    tileset_info = await(await fetch(`/get_tileset_info?${current_room.id}`)).json();
    tileset_image = new ImageData(new Uint8ClampedArray(await image.bytes()), 256, 256+16);
    draw_tileset_image();
}

function to_hex(num, length) {
    var s = num.toString(16).toUpperCase();
    while(s.length < length)
        s = "0" + s;
    return s;
}

function draw_hex2(ctx, x, y, num) {
    num = to_hex(num, 2);
    ctx.font = "12px monospace";
    ctx.fillStyle = "white";
    for(var yo of [9.5, 10.5, 11.5]) {
        for(var xo of [0.5, 1.5, 2.5]) {
            ctx.fillText(num, x * 16 + xo, y * 16 + yo);
        }
    }
    ctx.fillStyle = "black";
    ctx.fillText(num, x * 16 + 1.5, y * 16 + 10.5);
}

function get_tile_clicked(e) {
    var rect = e.target.getBoundingClientRect();
    var x = (e.clientX - rect.left) * window.devicePixelRatio;
    var y = (e.clientY - rect.top) * window.devicePixelRatio;
    return [~~(x/32), ~~(y/32)]
}

function canvasElement(w, h, scale, style) {
    w = w || 160;
    h = h || 128;
    scale = (scale || 1) / window.devicePixelRatio;
    var canvas = document.createElement("canvas");
    canvas.width = w;
    canvas.height = h;
    canvas.style.width = `${w * scale}px`;
    canvas.style.height = `${h * scale}px`;
    return canvas;
}

function createTable(data) {
    var table = document.createElement("table");
    for(var row of data) {
        var tr = document.createElement("tr");
        for(var col of row) {
            var td = document.createElement("td");
            if (col)
                td.appendChild(col);
            tr.appendChild(td);
        }
        table.appendChild(tr);
    }
    table.style.display = 'inline-block';
    return table
}

function roomDataSelector(label, key, table) {
    var span = document.createElement("div");
    span.appendChild(document.createTextNode(label));
    var select = document.createElement("select");
    span.appendChild(select);
    for(var option of table) {
        var opt = document.createElement('option');
        opt.value = option.value;
        opt.innerText = option.label;
        select.appendChild(opt);
    }
    for(var idx in select.options) {
        if (select.options[idx].value == current_room[key])
            select.selectedIndex = idx;
    }
    select.oninput = async function(e) {
        var image = await fetch(`/update_room_data?room=${current_room.id}&key=${key}&value=${select.value}`);
        current_room_image = new ImageData(new Uint8ClampedArray(await image.bytes()), 160, 128);
        draw_current_room();
        await update_tileset_image();
    };
    return span;
}

var palette_index_table = [
    {"value": 0x00, "label": "00: Mysterious Forest"},
    {"value": 0x01, "label": "01: Toronbo Shores"},
    {"value": 0x02, "label": "02: South of the Village (ext: L1 Tail Cave)"},
    {"value": 0x03, "label": "03: Mabe Village, South of the Village"},
    {"value": 0x04, "label": "04: Signpost Maze, Pothole Field, Ukuku Prairie (ext: L3 Key Cavern, Richard's Villa)"},
    {"value": 0x05, "label": "05: Ukuku Prairie (beehive, skull rock)"},
    {"value": 0x06, "label": "06: Kanalet Castle"},
    {"value": 0x07, "label": "07: Tabahl Wasteland, Cemetary, Koholint Prairie (ext: Camera Shop, Crazy Tracy, Witch's Hut)"},
    {"value": 0x08, "label": "08: Tal Tal Heights (ext: Raft Shop, pit south of the Ghost's gravestone)"},
    {"value": 0x09, "label": "09: Martha's Bay, Ukuku Prairie (ext: L5 Catfish's Maw, House by the Bay)"},
    {"value": 0x0A, "label": "0A: Ukuku Prairie (ext: Seashell Mansion)"},
    {"value": 0x0B, "label": "0B: Face Shrine"},
    {"value": 0x0C, "label": "0C: Animal Village, East of the Bay"},
    {"value": 0x0D, "label": "0D: Yarna Desert, East of the Bay"},
    {"value": 0x0E, "label": "0E: Goponga Swamp (ext: L2 Bottle Grotto)"},
    {"value": 0x0F, "label": "0F: Tal Tal Mountain Range"},
    {"value": 0x10, "label": "10: Goponga Swamp West"},
    {"value": 0x11, "label": "11: Rapids Ride, Tal Tal Heights"},
    {"value": 0x12, "label": "12: Face Shrine South"},
    {"value": 0x13, "label": "13: Mt. Tamaranch (ext: Wind Fish's Egg)"},
    {"value": 0x14, "label": "14: Mt. Tamaranch, Tal Tal Mountain Range (bridge west)"},
    {"value": 0x15, "label": "15: Tal Tal Mountain Range (ext: Hen House)"},
    {"value": 0x16, "label": "16: Tal Tal Mountain Range (ext: L7 Eagle's Tower)"},
    {"value": 0x17, "label": "17: Tal Tal Heights (ext: L4 Angler's Tunner)"},
    {"value": 0x18, "label": "18: Toronbo Shores (ext: Sale's House o' Bananas)"},
    {"value": 0x19, "label": "19: Tal Tal Mountain Range (ext: L8 Turtle Rock)"},
    {"value": 0x1A, "label": "1A: Kanalet Castle (Kiki's bridge)"},
    {"value": 0x1B, "label": "1B: Animal Village (ext: Christine's house)"},
    {"value": 0x1C, "label": "1C: Martha's Bay (North of L3 Key Cavern)"},
    {"value": 0x1D, "label": "1D: Face Shrine North (ext: L6 Face Shrine)"},
    {"value": 0x1E, "label": "1E: Mabe Village (ext: Ulrira's House)"},
]
var underworld_palette_index_table = [
    {"value": 0x00, "label": "00: "},
    {"value": 0x01, "label": "01: "},
    {"value": 0x02, "label": "02: "},
    {"value": 0x03, "label": "03: "},
    {"value": 0x04, "label": "04: "},
    {"value": 0x05, "label": "05: "},
    {"value": 0x06, "label": "06: "},
    {"value": 0x07, "label": "07: "},
    {"value": 0x08, "label": "08: "},
    {"value": 0x09, "label": "09: "},
    {"value": 0x0A, "label": "0A: "},
    {"value": 0x0B, "label": "0B: "},
    {"value": 0x0C, "label": "0C: "},
    {"value": 0x0D, "label": "0E: "},
    {"value": 0x0E, "label": "0D: "},
    {"value": 0x0F, "label": "0F: "},
    {"value": 0x10, "label": "10: "},
    {"value": 0x11, "label": "11: "},
    {"value": 0x12, "label": "12: "},
    {"value": 0x13, "label": "13: "},
    {"value": 0x14, "label": "14: "},
    {"value": 0x15, "label": "15: "},
    {"value": 0x16, "label": "16: "},
    {"value": 0x17, "label": "17: "},
    {"value": 0x18, "label": "18: "},
    {"value": 0x19, "label": "19: "},
    {"value": 0x1A, "label": "1A: "},
    {"value": 0x1B, "label": "1B: "},
    {"value": 0x1C, "label": "1C: "},
    {"value": 0x1D, "label": "1E: "},
    {"value": 0x1E, "label": "1D: "},
    {"value": 0x1F, "label": "1F: "},
    {"value": 0x20, "label": "20: "},
    {"value": 0x21, "label": "21: "},
    {"value": 0x22, "label": "22: "},
]
var overworld_tileset_table = [
    {"value": 0x0F, "label": "No change"},
    {"value": 0x1A, "label": "1A: CAMERA_SHOP"},
    {"value": 0x1C, "label": "1C: TURTLE_ROCK"},
    {"value": 0x1E, "label": "1E: SEASHELL_MANSION"},
    {"value": 0x20, "label": "20: MYSTERIOUS_WOODS"},
    {"value": 0x22, "label": "22: BEACH"},
    {"value": 0x24, "label": "24: PRAIRIE_STONE_HEAD"},
    {"value": 0x26, "label": "26: MABE_VILLAGE"},
    {"value": 0x28, "label": "28: KANALET_CASTLE"},
    {"value": 0x2A, "label": "2A: FACE_SHRINE"},
    {"value": 0x2C, "label": "2C: YARNA_DESERT"},
    {"value": 0x2E, "label": "2E: PRAIRIE_SOUTH"},
    {"value": 0x30, "label": "30: EAGLES_TOWER"},
    {"value": 0x32, "label": "32: RAFTING_GAME"},
    {"value": 0x34, "label": "34: ANGLERS_TUNNEL"},
    {"value": 0x36, "label": "36: GOPONGO_SWAMP"},
    {"value": 0x38, "label": "38: GRAVEYARD"},
    {"value": 0x3A, "label": "3A: MARTHAS_BAY"},
    {"value": 0x3C, "label": "3C: EGG"},
    {"value": 0x3E, "label": "3E: TARAMANCH_MIDDLE"},
]
var overworld_attr_table = [
    {'value': 'OverworldObjectsAttrmap_00', 'label': '00 TOWN Purple'},
    {'value': 'OverworldObjectsAttrmap_01', 'label': '01 TOWN Gray'},
    {'value': 'OverworldObjectsAttrmap_02', 'label': '02 TOWN Blue'},
    {'value': 'OverworldObjectsAttrmap_03', 'label': '03 24'},
    {'value': 'OverworldObjectsAttrmap_04', 'label': '04 22 3A Beach'},
    {'value': 'OverworldObjectsAttrmap_05', 'label': '05 2E'},
    {'value': 'OverworldObjectsAttrmap_06', 'label': '06 2E'},
    {'value': 'OverworldObjectsAttrmap_07', 'label': '07 26'},
    {'value': 'OverworldObjectsAttrmap_08', 'label': '08 0F 2A 3A'},
    {'value': 'OverworldObjectsAttrmap_09', 'label': '09 0F 3A'},
    {'value': 'OverworldObjectsAttrmap_0A', 'label': '0A 0F 26'},
    {'value': 'OverworldObjectsAttrmap_0B', 'label': '0B 2C DESERT'},
    {'value': 'OverworldObjectsAttrmap_0C', 'label': '0C 26 TOWN Pink'},
    {'value': 'OverworldObjectsAttrmap_0D', 'label': '0D 36 SWAMP'},
    {'value': 'OverworldObjectsAttrmap_0E', 'label': '0E 0F'},
    {'value': 'OverworldObjectsAttrmap_0F', 'label': '0F 0F 1A'},
    {'value': 'OverworldObjectsAttrmap_10', 'label': '10 20 WOODS A'},
    {'value': 'OverworldObjectsAttrmap_11', 'label': '11 0F WOODS B'},
    {'value': 'OverworldObjectsAttrmap_12', 'label': '12 26 TOWN Blue'},
    {'value': 'OverworldObjectsAttrmap_13', 'label': '13 0F 26 TOWN Red'},
    {'value': 'OverworldObjectsAttrmap_14', 'label': '14 0F 28 CASTLE Red'},
    {'value': 'OverworldObjectsAttrmap_15', 'label': '15 28 CASTLE Blue'},
    {'value': 'OverworldObjectsAttrmap_16', 'label': '16 28 CASTLE Red'},
    {'value': 'OverworldObjectsAttrmap_18', 'label': '18'},
    {'value': 'OverworldObjectsAttrmap_17', 'label': '17 24 3A'},
    {'value': 'OverworldObjectsAttrmap_19', 'label': '19 1E'},
    {'value': 'OverworldObjectsAttrmap_1A', 'label': '1A 0F 38'},
    {'value': 'OverworldObjectsAttrmap_1B', 'label': '1B 38'},
    {'value': 'OverworldObjectsAttrmap_1C', 'label': '1C 38'},
    {'value': 'OverworldObjectsAttrmap_1D', 'label': '1D 1C 3E TALTAL'},
    {'value': 'OverworldObjectsAttrmap_1E', 'label': '1E 1C TALTAL phone'},
    {'value': 'OverworldObjectsAttrmap_1F', 'label': '1F 2A ARMOS'},
    {'value': 'OverworldObjectsAttrmap_20', 'label': '20 0F'},
    {'value': 'OverworldObjectsAttrmap_21', 'label': '21 3C 3E EGG'},
    {'value': 'OverworldObjectsAttrmap_22', 'label': '22 30 3E TALTAL MID'},
    {'value': 'OverworldObjectsAttrmap_23', 'label': '23 30 EAGLE TOWER'},
    {'value': 'OverworldObjectsAttrmap_24', 'label': '24 3E'},
    {'value': 'OverworldObjectsAttrmap_25', 'label': '25 0F 34'},
    {'value': 'OverworldObjectsAttrmap_26', 'label': '26 3E'},
    {'value': 'OverworldObjectsAttrmap_27', 'label': '27 32 RAPIDS'},
]
var animation_table = [
    {'value': 0x00, 'label': '00: NONE'},
    {'value': 0x02, 'label': '02: TIDE'},
    {'value': 0x03, 'label': '03: VILLAGE'},
    {'value': 0x04, 'label': '04: DUNGEON_1'},
    {'value': 0x05, 'label': '05: UNDERGROUND'},
    {'value': 0x06, 'label': '06: LAVA'},
    {'value': 0x07, 'label': '07: DUNGEON_2'},
    {'value': 0x08, 'label': '08: QUICKSAND'},
    {'value': 0x09, 'label': '09: CURRENTS'},
    {'value': 0x0A, 'label': '0A: WATER WATERFALL RAPIDS1'},
    {'value': 0x0B, 'label': '0B: WATER WATERFALL SKYLINE'},
    {'value': 0x0C, 'label': '0C: WATER_DUNGEON'},
    {'value': 0x0D, 'label': '0D: LIGHT_BEAM'},
    {'value': 0x0E, 'label': '0E: CRYSTAL_BLOCK'},
    {'value': 0x0F, 'label': '0F: BUBBLES'},
    {'value': 0x10, 'label': '10: WEATHER_VANE'},
]
var underworld_tileset_table = [
    {"value": 0xFF, "label": "FF: No change"},
    {"value": 0x00, "label": "00: BOSS DOOR, STAIRS UP"},
    {"value": 0x01, "label": "01: DUNGEON ENTRANCE"},
    {"value": 0x02, "label": "02: FLIPDOOR, KEYBLOCK, STAIRS UP"},
    {"value": 0x03, "label": "03: KNIGHT IN WALL"},
    {"value": 0x04, "label": "04: SHOP"},
    {"value": 0x05, "label": "05: CAVE"},
    {"value": 0x06, "label": "06: BOSS DOOR, KEYBLOCK"},
    {"value": 0x07, "label": "07: KEYBLOCK, WALLSTAIRS UP, HOOK-BRIDGE"},
    {"value": 0x08, "label": "08: HOUSE"},
    {"value": 0x09, "label": "09: KEYBLOCK, CRYSTAL BLOCK, PUZZLE TILE"},
    {"value": 0x0A, "label": "0A: KEYBLOCK, CRYSTAL BLOCK, STAIRS UP"},
    {"value": 0x0B, "label": "0B: FLIPDOOR, WALLSTAIRS DOWN, STAIRS UP"},
    {"value": 0x0C, "label": "0C: CAVE, CRYSTAL BLOCK"},
    {"value": 0x0D, "label": "0D: HOOKSHOT BRIDGE"},
    {"value": 0x0E, "label": "0E: BOSSDOOR, WALLSTAIRS UP"},
    {"value": 0x0F, "label": "0F: MAD BATTER"},
    {"value": 0x17, "label": "17: BOSSDOOR, WALLSTAIRS UP"},
    {"value": 0x18, "label": "18: MAMU"},
    {"value": 0x19, "label": "19: FAIRY"},
    {"value": 0x1A, "label": "1A: WINDFISH FLOOR"},
]
var item_table = [
    {"value": 0x00, "label": "POWER_BRACELET"},
    {"value": 0x01, "label": "SHIELD"},
    {"value": 0x02, "label": "BOW"},
    {"value": 0x03, "label": "HOOKSHOT"},
    {"value": 0x04, "label": "MAGIC_ROD"},
    {"value": 0x05, "label": "PEGASUS_BOOTS"},
    {"value": 0x06, "label": "OCARINA"},
    {"value": 0x07, "label": "FEATHER"},
    {"value": 0x08, "label": "SHOVEL"},
    {"value": 0x09, "label": "MAGIC_POWDER"},
    {"value": 0x0A, "label": "BOMB"},
    {"value": 0x0B, "label": "SWORD"},
    {"value": 0x0C, "label": "FLIPPERS"},
    {"value": 0x0D, "label": "MAGNIFYING_LENS"},
    {"value": 0x10, "label": "MEDICINE"},
    {"value": 0x11, "label": "TAIL_KEY"},
    {"value": 0x12, "label": "ANGLER_KEY"},
    {"value": 0x13, "label": "FACE_KEY"},
    {"value": 0x14, "label": "BIRD_KEY"},
    // {"value": 0xFF, "label": "SLIME_KEY"},
    {"value": 0x15, "label": "GOLD_LEAF"},
    {"value": 0x1B, "label": "RUPEES_50"},
    {"value": 0x1C, "label": "RUPEES_20"},
    {"value": 0x1D, "label": "RUPEES_100"},
    {"value": 0x1E, "label": "RUPEES_200"},
    {"value": 0x1F, "label": "RUPEES_500"},
    {"value": 0x20, "label": "SEASHELL"},
    {"value": 0x21, "label": "MESSAGE"},
    {"value": 0x22, "label": "GEL"},
    // {"value": 0x00, "label": "BOOMERANG"},
    // {"value": 0x00, "label": "HEART_PIECE"},
    // {"value": 0x00, "label": "BOWWOW"},
    // {"value": 0x00, "label": "ARROWS_10"},
    // {"value": 0x00, "label": "SINGLE_ARROW"},
    // {"value": 0x00, "label": "ROOSTER"},
    // {"value": 0x00, "label": "HAMMER"},

    // {"value": "MAX_POWDER_UPGRADE", "label": "MAX_POWDER_UPGRADE"},
    // {"value": "MAX_BOMBS_UPGRADE", "label": "MAX_BOMBS_UPGRADE"},
    // {"value": "MAX_ARROWS_UPGRADE", "label": "MAX_ARROWS_UPGRADE"},

    // {"value": "RED_TUNIC", "label": "RED_TUNIC"},
    // {"value": "BLUE_TUNIC", "label": "BLUE_TUNIC"},
    // {"value": "HEART_CONTAINER", "label": "HEART_CONTAINER"},
    // {"value": "BAD_HEART_CONTAINER", "label": "BAD_HEART_CONTAINER"},

    // {"value": "TOADSTOOL", "label": "TOADSTOOL"},

    {"value": 0x1A, "label": "KEY"},
    // {"value": "KEY1", "label": "KEY1"},
    // {"value": "KEY2", "label": "KEY2"},
    // {"value": "KEY3", "label": "KEY3"},
    // {"value": "KEY4", "label": "KEY4"},
    // {"value": "KEY5", "label": "KEY5"},
    // {"value": "KEY6", "label": "KEY6"},
    // {"value": "KEY7", "label": "KEY7"},
    // {"value": "KEY8", "label": "KEY8"},
    // {"value": "KEY0", "label": "KEY0"},

    {"value": 0x19, "label": "NIGHTMARE_KEY"},
    // {"value": "NIGHTMARE_KEY1", "label": "NIGHTMARE_KEY1"},
    // {"value": "NIGHTMARE_KEY2", "label": "NIGHTMARE_KEY2"},
    // {"value": "NIGHTMARE_KEY3", "label": "NIGHTMARE_KEY3"},
    // {"value": "NIGHTMARE_KEY4", "label": "NIGHTMARE_KEY4"},
    // {"value": "NIGHTMARE_KEY5", "label": "NIGHTMARE_KEY5"},
    // {"value": "NIGHTMARE_KEY6", "label": "NIGHTMARE_KEY6"},
    // {"value": "NIGHTMARE_KEY7", "label": "NIGHTMARE_KEY7"},
    // {"value": "NIGHTMARE_KEY8", "label": "NIGHTMARE_KEY8"},
    // {"value": "NIGHTMARE_KEY0", "label": "NIGHTMARE_KEY0"},

    {"value": 0x16, "label": "MAP"},
    // {"value": "MAP1", "label": "MAP1"},
    // {"value": "MAP2", "label": "MAP2"},
    // {"value": "MAP3", "label": "MAP3"},
    // {"value": "MAP4", "label": "MAP4"},
    // {"value": "MAP5", "label": "MAP5"},
    // {"value": "MAP6", "label": "MAP6"},
    // {"value": "MAP7", "label": "MAP7"},
    // {"value": "MAP8", "label": "MAP8"},
    // {"value": "MAP0", "label": "MAP0"},
    {"value": 0x17, "label": "COMPASS"},
    // {"value": "COMPASS1", "label": "COMPASS1"},
    // {"value": "COMPASS2", "label": "COMPASS2"},
    // {"value": "COMPASS3", "label": "COMPASS3"},
    // {"value": "COMPASS4", "label": "COMPASS4"},
    // {"value": "COMPASS5", "label": "COMPASS5"},
    // {"value": "COMPASS6", "label": "COMPASS6"},
    // {"value": "COMPASS7", "label": "COMPASS7"},
    // {"value": "COMPASS8", "label": "COMPASS8"},
    // {"value": "COMPASS0", "label": "COMPASS0"},
    {"value": 0x18, "label": "STONE_BEAK"},
    // {"value": "STONE_BEAK1", "label": "STONE_BEAK1"},
    // {"value": "STONE_BEAK2", "label": "STONE_BEAK2"},
    // {"value": "STONE_BEAK3", "label": "STONE_BEAK3"},
    // {"value": "STONE_BEAK4", "label": "STONE_BEAK4"},
    // {"value": "STONE_BEAK5", "label": "STONE_BEAK5"},
    // {"value": "STONE_BEAK6", "label": "STONE_BEAK6"},
    // {"value": "STONE_BEAK7", "label": "STONE_BEAK7"},
    // {"value": "STONE_BEAK8", "label": "STONE_BEAK8"},
    // {"value": "STONE_BEAK0", "label": "STONE_BEAK0"},

    // {"value": "SONG1", "label": "SONG1"},
    // {"value": "SONG2", "label": "SONG2"},
    // {"value": "SONG3", "label": "SONG3"},

    // {"value": "INSTRUMENT1", "label": "INSTRUMENT1"},
    // {"value": "INSTRUMENT2", "label": "INSTRUMENT2"},
    // {"value": "INSTRUMENT3", "label": "INSTRUMENT3"},
    // {"value": "INSTRUMENT4", "label": "INSTRUMENT4"},
    // {"value": "INSTRUMENT5", "label": "INSTRUMENT5"},
    // {"value": "INSTRUMENT6", "label": "INSTRUMENT6"},
    // {"value": "INSTRUMENT7", "label": "INSTRUMENT7"},
    // {"value": "INSTRUMENT8", "label": "INSTRUMENT8"},

    // {"value": "TRADING_ITEM_YOSHI_DOLL", "label": "TRADING_ITEM_YOSHI_DOLL"},
    // {"value": "TRADING_ITEM_RIBBON", "label": "TRADING_ITEM_RIBBON"},
    // {"value": "TRADING_ITEM_DOG_FOOD", "label": "TRADING_ITEM_DOG_FOOD"},
    // {"value": "TRADING_ITEM_BANANAS", "label": "TRADING_ITEM_BANANAS"},
    // {"value": "TRADING_ITEM_STICK", "label": "TRADING_ITEM_STICK"},
    // {"value": "TRADING_ITEM_HONEYCOMB", "label": "TRADING_ITEM_HONEYCOMB"},
    // {"value": "TRADING_ITEM_PINEAPPLE", "label": "TRADING_ITEM_PINEAPPLE"},
    // {"value": "TRADING_ITEM_HIBISCUS", "label": "TRADING_ITEM_HIBISCUS"},
    // {"value": "TRADING_ITEM_LETTER", "label": "TRADING_ITEM_LETTER"},
    // {"value": "TRADING_ITEM_BROOM", "label": "TRADING_ITEM_BROOM"},
    // {"value": "TRADING_ITEM_FISHING_HOOK", "label": "TRADING_ITEM_FISHING_HOOK"},
    // {"value": "TRADING_ITEM_NECKLACE", "label": "TRADING_ITEM_NECKLACE"},
    // {"value": "TRADING_ITEM_SCALE", "label": "TRADING_ITEM_SCALE"},
    // {"value": "TRADING_ITEM_MAGNIFYING_GLASS", "label": "TRADING_ITEM_MAGNIFYING_GLASS"},

    // {"value": "TAIL_CAVE_OPENED", "label": "TAIL_CAVE_OPENED"},
    // {"value": "KEY_CAVERN_OPENED", "label": "KEY_CAVERN_OPENED"},
    // {"value": "ANGLER_TUNNEL_OPENED", "label": "ANGLER_TUNNEL_OPENED"},
    // {"value": "FACE_SHRINE_OPENED", "label": "FACE_SHRINE_OPENED"},
    // {"value": "CASTLE_GATE_OPENED", "label": "CASTLE_GATE_OPENED"},
    // {"value": "EAGLE_TOWER_OPENED", "label": "EAGLE_TOWER_OPENED"},
]
var event_table = [
    {"value": 0x00, "label": "00: None"},
    {"value": 0x0D, "label": "0D: THROW POT AT CHEST"},
    {"value": 0x21, "label": "21: KILL ENEMIES: OPEN DOOR"},
    {"value": 0x22, "label": "22: PUSH BLOCK: OPEN DOOR"},
    {"value": 0x23, "label": "23: BUTTON: OPEN DOOR"},
    {"value": 0x25, "label": "25: LIGHT TORCHES: OPEN DOOR"},
    {"value": 0x29, "label": "29: PUZZLE TILES: OPEN DOOR"},
    {"value": 0x2A, "label": "2A: SIDESCROLL BOSS DEAD: OPEN DOOR"},
    {"value": 0x2B, "label": "2B: THROW AT DOOR: OPEN DOOR"},
    {"value": 0x2C, "label": "2C: HORSE HEADS: OPEN DOOR"},
    {"value": 0x45, "label": "45: LIGHT TORCHES: KILL ENEMIES"},
    {"value": 0x48, "label": "48: KILL 'SPECIAL': KILL ENEMIES"},
    {"value": 0x61, "label": "61: KILL ENEMIES: REVEAL CHEST"},
    {"value": 0x63, "label": "63: BUTTON: REVEAL CHEST"},
    {"value": 0x65, "label": "65: LIGHT TORCHES: REVEAL CHEST"},
    {"value": 0x66, "label": "66: KILL IN ORDER: REVEAL CHEST"},
    {"value": 0x67, "label": "67: PUSH 2 BLOCKS: REVEAL CHEST"},
    {"value": 0x6C, "label": "6C: HORSE HEADS: REVEAL CHEST"},
    {"value": 0x6E, "label": "6E: FILL LAVA: REVEAL CHEST"},
    {"value": 0x81, "label": "81: KILL ENEMIES: DROP KEY"},
    {"value": 0x82, "label": "82: PUSH BLOCK: DROP KEY"},
    {"value": 0x87, "label": "87: PUSH 2 BLOCKS: DROP KEY"},
    {"value": 0x8E, "label": "8E: FILL LAVA: DROP KEY"},
    {"value": 0x8F, "label": "8F: SHOOT EYE STATUE: DROP KEY"},
    {"value": 0xA1, "label": "A1: KILL ENEMIES: REVEAL STAIRS"},
    {"value": 0xA7, "label": "A7: PUSH 2 BLOCKS: REVEAL STAIRS"},
    {"value": 0xA9, "label": "A9: PUZZLE TILES: REVEAL STAIRS"},
    {"value": 0xC1, "label": "C1: MINIBOSS"},
]