import streamlit as st
from PIL import Image
import io
import os


def resize_image(image, max_size):
    """Resize image to have a maximum side length of max_size while maintaining aspect ratio."""
    img = image.copy()
    img.thumbnail((max_size, max_size))
    return img


def get_file_size(img):
    """Get file size of image in KB."""
    buf = io.BytesIO()
    img.save(buf, format='png', quality=85, optimize=True)
    size_kb = buf.tell() / 1024
    return size_kb


def main():
    st.set_page_config(page_title="Image Resizer", page_icon=":material/image:")
    st.header(":red[Image Resizer]", divider='rainbow')

    uploaded_file = st.file_uploader("Choose an image...", type=["png", "jpg", "jpeg"])

    max_size_options = list(range(800, 99, -100))
    max_size = st.selectbox(
        "Select maximum image dimension",
        options=max_size_options,
        index=0,  # Default to 800
        help="The maximum width or height (in pixels) of the resized image. The image will be scaled proportionally so that neither dimension exceeds this value."
    )

    if uploaded_file is not None:
        original_image = Image.open(uploaded_file)
        st.image(original_image, caption="Original Image", use_column_width=True)

        original_size = uploaded_file.size / 1024  # Convert to KB
        st.write(f"Original file size: {original_size:.2f} KB")
        st.write(f"Original dimensions: {original_image.size[0]}x{original_image.size[1]} pixels")

        if st.button("Resize Image"):
            resized_image = resize_image(original_image, max_size)

            st.image(resized_image, caption="Resized Image", use_column_width=True)

            new_size = get_file_size(resized_image)
            st.write(f"Resized file size: {new_size:.2f} KB")
            st.write(f"Resized dimensions: {resized_image.size[0]}x{resized_image.size[1]} pixels")

            # Prepare resized image for download
            buf = io.BytesIO()
            resized_image.save(buf, format='png', quality=85, optimize=True)
            buf.seek(0)

            st.download_button(
                label="Download resized image",
                data=buf,
                file_name=f"{os.path.splitext(uploaded_file.name)[0]}_resized.jpg",
                mime="image/jpeg"
            )


if __name__ == "__main__":
    main()