import streamlit as st
from PIL import Image
from utils import mri_data_request

recommendation_dict = { "NonDemented": ["Live Brain Healthy Lifestyle", 
                "Engage in Mentally stimulating activities",
                "Continue regular health checkups",
                "Stay Socially active"],
      
      "MildDemented": ["Medications would be prescribed", 
                "Therapy could be carried out",
                "Caregiver would be required for patient"],
    "ModerateDemented": ["Medications would be prescribed", 
                "Home Care Services would be required for effective treatment",
                "Supportive environment would be required"],
    "VeryMildDemented": ["Some medications would be prescribed",
                "Engage in cognitive training and rehabilitation programs",
                "Implement safety measures at home to reduce accidents",
                "Join support groups"],
    
    "Not a Valid MRI Image": ["Please provide a valid MRI Image"]}


st.title('MRI Image Data')

st.markdown("## Please Provide Patient's MRI Image")

uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    # Display the uploaded image
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Image', use_column_width=True)

    if st.button("submit"):
        
        #convert image to bytes-like object that API requires
        image_bytes = uploaded_file.getvalue()
        response_mri = mri_data_request(image_bytes)

        #check if response mri is None
        if response_mri:
        
            if response_mri["message"]:
                st.markdown(f"## {response_mri['message']}")
    
                for i in recommendation_dict[response_mri['message']]:
                    st.write(f"- {i}")
            else:
                st.markdown(f"## Not Available. Please try again later.")
        else:
            st.markdown(f"## Not a Valid MRI Image.")
            st.write(f"- Please provide a valid MRI Image")
            pass
