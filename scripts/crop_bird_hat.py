import argparse
from pathlib import Path
from typing import Tuple

from PIL import Image, ImageChops, ImageFilter


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

