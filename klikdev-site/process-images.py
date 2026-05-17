"""Process screenshots for portfolio site: resize + blur PII regions."""
from PIL import Image, ImageFilter, ImageDraw, ImageEnhance
import os

ROOT = "/Users/macbook/Desktop/1-Projets-Dev"
KSAV = f"{ROOT}/klikphone-screenshots/final"
OUT = f"{ROOT}/klikdev-site/assets"
os.makedirs(OUT, exist_ok=True)


def blur_region(img, x1, y1, x2, y2, radius=24):
    """Apply Gaussian blur to a rectangular region (in-place)."""
    region = img.crop((x1, y1, x2, y2))
    blurred = region.filter(ImageFilter.GaussianBlur(radius=radius))
    img.paste(blurred, (x1, y1))
    return img


def resize_max_width(img, max_w=1800):
    w, h = img.size
    if w > max_w:
        new_h = int(h * max_w / w)
        return img.resize((max_w, new_h), Image.LANCZOS)
    return img


def add_border_radius(img, radius_pct=0.018):
    """Soft rounded corners via alpha mask. Returns RGBA."""
    w, h = img.size
    r = int(min(w, h) * radius_pct)
    mask = Image.new("L", (w, h), 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle((0, 0, w - 1, h - 1), radius=r, fill=255)
    img = img.convert("RGBA")
    img.putalpha(mask)
    return img


def save_jpg(img, path, quality=86):
    if img.mode == "RGBA":
        # Composite onto dark background to flatten
        bg = Image.new("RGB", img.size, (13, 17, 23))
        bg.paste(img, mask=img.split()[3])
        img = bg
    img.save(path, "JPEG", quality=quality, optimize=True, progressive=True)


def save_png(img, path):
    img.save(path, "PNG", optimize=True)


# ═══════════════════════════════════════════════════════════
# KLIKPHONE SAV — screenshots avec floutage PII
# ═══════════════════════════════════════════════════════════

# Image dims = 2880x1800 (Retina 2x of 1440x900)

# ─── d01 homepage : pas de PII, juste resize ───
img = Image.open(f"{KSAV}/d01-homepage.png").convert("RGB")
img = resize_max_width(img, 1800)
save_jpg(img, f"{OUT}/ksav-homepage.jpg")
print("✓ ksav-homepage.jpg", img.size)

# ─── d03 dashboard : flouter colonne CLIENT (noms + tel) ───
# Tableau commence vers y=1220 (header "58 actif(s)" + columns)
# Colonne CLIENT : x=720-1200 environ (entre TICKET et APPAREIL)
img = Image.open(f"{KSAV}/d03-dashboard.png").convert("RGB")
img = blur_region(img, 680, 1180, 1220, 1800, radius=28)
img = resize_max_width(img, 1800)
save_jpg(img, f"{OUT}/ksav-dashboard.jpg")
print("✓ ksav-dashboard.jpg", img.size)

# ─── d04 dashboard tickets : flouter toute la colonne CLIENT ───
img = Image.open(f"{KSAV}/d04-dashboard-tickets.png").convert("RGB")
img = blur_region(img, 680, 0, 1220, 1800, radius=28)
img = resize_max_width(img, 1800)
save_jpg(img, f"{OUT}/ksav-tickets.jpg")
print("✓ ksav-tickets.jpg", img.size)

# ─── d05 ticket detail : flouter header (nom+tel) + Client card ───
img = Image.open(f"{KSAV}/d05-ticket-detail.png").convert("RGB")
# Toute la ligne info client en haut (Julie Martin • Samsung • etc.)
img = blur_region(img, 340, 140, 2000, 260, radius=28)
# Ligne téléphone juste en dessous
img = blur_region(img, 340, 240, 900, 340, radius=26)
# Client card complète (avatar JM + nom + tel + email)
img = blur_region(img, 600, 760, 1800, 1480, radius=32)
img = resize_max_width(img, 1800)
save_jpg(img, f"{OUT}/ksav-ticket-detail.jpg")
print("✓ ksav-ticket-detail.jpg", img.size)

# ─── d10 suivi : pas de PII (juste KP-000252 + Samsung A51) ───
img = Image.open(f"{KSAV}/d10-suivi.png").convert("RGB")
img = resize_max_width(img, 1800)
save_jpg(img, f"{OUT}/ksav-suivi.jpg")
print("✓ ksav-suivi.jpg", img.size)

# ─── d17 reporting : pas de PII (KPIs aggrégés) ───
img = Image.open(f"{KSAV}/d17-reporting.png").convert("RGB")
img = resize_max_width(img, 1800)
save_jpg(img, f"{OUT}/ksav-reporting.jpg")
print("✓ ksav-reporting.jpg", img.size)

# ─── d18 reporting-graphs : pas de PII ───
img = Image.open(f"{KSAV}/d18-reporting-graphs.png").convert("RGB")
img = resize_max_width(img, 1800)
save_jpg(img, f"{OUT}/ksav-reporting-graphs.jpg")
print("✓ ksav-reporting-graphs.jpg", img.size)

# ─── d20 avis-google : pas de PII personnelle ───
img = Image.open(f"{KSAV}/d20-avis-google.png").convert("RGB")
img = resize_max_width(img, 1800)
save_jpg(img, f"{OUT}/ksav-avis-google.jpg")
print("✓ ksav-avis-google.jpg", img.size)

# ─── d11 dépôt-1-client (form vide, no PII) ───
img = Image.open(f"{KSAV}/d11-depot-1-client.png").convert("RGB")
img = resize_max_width(img, 1800)
save_jpg(img, f"{OUT}/ksav-depot.jpg")
print("✓ ksav-depot.jpg", img.size)

# ═══════════════════════════════════════════════════════════
# BATIVIO — captures live
# ═══════════════════════════════════════════════════════════

for src, out in [
    ("raw-bativio.png", "bativio-hero.jpg"),
    ("raw-bativio-2.png", "bativio-artisans.jpg"),
    ("raw-bativio-3.png", "bativio-process.jpg"),
]:
    p = f"{ROOT}/klikdev-site/{src}"
    if not os.path.exists(p):
        continue
    img = Image.open(p).convert("RGB")
    img = resize_max_width(img, 1800)
    save_jpg(img, f"{OUT}/{out}", quality=88)
    print(f"✓ {out}", img.size)

# ═══════════════════════════════════════════════════════════
# Mobile versions pour Klikphone (utilisés en accent)
# ═══════════════════════════════════════════════════════════
img = Image.open(f"{KSAV}/m01-homepage.png").convert("RGB")
img = resize_max_width(img, 720)
save_jpg(img, f"{OUT}/ksav-mobile-home.jpg")
print("✓ ksav-mobile-home.jpg", img.size)

img = Image.open(f"{KSAV}/m10-suivi.png").convert("RGB")
img = resize_max_width(img, 720)
save_jpg(img, f"{OUT}/ksav-mobile-suivi.jpg")
print("✓ ksav-mobile-suivi.jpg", img.size)

print("\nDONE — Total assets:")
for f in sorted(os.listdir(OUT)):
    size = os.path.getsize(os.path.join(OUT, f)) / 1024
    print(f"  {f}  ({size:.0f} Ko)")
