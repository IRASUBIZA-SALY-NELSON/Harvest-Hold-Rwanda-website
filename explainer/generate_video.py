#!/usr/bin/env python3
"""Generate Harvest Hold Rwanda SHCCS prototype explainer video frames."""

from __future__ import annotations

import math
import os
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent
FRAMES = ROOT / "frames"
W, H = 1280, 720
FPS = 24

GREEN = (46, 158, 74)
GREEN_DIM = (28, 95, 48)
ORANGE = (232, 140, 48)
CREAM = (236, 242, 232)
WHITE = (255, 255, 255)
DARK = (12, 22, 16)
PANEL = (20, 36, 26)
WOOD = (122, 84, 48)
WOOD_DK = (84, 56, 30)
CHARCOAL = (48, 48, 48)
WATER = (72, 160, 220)
COOL = (120, 210, 230)
WARM = (255, 150, 90)
ALERT = (220, 60, 50)

FONT_REG = "/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf"
FONT_BOLD = "/usr/share/fonts/truetype/noto/NotoSans-SemiCondensedSemiBold.ttf"


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    path = FONT_BOLD if bold else FONT_REG
    return ImageFont.truetype(path, size)


def lerp(a: float, b: float, t: float) -> float:
    return a + (b - a) * t


def clamp(t: float) -> float:
    return max(0.0, min(1.0, t))


def ease(t: float) -> float:
    t = clamp(t)
    return t * t * (3 - 2 * t)


def scene_progress(frame: int, start: int, end: int) -> float:
    if frame < start:
        return 0.0
    if frame >= end:
        return 1.0
    return ease((frame - start) / max(1, end - start))


def draw_bg(draw: ImageDraw.ImageDraw, img: Image.Image) -> None:
    for y in range(H):
        t = y / H
        r = int(lerp(10, 18, t))
        g = int(lerp(28, 42, t))
        b = int(lerp(16, 24, t))
        draw.line([(0, y), (W, y)], fill=(r, g, b))
    # soft radial glow
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    for i in range(8):
        alpha = 18 - i * 2
        pad = 40 + i * 50
        od.ellipse([pad, pad - 40, W - pad, H - pad + 80], fill=(46, 158, 74, alpha))
    img.alpha_composite(overlay)


def draw_header(draw: ImageDraw.ImageDraw, title: str, subtitle: str = "") -> None:
    draw.rounded_rectangle([36, 28, W - 36, 108], radius=18, fill=PANEL)
    draw.rectangle([36, 28, 48, 108], fill=ORANGE)
    draw.text((68, 42), title, font=font(28, True), fill=GREEN)
    if subtitle:
        draw.text((68, 76), subtitle, font=font(16), fill=CREAM)


def draw_footer(draw: ImageDraw.ImageDraw, step: str, progress: float) -> None:
    draw.text((48, H - 42), "Harvest Hold Rwanda  ·  Smart Hybrid Charcoal Cooler", font=font(14), fill=(160, 190, 165))
    draw.text((W - 220, H - 42), step, font=font(14, True), fill=ORANGE)
    # progress bar
    bw, bh = W - 96, 6
    x0, y0 = 48, H - 58
    draw.rounded_rectangle([x0, y0, x0 + bw, y0 + bh], radius=3, fill=(40, 60, 45))
    draw.rounded_rectangle([x0, y0, x0 + int(bw * progress), y0 + bh], radius=3, fill=GREEN)


def draw_cooler(
    draw: ImageDraw.ImageDraw,
    img: Image.Image,
    cx: int,
    cy: int,
    scale: float,
    wet: float,
    fan_angle: float,
    cool_flow: float,
    show_produce: bool = True,
    show_labels: bool = True,
    pump_on: bool = False,
    alert: bool = False,
) -> None:
    """Draw cutaway cooler diagram."""
    sw = int(420 * scale)
    sh = int(300 * scale)
    x0, y0 = cx - sw // 2, cy - sh // 2
    gap = int(36 * scale)

    # outer crate
    draw.rounded_rectangle([x0, y0, x0 + sw, y0 + sh], radius=10, fill=WOOD, outline=WOOD_DK, width=3)
    # charcoal walls (left/right/bottom gap)
    draw.rectangle([x0 + 8, y0 + 8, x0 + gap, y0 + sh - 8], fill=CHARCOAL)
    draw.rectangle([x0 + sw - gap, y0 + 8, x0 + sw - 8, y0 + sh - 8], fill=CHARCOAL)
    draw.rectangle([x0 + 8, y0 + sh - gap, x0 + sw - 8, y0 + sh - 8], fill=CHARCOAL)

    # wet charcoal shimmer
    if wet > 0:
        overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        od = ImageDraw.Draw(overlay)
        a = int(90 * wet)
        od.rectangle([x0 + 8, y0 + 8, x0 + gap, y0 + sh - 8], fill=(*WATER, a // 2))
        od.rectangle([x0 + sw - gap, y0 + 8, x0 + sw - 8, y0 + sh - 8], fill=(*WATER, a // 2))
        # droplets
        for i in range(6):
            dy = int((y0 + 20 + i * 35 + wet * 40) % (sh - 40))
            od.ellipse([x0 + gap // 2 - 3, y0 + dy, x0 + gap // 2 + 3, y0 + dy + 8], fill=(*WATER, a))
            od.ellipse([x0 + sw - gap // 2 - 3, y0 + dy, x0 + sw - gap // 2 + 3, y0 + dy + 8], fill=(*WATER, a))
        img.alpha_composite(overlay)

    # inner chamber
    ix0, iy0 = x0 + gap + 6, y0 + 18
    ix1, iy1 = x0 + sw - gap - 6, y0 + sh - gap - 6
    chamber = (35, 55, 42) if cool_flow < 0.3 else (30, 70, 55)
    draw.rounded_rectangle([ix0, iy0, ix1, iy1], radius=8, fill=chamber, outline=(70, 110, 80), width=2)

    # produce
    if show_produce:
        # tomatoes
        for i, (px, py) in enumerate([(ix0 + 40, iy1 - 45), (ix0 + 75, iy1 - 50), (ix0 + 55, iy1 - 70)]):
            draw.ellipse([px, py, px + 28, py + 28], fill=(200, 55, 45), outline=(150, 30, 25))
        # leafy greens
        draw.ellipse([ix1 - 90, iy1 - 70, ix1 - 30, iy1 - 25], fill=(70, 160, 70))
        draw.ellipse([ix1 - 110, iy1 - 55, ix1 - 55, iy1 - 20], fill=(50, 130, 55))
        # carrots
        draw.polygon([(ix0 + 120, iy1 - 25), (ix0 + 135, iy1 - 70), (ix0 + 145, iy1 - 25)], fill=(230, 120, 40))

    # water reservoir (top right)
    rx0, ry0 = x0 + sw - gap - 70, y0 - 55
    draw.rounded_rectangle([rx0, ry0, rx0 + 55, ry0 + 45], radius=6, fill=(40, 90, 140), outline=WATER, width=2)
    water_h = int(28 * (0.4 + 0.6 * wet))
    draw.rectangle([rx0 + 4, ry0 + 40 - water_h, rx0 + 51, ry0 + 41], fill=WATER)
    if pump_on:
        # drip line
        draw.line([(rx0 + 27, ry0 + 45), (rx0 + 27, y0 + 10)], fill=WATER, width=2)
        for i in range(3):
            dy = int((fan_angle * 20 + i * 12) % 40)
            draw.ellipse([rx0 + 24, y0 + 8 + dy, rx0 + 30, y0 + 16 + dy], fill=WATER)

    # solar panel on lid
    draw.rounded_rectangle([x0 + 40, y0 - 28, x0 + 160, y0 - 6], radius=3, fill=(20, 40, 80), outline=(80, 140, 200), width=2)
    for i in range(4):
        draw.line([x0 + 50 + i * 25, y0 - 26, x0 + 50 + i * 25, y0 - 8], fill=(60, 100, 160), width=1)

    # fan (right side)
    fx, fy = x0 + sw - 18, y0 + sh // 2
    draw.ellipse([fx - 22, fy - 22, fx + 22, fy + 22], fill=(30, 30, 30), outline=GREEN, width=2)
    for blade in range(3):
        ang = fan_angle + blade * (2 * math.pi / 3)
        x1 = fx + int(math.cos(ang) * 16)
        y1 = fy + int(math.sin(ang) * 16)
        draw.line([(fx, fy), (x1, y1)], fill=CREAM, width=4)
    draw.ellipse([fx - 5, fy - 5, fx + 5, fy + 5], fill=ORANGE)

    # airflow particles
    if cool_flow > 0:
        overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        od = ImageDraw.Draw(overlay)
        for i in range(10):
            t = (cool_flow + i * 0.08 + fan_angle * 0.02) % 1.0
            # warm in from right through charcoal
            wx = int(lerp(x0 + sw + 30, x0 + sw - gap // 2, t))
            wy = int(fy - 40 + (i % 5) * 18 + math.sin(t * 6 + i) * 4)
            od.ellipse([wx, wy, wx + 10, wy + 6], fill=(*WARM, int(140 * (1 - t))))
            # cool into chamber
            if t > 0.35:
                ct = (t - 0.35) / 0.65
                cxp = int(lerp(x0 + sw - gap, ix0 + 30, ct))
                cyp = int(fy - 20 + (i % 4) * 16)
                od.ellipse([cxp, cyp, cxp + 12, cyp + 7], fill=(*COOL, int(160 * (1 - ct * 0.5))))
        img.alpha_composite(overlay)

    # OLED + button
    ox0, oy0 = x0 + 24, y0 + sh // 2 - 30
    draw.rounded_rectangle([ox0, oy0, ox0 + 70, oy0 + 48], radius=4, fill=(10, 10, 10), outline=(80, 80, 80), width=2)
    temp = 22.5 - cool_flow * 8
    hum = 55 + cool_flow * 20
    oled_color = ALERT if alert else GREEN
    draw.text((ox0 + 8, oy0 + 6), f"{temp:.1f}°C", font=font(11, True), fill=oled_color)
    draw.text((ox0 + 8, oy0 + 22), f"RH {hum:.0f}%", font=font(10), fill=CREAM)
    draw.ellipse([ox0 + 28, oy0 + 55, ox0 + 42, oy0 + 69], fill=GREEN if not alert else ALERT)

    if show_labels:
        labels = [
            (x0 + sw // 2, y0 + sh + 18, "Produce chamber", CREAM),
            (x0 + gap // 2, y0 - 8, "Charcoal", (180, 180, 180)),
            (rx0 + 27, ry0 - 14, "Water", WATER),
            (fx, fy + 36, "DC fan", ORANGE),
            (x0 + 100, y0 - 40, "Solar", (120, 180, 255)),
        ]
        for lx, ly, text, col in labels:
            bbox = draw.textbbox((0, 0), text, font=font(12, True))
            tw = bbox[2] - bbox[0]
            draw.text((lx - tw // 2, ly), text, font=font(12, True), fill=col)


def draw_esp_block(draw: ImageDraw.ImageDraw, x: int, y: int, active: float, alert: bool = False) -> None:
    draw.rounded_rectangle([x, y, x + 260, y + 210], radius=12, fill=PANEL, outline=GREEN if active > 0.5 else (60, 80, 65), width=2)
    draw.text((x + 16, y + 12), "ESP32 DevKit C V4", font=font(16, True), fill=GREEN)
    items = [
        ("SHT31 T/H sensor", "I²C GPIO21/22"),
        ("Ethylene C₂H₄", "Ripening gas"),
        ("OLED 0.96\"", "Live status"),
        ("Fan + pump control", "Smart hybrid logic"),
        ("Buzzer + LED", "GPIO17 / GPIO19"),
    ]
    for i, (a, b) in enumerate(items):
        yy = y + 44 + i * 30
        on = active > i * 0.15
        draw.ellipse([x + 16, yy + 4, x + 28, yy + 16], fill=GREEN if on else (50, 70, 55))
        draw.text((x + 38, yy), a, font=font(13, True), fill=CREAM if on else (100, 120, 105))
        draw.text((x + 38, yy + 14), b, font=font(11), fill=(140, 170, 145) if on else (70, 90, 75))
    if alert:
        draw.rounded_rectangle([x + 16, y + 175, x + 244, y + 198], radius=6, fill=(80, 25, 20))
        draw.text((x + 28, y + 178), "ALERT · TEMP HIGH", font=font(13, True), fill=ALERT)


def draw_dashboard(draw: ImageDraw.ImageDraw, x: int, y: int, t: float) -> None:
    draw.rounded_rectangle([x, y, x + 340, y + 240], radius=12, fill=(18, 28, 22), outline=(60, 100, 70), width=2)
    draw.text((x + 16, y + 12), "IoT Dashboard", font=font(16, True), fill=GREEN)
    draw.text((x + 16, y + 34), "Live silo · Musanze Node 01", font=font(11), fill=(150, 180, 155))
    # mini chart
    pts = []
    for i in range(24):
        px = x + 20 + i * 12
        py = y + 120 - int(28 * math.sin(i * 0.35 + t * 4) + 18 * math.cos(i * 0.2))
        pts.append((px, py))
    if len(pts) > 1:
        draw.line(pts, fill=GREEN, width=3)
    draw.text((x + 16, y + 150), "Temp trend  ·  Humidity  ·  Ethylene", font=font(11), fill=(140, 170, 150))
    # kpi chips
    kpis = [("22.1°C", "Chamber"), ("78% RH", "Humidity"), ("OK", "Status")]
    for i, (v, l) in enumerate(kpis):
        kx = x + 16 + i * 105
        draw.rounded_rectangle([kx, y + 178, kx + 95, y + 220], radius=8, fill=(28, 48, 34))
        draw.text((kx + 10, y + 184), v, font=font(14, True), fill=ORANGE if i < 2 else GREEN)
        draw.text((kx + 10, y + 202), l, font=font(10), fill=CREAM)


def render_frame(n: int, total: int) -> Image.Image:
    img = Image.new("RGBA", (W, H), (*DARK, 255))
    draw = ImageDraw.Draw(img, "RGBA")
    draw_bg(draw, img)
    progress = n / max(1, total - 1)

    # Timeline (seconds at 24fps): ~52s total
    # 0-3 title, 3-8 problem, 8-16 cooler intro, 16-24 cooling cycle,
    # 24-32 electronics, 32-40 dashboard, 40-46 impact, 46-52 close

    t0 = 0
    t1 = 3 * FPS
    t2 = 8 * FPS
    t3 = 16 * FPS
    t4 = 24 * FPS
    t5 = 32 * FPS
    t6 = 40 * FPS
    t7 = 46 * FPS
    t8 = total

    if n < t1:
        p = scene_progress(n, t0, t1)
        draw_header(draw, "HARVEST HOLD RWANDA", "Eliminating post-harvest loss through IoT & AI")
        title_y = int(lerp(380, 300, p))
        alpha_note = int(255 * p)
        draw.text((W // 2 - 340, title_y), "How the Prototype Works", font=font(42, True), fill=WHITE)
        draw.text((W // 2 - 290, title_y + 60), "Smart Hybrid Charcoal Cooler (SHCCS)", font=font(22), fill=ORANGE)
        draw.text((W // 2 - 200, title_y + 110), "A visual guide before you build", font=font(18), fill=(180, 200, 185))
        draw_footer(draw, "01 / Intro", progress)

    elif n < t2:
        p = scene_progress(n, t1, t2)
        draw_header(draw, "THE PROBLEM", "Why smallholders need off-grid cold chain")
        stats = [
            ("40%", "Horticulture yield loss"),
            ("$140M+", "Lost rural income / year"),
            ("70%", "Farmers off-grid"),
        ]
        for i, (big, label) in enumerate(stats):
            appear = ease(clamp((p - i * 0.15) / 0.4))
            x = 90 + i * 380
            y = int(lerp(420, 280, appear))
            draw.rounded_rectangle([x, y, x + 320, y + 160], radius=16, fill=PANEL)
            draw.text((x + 28, y + 28), big, font=font(48, True), fill=GREEN)
            draw.text((x + 28, y + 100), label, font=font(16), fill=CREAM)
        draw_footer(draw, "02 / Problem", progress)

    elif n < t3:
        p = scene_progress(n, t2, t3)
        draw_header(draw, "THE HARDWARE", "Double-walled crate · charcoal · solar · IoT")
        draw_cooler(
            draw, img,
            cx=int(lerp(-200, 520, p)),
            cy=390,
            scale=1.05,
            wet=0.2,
            fan_angle=n * 0.15,
            cool_flow=0.15,
            show_labels=p > 0.55,
        )
        # side notes
        if p > 0.5:
            notes = [
                "• ~10 cm charcoal wall gap",
                "• Local wood + activated charcoal",
                "• No chemical refrigerants",
                "• Built for village assembly",
            ]
            draw.rounded_rectangle([820, 200, 1220, 420], radius=14, fill=PANEL)
            draw.text((845, 220), "Prototype build notes", font=font(18, True), fill=ORANGE)
            for i, line in enumerate(notes):
                draw.text((845, 265 + i * 32), line, font=font(15), fill=CREAM)
        draw_footer(draw, "03 / Hardware", progress)

    elif n < t4:
        # Cooling cycle animation
        local = (n - t3) / (t4 - t3)
        draw_header(draw, "COOLING CYCLE", "Evaporative cooling drops chamber 10–15°C")
        wet = ease(clamp((local - 0.05) / 0.25))
        pump = 0.1 < local < 0.7
        flow = ease(clamp((local - 0.25) / 0.35))
        draw_cooler(
            draw, img,
            cx=480,
            cy=400,
            scale=1.05,
            wet=wet,
            fan_angle=n * 0.35,
            cool_flow=flow,
            pump_on=pump,
            show_labels=True,
        )
        steps = [
            (0.05, "1. Water wets charcoal bed"),
            (0.25, "2. Fan pulls warm air through wet charcoal"),
            (0.45, "3. Evaporation cools air into chamber"),
            (0.65, "4. Sensors feed ESP32 control loop"),
            (0.80, "5. Data syncs to cloud dashboard"),
        ]
        draw.rounded_rectangle([860, 170, 1235, 520], radius=14, fill=PANEL)
        draw.text((885, 190), "Cycle steps", font=font(18, True), fill=ORANGE)
        for i, (thr, text) in enumerate(steps):
            on = local >= thr
            col = GREEN if on else (80, 100, 85)
            draw.ellipse([885, 240 + i * 48, 901, 256 + i * 48], fill=col)
            draw.text((915, 236 + i * 48), text, font=font(14, True if on else False), fill=CREAM if on else (110, 130, 115))
        draw_footer(draw, "04 / Cooling", progress)

    elif n < t5:
        local = (n - t4) / (t5 - t4)
        draw_header(draw, "ELECTRONICS BRAIN", "ESP32 + sensors + solar power path")
        draw_cooler(
            draw, img,
            cx=340,
            cy=400,
            scale=0.78,
            wet=0.8,
            fan_angle=n * 0.3,
            cool_flow=0.85,
            show_labels=False,
            alert=local > 0.75,
        )
        draw_esp_block(draw, 720, 190, active=local, alert=local > 0.75)
        # power note
        draw.rounded_rectangle([720, 430, 1180, 540], radius=12, fill=PANEL)
        draw.text((745, 448), "Power: Solar → TP4056 → 3.7V LiPo → 5V ESP32", font=font(14, True), fill=ORANGE)
        draw.text((745, 478), "I²C bus: SHT31 + OLED on GPIO21 (SDA) / GPIO22 (SCL)", font=font(13), fill=CREAM)
        draw.text((745, 505), "Alerts: buzzer + red LED when thresholds breach", font=font(13), fill=CREAM)
        draw_footer(draw, "05 / Electronics", progress)

    elif n < t6:
        local = (n - t5) / (t6 - t5)
        draw_header(draw, "DASHBOARD & MARKET VALUE", "Wi-Fi / MQTT → certification + fleet ops")
        draw_cooler(
            draw, img,
            cx=300,
            cy=410,
            scale=0.7,
            wet=0.85,
            fan_angle=n * 0.25,
            cool_flow=0.9,
            show_labels=False,
        )
        # signal dots
        for i in range(5):
            a = ease(clamp(local * 1.5 - i * 0.12))
            x = 480 + i * 55
            y = 300 - abs(i - 2) * 8
            r = int(6 + a * 4)
            overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
            od = ImageDraw.Draw(overlay)
            od.ellipse([x - r, y - r, x + r, y + r], fill=(*GREEN, int(220 * a)))
            img.alpha_composite(overlay)
        draw_dashboard(draw, 860, 180, local)
        bullets = [
            "Live T/H + ethylene ripeness index",
            "SMS / alert when storage is unsafe",
            "Downloadable quality certificates",
            "Multi-silo fleet view for cooperatives",
        ]
        draw.rounded_rectangle([80, 540, 820, 640], radius=12, fill=PANEL)
        for i, b in enumerate(bullets):
            col = CREAM if local > i * 0.18 else (90, 110, 95)
            draw.text((110 + (i % 2) * 360, 555 + (i // 2) * 40), "• " + b, font=font(14), fill=col)
        draw_footer(draw, "06 / Dashboard", progress)

    elif n < t7:
        p = scene_progress(n, t6, t7)
        draw_header(draw, "IMPACT FOR FARMERS", "Cool longer. Prove quality. Earn more.")
        cards = [
            ("3–7 days", "Extra shelf life without grid power"),
            ("10–15°C", "Cooler than ambient air"),
            ("100 FRW", "Per crate / day HaaS fee model"),
            ("Certified", "Logs for premium market access"),
        ]
        for i, (big, small) in enumerate(cards):
            appear = ease(clamp((p - i * 0.12) / 0.35))
            x = 70 + (i % 4) * 300
            y = int(lerp(450, 270, appear))
            draw.rounded_rectangle([x, y, x + 275, y + 200], radius=16, fill=PANEL)
            draw.rectangle([x, y, x + 8, y + 200], fill=ORANGE if i % 2 else GREEN)
            draw.text((x + 28, y + 40), big, font=font(28, True), fill=GREEN)
            # wrap small text
            draw.text((x + 28, y + 110), small[:18], font=font(15), fill=CREAM)
            draw.text((x + 28, y + 132), small[18:].strip(), font=font(15), fill=CREAM)
        draw_footer(draw, "07 / Impact", progress)

    else:
        p = scene_progress(n, t7, t8)
        draw_header(draw, "READY TO BUILD", "Prototype checklist for your first unit")
        checklist = [
            "Cut double-walled crate (~10 cm charcoal gap)",
            "Install water reservoir + drip/wetting path",
            "Mount 5V DC fan for charcoal airflow",
            "Wire ESP32 + SHT31 + OLED (I²C)",
            "Add TP4056 + LiPo + solar charge path",
            "Set alert thresholds → buzzer/LED",
            "Publish MQTT → dashboard charts",
        ]
        draw.rounded_rectangle([120, 160, 1160, 560], radius=18, fill=PANEL)
        for i, item in enumerate(checklist):
            on = p > i * 0.1
            yy = 190 + i * 48
            draw.rounded_rectangle([160, yy, 200, yy + 28], radius=6, outline=GREEN if on else (70, 90, 75), width=2)
            if on:
                draw.text((170, yy + 2), "✓", font=font(16, True), fill=GREEN)
            draw.text((220, yy + 2), item, font=font(18), fill=CREAM if on else (100, 120, 105))
        draw.text((W // 2 - 260, 600), "Securing Rwanda's harvest — one village at a time", font=font(16), fill=ORANGE)
        draw_footer(draw, "08 / Build", progress)

    # flatten
    return img.convert("RGB")


def main() -> None:
    FRAMES.mkdir(parents=True, exist_ok=True)
    for old in FRAMES.glob("*.png"):
        old.unlink()

    duration_s = 52
    total = duration_s * FPS
    print(f"Rendering {total} frames at {W}x{H} @ {FPS}fps …")
    for n in range(total):
        frame = render_frame(n, total)
        frame.save(FRAMES / f"frame_{n:05d}.png")
        if n % 48 == 0:
            print(f"  {n}/{total} ({100 * n / total:.0f}%)")
    print("Done frames.")


if __name__ == "__main__":
    main()
