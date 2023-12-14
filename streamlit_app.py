"""
Class: CS230--Section 3
Name: Claudia Wang
Description: 
I pledge that I have completed the programming assignment independently.
I have not copied the code from a student or any source.
I have not given my code to any student. 
"""

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


# read data
def readData():
    return pd.read_csv("trashschedulesbyaddress_7000_sample.csv")


# hello
def hello():
    st.title("Welcome to the Trash Schedule! 🗑️")
    st.sidebar.success("Select a section above.")
    st.image("TrashCollection.jpg")
    st.markdown(
        """
        Welcome to the Trash Schedule App. This app allows users to enter a specific address in the Boston area to 
        check the weekly garbage collection time for that address.
        
        **👈 Select a section from the navigation on the left** to see more details!
        
        ### Want to learn more?
        Check out [TRASH SCHEDULES BY ADDRESS](https://data.boston.gov/dataset/trash-schedules-by-address)
        """
    )


# Map
def dataAnalysis():
    df = readData()
    st.title("📊 Basic Data Analysis of the Trash Schedule")
    st.header("The Map of trash collection addresses")
    st.write("The map below highlights the trash collection points in the Boston area.")
    st.map(data=df, latitude='y_coord', longitude='x_coord', color='#0000FF', zoom=10)

    st.header("Same Trash Days in Different City")
    st.write("This bar chart represents the count of different trash days within the selected city's zip codes.")
    cities = df['mailing_neighborhood'].unique()
    selected_city = st.selectbox('Select a city', cities)
    filtered_data = df[df['mailing_neighborhood'] == selected_city]
    grouped = filtered_data.groupby(['zip_code', 'trashday']).size().reset_index(name='count')
    trash_days = grouped['trashday'].unique()
    zip_codes = grouped['zip_code'].unique()
    fig, ax = plt.subplots(figsize=(10, 6))
    for trash_day in trash_days:
        counts = grouped[grouped['trashday'] == trash_day]['count']
        x_labels = grouped[grouped['trashday'] == trash_day]['zip_code']
        if len(x_labels) > 0:
            x_positions = np.arange(len(x_labels))
            ax.bar(x_positions, counts, label=trash_day)
    ax.set_xlabel('Zip Codes')
    ax.set_ylabel('Count of Trash Days')
    ax.set_title(f'Trash Days in {selected_city}')
    ax.set_xticks(np.arange(len(zip_codes)))
    ax.set_xticklabels(zip_codes.astype(int))
    ax.legend(title='Trash Day', loc='upper right')
    st.pyplot(fig)

    st.header("Same Trash Days in Different Zip Codes")
    st.write("This bar chart represents the count of different trash days for the selected ZIP code")
    df['zip_code'] = df['zip_code'].astype(int)
    zip_codes = df['zip_code'].unique()
    selected_zip_code = st.selectbox('Select a ZIP code', zip_codes)
    zip_code_data = df[df['zip_code'] == selected_zip_code]
    grouped = zip_code_data.groupby('trashday').size()
    fig, ax = plt.subplots()
    ax.bar(grouped.index, grouped.values, color='green')
    ax.set_xlabel('Trash Days')
    ax.set_ylabel('Count')
    ax.set_title(f'Trash Day Counts for ZIP code {selected_zip_code}')
    st.pyplot(fig)

    st.header('Unassigned Addresses without Trashday')
    df.rename(columns={
        'sam_address_id': 'Address ID',
        'full_address': 'Full Address',
        'mailing_neighborhood': 'Neighborhood',
        'zip_code': 'Zip Code'
    }, inplace=True)
    unassigned_addresses = df[df['trashday'].isnull()]
    st.write("This table represents the addresses in the dataset that haven't been assigned a trashday.")
    st.dataframe(unassigned_addresses)

    st.header("Same PWD Frequency")
    district_counts = df['pwd_district'].value_counts()
    district_counts_sorted = district_counts.sort_values()
    fig, ax = plt.subplots(figsize=(8, 6))
    district_counts_sorted.plot(kind='bar', ax=ax)
    ax.set_xlabel('PWD District')
    ax.set_ylabel('Count')
    ax.set_title('Frequency of PWD Districts')
    plt.xticks(rotation=45)
    st.pyplot(fig)
    st.write("This bar chart represents the frequency of Public Works Districts (PWD Districts) in the dataset. "
             "The x-axis shows different PWD Districts, while the y-axis displays the count of occurrences of each "
             "district.")


# Find Trash Day
def findTrashDayByID():
    df = readData()
    st.title("🆔 Find Your Trash Day By SAM Address ID")
    ID = st.text_input("Please enter your address' ID in the Street Address Management system: ")
    if st.button('Search'):
        info = df[df['sam_address_id'] == int(ID)]
        if not info.empty:
            fullAddress = info['full_address'].values[0]
            mailingNeighborhood = info['mailing_neighborhood'].values[0]
            zipCode = info['zip_code'].values[0]
            trashDay = info['trashday'].values[0] if 'trashday' in info.columns else None
            st.header("Your address' information:")
            st.write(f"Full Address: {fullAddress}")
            st.write(f"Mailing Neighborhood: {mailingNeighborhood}")
            st.write(f"Zip Code: {zipCode}")
            if trashDay:
                st.write(f"Trash Day: {trashDay}")
            else:
                st.write(
                    "This address ID does not have a trash day information yet. If updates occur, we'll notify "
                    "you via email.")
                email = st.text_input('Enter your email')
                exactAddress = st.text_input('Enter your exact address')
                if st.button('Submit'):
                    if not email:
                        st.write("Please enter your email.")
                    if not exactAddress:
                        st.write("Please enter your exact address.")
                    else:
                        st.write("Thank you! We'll keep you updated.")
        else:
            st.markdown("<span style='color:red'>Address ID not found. Please try again.</span>",
                        unsafe_allow_html=True)


def findTrashDayByAddress():
    df = readData()
    st.title("🏠 Find Your Trash Day By Full Address")
    address = st.text_input("Please enter your full address: ")
    if st.button('Search'):
        info = df[df['full_address'] == address]
        if not info.empty:
            ID = int(info['sam_address_id'].values[0])
            mailingNeighborhood = info['mailing_neighborhood'].values[0]
            zipCode = info['zip_code'].values[0]
            trashDay = info['trashday'].values[0] if 'trashday' in info.columns else None
            st.header("Your address' information:")
            st.write(f"SAM Address ID: {ID}")
            st.write(f"Mailing Neighborhood: {mailingNeighborhood}")
            st.write(f"Zip Code: {zipCode}")
            if trashDay:
                st.write(f"Trash Day: {trashDay}")
            else:
                st.write("This address does not have a trash day information yet. If updates occur, we'll notify "
                         "you via email.")
                email = st.text_input('Enter your email')

                exactAddress = st.text_input('Enter your exact address')
                if st.button('Submit'):
                    if "@" in email and email[-4:] == ".com":
                        if not email.empty:
                            st.write("Please enter your email.")
                        if not exactAddress.empty:
                            st.write("Please enter your exact address.")
                        else:
                            st.write("Thank you! We'll keep you updated.")
                    else:
                        st.markdown("<span style='color:red'>Invalid email! Please try it again.</span>",
                                    unsafe_allow_html=True)
        else:
            st.markdown("<span style='color:red'>Address not found. Please try again.</span>",
                        unsafe_allow_html=True)


def thanks(name, message='Thanks'):
    return f"{message}, {name}!"


def contact():
    st.title("📧 Contact Us")
    name = st.text_input("Your Name: ")
    email = st.text_input("Your Email: ")
    options = [
        "Suggestion for improvement",
        "Report missing data",
        "Report incorrect data",
        "Job application",
        "Other"
    ]
    selectedOptions = st.multiselect("Please select your request type", options)
    message = st.text_area("Your Message: ")
    if st.button("Submit"):
        if "@" in email and email[-4:] == ".com":
            if not name or not email or not message or not selectedOptions:
                st.markdown("<span style='color:red'>Error! Please complete all fields.</span>", unsafe_allow_html=True)
            else:
                st.balloons()
                success_message = thanks(name, "We have received your message. Thank you")
                st.success(success_message)
                st.success("Expect a reply within 3-5 working days.")
        else:
            st.markdown("<span style='color:red'>Invalid email! Please try it again.</span>",
                        unsafe_allow_html=True)


pageName = {
    "👋🏻 Hello": hello,
    "📊 Basic Data Analysis": dataAnalysis,
    "🆔 Find Trash Day by ID": findTrashDayByID,
    "🏠 Find Trash Day by Address": findTrashDayByAddress,
    "📧 Contact Us": contact
}

section = st.sidebar.selectbox("Navigation", pageName.keys())
pageName[section]()
