import streamlit as st
from PIL import Image
from io import BytesIO


st.set_page_config(
    page_title="Steganography",layout="wide"
)
# Convert encoding data into 8-bit binary
# form using ASCII value of characters
def genData(data):
 
        # list of binary codes
        # of given data
        newd = []
 
        for i in data:
            newd.append(format(ord(i), '08b'))
        return newd


# Pixels are modified according to the
# 8-bit binary data and finally returned
def modPix(pix, data):
 
    datalist = genData(data)
    lendata = len(datalist)
    imdata = iter(pix)
 
    for i in range(lendata):
 
        # Extracting 3 pixels at a time
        pix = [value for value in imdata.__next__()[:3] +
                                imdata.__next__()[:3] +
                                imdata.__next__()[:3]]
 
        # Pixel value should be made
        # odd for 1 and even for 0
        for j in range(0, 8):
            if (datalist[i][j] == '0' and pix[j]% 2 != 0):
                pix[j] -= 1
 
            elif (datalist[i][j] == '1' and pix[j] % 2 == 0):
                if(pix[j] != 0):
                    pix[j] -= 1
                else:
                    pix[j] += 1
                # pix[j] -= 1
 
        # Eighth pixel of every set tells
        # whether to stop ot read further.
        # 0 means keep reading; 1 means thec
        # message is over.
        if (i == lendata - 1):
            if (pix[-1] % 2 == 0):
                if(pix[-1] != 0):
                    pix[-1] -= 1
                else:
                    pix[-1] += 1
 
        else:
            if (pix[-1] % 2 != 0):
                pix[-1] -= 1
 
        pix = tuple(pix)
        yield pix[0:3]
        yield pix[3:6]
        yield pix[6:9]
 
def encode_enc(newimg, data):
    w = newimg.size[0]
    (x, y) = (0, 0)
 
    for pixel in modPix(newimg.getdata(), data):
 
        # Putting modified pixels in the new image
        newimg.putpixel((x, y), pixel)
        if (x == w - 1):
            x = 0
            y += 1
        else:
            x += 1

# Decode the data in the image
def decode(image):
 
    data = ''
    imgdata = iter(image.getdata())
 
    while (True):
        pixels = [value for value in imgdata.__next__()[:3] +
                                imgdata.__next__()[:3] +
                                imgdata.__next__()[:3]]
 
        # string of binary data
        binstr = ''
 
        for i in pixels[:8]:
            if (i % 2 == 0):
                binstr += '0'
            else:
                binstr += '1'
 
        data += chr(int(binstr, 2))
        if (pixels[-1] % 2 != 0):
            return data
        

icon1_path = "NCPweb.png"
icon2_path = "aitec.png"
title = "   Data Science Lab"
subheader = "Welcome to Steganography"
col1, emp1,col2,emp2 , col3= st.columns([1,1,2,1,1])
with col1:
    st.image(icon1_path)
with col3:
    st.image(icon2_path)
with col2:
    st.title(title)
    st.header("")
    st.header(subheader)
    
with emp1:
    st.write("")
with emp2:
    st.write("")

# Add content below the header and icons
# Replace this section with your actual page content
st.header("")
def get_image_download_link(img,filename,text):
    buffered = BytesIO()
    img.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    href =  f'<a href="data:file/txt;base64,{img_str}" download="{filename}">{text}</a>'
    return href
col11 ,col3, col22 = st.columns([5,1,5])
with col11:
    st.header("Encode Yout Text in an Image")
    st.header("Please Select an Image (PNG Format)")
    file  = st.file_uploader("Your Image to Encode (PNG)")
    selected = False
    textpresent = False
    if file:
        st.write('You selected `%s`' %(file.name))
        selected = True
    txt = st.text_area("Text to Encode")
    if txt:
        textpresent = True
    text = st.text_input("Encoded File Name", "")
    encode = st.button("Encode")
    if encode and selected and textpresent:
        image = Image.open(file)
        st.subheader("Original Image")
        st.image(image)
        newimg = image.copy()
        encode_enc(newimg, txt)
        buf = BytesIO()
        newimg.save(buf, format=image.format)
        byte_im = buf.getvalue()
        st.subheader("Encoded Imgae")
        st.image(newimg)
        filename = file.name
        if text and text != filename:
            filename = text
        st.download_button(label="Download image",data=byte_im, file_name=filename, mime="image")
with col22:
    st.header("Decode Your Text From the Image")
    st.header("Please Select an Image to Decode")
    fileDecode  = st.file_uploader("Your Image to Decode (PNG Format)")
    selected = False
    if fileDecode:
        st.write('You selected `%s`' %(fileDecode.name))
        selected = True
    decodeButton = st.button("Decode")
    if selected and decodeButton:
        image = Image.open(fileDecode , 'r')
        decodedMessage = decode(image=image)
        st.header("Your Decoded Message")
        if decodedMessage:
            st.write(decodedMessage)
        st.subheader("Your Imgae")
        st.image(image)
with col3:
    st.write(' ')


