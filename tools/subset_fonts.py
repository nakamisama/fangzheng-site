"""按页面实际用字裁剪中文字体子集。

用法：python tools/subset_fonts.py
输入：assets/fonts/raw-*.woff2（缺失时自动从 unpkg 下载）
输出：assets/fonts/nssc-*.woff2
新增文案后需重跑本脚本，否则新字会回退到系统字体。
"""
from __future__ import annotations

import pathlib
import sys
import urllib.error
import urllib.request

from fontTools import subset
from fontTools.ttLib import TTFont

ROOT = pathlib.Path(__file__).resolve().parent.parent
FONT_DIR = ROOT / "assets" / "fonts"
WEIGHTS = (300, 400, 600, 700)
RAW_URL = (
    "https://unpkg.com/@fontsource/noto-serif-sc@5.0.0/files/"
    "noto-serif-sc-chinese-simplified-{weight}-normal.woff2"
)

# 站点自身文案 + 常见标点数字英文
BASE_CHARS = (
    "方正贤良工作室方寸之间亦有江湖"
    "xyzwq"
)
ASCII = "".join(chr(c) for c in range(0x20, 0x7F))
EXTRA = "　、。，．·“”‘’（）《》〈〉—…·！？：；【】「」『』￥·•–×°"


def collect_text() -> str:
    """收集所有需要嵌入的字符。"""
    chars = set(ASCII) | set(EXTRA) | set(BASE_CHARS)
    # 从 HTML / CSS / JS 中提取文本，避免手工维护字表
    for pattern in ("*.html", "assets/**/*.css", "assets/**/*.js"):
        for path in ROOT.glob(pattern):
            text = path.read_text(encoding="utf-8")
            chars.update(text)
    # 去掉控制字符
    chars = {c for c in chars if c.isprintable() or c in "\u3000"}
    return "".join(sorted(chars))


def ensure_raw(weight: int) -> pathlib.Path:
    """原始字体缺失时自动下载，下载后不入库（见 .gitignore）。"""
    src = FONT_DIR / f"raw-{weight}.woff2"
    if src.exists():
        return src
    url = RAW_URL.format(weight=weight)
    print(f"下载 {url}")
    try:
        with urllib.request.urlopen(url, timeout=120) as resp:
            src.write_bytes(resp.read())
    except (urllib.error.URLError, TimeoutError) as exc:
        raise SystemExit(f"下载失败：{exc}\n可手动下载后放到 {src}") from exc
    return src


def main() -> int:
    text = collect_text()
    print(f"收集到 {len(text)} 个字符")
    for weight in WEIGHTS:
        src = ensure_raw(weight)
        dst = FONT_DIR / f"nssc-{weight}.woff2"
        opts = subset.Options()
        opts.flavor = "woff2"
        opts.layout_features = ["*"]
        opts.name_IDs = ["*"]
        opts.notdef_outline = True
        opts.hinting = False
        opts.desubroutinize = True
        font = TTFont(src)
        sub = subset.Subsetter(options=opts)
        sub.populate(text=text)
        sub.subset(font)
        font.flavor = "woff2"
        font.save(dst)
        src_kb = src.stat().st_size / 1024
        dst_kb = dst.stat().st_size / 1024
        print(f"{weight}: {src_kb:.0f}KB -> {dst_kb:.0f}KB")
    return 0


if __name__ == "__main__":
    sys.exit(main())
