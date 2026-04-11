"""
Generate project banners for Kohaku-branded projects.

Usage:
  python scripts/generate_banner.py Terrarium --tagline "A universal agent-level abstraction framework."
  python scripts/generate_banner.py Vault --tagline "SQLite-backed persistent storage."

Opens the banner in the default browser.
"""

import argparse
import html
import webbrowser
from pathlib import Path

TEMPLATE = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;800&display=swap');
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}

  body {{
    width: {width}px;
    height: {height}px;
    overflow: hidden;
    background: linear-gradient(135deg, #1A1820, #1E1A2A);
    display: flex;
    align-items: center;
    font-family: 'Inter', system-ui, sans-serif;
    position: relative;
  }}

  /* Subtle background glow */
  .glow {{
    position: absolute; border-radius: 50%; opacity: 0.07; pointer-events: none;
  }}
  .g1 {{ width: 500px; height: 500px; background: radial-gradient(circle, #5A4FCF, transparent 70%); top: -150px; right: -100px; }}
  .g2 {{ width: 350px; height: 350px; background: radial-gradient(circle, #E8A0BF, transparent 70%); bottom: -100px; left: 150px; }}

  /* Bottom accent */
  .accent {{
    position: absolute; bottom: 0; left: 0; right: 0; height: 3px;
    background: linear-gradient(90deg, #D4920A, #E8A0BF, #5A4FCF, #2D5FA0);
  }}

  /* Avatar */
  .avatar-wrap {{ flex-shrink: 0; margin-left: {margin_left}px; margin-right: {gap}px; }}
  .avatar {{
    width: {avatar_size}px; height: {avatar_size}px;
    border-radius: 50%; object-fit: cover;
    border: 2.5px solid rgba(90, 79, 207, 0.35);
    box-shadow: 0 0 40px rgba(90, 79, 207, 0.12), 0 0 80px rgba(232, 160, 191, 0.06);
  }}

  /* Text */
  .text {{ display: flex; flex-direction: column; gap: 8px; }}
  .title {{ line-height: 1; }}
  .prefix {{
    font-weight: 800; font-size: {font_size}px; color: #F0B840;
    letter-spacing: -2px;
  }}
  .project {{
    font-weight: 300; font-size: {font_size}px; color: #8B83DB;
    letter-spacing: -1px;
  }}
  .tagline {{
    font-weight: 300; font-size: {tagline_size}px;
    color: rgba(232, 224, 216, 0.4); letter-spacing: 0.3px;
  }}
</style>
</head>
<body>
  <div class="glow g1"></div>
  <div class="glow g2"></div>
  <div class="accent"></div>

  {avatar_html}

  <div class="text">
    <div class="title">
      <span class="prefix">Kohaku</span><span class="project">{project}</span>
    </div>
    {tagline_html}
  </div>
</body>
</html>"""


def generate(
    project: str,
    tagline: str = "",
    avatar_path: str | None = None,
    width: int = 1280,
    height: int = 320,
    font_size: int = 72,
    tagline_size: int = 20,
    avatar_size: int = 200,
    margin_left: int = 60,
    gap: int = 45,
) -> str:
    avatar_html = ""
    if avatar_path:
        avatar_html = (
            f'<div class="avatar-wrap">'
            f'<img class="avatar" src="{html.escape(avatar_path)}" alt="Kohaku">'
            f'</div>'
        )

    tagline_html = ""
    if tagline:
        tagline_html = f'<div class="tagline">{html.escape(tagline)}</div>'

    return TEMPLATE.format(
        project=html.escape(project),
        tagline_html=tagline_html,
        avatar_html=avatar_html,
        width=width,
        height=height,
        font_size=font_size,
        tagline_size=tagline_size,
        avatar_size=avatar_size,
        margin_left=margin_left,
        gap=gap,
    )


def main():
    parser = argparse.ArgumentParser(description="Generate Kohaku project banner")
    parser.add_argument("project", help="Project name (e.g. Terrarium, Vault)")
    parser.add_argument("--tagline", default="", help="Tagline text")
    parser.add_argument("--avatar", default=None, help="Path to avatar image")
    parser.add_argument("--width", type=int, default=1280)
    parser.add_argument("--height", type=int, default=320)
    parser.add_argument("--font-size", type=int, default=72)
    parser.add_argument("--avatar-size", type=int, default=200)
    parser.add_argument("-o", "--output", default=None, help="Output HTML path")
    args = parser.parse_args()

    banner = generate(
        project=args.project,
        tagline=args.tagline,
        avatar_path=args.avatar,
        width=args.width,
        height=args.height,
        font_size=args.font_size,
        avatar_size=args.avatar_size,
    )

    out = Path(args.output) if args.output else Path(f"banner_{args.project.lower()}.html")
    out.write_text(banner, encoding="utf-8")
    print(f"Saved: {out}")
    webbrowser.open(str(out.resolve()))


if __name__ == "__main__":
    main()
