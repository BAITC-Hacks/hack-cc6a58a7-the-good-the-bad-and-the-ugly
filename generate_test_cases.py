"""Generate extra images for checking the red-area threshold."""

from pathlib import Path

from PIL import Image, ImageDraw


ROOT = Path(__file__).resolve().parent
OUTPUT_DIR = ROOT / "images" / "test_cases"
SIZE = (400, 400)


def save_case(name: str, draw_callback) -> None:
    image = Image.new("RGB", SIZE, (40, 150, 95))
    draw_callback(ImageDraw.Draw(image))
    image.save(OUTPUT_DIR / f"{name}.png")


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    save_case("01_no_red", lambda draw: draw.rectangle((30, 30, 370, 370), fill=(35, 95, 180)))

    def fifteen_percent(draw: ImageDraw.ImageDraw) -> None:
        draw.rectangle((0, 0, 59, 399), fill=(220, 35, 45))

    save_case("02_fifteen_percent_red", fifteen_percent)

    def twenty_percent(draw: ImageDraw.ImageDraw) -> None:
        draw.rectangle((0, 0, 79, 399), fill=(220, 35, 45))

    save_case("03_exactly_twenty_percent_red", twenty_percent)

    def twenty_five_percent(draw: ImageDraw.ImageDraw) -> None:
        draw.rectangle((0, 0, 99, 399), fill=(220, 35, 45))

    save_case("04_twenty_five_percent_red", twenty_five_percent)

    def mostly_red(draw: ImageDraw.ImageDraw) -> None:
        draw.rectangle((25, 25, 375, 375), fill=(220, 35, 45))

    save_case("05_mostly_red", mostly_red)
    print(f"Created test images in {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
