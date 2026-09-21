"""Create the two sample images used in the README and demo commands."""

from pathlib import Path

from PIL import Image, ImageDraw


ROOT = Path(__file__).resolve().parent
IMAGES_DIR = ROOT / "images"
SIZE = (512, 512)


def main() -> None:
    IMAGES_DIR.mkdir(exist_ok=True)

    ok = Image.new("RGB", SIZE, (42, 150, 95))
    ok_draw = ImageDraw.Draw(ok)
    ok_draw.rectangle((64, 64, 448, 448), fill=(53, 168, 112), outline=(220, 250, 230), width=8)
    ok.save(IMAGES_DIR / "ok.png")

    defect = Image.new("RGB", SIZE, (242, 242, 242))
    defect_draw = ImageDraw.Draw(defect)
    defect_draw.rectangle((48, 48, 464, 464), fill=(220, 35, 45), outline=(130, 15, 25), width=8)
    defect.save(IMAGES_DIR / "defect.png")

    print(f"Created {IMAGES_DIR / 'ok.png'}")
    print(f"Created {IMAGES_DIR / 'defect.png'}")


if __name__ == "__main__":
    main()
