import streamlit as st
from time import sleep
from utils import table_data_request, nav_page

st.title('Numeric Medical Data')

st.markdown("## Please Enter Patient's Data")


recommendation_dict = { "Non Demented": ["Live Brain Healthy Lifestyle", 
                "Engage in Mentally stimulating activities",
                "Continue regular health checkups",
                "Stay Socially active"]
    }


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

    response_table = table_data_request(input_dict)

    if response_table["response"]:

        if response_table["response"] in ["Positive-Demented", "Converted"]:
            
            st.markdown(f'## Diagnostic Result is Positive')
            sleep(5)
            nav_page("image_data")
            


        elif response_table["response"] == "Non Demented":

            st.markdown(f"# {response_table['response']}")

            for i in recommendation_dict[response_table['response']]:
                st.write(f"- {i}")

            
        else:
            st.markdown(f"## Invalid")

    else:
        st.markdown(f"## Not Available. Please try again later.")
