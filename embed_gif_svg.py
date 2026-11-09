import base64
import os
import cv2
import numpy as np
from PIL import Image, ImageSequence

def build_svg_cards():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    gif_path = os.path.join(script_dir, "coding_sticker.gif")
    
    # 1. Dark Mode: original GIF with dark background (unchanged)
    with open(gif_path, "rb") as f:
        dark_gif_bytes = f.read()
    dark_b64 = base64.b64encode(dark_gif_bytes).decode("utf-8")
    dark_data_uri = f"data:image/gif;base64,{dark_b64}"
    
    # 2. Light Mode: 5-frame animated GIF with pure white background outside
    # Uses commit 5069356 solid silhouette so that the desk, hands, keyboard, monitor,
    # chair, and legs retain all of their original internal black background and details.
    # ONLY removes the small vertical gap between the person's face and the monitor (Y: 240..400, X: 370..412).
    orig_gif = Image.open(gif_path)
    bg = np.array([34, 27, 22], dtype=np.uint8) # BGR for OpenCV
    
    combined_mask = np.zeros((orig_gif.height, orig_gif.width), dtype=np.uint8)
    frames_bgr = []
    
    for frame in ImageSequence.Iterator(orig_gif):
        rgb_arr = np.array(frame.convert("RGB"))
        bgr_arr = cv2.cvtColor(rgb_arr, cv2.COLOR_RGB2BGR)
        frames_bgr.append(bgr_arr)
        
        diff = np.abs(bgr_arr.astype(int) - bg.astype(int))
        mask = np.any(diff > 5, axis=2).astype(np.uint8) * 255
        combined_mask = cv2.bitwise_or(combined_mask, mask)
    
    # Solid silhouette preserving full monitor rectangle, desk, chair, and internal details
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (25, 25))
    closed = cv2.morphologyEx(combined_mask, cv2.MORPH_CLOSE, kernel)
    
    contours, _ = cv2.findContours(closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    silhouette = np.zeros_like(combined_mask)
    for cnt in contours:
        if cv2.contourArea(cnt) > 500:
            cv2.drawContours(silhouette, [cnt], -1, 255, -1)
            
    kernel_smooth = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7))
    silhouette = cv2.morphologyEx(silhouette, cv2.MORPH_CLOSE, kernel_smooth)
    
    # ONLY remove the black background in the gap between the person's face and the monitor
    h_idx = np.arange(orig_gif.height)[:, None]
    w_idx = np.arange(orig_gif.width)[None, :]
    gap = (combined_mask == 0) & (w_idx >= 370) & (w_idx < 413) & (h_idx >= 240) & (h_idx < 400)
    silhouette[gap] = 0
    
    # Create white-background frames
    white_frames = []
    for bgr in frames_bgr:
        out_bgr = np.full_like(bgr, 255) # pure white
        out_bgr[silhouette > 0] = bgr[silhouette > 0] # preserve all internal details
        rgb_out = cv2.cvtColor(out_bgr, cv2.COLOR_BGR2RGB)
        white_frames.append(Image.fromarray(rgb_out))
        
    # Save as 5-frame animated GIF
    light_gif_path = os.path.join(script_dir, "coding_sticker_light.gif")
    white_frames[0].save(
        light_gif_path,
        save_all=True,
        append_images=white_frames[1:],
        duration=orig_gif.info.get("duration", 90),
        loop=0
    )
    
    with open(light_gif_path, "rb") as f:
        light_gif_bytes = f.read()
    light_b64 = base64.b64encode(light_gif_bytes).decode("utf-8")
    light_data_uri = f"data:image/gif;base64,{light_b64}"
    
    print(f"Generated light animated GIF: {light_gif_path} ({len(light_gif_bytes)/1024:.1f} KB)")
    
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
    # Pure white card background. Animated character with NO black box, NO dark rect.
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

<!-- Animated Coding Character (Seamless on white, NO black box, all internal details intact) -->
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
    print("SVGs successfully generated! All internal details intact, gap cleanly opened.")

if __name__ == '__main__':
    build_svg_cards()
