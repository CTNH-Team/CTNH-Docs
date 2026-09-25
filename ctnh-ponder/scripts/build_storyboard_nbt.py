#!/usr/bin/env python3
"""Build (or check) a Ponder storyboard .nbt from a JSON blueprint.

Zero dependencies: Python 3 standard library only (json / struct / gzip).
The LLM writes a readable JSON blueprint; this script emits the gzip-compressed
binary NBT that Ponder loads from assets/<modid>/ponder/<path>.nbt.

Usage
-----
    python build_storyboard_nbt.py blueprint.json              # uses "output" from the blueprint
    python build_storyboard_nbt.py blueprint.json -o out.nbt   # explicit target
    python build_storyboard_nbt.py blueprint.json --print      # compile + dump a summary, write nothing
    python build_storyboard_nbt.py --check out.nbt             # validate an existing .nbt

Blueprint schema (see ../assets/storyboard-blueprint.template.json)
------------------------------------------------------------------
{
  "output": "modules/<Module>/src/main/resources/assets/<modid>/ponder/<path>.nbt",
  "age": "mechanical" | "electric",     # picks the default floor material
  "floor": "create:andesite_casing",    # optional explicit override
  "floor_padding": 1,                   # optional, default 1 (one ring on every side)
  "data_version": 3465,                 # optional
  "structure": [
    {"pos": [1, 1, 1], "block": "gtceu:coke_oven_bricks"},
    {"pos": [2, 1, 2], "block": "gtceu:coke_oven", "controller": true}
  ],
  "entities": [ ... ]                   # optional raw passthrough
}

Rules enforced
--------------
* Floor sits at y=0 and covers the structure footprint grown by "floor_padding"
  on EVERY side (+2 per horizontal axis).  3x3 structure -> 5x5 floor.
* Structure blocks must start at y>=1 (y=0 is reserved for the floor).
* Shipped size is [floorX, maxY+1, floorZ].
* A block marked "controller": true gets facing=north + upwards_facing=north
  unless the blueprint states those properties explicitly. Set
  "controller_props": false (per block, or at blueprint level) for machines whose
  rotation state is NONE -- drums, tanks, single-state blocks -- which carry no
  facing property at all.
* Output is deterministic: palette and blocks are sorted, gzip mtime is 0.
"""

from __future__ import annotations

import argparse
import gzip
import io
import json
import struct
import sys
from pathlib import Path

# --------------------------------------------------------------------------
# NBT tag ids
# --------------------------------------------------------------------------
TAG_END = 0
TAG_BYTE = 1
TAG_SHORT = 2
TAG_INT = 3
TAG_LONG = 4
TAG_FLOAT = 5
TAG_DOUBLE = 6
TAG_BYTE_ARRAY = 7
TAG_STRING = 8
TAG_LIST = 9
TAG_COMPOUND = 10
TAG_INT_ARRAY = 11
TAG_LONG_ARRAY = 12

TAG_NAMES = {
    TAG_END: "end", TAG_BYTE: "byte", TAG_SHORT: "short", TAG_INT: "int",
    TAG_LONG: "long", TAG_FLOAT: "float", TAG_DOUBLE: "double",
    TAG_BYTE_ARRAY: "byte[]", TAG_STRING: "string", TAG_LIST: "list",
    TAG_COMPOUND: "compound", TAG_INT_ARRAY: "int[]", TAG_LONG_ARRAY: "long[]",
}

DEFAULT_DATA_VERSION = 3465
FLOOR_BY_AGE = {
    "mechanical": "create:andesite_casing",   # 机械时代 -> 安山机壳
    "electric": "create:railway_casing",      # 电力时代 -> 列车机壳
}
CONTROLLER_DEFAULT_PROPS = {"facing": "north", "upwards_facing": "north"}


class BlueprintError(Exception):
    """Raised for anything the blueprint author must fix."""


# --------------------------------------------------------------------------
# minimal NBT writer
# --------------------------------------------------------------------------
class Tag:
    __slots__ = ("kind", "value")

    def __init__(self, kind: int, value):
        self.kind = kind
        self.value = value


def _write_string(out: io.BytesIO, text: str) -> None:
    raw = text.encode("utf-8")
    out.write(struct.pack(">H", len(raw)))
    out.write(raw)


def _write_payload(out: io.BytesIO, tag: Tag) -> None:
    kind, value = tag.kind, tag.value
    if kind == TAG_BYTE:
        out.write(struct.pack(">b", value))
    elif kind == TAG_SHORT:
        out.write(struct.pack(">h", value))
    elif kind == TAG_INT:
        out.write(struct.pack(">i", value))
    elif kind == TAG_LONG:
        out.write(struct.pack(">q", value))
    elif kind == TAG_FLOAT:
        out.write(struct.pack(">f", value))
    elif kind == TAG_DOUBLE:
        out.write(struct.pack(">d", value))
    elif kind == TAG_STRING:
        _write_string(out, value)
    elif kind == TAG_BYTE_ARRAY:
        out.write(struct.pack(">i", len(value)))
        out.write(bytes((int(v) & 0xFF) for v in value))
    elif kind == TAG_INT_ARRAY:
        out.write(struct.pack(">i", len(value)))
        for v in value:
            out.write(struct.pack(">i", int(v)))
    elif kind == TAG_LONG_ARRAY:
        out.write(struct.pack(">i", len(value)))
        for v in value:
            out.write(struct.pack(">q", int(v)))
    elif kind == TAG_LIST:
        elem = value[0].kind if value else TAG_END
        out.write(struct.pack(">b", elem))
        out.write(struct.pack(">i", len(value)))
        for item in value:
            _write_payload(out, item)
    elif kind == TAG_COMPOUND:
        for name, child in value:
            out.write(struct.pack(">b", child.kind))
            _write_string(out, name)
            _write_payload(out, child)
        out.write(b"\x00")
    else:
        raise BlueprintError("cannot serialise tag " + TAG_NAMES.get(kind, str(kind)))


def write_nbt(root: Tag, name: str = "") -> bytes:
    """Serialise a TAG_Compound as a root-level NBT document (uncompressed)."""
    out = io.BytesIO()
    out.write(struct.pack(">b", TAG_COMPOUND))
    _write_string(out, name)
    _write_payload(out, root)
    return out.getvalue()


def gzip_deterministic(raw: bytes) -> bytes:
    """gzip with mtime=0 so byte output is reproducible."""
    buffer = io.BytesIO()
    with gzip.GzipFile(fileobj=buffer, mode="wb", compresslevel=9, mtime=0) as gz:
        gz.write(raw)
    return buffer.getvalue()


# --------------------------------------------------------------------------
# JSON -> NBT conversion
# --------------------------------------------------------------------------
def json_to_tag(value):
    """Convert plain JSON to a Tag.

    Type mapping
      true/false            -> byte
      int                   -> int
      float                 -> double
      "text"                -> string
      [ ... ]               -> list (element type taken from the first entry)
      { ... }               -> compound

    Typed override, when the default is wrong for Minecraft:
      {"__b": 1} {"__s": 1} {"__i": 1} {"__l": 1} {"__f": 1.5} {"__d": 1.5}
      {"__ba": [1,2]} {"__ia": [1,2]} {"__la": [1,2]}
    """
    if isinstance(value, Tag):
        return value
    if isinstance(value, bool):
        return Tag(TAG_BYTE, 1 if value else 0)
    if isinstance(value, int):
        return Tag(TAG_INT, value)
    if isinstance(value, float):
        return Tag(TAG_DOUBLE, value)
    if isinstance(value, str):
        return Tag(TAG_STRING, value)
    if isinstance(value, list):
        return Tag(TAG_LIST, [json_to_tag(v) for v in value])
    if isinstance(value, dict):
        for marker, kind in (
            ("__b", TAG_BYTE), ("__s", TAG_SHORT), ("__i", TAG_INT), ("__l", TAG_LONG),
            ("__f", TAG_FLOAT), ("__d", TAG_DOUBLE), ("__ba", TAG_BYTE_ARRAY),
            ("__ia", TAG_INT_ARRAY), ("__la", TAG_LONG_ARRAY),
        ):
            if marker in value:
                if len(value) != 1:
                    raise BlueprintError(marker + " must be the only key of its object")
                return Tag(kind, value[marker])
        return Tag(TAG_COMPOUND, [(k, json_to_tag(v)) for k, v in value.items()])
    raise BlueprintError("unsupported JSON value: " + repr(value))


# --------------------------------------------------------------------------
# minimal NBT reader (for --check)
# --------------------------------------------------------------------------
def read_nbt(raw: bytes):
    if raw[:2] == b"\x1f\x8b":
        raw = gzip.decompress(raw)
    offset = 0

    def u1():
        nonlocal offset
        v = raw[offset]
        offset += 1
        return v

    def payload(kind):
        nonlocal offset
        if kind == TAG_BYTE:
            v = struct.unpack_from(">b", raw, offset)[0]; offset += 1; return v
        if kind == TAG_SHORT:
            v = struct.unpack_from(">h", raw, offset)[0]; offset += 2; return v
        if kind == TAG_INT:
            v = struct.unpack_from(">i", raw, offset)[0]; offset += 4; return v
        if kind == TAG_LONG:
            v = struct.unpack_from(">q", raw, offset)[0]; offset += 8; return v
        if kind == TAG_FLOAT:
            v = struct.unpack_from(">f", raw, offset)[0]; offset += 4; return v
        if kind == TAG_DOUBLE:
            v = struct.unpack_from(">d", raw, offset)[0]; offset += 8; return v
        if kind in (TAG_BYTE_ARRAY, TAG_INT_ARRAY, TAG_LONG_ARRAY):
            n = struct.unpack_from(">i", raw, offset)[0]; offset += 4
            fmt = {TAG_BYTE_ARRAY: ">b", TAG_INT_ARRAY: ">i", TAG_LONG_ARRAY: ">q"}[kind]
            size = {TAG_BYTE_ARRAY: 1, TAG_INT_ARRAY: 4, TAG_LONG_ARRAY: 8}[kind]
            vals = list(struct.unpack_from(">" + fmt[1] * n, raw, offset)) if n else []
            offset += n * size
            return vals
        if kind == TAG_STRING:
            n = struct.unpack_from(">H", raw, offset)[0]; offset += 2
            text = raw[offset:offset + n].decode("utf-8"); offset += n
            return text
        if kind == TAG_LIST:
            elem = u1()
            n = struct.unpack_from(">i", raw, offset)[0]; offset += 4
            return [payload(elem) for _ in range(n)]
        if kind == TAG_COMPOUND:
            result = {}
            while True:
                child = u1()
                if child == TAG_END:
                    return result
                n = struct.unpack_from(">H", raw, offset)[0]; offset += 2
                key = raw[offset:offset + n].decode("utf-8"); offset += n
                result[key] = payload(child)
        raise BlueprintError("unknown tag id " + str(kind))

    if u1() != TAG_COMPOUND:
        raise BlueprintError("root tag is not a compound")
    n = struct.unpack_from(">H", raw, offset)[0]; offset += 2
    offset += n
    return payload(TAG_COMPOUND)


def inspect(path: Path) -> None:
    """Print a human-readable summary of an existing storyboard (used by --check)."""
    data = read_nbt(path.read_bytes())
    palette = data.get("palette", [])
    blocks = data.get("blocks", [])
    size = data.get("size", [])
    name_of = lambda i: palette[i].get("Name", "?") if 0 <= i < len(palette) else "?"
    props_of = lambda i: palette[i].get("Properties", {}) if 0 <= i < len(palette) else {}
    floor = [b for b in blocks if b["pos"][1] == 0]
    body = [b for b in blocks if b["pos"][1] > 0]

    print("file        : " + str(path))
    print("DataVersion : " + str(data.get("DataVersion")))
    print("size        : " + str(size))
    print("blocks      : " + str(len(blocks)) + " (floor " + str(len(floor)) + ", body " + str(len(body)) + ")")
    materials = {}
    for b in floor:
        materials[name_of(b["state"])] = materials.get(name_of(b["state"]), 0) + 1
    print("floor       : " + json.dumps(materials, ensure_ascii=False))
    if body:
        xs = [b["pos"][0] for b in body]
        ys = [b["pos"][1] for b in body]
        zs = [b["pos"][2] for b in body]
        print("body bounds : x %d..%d  y %d..%d  z %d..%d"
              % (min(xs), max(xs), min(ys), max(ys), min(zs), max(zs)))
    problems = validate(size, palette, blocks)
    for line in problems:
        print("warning     : " + line)
    if not problems:
        print("validation  : ok")


# --------------------------------------------------------------------------
# validation
# --------------------------------------------------------------------------
def validate(size, palette, blocks):
    problems = []
    if len(size) != 3 or min(size) <= 0:
        problems.append("size is not a positive 3-vector: " + str(size))
        return problems
    sx, sy, sz = size
    occupied = set()
    for b in blocks:
        x, y, z = b["pos"]
        if not (0 <= x < sx and 0 <= y < sy and 0 <= z < sz):
            problems.append("block out of bounds at " + str(b["pos"]) + " (size " + str(size) + ")")
        if (x, y, z) in occupied:
            problems.append("duplicate block at " + str(b["pos"]))
        occupied.add((x, y, z))

    floor = {(b["pos"][0], b["pos"][2]) for b in blocks if b["pos"][1] == 0}
    missing = [(x, z) for x in range(sx) for z in range(sz) if (x, z) not in floor]
    if missing:
        problems.append("floor has %d hole(s), e.g. %s" % (len(missing), missing[:4]))

    floor_materials = {palette[b["state"]].get("Name") for b in blocks if b["pos"][1] == 0}
    body_materials = {palette[b["state"]].get("Name") for b in blocks if b["pos"][1] > 0}
    for name in sorted(floor_materials & body_materials):
        problems.append("material used for both floor and structure: " + name)

    used = {b["state"] for b in blocks}
    for i, entry in enumerate(palette):
        if i not in used:
            problems.append("palette entry %d unused: %s" % (i, entry.get("Name")))
    return problems


# --------------------------------------------------------------------------
# blueprint compiler
# --------------------------------------------------------------------------
def _pos(entry, field="pos"):
    value = entry.get(field)
    if not isinstance(value, list) or len(value) != 3 or not all(isinstance(v, int) for v in value):
        raise BlueprintError("'%s' must be a [x, y, z] int list, got %r" % (field, value))
    return tuple(value)


def compile_blueprint(blueprint: dict):
    structure = blueprint.get("structure")
    if not isinstance(structure, list) or not structure:
        raise BlueprintError("'structure' must be a non-empty list of blocks")

    age = blueprint.get("age", "mechanical")
    floor_block = blueprint.get("floor")
    if floor_block is None:
        if age not in FLOOR_BY_AGE:
            raise BlueprintError("'age' must be one of %s or set 'floor' explicitly" % sorted(FLOOR_BY_AGE))
        floor_block = FLOOR_BY_AGE[age]
    padding = blueprint.get("floor_padding", 1)
    if not isinstance(padding, int) or padding < 0:
        raise BlueprintError("'floor_padding' must be a non-negative int")

    cells = []
    controllers = []
    for i, entry in enumerate(structure):
        if not isinstance(entry, dict):
            raise BlueprintError("structure[%d] is not an object" % i)
        block = entry.get("block")
        if not isinstance(block, str) or ":" not in block:
            raise BlueprintError("structure[%d].block must be a namespaced id" % i)
        pos = _pos(entry)
        if pos[1] < 1:
            raise BlueprintError("structure[%d] at y=%d: y=0 is reserved for the floor" % (i, pos[1]))
        props = dict(entry.get("props", {}))
        if entry.get("controller"):
            controllers.append((i, pos, block, props))
            # RotationState.NONE machines (drums, tanks) have no facing property;
            # "controller_props": false keeps their state clean.
            if entry.get("controller_props", blueprint.get("controller_props", True)):
                for key, value in CONTROLLER_DEFAULT_PROPS.items():
                    props.setdefault(key, value)
        cells.append({"pos": pos, "block": block, "props": props, "nbt": entry.get("nbt")})

    if not controllers:
        raise BlueprintError("no block marked 'controller': true; mark the multiblock controller "
                             "(for a single-block machine mark that block)")

    seen = set()
    for cell in cells:
        if cell["pos"] in seen:
            raise BlueprintError("duplicate structure position " + str(cell["pos"]))
        seen.add(cell["pos"])

    xs = [c["pos"][0] for c in cells]
    ys = [c["pos"][1] for c in cells]
    zs = [c["pos"][2] for c in cells]
    min_x, max_x = min(xs), max(xs)
    min_z, max_z = min(zs), max(zs)

    # shift so that the floor ring starts at index 0
    shift_x = padding - min_x
    shift_z = padding - min_z
    floor_w = (max_x - min_x + 1) + 2 * padding
    floor_d = (max_z - min_z + 1) + 2 * padding
    size = [floor_w, max(ys) + 1, floor_d]

    blocks = []
    for x in range(floor_w):
        for z in range(floor_d):
            blocks.append((x, 0, z, floor_block, {}, None))
    for cell in cells:
        x = cell["pos"][0] + shift_x
        y = cell["pos"][1]
        z = cell["pos"][2] + shift_z
        blocks.append((x, y, z, cell["block"], cell["props"], cell["nbt"]))

    # deterministic palette: sort by (name, props)
    def state_key(entry):
        return (entry[3], json.dumps(entry[4], sort_keys=True))

    palette_keys = sorted({state_key(b) for b in blocks}, key=lambda k: (k[0], k[1]))
    palette_index = {key: i for i, key in enumerate(palette_keys)}

    palette_tag = []
    for block, props_json in palette_keys:
        entry = {"Name": block}
        props = json.loads(props_json)
        if props:
            entry["Properties"] = {k: str(v) for k, v in sorted(props.items())}
        palette_tag.append(json_to_tag(entry))

    blocks_tag = []
    for x, y, z, block, props, nbt in sorted(blocks, key=lambda b: (b[1], b[2], b[0])):
        entry = {
            "pos": [x, y, z],
            "state": palette_index[(block, json.dumps(props, sort_keys=True))],
        }
        if nbt is not None:
            entry["nbt"] = nbt
        blocks_tag.append(json_to_tag(entry))

    root = {
        "size": size,
        "entities": blueprint.get("entities", []),
        "blocks": blocks_tag,
        "palette": palette_tag,
        "DataVersion": blueprint.get("data_version", DEFAULT_DATA_VERSION),
    }
    root_tag = json_to_tag(root)

    # shift controller info back into a readable report
    report = []
    for index, pos, block, props in controllers:
        report.append({
            "pos": [pos[0] + shift_x, pos[1], pos[2] + shift_z],
            "block": block,
            "props": props,
        })

    # normalised views so validate()/dump_summary() work on both compile and --check
    palette_view = []
    for block, props_json in palette_keys:
        palette_view.append({"Name": block, "Properties": json.loads(props_json)})
    blocks_view = []
    for x, y, z, block, props, nbt in blocks:
        entry = {
            "pos": [x, y, z],
            "state": palette_index[(block, json.dumps(props, sort_keys=True))],
            "block": block,
        }
        if nbt is not None:
            entry["nbt"] = nbt
        blocks_view.append(entry)
    return root_tag, size, report, palette_view, blocks_view


def dump_summary(size, controllers, blocks):
    print("size        : " + str(size) + "  (floor " + str(size[0]) + "x" + str(size[2]) + ")")
    materials = {}
    for b in blocks:
        if b["pos"][1] == 0:
            name = b.get("block", "?")
            materials[name] = materials.get(name, 0) + 1
    print("floor       : " + json.dumps(materials, ensure_ascii=False))
    print("blocks      : " + str(len(blocks)))
    for c in controllers:
        print("controller  : " + json.dumps(c, ensure_ascii=False))
    body = [b["pos"] for b in blocks if b["pos"][1] > 0]
    if body:
        print("structure   : x %d..%d  y %d..%d  z %d..%d"
              % (min(p[0] for p in body), max(p[0] for p in body),
                 min(p[1] for p in body), max(p[1] for p in body),
                 min(p[2] for p in body), max(p[2] for p in body)))


# --------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------
def main(argv=None):
    parser = argparse.ArgumentParser(description="Build or check a Ponder storyboard .nbt")
    parser.add_argument("blueprint", nargs="?", help="JSON blueprint to compile")
    parser.add_argument("-o", "--output", help="override the blueprint's 'output' path")
    parser.add_argument("--print", dest="dry_run", action="store_true", help="compile and report, write nothing")
    parser.add_argument("--check", metavar="NBT", help="inspect and validate an existing .nbt")
    args = parser.parse_args(argv)

    if args.check:
        inspect(Path(args.check))
        return 0

    if not args.blueprint:
        parser.error("a blueprint path is required unless --check is used")

    path = Path(args.blueprint)
    blueprint = json.loads(path.read_text(encoding="utf-8"))
    root_tag, size, controllers, palette, blocks = compile_blueprint(blueprint)
    dump_summary(size, controllers, blocks)

    for line in validate(size, palette, blocks):
        print("warning     : " + line)

    if args.dry_run:
        print("dry run     : nothing written")
        return 0

    target = Path(args.output or blueprint.get("output") or "")
    if not str(target) or str(target) == ".":
        raise BlueprintError("no output path: set 'output' in the blueprint or pass -o")
    target.parent.mkdir(parents=True, exist_ok=True)
    payload = gzip_deterministic(write_nbt(root_tag))
    target.write_bytes(payload)
    print("written     : %s (%d bytes, DataVersion %s)"
          % (target, len(payload), blueprint.get("data_version", DEFAULT_DATA_VERSION)))
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except BlueprintError as error:
        print("error: " + str(error), file=sys.stderr)
        sys.exit(2)
