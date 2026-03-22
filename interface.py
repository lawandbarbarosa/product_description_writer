import streamlit as st
import requests
import os
from dotenv import load_dotenv

load_dotenv()

BACK_END_URL = "https://f23uvrabfm.us-east-1.awsapprunner.com"

st.set_page_config(
    page_title="SIMKO AI, e-commerce product description writer",
    page_icon="✍️",
    layout="wide"
)


st.title("✍️ AI Product Description Generator")
st.markdown("Generate high-converting, SEO-optimized product descriptions for your e-commerce store.")

with st.sidebar:

    st.header("Product Details")

    with st.form("product_form"):
        product_name = st.text_input("Product_name", placeholder="e.g. Apex Frontier Jeans")
        product_category = st.text_input("category", placeholder="e.g. Apparel / Menswear")

        target_audience = st.text_input(
            "Target Audience",
            placeholder="e.g. Urban professionals aged 20-40"
        )

        tone = st.selectbox(
            "Brand tone",
            ["Professional", "Rugged", "Luxury", "Playful", "Urgent", "Informative"],
            index = 0
        )

        features_text = st.text_area(
            "Key Features (one per line)",
            placeholder="14oz Selvedge Denim\nDouble-stitched seams\nSlim fit"
        )

        submit_button = st.form_submit_button("generate description", use_container_width= True)


if submit_button:
    if not product_name or not features_text:
        st.error("Please provide at least a Product Name and some Features.")
    else:

        feature_list = [f.strip() for f in features_text.split("\n") if f.strip()]

        paylodad = {
            "product_name": product_name,
            "product_category": product_category,
            "key_features": feature_list,
            "target_audience": target_audience,
            "tone": tone
        }

        with st.status('🤖 Agent is working...', expanded=True) as status:
            try:
                st.write("Sending data to research node...")
                response = requests.post(f"{BACK_END_URL}/generate", json=paylodad)


                if response.status_code == 200:
                    data = response.json()
                    status.update(label ="✅ description generates", state = 'complete', expanded=False)

                    tab1, tab2, tab3 = st.tabs(["✨ Final Copy", "✍️ First Draft", "🔍 Research Notes"])

                    with tab1:
                        st.subheader("ready to publish")
                        st.markdown(data['final_description'])
                        st.button("copy to clipboard", on_click=lambda: st.write("Copied! (Demo only)"))
                    
                    with tab2:
                        st.info("This is the initial draft before the refinement stage.")
                        st.markdown(data['draft_description'])
                    
                    with tab3:
                        st.write("The AI researched these insights to build your copy: ")
                        st.markdown(data['research_notes'])
                else:
                    st.error(f"Error from API {response.text}")
                    status.update(label = '❌ Generation Failed', state = "error")

            except Exception as e:
                st.error(f"Could not connect to the backend: {e}")
                status.update(label = "❌ Connection Error", state = 'error')

else:
    st.info("Fill out the product details in the sidebar to get started.")