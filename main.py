import streamlit as st
import plotly.express as px
from backend import get_data


# Add title, text input, slider, selectbox and subheader
st.title("Weather Forecast for the Next Days")

place = st.text_input(label="Place:")

days = st.slider(label="Forecast Days", min_value=1, max_value=5,
                 help="Select the number of forecasted days")

option = st.selectbox(label="Select data to view",
                      options=["Temperature", "Sky"])

st.subheader(f"{option} for the next {days} days in {place}")

if place:
    # Get the temperature/sky data
    try:
        filtered_data = get_data(place, days)
        if option == "Temperature":
            temperatures = [(dicio["main"]["temp"]) /
                            10 for dicio in filtered_data]
            date = [dicio["dt_txt"] for dicio in filtered_data]
            # Create a temperature plot
            figure = px.line(x=date, y=temperatures, labels={
                "x": "Date", "y": "Temperature (C)"})

            st.plotly_chart(figure)

        if option == "Sky":
            images = {"Clear": "images/clear.png", "Clouds": "images/cloud.png",
                      "Rain": "images/rain.png", "Snow": "images/snow.png"}
            sky_conditions = [dicio["weather"][0]["main"]
                              for dicio in filtered_data]
            images_paths = [images[condition] for condition in sky_conditions]

            st.image(images_paths, width=115)

    except KeyError:
        st.write(
            "You entered a non existent place, please change your input")
