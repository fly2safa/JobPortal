import argparse
from pathlib import Path

from PIL import Image, ImageDraw, ImageOps


def find_hat_bbox(img: Image.Image, threshold: int = 60) -> tuple[int, int, int, int]:
	"""
	Locate the hat more robustly:
	1) Threshold dark pixels (near-black).
	2) Restrict search to a top-left ROI where the hat lives.
	3) Seed flood-fill from the topmost dark pixel to capture just the connected hat region.
	"""
	# Convert to grayscale and threshold dark regions
	gray = img.convert("L")
	mask = gray.point(lambda p: 255 if p < threshold else 0).convert("L")

	w, h = img.size
	# Restrict to top-left area to avoid text/body: left 50%, top 55% of the image
	search_box = (0, 0, int(w * 0.5), int(h * 0.55))
	mask_region = mask.crop(search_box)

	# Find topmost white pixel in mask_region
	pixels = mask_region.load()
	rw, rh = mask_region.size
	seed = None
	for y in range(rh):
		for x in range(rw):
			if pixels[x, y] == 255:
				seed = (x, y)
				break
		if seed:
			break

	if seed is None:
		# Fallback: expand ROI slightly
		search_box = (0, 0, int(w * 0.6), int(h * 0.65))
		mask_region = mask.crop(search_box)
		pixels = mask_region.load()
		rw, rh = mask_region.size
		for y in range(rh):
			for x in range(rw):
				if pixels[x, y] == 255:
					seed = (x, y)
					break
			if seed:
				break
		if seed is None:
			raise RuntimeError("Could not locate a dark region likely to be the hat.")

	# Flood-fill the connected component of the hat region
	ImageDraw.floodfill(mask_region, seed, 128, thresh=0)

	# Build a binary image of just the filled region (value 128)
	component = mask_region.point(lambda p: 255 if p == 128 else 0).convert("L")
	bbox = component.getbbox()
	if bbox is None:
		raise RuntimeError("Failed to isolate hat region after flood fill.")

	# Translate bbox back to full-image coordinates
	x0, y0, x1, y1 = bbox
	return (x0 + search_box[0], y0 + search_box[1], x1 + search_box[0], y1 + search_box[1])


def shrink_hat(input_path: Path, output_path: Path, scale: float) -> None:
	img = Image.open(input_path).convert("RGBA")
	w, h = img.size

	# Locate hat
	hat_bbox = find_hat_bbox(img)
	hx0, hy0, hx1, hy1 = hat_bbox

	# Crop hat
	hat = img.crop(hat_bbox)
	hat_w, hat_h = hat.size

	# Compute new size
	new_hat_w = max(1, int(hat_w * scale))
	new_hat_h = max(1, int(hat_h * scale))
	hat_small = hat.resize((new_hat_w, new_hat_h), Image.LANCZOS)

	# Clear original hat area to white (assumes white background)
	draw = ImageDraw.Draw(img)
	draw.rectangle(hat_bbox, fill=(255, 255, 255, 255))

	# Paste the smaller hat centered on original hat center
	center_x = hx0 + hat_w // 2
	center_y = hy0 + hat_h // 2
	new_x0 = int(center_x - new_hat_w // 2)
	new_y0 = int(center_y - new_hat_h // 2)

	img.paste(hat_small, (new_x0, new_y0), hat_small)

	# Save result
	output_path.parent.mkdir(parents=True, exist_ok=True)
	img.save(output_path)
	print(f"Saved: {output_path}")


def main():
	parser = argparse.ArgumentParser(description="Shrink the hat in TalentNest logo PNG.")
	parser.add_argument("input", type=Path, help="Path to input PNG (e.g., images/TalentNest.png)")
	parser.add_argument("--scale", type=float, default=0.85, help="Scale factor for hat (default: 0.85)")
	parser.add_argument("--output", type=Path, default=None, help="Output path (default: <input>.small.png)")
	args = parser.parse_args()

	input_path: Path = args.input
	output_path: Path = args.output or input_path.with_name(input_path.stem + ".small.png")

	shrink_hat(input_path, output_path, scale=args.scale)


if __name__ == "__main__":
	main()

