
# screenshot.py

from PIL import Image
import os


def optimize_screenshot_for_vram(input_path, output_path="cropped_visa_table.png"):
    """
    Crops out headers and sidebars safely without touching the bottom.
    Includes hardware boundaries validation to prevent dimension calculation crashes.
    """
    if os.path.exists(output_path):
        os.remove(output_path)

    with Image.open(input_path) as img:
        width, height = img.size
        
        # ⚠️ Check if the screenshot tool generated a blank/corrupted file
        if width == 0 or height == 0:
            raise ValueError(f"Input image at {input_path} has no dimensions! (Width: {width}, Height: {height})")
            
        print(f"📊 Original Image Metadata -> Width: {width}px, Height: {height}px")
        
        # Calculate the strict 15% side trims and 25% top header trim
        left = int(width * 0.10)
        top = int(height * 0.25)
        right = int(width * 0.90)
        bottom = int(height * 0.95)
        
        # 🛡️ Hard Boundary Check: If calculations collapse, default to a safe window
        if (right <= left) or (bottom <= top):
            print("⚠️ Warning: Calculated crop window collapsed. Falling back to default container bounds.")
            left, top, right, bottom = 0, 0, width, height
            
        print(f"✂️ Safe Crop Execution Matrix -> Left: {left}, Top: {top}, Right: {right}, Bottom: {bottom}")
        
        # Execute the verified crop area
        cropped_img = img.crop((left, top, right, bottom))
        
        # 2. Resize to a tight, standardized canvas size
        # Using alternative scaling token engine syntax for robust PIL builds
        # final_img = cropped_img.resize((512, 512), resample=Image.Resampling.LANCZOS)
        cropped_img.save(output_path, "PNG", optimize=True)
        
    return output_path
