import streamlit as st
from PIL import Image
import io
import os


def resize_image(image, max_size=600):
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

    if uploaded_file is not None:
        original_image = Image.open(uploaded_file)
        st.image(original_image, caption="Original Image", use_column_width=True)

        original_size = uploaded_file.size / 1024  # Convert to KB
        st.write(f"Original file size: {original_size:.2f} KB")

        if st.button("Resize Image"):
            resized_image = resize_image(original_image)

            st.image(resized_image, caption="Resized Image", use_column_width=True)

            new_size = get_file_size(resized_image)
            st.write(f"Resized file size: {new_size:.2f} KB")

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