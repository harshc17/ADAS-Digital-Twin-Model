from pathlib import Path
import math

from PIL import Image, ImageDraw, ImageFont


OUT = Path("docs/images")
OUT.mkdir(parents=True, exist_ok=True)


def font(size, bold=False):
    paths = [
        "C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf",
        "C:/Windows/Fonts/calibrib.ttf" if bold else "C:/Windows/Fonts/calibri.ttf",
    ]
    for path in paths:
        try:
            return ImageFont.truetype(path, size)
        except OSError:
            pass
    return ImageFont.load_default()


def box(draw, xy, title, subtitle, fill="#ffffff", outline="#164e63"):
    draw.rounded_rectangle(xy, radius=18, fill=fill, outline=outline, width=3)
    draw.text((xy[0] + 24, xy[1] + 22), title, font=font(28, True), fill="#0f172a")
    y = xy[1] + 68
    for line in subtitle.split("\n"):
        draw.text((xy[0] + 24, y), line, font=font(21), fill="#334155")
        y += 30


def arrow(draw, start, end, color="#2563eb"):
    draw.line([start, end], fill=color, width=5)
    angle = math.atan2(end[1] - start[1], end[0] - start[0])
    size = 16
    pts = [
        end,
        (end[0] - size * math.cos(angle - 0.45), end[1] - size * math.sin(angle - 0.45)),
        (end[0] - size * math.cos(angle + 0.45), end[1] - size * math.sin(angle + 0.45)),
    ]
    draw.polygon(pts, fill=color)


def architecture():
    img = Image.new("RGB", (1600, 900), "#f8fafc")
    d = ImageDraw.Draw(img)
    d.text((55, 42), "ADAS Digital Twin Model", font=font(52, True), fill="#0f3b63")
    d.text((58, 105), "Speed Limit Detection and Vehicle Speed Control", font=font(28), fill="#475569")
    d.line((55, 155, 1545, 155), fill="#94a3b8", width=3)

    items = [
        ((70, 230, 360, 400), "Road Scene", "Virtual road\nlane markings\nspeed signs"),
        ((440, 230, 730, 400), "Sensor View", "Detection region\ncamera-like input\nsign observation"),
        ((810, 230, 1100, 400), "ML Detector", "Sign confidence\nclass decision\nstable output"),
        ((1180, 230, 1470, 400), "State Logic", "Speed limit to\nreference speed\nmode selection"),
        ((270, 575, 560, 745), "PID Controller", "Speed error\nKp Ki Kd terms\ncontrol output"),
        ((650, 575, 940, 745), "Vehicle Model", "Throttle/brake\ndrag/friction\nactual speed"),
        ((1030, 575, 1320, 745), "Dashboard", "Telemetry\ncharts\nactuator status"),
    ]
    for xy, title, subtitle in items:
        box(d, xy, title, subtitle)

    arrow(d, (360, 315), (440, 315))
    arrow(d, (730, 315), (810, 315))
    arrow(d, (1100, 315), (1180, 315))
    arrow(d, (1325, 400), (810, 575))
    arrow(d, (650, 660), (560, 660), "#dc2626")
    arrow(d, (940, 660), (1030, 660), "#16a34a")
    d.text((70, 820), "Closed-loop behavior: the detected sign updates target speed, and vehicle speed feedback continuously corrects the control output.", font=font(23), fill="#475569")
    img.save(OUT / "adas_architecture.png")


def dashboard():
    img = Image.new("RGB", (1600, 950), "#08111f")
    d = ImageDraw.Draw(img)
    d.rectangle((0, 0, 1600, 95), fill="#111827")
    d.text((40, 28), "ADAS DIGITAL TWIN DASHBOARD", font=font(42, True), fill="#f59e0b")
    d.text((1060, 35), "ONLINE  |  SIMULATION MODE", font=font(24, True), fill="#22c55e")

    d.rounded_rectangle((45, 140, 610, 875), radius=18, fill="#111827", outline="#334155", width=3)
    d.text((75, 170), "Road Scene and Sensor View", font=font(29, True), fill="#e5e7eb")
    d.polygon([(215, 830), (430, 830), (530, 240), (115, 240)], fill="#1f2937", outline="#64748b")
    for y in range(295, 780, 95):
        d.line((322, y, 322, y + 52), fill="#f8fafc", width=6)
    d.rectangle((275, 725, 370, 825), fill="#2563eb", outline="#93c5fd", width=3)
    d.rectangle((135, 335, 510, 645), outline="#22c55e", width=4)
    d.text((150, 655), "Detection Zone", font=font(22), fill="#22c55e")
    d.ellipse((455, 285, 540, 370), fill="#ffffff", outline="#ef4444", width=8)
    d.text((480, 312), "50", font=font(31, True), fill="#111827")

    d.rounded_rectangle((660, 140, 1040, 430), radius=18, fill="#111827", outline="#334155", width=3)
    d.text((690, 170), "Vehicle Telemetry", font=font(29, True), fill="#e5e7eb")
    d.text((730, 235), "47", font=font(88, True), fill="#f8fafc")
    d.text((835, 280), "km/h", font=font(28), fill="#94a3b8")
    d.text((700, 355), "Reference speed: 50 km/h", font=font(23), fill="#38bdf8")
    d.text((700, 388), "Vehicle mode: DRIVE", font=font(23), fill="#22c55e")

    d.rounded_rectangle((1090, 140, 1555, 430), radius=18, fill="#111827", outline="#334155", width=3)
    d.text((1120, 170), "Sign Detection Confidence", font=font(29, True), fill="#e5e7eb")
    for i, (label, pct, color) in enumerate([("30", 35, "#64748b"), ("50", 92, "#22c55e"), ("80", 19, "#64748b")]):
        y = 245 + i * 58
        d.ellipse((1130, y - 18, 1178, y + 30), fill="#ffffff", outline="#ef4444", width=5)
        d.text((1144, y - 6), label, font=font(17, True), fill="#111827")
        d.rectangle((1210, y, 1470, y + 18), fill="#1f2937")
        d.rectangle((1210, y, 1210 + int(260 * pct / 100), y + 18), fill=color)
        d.text((1490, y - 8), f"{pct}%", font=font(22), fill="#e5e7eb")

    d.rounded_rectangle((660, 475, 1040, 875), radius=18, fill="#111827", outline="#334155", width=3)
    d.text((690, 505), "Actuator Output", font=font(29, True), fill="#e5e7eb")
    for label, pct, color, y in [("Throttle", 42, "#22c55e", 600), ("Brake", 0, "#ef4444", 700)]:
        d.text((700, y - 12), label, font=font(24), fill="#e5e7eb")
        d.rectangle((825, y, 990, y + 24), fill="#1f2937")
        d.rectangle((825, y, 825 + int(165 * pct / 100), y + 24), fill=color)
        d.text((700, y + 35), f"{pct}%", font=font(30, True), fill=color)

    d.rounded_rectangle((1090, 475, 1555, 875), radius=18, fill="#111827", outline="#334155", width=3)
    d.text((1120, 505), "Error Response", font=font(29, True), fill="#e5e7eb")
    d.line((1145, 805, 1505, 805), fill="#64748b", width=2)
    d.line((1145, 555, 1145, 805), fill="#64748b", width=2)
    pts = []
    for x in range(0, 350, 8):
        y = 690 + int(80 * math.exp(-x / 120) * math.sin(x / 23))
        pts.append((1145 + x, y))
    d.line(pts, fill="#f59e0b", width=5)
    img.save(OUT / "adas_dashboard.png")


architecture()
dashboard()
print("Generated README images in docs/images")
