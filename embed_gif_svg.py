import base64
import os

def build_svg_cards():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    gif_path = os.path.join(script_dir, "coding_sticker.gif")
    
    # Read original GIF (used for BOTH dark and light mode - NO modification)
    with open(gif_path, "rb") as f:
        gif_bytes = f.read()
    gif_b64 = base64.b64encode(gif_bytes).decode("utf-8")
    gif_data_uri = f"data:image/gif;base64,{gif_b64}"
    
    # --- DARK MODE SVG (unchanged) ---
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
<image href="{gif_data_uri}" xlink:href="{gif_data_uri}" x="15" y="60" width="390" height="390" preserveAspectRatio="xMidYMid meet" />

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
    # Original GIF untouched, sitting in a rounded dark container on white card
    # The dark container matches the GIF bg so the character blends perfectly
    # It looks like a terminal/code window embedded in the white card
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

<!-- White card background -->
<rect width="985px" height="530px" fill="#ffffff" stroke="#d0d7de" stroke-width="1" rx="15"/>

<!-- Dark rounded container for the character GIF (matches GIF bg perfectly) -->
<rect x="20" y="55" width="380" height="400" fill="#161b22" rx="12"/>

<!-- Original GIF sitting perfectly inside the dark container -->
<image href="{gif_data_uri}" xlink:href="{gif_data_uri}" x="15" y="60" width="390" height="390" preserveAspectRatio="xMidYMid meet" />

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
    print("SVGs generated! Original GIF used for both modes.")

if __name__ == '__main__':
    build_svg_cards()
