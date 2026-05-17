"""Build hero tile thumbnails — small embedded screenshots for showcase tiles."""
from PIL import Image
import os

ROOT = "/Users/macbook/Desktop/1-Projets-Dev/klikdev-site"
OUT = f"{ROOT}/assets"

# Target thumbnail size (5:4 landscape, fits inside 3:4 portrait tile)
TILE_W, TILE_H = 480, 384


def crop_resize(img, crop_box, out_w=TILE_W, out_h=TILE_H, quality=86):
    """Crop a region then resize to target dims preserving aspect (cover)."""
    img = img.crop(crop_box)
    # Cover-style resize
    src_w, src_h = img.size
    src_ratio = src_w / src_h
    target_ratio = out_w / out_h
    if src_ratio > target_ratio:
        # source too wide → crop sides
        new_w = int(src_h * target_ratio)
        offset = (src_w - new_w) // 2
        img = img.crop((offset, 0, offset + new_w, src_h))
    elif src_ratio < target_ratio:
        # source too tall → crop top/bottom
        new_h = int(src_w / target_ratio)
        offset = (src_h - new_h) // 2
        img = img.crop((0, offset, src_w, offset + new_h))
    img = img.resize((out_w, out_h), Image.LANCZOS)
    return img


def save_tile(img, name, quality=86):
    img.save(f"{OUT}/tile-{name}.jpg", "JPEG", quality=quality, optimize=True, progressive=True)
    size = os.path.getsize(f"{OUT}/tile-{name}.jpg") / 1024
    print(f"✓ tile-{name}.jpg  {img.size}  ({size:.0f} Ko)")


# Project-visual region in raw Chrome screenshots (Retina 2x)
PV_BOX = (1526, 330, 2584, 1176)  # x1, y1, x2, y2 in 2880x1506 retina screenshot

# ─── Klik&Go (from raw-tile-klikandgo.png) ───
img = Image.open(f"{ROOT}/raw-tile-klikandgo.png").convert("RGB")
img = crop_resize(img, PV_BOX)
save_tile(img, "klikandgo")

# ─── Invoquo ───
img = Image.open(f"{ROOT}/raw-tile-invoquo.png").convert("RGB")
img = crop_resize(img, PV_BOX)
save_tile(img, "invoquo")

# ─── MonPCMI13 ───
img = Image.open(f"{ROOT}/raw-tile-pcmi13.png").convert("RGB")
img = crop_resize(img, PV_BOX)
save_tile(img, "pcmi13")

# ─── Bativio (use real capture) ───
# bativio-hero.jpg is 1800x941. Take a center crop showing the hero headline.
img = Image.open(f"{OUT}/bativio-hero.jpg").convert("RGB")
# Crop a centered area with the headline (avoid top nav, bottom search inputs)
img = crop_resize(img, (300, 100, 1500, 1000))
save_tile(img, "bativio")

# ─── Klikphone SAV (use homepage splash) ───
# ksav-homepage.jpg is 1800x1125. Center crop with the KLIKPHONE logo + cards.
img = Image.open(f"{OUT}/ksav-homepage.jpg").convert("RGB")
img = crop_resize(img, (350, 0, 1450, 1125))
save_tile(img, "ksav")

print("\nDONE — Tile thumbnails:")
for f in sorted(os.listdir(OUT)):
    if f.startswith("tile-"):
        size = os.path.getsize(os.path.join(OUT, f)) / 1024
        print(f"  {f}  ({size:.0f} Ko)")
