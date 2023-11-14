import streamlit as st
import requests

def main():
    st.title("ALzheimers Detection Model")

    input_dict = {
        "visit": "",
        "mr_delay": "",
        "m_f": "",
        "hand": "",
        "age": "",
        "educ": "",
        "ses": "",
        "mmse": "",
        "cdr": "",
        "etiv": "",
        "nwbv": "",
        "asf": ""
    }

    for key, value in input_dict.items():
        #visit = st.number_input("Visit")
        #input_dict[key] = st.number_input(f"{key}")

        if key not in st.session_state:
           st.session_state[key] = 0.00
        input_dict[key] = st.number_input(f"{key}", value=st.session_state[key],
                                          min_value=0.00, max_value=10000.00)


    if st.button("Submit"):
        print(input_dict)

        response_table = table_data_request(input_dict)

        print(response_table["response"])

        if response_table["response"] in ["Positive-Demented", "Converted"]:
            
            #st.write(f'{response_table["response"]}')

            """mri_image_placeholder = st.empty()
            mri_image = mri_image_placeholder.file_uploader("Upload an image")


    
            if mri_image is not None:
                st.image(mri_image, caption='Uploaded Image', use_column_width=True)"""

            if 'clicked' not in st.session_state:
                st.session_state.clicked = False

            def set_clicked():
                st.session_state.clicked = True

            st.button('Upload File', on_click=set_clicked)
            if st.session_state.clicked:
                uploaded_file = st.file_uploader("Choose a file")
                print(uploaded_file)
                if uploaded_file is not None:
                    # print(uploaded_file)
                    st.write("You selected the file:", uploaded_file.name)


        elif response_table["response"] == "Non-Demented":
            pass
            #res = mri_image()

            """if st.button("Upload"):
                
                cached_image = load_image(mri_image)
                st.image(cached_image, caption="MRI Image")
                print(mri_image)"""
        else:
            print("Invalid")



def table_data_request(data):
    url = "http://localhost:5005/values/"

    response = requests.post(url, json=data)

    if response.status_code == 200:
        return response.json()
    return None


def mri_image():
    st.header('MRI Image')

    holder = st.empty()
    mri_image = holder.file_uploader("Choose Image", type=["jpeg", "jpg", "png", "webp"])
    if mri_image is not None:
        st.image(load_image(mri_image), width=200)
        print("Image Exists")
        holder.empty()

    return None

def mri_data_request(data):
    url = "http://localhost:5005/image/"

    response = requests.post(url, file=data)

    if response.status_code == 200:
        return response.json()
    return None

@st.cache
def load_image(uploaded_file):
    return uploaded_file


if __name__ == "__main__":
    main()