"""
Give every photo the site's look, so they read as one set.

    python3 tools/process_photos.py  incoming/  photos/

For each image in incoming/ it:
  1. fixes rotation from the camera's orientation tag
  2. applies a partial white balance (fixes blue restaurant / aquarium casts)
  3. sets gentle levels and evens out exposure
  4. adds a soft contrast curve, a warm tone, and slightly mutes the color
  5. resizes to 1400 px on the long side
  6. saves a JPEG near 250 KB with ALL metadata removed (no GPS, no camera info)

It also writes photos/_before_after.jpg so you can compare a few results.
Needs Pillow:  pip install pillow
"""
import sys, io
from pathlib import Path
from PIL import Image, ImageOps, ImageEnhance, ImageStat

LONG_SIDE = 1400
TARGET_KB = 250
EXTS = {".jpg", ".jpeg", ".png", ".heic", ".webp", ".tif", ".tiff"}


def white_balance(img, strength=0.55):
    """Gray-world white balance, blended partway so photos keep their mood."""
    r, g, b = ImageStat.Stat(img).mean
    avg = (r + g + b) / 3
    gains = [1 + strength * (avg / max(c, 1) - 1) for c in (r, g, b)]
    ch = [c.point(lambda v, k=k: min(255, int(v * k))) for c, k in zip(img.split(), gains)]
    return Image.merge("RGB", ch)


def levels_and_exposure(img, target=118):
    img = ImageOps.autocontrast(img, cutoff=0.6)            # gentle levels
    lum = ImageStat.Stat(img.convert("L")).mean[0]
    factor = max(0.8, min(1.25, (target / max(lum, 1)) ** 0.5))  # nudge toward the same brightness
    return ImageEnhance.Brightness(img).enhance(factor)


def soft_curve(img, amount=0.12):
    import math
    # S-curve: darkens shadows a little, lifts highlights a little
    lut = [max(0, min(255, int(255 * (v / 255 - amount * math.sin(2 * math.pi * v / 255) / (2 * math.pi))))) for v in range(256)]
    return img.point(lut * 3)


def warm_and_mute(img):
    r, g, b = img.split()
    r = r.point(lambda v: min(255, int(v * 1.035 + 3)))
    b = b.point(lambda v: int(v * 0.95))
    img = Image.merge("RGB", (r, g, b))
    return ImageEnhance.Color(img).enhance(0.88)


def save_small(img, dest):
    """Lower JPEG quality until the file is near TARGET_KB."""
    for q in range(88, 54, -4):
        buf = io.BytesIO()
        img.save(buf, "JPEG", quality=q, optimize=True, progressive=True)  # no exif= -> metadata stripped
        if buf.tell() <= TARGET_KB * 1024:
            break
    dest.write_bytes(buf.getvalue())
    return buf.tell() // 1024


def process(src):
    img = ImageOps.exif_transpose(Image.open(src)).convert("RGB")
    img.thumbnail((LONG_SIDE, LONG_SIDE), Image.LANCZOS)
    before = img.copy()
    img = white_balance(img)
    img = levels_and_exposure(img)
    img = soft_curve(img)
    img = warm_and_mute(img)
    return before, img


def main(inp, out):
    inp, out = Path(inp), Path(out)
    out.mkdir(parents=True, exist_ok=True)
    pairs = []
    for f in sorted(p for p in inp.iterdir() if p.suffix.lower() in EXTS):
        before, after = process(f)
        dest = out / (f.stem.lower().replace(" ", "-") + ".jpg")
        kb = save_small(after, dest)
        print(f"{f.name:30s} -> {dest.name:30s} {after.size[0]}x{after.size[1]}  {kb} KB")
        pairs.append((before, after))
    if pairs:  # before/after sheet of up to 4 photos
        h = 300
        rows = []
        for b, a in pairs[:4]:
            w = int(b.width * h / b.height)
            rows.append((b.resize((w, h)), a.resize((w, h))))
        W = max(r[0].width for r in rows) * 2 + 30
        sheet = Image.new("RGB", (W, len(rows) * (h + 10) + 10), (15, 59, 45))
        for i, (b, a) in enumerate(rows):
            sheet.paste(b, (10, 10 + i * (h + 10)))
            sheet.paste(a, (20 + b.width, 10 + i * (h + 10)))
        sheet.save(out / "_before_after.jpg", quality=85)
        print("Comparison sheet:", out / "_before_after.jpg", "(delete it before publishing)")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    main(sys.argv[1], sys.argv[2])
