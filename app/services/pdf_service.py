import os
import uuid
import pikepdf
from fastapi import UploadFile
from PIL import Image
import io

UPLOAD_DIR = "tmp"
os.makedirs(UPLOAD_DIR, exist_ok=True)

async def compress_pdf(file: UploadFile):

    input_path = os.path.join(UPLOAD_DIR, f"{uuid.uuid4()}.pdf")
    output_path = os.path.join(UPLOAD_DIR, f"compressed_{uuid.uuid4()}.pdf")

    # Save uploaded file
    with open(input_path, "wb") as f:
        content = await file.read()
        f.write(content)

    with pikepdf.open(input_path) as pdf:

        for page in pdf.pages:
            for image_name, raw_image in page.images.items():

                try:
                    image_obj = raw_image.get_object()
                    image_data = image_obj.read_bytes()

                    img = Image.open(io.BytesIO(image_data))

                    # Convert to JPEG (strong compression)
                    img = img.convert("RGB")

                    compressed_io = io.BytesIO()
                    img.save(
                        compressed_io,
                        format="JPEG",
                        quality=40,  # 🔥 Change this (20–60)
                        optimize=True
                    )

                    image_obj.write(compressed_io.getvalue())

                except Exception:
                    continue

        pdf.save(output_path)

    return output_path