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
