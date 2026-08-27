import argparse
import os
import sys
import json
import http.server
import map.disasm
import map.editorserver
import map.export


def main(args):
    parser = argparse.ArgumentParser()
    parser.add_argument("map_json_file")
    parser.add_argument("disasm_path")
    parser.add_argument("--from-disasm", action="store_true")
    parser.add_argument("--to-disasm", action="store_true")
    parser.add_argument("--edit", action="store_true", help="Run the editor. Default if from/to-disasm is not specified")
    args = parser.parse_args(args)

    if args.from_disasm:
        if os.path.exists(args.map_json_file):
            print("Not overriding existing json file. Exporting is not perfect and should only be done once.")
            exit(1)
        data = map.disasm.room_data_to_json(args.disasm_path)
        json.dump(data, open(args.map_json_file, "wt"), indent="  ")
    if args.edit or (not args.from_disasm and not args.to_disasm):
        server = map.editorserver.EditorServer(args.disasm_path)
        server.load_map_json(args.map_json_file)
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            pass
    if args.to_disasm:
        map.export.do_export(args.disasm_path, json.load(open(args.map_json_file, "rt")))

if __name__ == "__main__":
    main(sys.argv[1:])
