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
    
    # 2. Light Mode: 5-frame animated GIF with pure white background
    # Multi-component segmentation:
    # - Person (X < 413): closed with tight 12x12 kernel for crisp hair, face, body, hands
    # - Monitor screen (X >= 413, Y between 240 and 420): closed with 15x15 kernel for solid full screen
    # - Desk & Stand (Y >= 420): closed with 5x5 kernel for crisp table and stand lines
    # - Gap between human & monitor: naturally open white space!
    # - Space under monitor & desk: naturally open white space!
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
    
    # Person silhouette (X < 413)
    person_mask = combined_mask.copy()
    person_mask[:, 413:] = 0
    k_person = cv2.getStructuringElement(cv2.MORPH_RECT, (12, 12))
    person_closed = cv2.morphologyEx(person_mask, cv2.MORPH_CLOSE, k_person)
    cnts_p, _ = cv2.findContours(person_closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    person_sil = np.zeros_like(combined_mask)
    for c in cnts_p:
        if cv2.contourArea(c) > 200:
            cv2.drawContours(person_sil, [c], -1, 255, -1)
            
    # Monitor screen silhouette (X >= 413, Y: 240..420)
    monitor_sil = np.zeros_like(combined_mask)
    mon_mask = combined_mask.copy()
    mon_mask[:, :413] = 0
    mon_mask[420:, :] = 0
    k_mon = cv2.getStructuringElement(cv2.MORPH_RECT, (15, 15))
    mon_closed = cv2.morphologyEx(mon_mask, cv2.MORPH_CLOSE, k_mon)
    cnts_m, _ = cv2.findContours(mon_closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for c in cnts_m:
        if cv2.contourArea(c) > 500:
            cv2.drawContours(monitor_sil, [c], -1, 255, -1)
            
    # Desk and monitor stand (Y >= 420)
    rest_mask = combined_mask.copy()
    rest_mask[:420, 413:] = 0
    k_rest = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    rest_sil = cv2.morphologyEx(rest_mask, cv2.MORPH_CLOSE, k_rest)
    rest_sil = cv2.bitwise_or(rest_sil, combined_mask)
    
    # Combine all components
    final_sil = cv2.bitwise_or(person_sil, monitor_sil)
    final_sil = cv2.bitwise_or(final_sil, rest_sil)
    
    # Create white-background frames
    white_frames = []
    for bgr in frames_bgr:
        out_bgr = np.full_like(bgr, 255) # pure white
        out_bgr[final_sil > 0] = bgr[final_sil > 0] # preserve all character and monitor details
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
    print("SVGs successfully generated with clean multi-component cutout!")

if __name__ == '__main__':
    build_svg_cards()
