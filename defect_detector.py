#!/usr/bin/env python3
"""Classify an image as OK or DEFECT using a simple red-pixel rule."""

from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass
from pathlib import Path

from PIL import Image, UnidentifiedImageError


@dataclass(frozen=True)
class DetectorConfig:
    """Thresholds for the rule-based detector."""

    red_min: int = 120
    dominance: float = 1.20
    defect_ratio: float = 0.20


DEFAULT_CONFIG = DetectorConfig()


def red_pixel_ratio(image: Image.Image, config: DetectorConfig = DEFAULT_CONFIG) -> float:
    """Return the share of pixels that are clearly red.

    A pixel is considered red when its red channel is bright enough and is
    stronger than both the green and blue channels by the configured margin.
    The image is converted to RGB, so PNG alpha channels are supported too.
    """

    rgb_image = image.convert("RGB")
    # Pillow 12 renamed getdata() to get_flattened_data(). Keep a fallback so
    # the project also works with the older versions allowed by requirements.
    get_flattened_data = getattr(rgb_image, "get_flattened_data", None)
    pixels = get_flattened_data() if get_flattened_data else rgb_image.getdata()
    total_pixels = rgb_image.width * rgb_image.height

    if total_pixels == 0:
        return 0.0

    red_pixels = sum(
        1
        for red, green, blue in pixels
        if red >= config.red_min
        and red > green * config.dominance
        and red > blue * config.dominance
    )
    return red_pixels / total_pixels


def classify_image(path: str | Path, config: DetectorConfig = DEFAULT_CONFIG) -> str:
    """Classify an image path and return exactly ``OK`` or ``DEFECT``."""

    with Image.open(path) as image:
        ratio = red_pixel_ratio(image, config)

    return "DEFECT" if ratio >= config.defect_ratio else "OK"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Print OK when an image has no significant red area; otherwise print DEFECT."
    )
    parser.add_argument("image", type=Path, help="Path to an image file")
    parser.add_argument(
        "--red-min",
        type=int,
        default=DEFAULT_CONFIG.red_min,
        help=f"Minimum red channel value (default: {DEFAULT_CONFIG.red_min})",
    )
    parser.add_argument(
        "--dominance",
        type=float,
        default=DEFAULT_CONFIG.dominance,
        help=f"How much red must dominate green and blue (default: {DEFAULT_CONFIG.dominance})",
    )
    parser.add_argument(
        "--defect-ratio",
        type=float,
        default=DEFAULT_CONFIG.defect_ratio,
        help=f"Red-pixel share that triggers DEFECT (default: {DEFAULT_CONFIG.defect_ratio})",
    )
    parser.add_argument(
        "--show-ratio",
        action="store_true",
        help="Also print the calculated red-pixel share",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)

    if not 0 <= args.red_min <= 255:
        print("error: --red-min must be between 0 and 255", file=sys.stderr)
        return 2
    if args.dominance <= 0:
        print("error: --dominance must be greater than 0", file=sys.stderr)
        return 2
    if not 0 <= args.defect_ratio <= 1:
        print("error: --defect-ratio must be between 0 and 1", file=sys.stderr)
        return 2

    config = DetectorConfig(
        red_min=args.red_min,
        dominance=args.dominance,
        defect_ratio=args.defect_ratio,
    )

    try:
        with Image.open(args.image) as image:
            ratio = red_pixel_ratio(image, config)
            result = "DEFECT" if ratio >= config.defect_ratio else "OK"
    except FileNotFoundError:
        print(f"error: file not found: {args.image}", file=sys.stderr)
        return 1
    except UnidentifiedImageError:
        print(f"error: unsupported or corrupted image: {args.image}", file=sys.stderr)
        return 1
    except OSError as error:
        print(f"error: cannot read image: {error}", file=sys.stderr)
        return 1

    if args.show_ratio:
        print(f"{result} (red_ratio={ratio:.3f})")
    else:
        print(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
