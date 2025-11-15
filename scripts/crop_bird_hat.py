import argparse
from pathlib import Path
from typing import Tuple

from PIL import Image, ImageChops, ImageFilter
import colorsys


def find_bird_hat_bbox(
	img: Image.Image,
	white_threshold: int = 245,
	left_roi_factor: float = 0.32,
) -> Tuple[int, int, int, int]:
	"""
	Find a bounding box around the bird + hat icon on the left.
	Heuristic:
	- Most of the canvas is white; the icon is the primary non-white blob
	  in the left ~30-35% of the image width.
	- We create a mask of non-white pixels and compute its bbox within a left ROI.
	"""
	# Normalize to RGB
	rgb = img.convert("RGB")
	w, h = rgb.size

	# Build a "non-white" mask
	# Any channel below white_threshold is considered non-white
	r, g, b = rgb.split()
	# Point maps: channel < threshold -> 255 (non-white), else 0
	rm = r.point(lambda p: 255 if p < white_threshold else 0)
	gm = g.point(lambda p: 255 if p < white_threshold else 0)
	bm = b.point(lambda p: 255 if p < white_threshold else 0)
	nonwhite = ImageChops.lighter(ImageChops.lighter(rm, gm), bm)

	# Restrict to left ROI to avoid catching the wordmark
	left_roi = (0, 0, int(w * left_roi_factor), h)
	roi_img = nonwhite.crop(left_roi)
	bbox = roi_img.getbbox()
	if bbox is None:
		# Fallback: expand ROI slightly
		left_roi = (0, 0, int(w * min(0.40, max(left_roi_factor + 0.08, 0.36))), h)
		roi_img = nonwhite.crop(left_roi)
		bbox = roi_img.getbbox()
		if bbox is None:
			raise RuntimeError("Could not find non-white content for bird/hat within the left ROI.")

	# Translate bbox to full image coords
	x0, y0, x1, y1 = bbox
	x0 += left_roi[0]
	y0 += left_roi[1]
	x1 += left_roi[0]
	y1 += left_roi[1]

	# Add a small padding
	pad_x = max(4, (x1 - x0) // 20)
	pad_y = max(4, (y1 - y0) // 20)
	x0 = max(0, x0 - pad_x)
	y0 = max(0, y0 - pad_y)
	x1 = min(w, x1 + pad_x)
	y1 = min(h, y1 + pad_y)

	return (x0, y0, x1, y1)


def crop_bird_hat(input_path: Path, output_path: Path) -> None:
	img = Image.open(input_path).convert("RGBA")
	bbox = find_bird_hat_bbox(img)
	cropped = img.crop(bbox)

	# Make background transparent by flood-filling near-white from edges
	cropped = make_bg_transparent(cropped)

	# Recolor hat (dark neutral pixels) to bird brand blue
	cropped = recolor_hat_to_bird_blue(cropped)

	output_path.parent.mkdir(parents=True, exist_ok=True)
	cropped.save(output_path)
	print(f"Cropped bird+hat saved to: {output_path}")


def make_bg_transparent(img: Image.Image, white_threshold: int = 245) -> Image.Image:
	"""
	Set near-white pixels transparent so the icon works on any background.
	- Build a near-white mask
	- Convert those pixels to transparent
	- Feather edges slightly for smoother results
	"""
	rgb = img.convert("RGB")
	r, g, b = rgb.split()
	rm = r.point(lambda p: 255 if p >= white_threshold else 0)
	gm = g.point(lambda p: 255 if p >= white_threshold else 0)
	bm = b.point(lambda p: 255 if p >= white_threshold else 0)
	white_mask = ImageChops.multiply(ImageChops.multiply(rm, gm), bm)  # 255 where near-white

	# Alpha: transparent where near-white, opaque elsewhere
	alpha = white_mask.point(lambda p: 0 if p == 255 else 255).convert("L")

	# Feather edges slightly
	alpha = alpha.filter(ImageFilter.GaussianBlur(radius=0.6))

	# Combine with original
	result = img.copy()
	result.putalpha(alpha)
	return result


def recolor_hat_to_bird_blue(
	img: Image.Image,
	target_rgb: Tuple[int, int, int] = (7, 82, 153),
	brightness_thresh: int = 160,
	saturation_thresh: int = 40,
) -> Image.Image:
	"""
	Recolor hat to brand blue using HSV to catch all dark, low-saturation pixels.
	- S (saturation) below saturation_thresh considered neutral/gray/black.
	- V (brightness) below brightness_thresh considered dark.
	- Preserves alpha. Skips already-blue pixels.
	"""
	if img.mode != "RGBA":
		img = img.convert("RGBA")

	pixels = img.load()
	w, h = img.size

	tr, tg, tb = target_rgb

	for y in range(h):
		for x in range(w):
			r, g, b, a = pixels[x, y]
			if a == 0:
				continue

			# Skip pixels that are already blue-ish (to avoid recoloring the bird).
			# Blue-ish: b is dominant and saturation is moderate.
			max_ch = max(r, g, b)
			if b == max_ch and b > 100 and b > r + 20 and b > g + 20:
				continue

			# Convert to HSV (0..1)
			hh, ss, vv = colorsys.rgb_to_hsv(r / 255.0, g / 255.0, b / 255.0)
			S = int(ss * 255)
			V = int(vv * 255)

			if S <= saturation_thresh and V <= brightness_thresh:
				pixels[x, y] = (tr, tg, tb, a)

	return img

def main():
	parser = argparse.ArgumentParser(description="Crop the bird+hat icon from TalentNest.png")
	parser.add_argument("input", type=Path, help="Path to input PNG (e.g., images/TalentNest.png)")
	parser.add_argument("--output", type=Path, default=None, help="Output path (e.g., frontend/public/logo-bird.png)")
	args = parser.parse_args()

	input_path: Path = args.input
	default_out = input_path.parent.parent / "frontend" / "public" / "logo-bird.png"
	output_path: Path = args.output or default_out

	crop_bird_hat(input_path, output_path)


if __name__ == "__main__":
	main()

