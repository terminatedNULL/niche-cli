import re
import os
import argparse

"""
This tool is used to generate a text expansion snippet file for Obsidian's
LaTeX plugin, with support for custom trigger syntaxes, stroke width, and colors. 
Snippets use discord's emoji syntax by default (:icon-name:) along with stroke-width 
scaling proportionately.

This tool requires a local download of the Lucide icons folder in the script directory:
https://github.com/lucide-icons/lucide/tree/main/icons
"""

STROKE_WIDTH = 10
VIEWBOX_SIZE = 24

if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser(description="Generate Obsidian LaTeX snippet for Lucide icons.")
    arg_parser.add_argument("-s", "--size", type=int, action="store", help="Generate icons snippet")
    arg_parser.add_argument("-pre", type=str, action="store", default=":", help="Prefix for icon names")
    arg_parser.add_argument("-post", type=str, action="store", default=":", help="Suffix for icon names")
    arg_parser.add_argument("-sw", "--stroke-width", type=int, action="store", dest="stroke_width", help="The stroke width of the icons")
    arg_parser.add_argument("-c", "--color", type=str, action="store", default="currentColor", help="The color of the icons")
    args = arg_parser.parse_args()

    icon_map = {}
    size = 10
    if args.size and isinstance(args.size, int) and args.size > 0:
        size = args.size

    if args.stroke_width:
        stroke_width = args.stroke_width
    else:
        stroke_width = STROKE_WIDTH * (size / VIEWBOX_SIZE)

    print(f"Generating icon snippets with:\n + size: {size}\n + syntax: {args.pre}icon-name{args.post}\n + stroke width: {stroke_width}\n + color: {args.color}")
    count = 0
    for node, dirs, files in os.walk("icons"):
        for file in files:
            if file.endswith(".svg"):
                name = f"{args.pre}{file[:-4]}{args.post}"
                
                with open(os.path.join(node, file), "r") as f:    
                    content = f.read().replace("\"", "'")
                    content = re.sub(r"width='\d+'", f"width='{size}'", content)
                    content = re.sub(r"height='\d+'", f"height='{size}'", content)
                    content = re.sub(r"stroke-width='\d*'", f"stroke-width='{stroke_width}'", content)
                    content = re.sub(r"stroke='.*'", f"stroke='{args.color}'", content)
                    icon_map[name] = content
                count += 1

    with open("lucide_icons.txt", "w") as f:
        f.write("[\n")
        for name, content in icon_map.items():
            f.write(f"\t{{ trigger: \"{name}\", replacement: \"{content.replace("\n", " ")}\", options: \"tA\" }},\n")
        f.write("\n]")

    print(f"Generated {len(icon_map)} icon snippets.")
