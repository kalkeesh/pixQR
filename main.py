import streamlit as st
import qrcode
from io import BytesIO
import base64
from PIL import Image
from streamlit_lottie import st_lottie
import json

if st.button("@", key="info_button"):
    with st.expander("info"):
        st.write("""
Create a QR CODE of your own...!!
- Enter the required text or link and
    - Click on "Generate QR" to get a basic QR code.
    - Select a 4:4 image to be used as a background for the QR code, then click on "Generate QR".
    - Click on "PNG QR" to get a PNG form of the QR code.
- Hope this was helpful..!
        """)



def load_lottiefile(filepath: str):
    with open(filepath, "r") as f:
        return json.load(f)
lottie_download = load_lottiefile("ldr.json")

def generate_qr_code(payload: str, size: int, color: str, background_img: Image = None):
    try:
        QRcode = qrcode.QRCode(
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=int(size / 20),
            border=1,
        )
        QRcode.add_data(payload)
        QRcode.make()
        
        if background_img:
            bg_width, bg_height = background_img.size
            if bg_width != bg_height:
                min_size = min(bg_width, bg_height)
                background_img = background_img.resize((min_size, min_size))
            QRimg = QRcode.make_image(fill_color=color, back_color="transparent").convert('RGBA')
            qr_img = QRimg.resize(background_img.size, Image.LANCZOS)            
            final_img = Image.alpha_composite(background_img.convert('RGBA'), qr_img)
        else:
            QRimg = QRcode.make_image(fill_color=color, back_color="white").convert('RGBA')
            final_img = QRimg
        return final_img
    except Exception as e:
        st.error(f"Error generating QR code: {e}")
        return None



# st.title("QR Code Generator")
st.image("title.png", use_column_width=True)
st_lottie(lottie_download, height=300, key="continue_animation")

qr_payload = st.text_input("Enter the text for the QR code:")
size = st.slider("Select size of the QR code:", min_value=100, max_value=1024, value=300)
color = st.color_picker("Pick a color for the QR code:", "#000000")
bg_file = st.file_uploader("Upload a background image for the QR code:", type=["png", "jpg", "jpeg"])

def generate_qr_code_transparent(payload: str, size: int, color: str):
    try:
        QRcode = qrcode.QRCode(
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=int(size / 20),
            border=1,
        )
        QRcode.add_data(payload)
        QRcode.make()        
        QRimg = QRcode.make_image(fill_color=color, back_color="transparent").convert('RGBA')
        
        return QRimg
    except Exception as e:
        st.error(f"Error generating QR code: {e}")
        return None

if st.button("Generate QR Code"):
    if qr_payload:
        if bg_file:
            bg_image = Image.open(BytesIO(bg_file.read())).convert('RGBA')
            generated_qr = generate_qr_code(qr_payload, size, color, bg_image)
        else:
            generated_qr = generate_qr_code(qr_payload, size, color)
        
        if generated_qr:
            buf = BytesIO()
            generated_qr.save(buf, format='PNG')
            byte_im = buf.getvalue()

            base64_img = base64.b64encode(byte_im).decode()

            st.markdown(
                f"""
                <div style="display: flex; justify-content: center;">
                    <img src="data:image/png;base64,{base64_img}" alt="Generated QR Code" width=300/>
                </div>
                """,
                unsafe_allow_html=True
            )

            st.download_button(
                label="Download QR Code",
                data=byte_im,
                file_name="qr_code.png",
                mime="image/png"
            )
    else:
        st.error("Please enter a payload for the QR code.")
st.text("")
st.text("")
st.text("")
st.text("")
st.text("")
st.text("")
if st.button("Generate png QR"):
    if qr_payload:
        generated_qr_transparent = generate_qr_code_transparent(qr_payload, size, color)
        
        if generated_qr_transparent:
            buf = BytesIO()
            generated_qr_transparent.save(buf, format='PNG')
            byte_im_transparent = buf.getvalue()
            base64_img_transparent = base64.b64encode(byte_im_transparent).decode()
            st.markdown(
                f"""
                <div style="display: flex; justify-content: center;">
                    <img src="data:image/png;base64,{base64_img_transparent}" alt="Generated QR Code" width="{size}"/>
                </div>
                """,
                unsafe_allow_html=True
            )

            st.download_button(
                label="Download QR Code with Transparent Background",
                data=byte_im_transparent,
                file_name="qr_code_transparent.png",
                mime="image/png"
            )
    else:
        st.error("Please enter a text for the QR code.")
st.text("") 
st.text("") 
st.text("") 
st.text("") 
st.text("") 
st.text("") 
if st.button("About Creator🧐", key="about_creator_button"):
    with st.expander("kalkeesh jami"):
        st.image("mypic.jpg", use_column_width=True)
        st.write("""
        Hello! I'm KALKEESH JAMI #AKA Kalki, a passionate developer exploring the world of AI and programming.
        
        - I love building applications that make life easier.
        - I'm good at Python and data analysis.
        - Don't misunderstand me as a nerd; I'm socially adept too! 😄
        - Thank you for checking out my app!
        
        Do check out my [LinkedIn](https://www.linkedin.com/in/kalkeesh-jami-42891b260/) and [GitHub](https://github.com/kalkeesh/).
        """)
