import streamlit as st
import pandas as pd
import plotly.express as px
st.set_page_config(page_title='Training dashboard',
                       page_icon='car',
                        layout='wide',initial_sidebar_state='expanded')


def load_data():
    try:
        st.header('D-SIRE TRAINING JOURNEY   : 🏆')

        st.image("Dsire.jpg")
    #this is for uploading the file 
        upload_option = st.sidebar.selectbox("Upload file : Optional", ["Yes", "No"], index=1)
        fl = None  # Declare fl here

        if upload_option == "Yes":
            fl = st.sidebar.file_uploader("Upload file Optional:")

        if fl is not None:
            # Process the uploaded file
            st.write("File uploaded successfully!")
        else:
            st.write("No file uploaded.")
          
        #st.image("https://raw.githubusercontent.com/imrank4/trainingdashboard/main/Dsire.jpg")
        if fl is not None:  # If file uploaded
            filename = fl.name
            st.write("Uploaded filename:", filename)
            df = pd.read_csv(fl)  # Read uploaded file directly
        else:  # If no file uploaded, load data from a URL
            url = 'https://raw.githubusercontent.com/imrank4/trainingdashboard/main/py.csv'
      
            df = pd.read_csv(url)
      # if fl is not None:
        #     filename = fl.name
        #     st.write(filename)
            
        #     df = pd.read_csv(fl)  # Read uploaded file directly
        # else:
        #     url = 'https://raw.githubusercontent.com/imrank4/trainingdashboard/main/py.csv'

        #     df = pd.read_csv(url)
        
        # Assuming the columns exist in the loaded DataFrame
        df = df.loc[:, ["DEALER ZONE", "DEALER GROUP", "DEALER NAME","DEALER CODE","USER ID",  "FULL NAME", "JOB TITLE", "JOINING DATE", "DSIRE STATUS", "WBT", "ASSESSMENT","R-AGING", "DSIRE TARGET"]]
        
        # You may also use slicing method for this 
        # df = df.iloc[0:20, 2:8]
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None

def search_and_filter_data(df):
    st.markdown('<style>div.block-container{padding-top:2rem;}<style>', unsafe_allow_html=True)
    st.subheader(' Search and Filter Data :mag:')
    with st.sidebar:
        st.header("Choose Filter:")
        zone = st.text_input('Enter Region:')
        dealer_group = st.text_input('Enter Dealer Group: Name')
        #dealer_group = st.multiselect('Enter Dealer group: Name',options=filtered_data['DEALER CODE'].unique())
        dealer_code = st.text_input('Enter Dealer Code:')
        
        
    filtered_data = df.copy()  # Initially, the filtered data is the same as the original data

    # Filter by both dealer code and dealer group
    if dealer_code and dealer_group:
        filtered_data = filtered_data[(filtered_data['DEALER CODE'].str.contains(dealer_code, case=False)) & 
                                      (filtered_data['DEALER GROUP'].str.contains(dealer_group, case=False))]
    # Filter by dealer code only
    elif dealer_code:
        filtered_data = filtered_data[filtered_data['DEALER CODE'].str.contains(dealer_code, case=False)]

    # Filter by dealer group only
    elif dealer_group:
        filtered_data = filtered_data[filtered_data['DEALER GROUP'].str.contains(dealer_group, case=False)]
    
    # Filter by profile only
    elif zone:
        filtered_data = filtered_data[filtered_data['DEALER ZONE'].str.contains(zone, case=False)]

    if dealer_code or dealer_group or zone:  # Display table only if any filter criteria are entered
        st.write(filtered_data)

        # DSIRE GRAPH CREATION
        try:
            # Create bar chart showing the count of training statuses and targets per dealer zone
            training_count_df = filtered_data.groupby(["DEALER CODE", "DSIRE STATUS", "DSIRE TARGET"]).size().reset_index(name="COUNT")

            # Create bar chart showing the count of training statuses per dealer zone
            fig = px.bar(training_count_df, x="DSIRE STATUS", y="COUNT", color="DSIRE TARGET",
                         title="Current Training Status", barmode="group", text="COUNT", facet_row="DEALER CODE", facet_row_spacing=0.5)

            # Add value labels on top of the bars
            fig.update_traces(textposition='auto')

            # Remove x-axis and y-axis labels
            fig.update_layout(xaxis_title="", yaxis_title="")

            # Display the bar chart
            st.subheader("Training Status by Dealer Code")
            st.plotly_chart(fig, use_container_width=True)

        except ValueError as e:
            if "Vertical spacing cannot be greater than" in str(e):
                st.warning("Too many unique values for Dealer code, Please select a different dataset or column.")
            else:
                raise e
    else:
        st.write("Enter filter criteria for data visiblity.")  # Display a message to prompt user for input

def main():
    df = load_data()
    if df is not None:
        search_and_filter_data(df)

if __name__ == "__main__":
    main()

# import streamlit as st
# import pandas as pd
# import plotly.express as px
# import os

# st.set_page_config(page_title='Training dashboard',
#                        page_icon='car',
#                         layout='wide',initial_sidebar_state='expanded')

# def load_data():
#     try:
#         fl = st.file_uploader(":file_folder: Upload mentioned file type: csv, xlsx, xls", type=(["csv", "xls", "xlsx"]))
#         if fl is not None:  # If file uploaded
#             filename = fl.name
#             st.write("Uploaded filename:", filename)
#             df = pd.read_csv(fl)  # Read uploaded file directly
#         else:  # If no file uploaded, load data from a URL
#             url = 'https://raw.githubusercontent.com/imrank4/trainingdashboard/main/py.csv'
#             st.write("No file uploaded. Loading data from URL...")
#             df = pd.read_csv(url)
#       # if fl is not None:
#         #     filename = fl.name
#         #     st.write(filename)
            
#         #     df = pd.read_csv(fl)  # Read uploaded file directly
#         # else:
#         #     url = 'https://raw.githubusercontent.com/imrank4/trainingdashboard/main/py.csv'

#         #     df = pd.read_csv(url)
        
#         # Assuming the columns exist in the loaded DataFrame
#         df = df.loc[:, ["DEALER ZONE", "DEALER GROUP", "DEALER CODE", "DSIRE STATUS", "DSIRE TARGET", "FULL NAME", "JOB TITLE", "TRAINING STATUS", "WBT", "ASSESSMENT", "NUMBERS"]]
        
#         # You may also use slicing method for this 
#         # df = df.iloc[0:20, 2:8]
#         return df
#     except Exception as e:
#         st.error(f"Error loading data: {e}")
#         return None

# def search_and_filter_data(df):
#     st.markdown('<style>div.block-container{padding-top:1rem;}<style>', unsafe_allow_html=True)
#     st.title(':mag: Search and Filter Data ')
#     with st.sidebar:
#         st.header("Choose Filter:")
#         dealer_group = st.text_input('Enter Dealer group: Name')
#         dealer_code = st.text_input('Enter Dealer code: ABCD')
#         profile = st.text_input('Enter Profile: SC or TL Etc')
        
#     filtered_data = df.copy()  # Initially, the filtered data is the same as the original data

#     # Filter by both dealer code and dealer group
#     if dealer_code and dealer_group:
#         filtered_data = filtered_data[(filtered_data['DEALER CODE'].str.contains(dealer_code, case=False)) & 
#                                       (filtered_data['DEALER GROUP'].str.contains(dealer_group, case=False))]
#     # Filter by dealer code only
#     elif dealer_code:
#         filtered_data = filtered_data[filtered_data['DEALER CODE'].str.contains(dealer_code, case=False)]

#     # Filter by dealer group only
#     elif dealer_group:
#         filtered_data = filtered_data[filtered_data['DEALER GROUP'].str.contains(dealer_group, case=False)]
    
#     # Filter by profile only
#     elif profile:
#         filtered_data = filtered_data[filtered_data['PROFILE'].str.contains(profile, case=False)]

#     st.write(filtered_data)

#     # DSIRE GRAPH CREATION
#     try:
#         # Create bar chart showing the count of training statuses and targets per dealer zone
#         training_count_df = filtered_data.groupby(["DEALER CODE", "DSIRE STATUS", "DSIRE TARGET"]).size().reset_index(name="COUNT")

#         # Create bar chart showing the count of training statuses per dealer zone
#         fig = px.bar(training_count_df, x="DSIRE STATUS", y="COUNT", color="DSIRE TARGET",
#                      title="Training Status by Zone", barmode="group", text="COUNT", facet_row="DEALER CODE", facet_row_spacing=0.5)

#         # Add value labels on top of the bars
#         fig.update_traces(textposition='auto')

#         # Remove x-axis and y-axis labels
#         fig.update_layout(xaxis_title="", yaxis_title="")

#         # Display the bar chart
#         st.subheader("Training Status by Dealer code")
#         st.plotly_chart(fig, use_container_width=True)

#     except ValueError as e:
#         if "Vertical spacing cannot be greater than" in str(e):
#             st.warning("Too many unique values for Dealer code, Please select a different dataset or column.")
#         else:
#             raise e

# def main():
#     df = load_data()
#     if df is not None:
#         search_and_filter_data(df)

# if __name__ == "__main__":
#     main()
