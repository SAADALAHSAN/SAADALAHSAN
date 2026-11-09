import base64
import os
from collections import deque
from PIL import Image

def flood_fill_white(img_path):
    """
    Flood-fill from all edge pixels to replace ONLY the outer background
    with white. Internal dark pixels (same color as bg but enclosed inside
    the character) are preserved perfectly.
    """
    im = Image.open(img_path).convert("RGB")
    w, h = im.size
    pixels = im.load()
    
    # Background color: RGB(22, 27, 34) with tolerance of 8
    bg_r, bg_g, bg_b = 22, 27, 34
    tol = 8
    
    def is_bg(r, g, b):
        return abs(r - bg_r) <= tol and abs(g - bg_g) <= tol and abs(b - bg_b) <= tol
    
    # BFS flood-fill from ALL edge pixels that match background
    visited = set()
    queue = deque()
    
    # Seed from all 4 edges
    for x in range(w):
        for y_edge in [0, h - 1]:
            r, g, b = pixels[x, y_edge]
            if is_bg(r, g, b) and (x, y_edge) not in visited:
                queue.append((x, y_edge))
                visited.add((x, y_edge))
    for y in range(h):
        for x_edge in [0, w - 1]:
            r, g, b = pixels[x_edge, y]
            if is_bg(r, g, b) and (x_edge, y) not in visited:
                queue.append((x_edge, y))
                visited.add((x_edge, y))
    
    # BFS
    while queue:
        cx, cy = queue.popleft()
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = cx + dx, cy + dy
            if 0 <= nx < w and 0 <= ny < h and (nx, ny) not in visited:
                r, g, b = pixels[nx, ny]
                if is_bg(r, g, b):
                    visited.add((nx, ny))
                    queue.append((nx, ny))
    
    # Replace only the outer (visited) pixels with white
    for (x, y) in visited:
        pixels[x, y] = (255, 255, 255)
    
    print(f"Flood-fill complete: {len(visited)} outer bg pixels -> white")
    return im


def build_svg_cards():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    gif_path = os.path.join(script_dir, "coding_sticker.gif")
    
    # 1. Dark Mode: original GIF with dark background (unchanged)
    with open(gif_path, "rb") as f:
        dark_gif_bytes = f.read()
    dark_b64 = base64.b64encode(dark_gif_bytes).decode("utf-8")
    dark_data_uri = f"data:image/gif;base64,{dark_b64}"
    
    # 2. Light Mode: Flood-fill outer bg -> white, keep character intact
    light_img = flood_fill_white(gif_path)
    
    # Save as PNG for embedding
    light_path = os.path.join(script_dir, "coding_sticker_light.png")
    light_img.save(light_path, "PNG")
    
    with open(light_path, "rb") as f:
        light_b64 = base64.b64encode(f.read()).decode("utf-8")
    light_data_uri = f"data:image/png;base64,{light_b64}"
    
    print(f"Light mode image saved: {light_path}")
    
    # --- DARK MODE SVG ---
    dark_svg = f"""<?xml version='1.0' encoding='UTF-8'?>
<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" font-family="ConsolasFallback,Consolas,monospace" width="985px" height="530px" font-size="14.5px">
<style>
@font-face {{
src: local('Consolas'), local('Consolas Bold');
font-family: 'ConsolasFallback';
font-display: swap;
-webkit-size-adjust: 109%;
size-adjust: 109%;
}}
.key {{fill: #ffa657;}}
.value {{fill: #a5d6ff;}}
.addColor {{fill: #3fb950;}}
.delColor {{fill: #f85149;}}
.cc {{fill: #616e7f;}}
text, tspan {{white-space: pre;}}
</style>
<rect width="985px" height="530px" fill="#161b22" rx="15"/>

<!-- Animated ASCII Coding GIF Sticker on Left Side -->
<image href="{dark_data_uri}" xlink:href="{dark_data_uri}" x="15" y="60" width="390" height="390" preserveAspectRatio="xMidYMid meet" />

<!-- Terminal Profile Details on Right Side -->
<text x="415" y="35" fill="#c9d1d9">
<tspan x="415" y="35">saadalahsan</tspan> <tspan class="cc">-————————————————————————————————-—-</tspan>
<tspan x="415" y="58" class="cc">. </tspan><tspan class="key">OS</tspan>:<tspan class="cc"> ...................... </tspan><tspan class="value">Windows 10, Linux</tspan>
<tspan x="415" y="81" class="cc">. </tspan><tspan class="key">Uptime</tspan>:<tspan class="cc"> .................. </tspan><tspan class="value">Learner since day 1</tspan>
<tspan x="415" y="104" class="cc">. </tspan><tspan class="key">Role</tspan>:<tspan class="cc"> .................... </tspan><tspan class="value">Full-Stack Product Builder</tspan>
<tspan x="415" y="127" class="cc">. </tspan><tspan class="key">Focus</tspan>:<tspan class="cc"> ........... </tspan><tspan class="value">Trading, Web3, AI Automation</tspan>
<tspan x="415" y="150" class="cc">. </tspan><tspan class="key">IDE</tspan>:<tspan class="cc"> ...................... </tspan><tspan class="value">VSCode, Cursor</tspan>
<tspan x="415" y="173" class="cc">. </tspan>
<tspan x="415" y="196" class="cc">. </tspan><tspan class="key">Languages</tspan>.<tspan class="key">Programming</tspan>:<tspan class="cc"> .. </tspan><tspan class="value">JS, TS, Python, Rust, C++</tspan>
<tspan x="415" y="219" class="cc">. </tspan><tspan class="key">Languages</tspan>.<tspan class="key">Markup</tspan>:<tspan class="cc"> ......... </tspan><tspan class="value">HTML, CSS, JSON, YAML</tspan>
<tspan x="415" y="242" class="cc">. </tspan><tspan class="key">Languages</tspan>.<tspan class="key">Real</tspan>:<tspan class="cc"> ..................... </tspan><tspan class="value">Bangla, English</tspan>
<tspan x="415" y="265" class="cc">. </tspan>
<tspan x="415" y="288" class="cc">. </tspan><tspan class="key">Frameworks</tspan>:<tspan class="cc"> ............. </tspan><tspan class="value">React, Next.js, Node.js, Vite</tspan>
<tspan x="415" y="311" class="cc">. </tspan><tspan class="key">Databases</tspan>:<tspan class="cc"> .............. </tspan><tspan class="value">MongoDB, MySQL, Firebase</tspan>
<tspan x="415" y="334" class="cc">. </tspan><tspan class="key">Cloud</tspan>:<tspan class="cc"> ................... </tspan><tspan class="value">AWS, GCP, Azure, Vercel</tspan>
<tspan x="415" y="357" class="cc">. </tspan><tspan class="key">Web3</tspan>:<tspan class="cc"> .... </tspan><tspan class="value">Ethereum, Solana, Polygon, Hardhat</tspan>
<tspan x="415" y="390">- Contact</tspan> <tspan class="cc">-————————————————————————————————-—-</tspan>
<tspan x="415" y="413" class="cc">. </tspan><tspan class="key">Email</tspan>:<tspan class="cc"> .................. </tspan><tspan class="value">saadalahsanmain@gmail.com</tspan>
<tspan x="415" y="436" class="cc">. </tspan><tspan class="key">LinkedIn</tspan>:<tspan class="cc"> ........................ </tspan><tspan class="value">saadalahsan</tspan>
<tspan x="415" y="459" class="cc">. </tspan><tspan class="key">X/Twitter</tspan>:<tspan class="cc"> .................... </tspan><tspan class="value">@SaadAl_Ahsan</tspan>
<tspan x="415" y="482" class="cc">. </tspan><tspan class="key">Discord</tspan>:<tspan class="cc"> .......................... </tspan><tspan class="value">shopnil</tspan>
</text>
</svg>
"""

    # --- LIGHT MODE SVG ---
    light_svg = f"""<?xml version='1.0' encoding='UTF-8'?>
<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" font-family="ConsolasFallback,Consolas,monospace" width="985px" height="530px" font-size="14.5px">
<style>
@font-face {{
src: local('Consolas'), local('Consolas Bold');
font-family: 'ConsolasFallback';
font-display: swap;
-webkit-size-adjust: 109%;
size-adjust: 109%;
}}
/* GitHub Light Mode High-Contrast Colors */
.key {{fill: #bc4c00;}}
.value {{fill: #0969da;}}
.addColor {{fill: #1a7f37;}}
.delColor {{fill: #cf222e;}}
.cc {{fill: #57606a;}}
text, tspan {{white-space: pre;}}
</style>

<!-- Light Mode Card Background with subtle GitHub border -->
<rect width="985px" height="530px" fill="#ffffff" stroke="#d0d7de" stroke-width="2" rx="15"/>

<!-- Coder character with white bg (flood-filled, all internal details intact) -->
<image href="{light_data_uri}" xlink:href="{light_data_uri}" x="15" y="60" width="390" height="390" preserveAspectRatio="xMidYMid meet" />

<!-- Terminal Profile Details on Right Side -->
<text x="415" y="35" fill="#24292f">
<tspan x="415" y="35">saadalahsan</tspan> <tspan class="cc">-————————————————————————————————-—-</tspan>
<tspan x="415" y="58" class="cc">. </tspan><tspan class="key">OS</tspan>:<tspan class="cc"> ...................... </tspan><tspan class="value">Windows 10, Linux</tspan>
<tspan x="415" y="81" class="cc">. </tspan><tspan class="key">Uptime</tspan>:<tspan class="cc"> .................. </tspan><tspan class="value">Learner since day 1</tspan>
<tspan x="415" y="104" class="cc">. </tspan><tspan class="key">Role</tspan>:<tspan class="cc"> .................... </tspan><tspan class="value">Full-Stack Product Builder</tspan>
<tspan x="415" y="127" class="cc">. </tspan><tspan class="key">Focus</tspan>:<tspan class="cc"> ........... </tspan><tspan class="value">Trading, Web3, AI Automation</tspan>
<tspan x="415" y="150" class="cc">. </tspan><tspan class="key">IDE</tspan>:<tspan class="cc"> ...................... </tspan><tspan class="value">VSCode, Cursor</tspan>
<tspan x="415" y="173" class="cc">. </tspan>
<tspan x="415" y="196" class="cc">. </tspan><tspan class="key">Languages</tspan>.<tspan class="key">Programming</tspan>:<tspan class="cc"> .. </tspan><tspan class="value">JS, TS, Python, Rust, C++</tspan>
<tspan x="415" y="219" class="cc">. </tspan><tspan class="key">Languages</tspan>.<tspan class="key">Markup</tspan>:<tspan class="cc"> ......... </tspan><tspan class="value">HTML, CSS, JSON, YAML</tspan>
<tspan x="415" y="242" class="cc">. </tspan><tspan class="key">Languages</tspan>.<tspan class="key">Real</tspan>:<tspan class="cc"> ..................... </tspan><tspan class="value">Bangla, English</tspan>
<tspan x="415" y="265" class="cc">. </tspan>
<tspan x="415" y="288" class="cc">. </tspan><tspan class="key">Frameworks</tspan>:<tspan class="cc"> ............. </tspan><tspan class="value">React, Next.js, Node.js, Vite</tspan>
<tspan x="415" y="311" class="cc">. </tspan><tspan class="key">Databases</tspan>:<tspan class="cc"> .............. </tspan><tspan class="value">MongoDB, MySQL, Firebase</tspan>
<tspan x="415" y="334" class="cc">. </tspan><tspan class="key">Cloud</tspan>:<tspan class="cc"> ................... </tspan><tspan class="value">AWS, GCP, Azure, Vercel</tspan>
<tspan x="415" y="357" class="cc">. </tspan><tspan class="key">Web3</tspan>:<tspan class="cc"> .... </tspan><tspan class="value">Ethereum, Solana, Polygon, Hardhat</tspan>
<tspan x="415" y="390">- Contact</tspan> <tspan class="cc">-————————————————————————————————-—-</tspan>
<tspan x="415" y="413" class="cc">. </tspan><tspan class="key">Email</tspan>:<tspan class="cc"> .................. </tspan><tspan class="value">saadalahsanmain@gmail.com</tspan>
<tspan x="415" y="436" class="cc">. </tspan><tspan class="key">LinkedIn</tspan>:<tspan class="cc"> ........................ </tspan><tspan class="value">saadalahsan</tspan>
<tspan x="415" y="459" class="cc">. </tspan><tspan class="key">X/Twitter</tspan>:<tspan class="cc"> .................... </tspan><tspan class="value">@SaadAl_Ahsan</tspan>
<tspan x="415" y="482" class="cc">. </tspan><tspan class="key">Discord</tspan>:<tspan class="cc"> .......................... </tspan><tspan class="value">shopnil</tspan>
</text>
</svg>
"""

    dark_out = os.path.join(script_dir, "profile_card.svg")
    light_out = os.path.join(script_dir, "profile_card_light.svg")
    dark_copy = os.path.join(script_dir, "dark_mode.svg")
    
    with open(dark_out, "w", encoding="utf-8") as f:
        f.write(dark_svg)
    with open(dark_copy, "w", encoding="utf-8") as f:
        f.write(dark_svg)
    with open(light_out, "w", encoding="utf-8") as f:
        f.write(light_svg)
    print("SVGs successfully generated! Character intact with flood-fill approach.")

if __name__ == '__main__':
    build_svg_cards()
