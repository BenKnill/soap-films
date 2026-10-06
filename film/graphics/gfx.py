"""Drawing helpers for the film's 2D shots and overlays: fonts with a glyph fallback, 2x supersampled canvases,
the dark chart palette (dataviz reference palette, dark steps, validated on #0d0d0c), easing."""
import math, os
from PIL import Image, ImageDraw, ImageFont

W, H, SS = 1920, 1080, 2
BG = (13, 13, 12)
INK, INK2, MUTED, GRID = (255, 255, 255), (195, 194, 183), (128, 127, 120), (44, 44, 41)
BLUE, ORANGE, AQUA = (57, 135, 229), (217, 89, 38), (25, 158, 112)      # categorical slots 1-3 (dark)
GOLD = (236, 196, 96)                                                     # highlight ink for proved/claims
FONT_DIRS = ["/usr/share/fonts/truetype/ubuntu", "/System/Library/Fonts"]
UB = {"L": "Ubuntu-L.ttf", "R": "Ubuntu-R.ttf", "M": "Ubuntu-M.ttf", "B": "Ubuntu-B.ttf", "MONO": "UbuntuMono-R.ttf"}
FALLBACK = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def _path(name):
    for d in FONT_DIRS:
        p = os.path.join(d, name)
        if os.path.exists(p): return p
    return FALLBACK


class Face:
    """a font at supersampled size (ss), with DejaVu for glyphs the main font lacks; draws by baseline"""
    def __init__(self, weight, size, ss=None):
        self.ss = SS if ss is None else ss
        self.size = size * self.ss
        self.f = ImageFont.truetype(_path(UB[weight]), self.size)
        self.fb = ImageFont.truetype(FALLBACK, self.size) if os.path.exists(FALLBACK) else None
        self.notdef = self.f.getmask("￿").getbbox(); self.has = {}
        self.ascent = self.f.getmetrics()[0]

    def _font(self, c):
        if self.fb is None or c.isspace(): return self.f
        if c not in self.has: self.has[c] = self.f.getmask(c).getbbox() != self.notdef or c in "0123456789"
        return self.f if self.has[c] else self.fb

    def runs(self, text):
        out = []
        for c in text:
            f = self._font(c)
            if out and out[-1][0] is f: out[-1][1] += c
            else: out.append([f, c])
        return out

    def length(self, text): return sum(f.getlength(t) for f, t in self.runs(text)) / self.ss

    def draw(self, d, xy, text, fill, anchor="l"):
        """xy in output pixels; anchor l/c/r horizontally; y is the baseline"""
        w = self.length(text)
        x = xy[0] - (w / 2 if anchor == "c" else w if anchor == "r" else 0)
        X, Y = x * self.ss, xy[1] * self.ss
        for f, t in self.runs(text):
            d.text((X, Y), t, font=f, fill=fill, anchor="ls"); X += f.getlength(t)
        return w


_faces = {}


def face(weight, size, ss=None):
    k = (weight, size, ss)
    if k not in _faces: _faces[k] = Face(weight, size, ss)
    return _faces[k]


def canvas(bg=BG):
    im = Image.new("RGB", (W * SS, H * SS), bg)
    return im, ImageDraw.Draw(im)


def finish(im):
    return im.resize((W, H), Image.LANCZOS)


def S(v): return v * SS


def line(d, pts, fill, width=2):
    d.line([(S(x), S(y)) for x, y in pts], fill=fill, width=int(width * SS), joint="curve")


def dot(d, x, y, r, fill, ring=None):
    if ring: d.ellipse([S(x - r - 2), S(y - r - 2), S(x + r + 2), S(y + r + 2)], fill=ring)
    d.ellipse([S(x - r), S(y - r), S(x + r), S(y + r)], fill=fill)


def rrect(d, box, r, fill=None, outline=None, width=1):
    d.rounded_rectangle([S(box[0]), S(box[1]), S(box[2]), S(box[3])], radius=S(r), fill=fill, outline=outline, width=int(width * SS))


def mix(c, bg, a):
    a = max(0.0, min(1.0, a)); return tuple(int(round(bg[i] + (c[i] - bg[i]) * a)) for i in range(3))


def ease(t):
    t = max(0.0, min(1.0, t)); return t * t * (3 - 2 * t)


def ramp(t, t0, dur=0.6):
    """0 before t0, eased to 1 over dur seconds"""
    return ease((t - t0) / dur) if dur > 0 else float(t >= t0)


def badge(d, x, y, text, color, size=22, anchor="l"):
    """a small outlined tag; returns its width"""
    fc = face("M", size); w = fc.length(text) + 22; h = size + 14
    x0 = x - (w if anchor == "r" else w / 2 if anchor == "c" else 0)
    rrect(d, (x0, y - h + 8, x0 + w, y + 8), 6, outline=color, width=2)
    fc.draw(d, (x0 + 11, y), text, color)
    return w
