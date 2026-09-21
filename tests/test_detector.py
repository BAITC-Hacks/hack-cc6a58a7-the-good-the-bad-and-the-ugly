import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from defect_detector import DetectorConfig, classify_image, red_pixel_ratio  # noqa: E402


class DetectorTests(unittest.TestCase):
    def create_image(self, image: Image.Image, directory: str, name: str) -> Path:
        path = Path(directory) / name
        image.save(path)
        return path

    def test_green_square_is_ok(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = self.create_image(Image.new("RGB", (32, 32), (30, 160, 90)), directory, "ok.png")
            self.assertEqual(classify_image(path), "OK")

    def test_red_square_is_defect(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = self.create_image(Image.new("RGB", (32, 32), (220, 30, 40)), directory, "defect.png")
            self.assertEqual(classify_image(path), "DEFECT")

    def test_small_red_area_is_ok(self) -> None:
        image = Image.new("RGB", (100, 100), (30, 160, 90))
        for x in range(10):
            for y in range(100):
                image.putpixel((x, y), (220, 30, 40))

        with tempfile.TemporaryDirectory() as directory:
            path = self.create_image(image, directory, "small-red-area.png")
            self.assertLess(red_pixel_ratio(image), 0.20)
            self.assertEqual(classify_image(path), "OK")

    def test_custom_ratio_threshold(self) -> None:
        image = Image.new("RGB", (10, 10), (30, 160, 90))
        for x in range(5):
            for y in range(10):
                image.putpixel((x, y), (220, 30, 40))

        with tempfile.TemporaryDirectory() as directory:
            path = self.create_image(image, directory, "half-red.png")
            config = DetectorConfig(defect_ratio=0.60)
            self.assertEqual(classify_image(path, config), "OK")

    def test_cli_prints_only_result_by_default(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = self.create_image(Image.new("RGB", (8, 8), (220, 30, 40)), directory, "defect.png")
            completed = subprocess.run(
                [sys.executable, str(ROOT / "defect_detector.py"), str(path)],
                capture_output=True,
                text=True,
                check=False,
            )

        self.assertEqual(completed.returncode, 0)
        self.assertEqual(completed.stdout.strip(), "DEFECT")
        self.assertEqual(completed.stderr, "")


if __name__ == "__main__":
    unittest.main()
