# -*- coding: utf-8 -*-
# 질감 생성기. 실행: python3 _build/tex.py  → assets/img/ 에 PNG/WebP를 쓴다.
# 찢긴 종이 가장자리(edge), 잉크 튐(ink), 먼지·긁힘(dust). 매번 같은 결과가 나오도록 시드 고정.
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "assets", "img")
os.makedirs(OUT, exist_ok=True)
rng = np.random.default_rng(800)


def fbm1d(n, octaves=7, base=6):
    x = np.zeros(n)
    for o in range(octaves):
        f = base * 2 ** o
        pts = rng.standard_normal(f + 2)
        xs = np.linspace(0, f, n)
        x += np.interp(xs, np.arange(f + 2), pts) / (1.6 ** o)
    return x / np.abs(x).max()


def edge(w=2400, h=140):
    """위쪽이 찢긴 띠. 흰(불투명) 부분이 남는 쪽. 아래로 갈수록 꽉 찬다."""
    prof = fbm1d(w) * 0.5 + 0.5           # 0..1
    line = (h * 0.28 + prof * h * 0.42).astype(int)
    a = np.zeros((h, w), np.uint8)
    yy = np.arange(h)[:, None]
    a[yy >= line[None, :]] = 255
    # 가장자리 근처 잉크 부스러기
    im = Image.fromarray(a)
    d = ImageDraw.Draw(im)
    for _ in range(900):
        x = int(rng.integers(0, w))
        y = int(line[x] - abs(rng.normal(0, h * 0.12)))
        r = abs(rng.normal(0, 1.4)) + 0.4
        d.ellipse([x - r, y - r, x + r, y + r], fill=255)
    for _ in range(500):  # 안쪽 구멍
        x = int(rng.integers(0, w))
        y = int(line[x] + abs(rng.normal(0, h * 0.1)))
        r = abs(rng.normal(0, 1.2)) + 0.3
        d.ellipse([x - r, y - r, x + r, y + r], fill=0)
    im = im.filter(ImageFilter.GaussianBlur(0.6)).point(lambda v: 255 if v > 120 else 0)
    rgba = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    rgba.putalpha(im)
    rgba = Image.merge("RGBA", (im, im, im, im))
    rgba.save(os.path.join(OUT, "edge.png"), optimize=True)


def ink(w=1400, h=900):
    """잉크 튐. 검정 위주, 투명 바탕."""
    # 부드러운 2D 잡음 여러 겹 → 불규칙한 잉크 얼룩
    def noise2d(scale):
        small = rng.random((max(2, h // scale), max(2, w // scale))).astype(np.float32)
        return np.asarray(Image.fromarray((small * 255).astype(np.uint8)).resize((w, h), Image.BICUBIC), np.float32) / 255
    n = noise2d(90) * .5 + noise2d(30) * .3 + noise2d(9) * .2
    yy, xx = np.mgrid[0:h, 0:w]
    field = np.zeros((h, w), np.float32)
    for _ in range(4):  # 얼룩 중심
        cx, cy, R = rng.uniform(.25, .75) * w, rng.uniform(.3, .7) * h, rng.uniform(70, 170)
        field = np.maximum(field, np.exp(-((xx - cx) ** 2 + ((yy - cy) * 1.25) ** 2) / (2 * R * R)))
    a = ((field * .9 + n * .55) > .82).astype(np.uint8) * 255
    im = Image.fromarray(a)
    d = ImageDraw.Draw(im)
    for _ in range(260):  # 튄 방울, 길쭉하게
        x, y = rng.uniform(0, w), rng.uniform(0, h)
        r = abs(rng.normal(0, 2.2)) + .5
        ang = rng.uniform(0, np.pi); L = r * rng.uniform(1, 4)
        d.line([x - np.cos(ang) * L, y - np.sin(ang) * L, x + np.cos(ang) * L, y + np.sin(ang) * L], fill=255, width=max(1, int(r)))
        d.ellipse([x - r, y - r, x + r, y + r], fill=255)
    for _ in range(1400):
        x, y = rng.integers(0, w), rng.integers(0, h)
        r = abs(rng.normal(0, .8)) + .3
        d.ellipse([x - r, y - r, x + r, y + r], fill=255)
    im = im.filter(ImageFilter.GaussianBlur(1.4)).point(lambda v: 255 if v > 100 else 0)
    rgba = Image.merge("RGBA", (Image.new("L", (w, h), 10),) * 3 + (im,))
    rgba.save(os.path.join(OUT, "ink.png"), optimize=True)


def dust(w=1024, h=1024):
    """먼지와 긁힘. 흰색, 투명 바탕. 그림 위에 screen으로 얹는다."""
    im = Image.new("L", (w, h), 0)
    d = ImageDraw.Draw(im)
    for _ in range(700):
        x, y = rng.integers(0, w), rng.integers(0, h)
        r = abs(rng.normal(0, .7)) + .2
        d.ellipse([x - r, y - r, x + r, y + r], fill=int(rng.integers(90, 255)))
    for _ in range(26):  # 머리카락 같은 긁힘
        x, y = rng.uniform(0, w), rng.uniform(0, h)
        ang = rng.uniform(0, np.pi)
        pts = []
        for k in range(int(rng.integers(8, 30))):
            ang += rng.normal(0, .25)
            x += np.cos(ang) * 6; y += np.sin(ang) * 6
            pts.append((x, y))
        d.line(pts, fill=int(rng.integers(70, 180)), width=1)
    for _ in range(5):  # 세로 필름 긁힘
        x = rng.integers(0, w)
        d.line([x, 0, x + rng.integers(-6, 6), h], fill=int(rng.integers(40, 90)), width=1)
    rgba = Image.merge("RGBA", (Image.new("L", (w, h), 255),) * 3 + (im,))
    rgba.save(os.path.join(OUT, "dust.png"), optimize=True)


if __name__ == "__main__":
    edge(); ink(); dust()
    for f in sorted(os.listdir(OUT)):
        print(f, os.path.getsize(os.path.join(OUT, f)) // 1024, "KB")
