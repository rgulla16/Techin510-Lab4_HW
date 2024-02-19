import streamlit as st
from datetime import datetime, timedelta
import pytz
import requests

# Alpha Vantage API Key (Replace with your own key)
alpha_vantage_api_key = "YOUR_ALPHA_VANTAGE_API_KEY"

# OpenWeatherMap API Key (Replace with your own key)
openweathermap_api_key = "YOUR_OPENWEATHERMAP_API_KEY"

def get_stock_data(symbol):
    endpoint = "https://www.alphavantage.co/query"
    params = {
        "function": "GLOBAL_QUOTE",
        "symbol": symbol,
        "apikey": alpha_vantage_api_key
    }

    response = requests.get(endpoint, params=params)
    print(response)
    data = response.json()
    print(data)


    if "Global Quote" in data:
        return data["Global Quote"]
    else:
        return None

def get_weather_data(city):
    endpoint = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": openweathermap_api_key
    }

    response = requests.get(endpoint, params=params)
    data = response.json()

    if "main" in data and "weather" in data:
        return data
    else:
        return None



# Streamlit app
def main():

    st.title("Real-time World Information")

    # Nasdaq
    nasdaq_data = get_stock_data("^IXIC")
    if nasdaq_data:
        st.write(f"**Nasdaq Index:** {nasdaq_data['05. price']}")
        st.write(f"**Change:** {nasdaq_data['10. change percent']}")
    else:
        st.warning("Nasdaq data not available.")

    # Dow Jones Industrial Average
    dow_data = get_stock_data("^DJI")
    if dow_data:
        st.write(f"**Dow Jones Index:** {dow_data['05. price']}")
        st.write(f"**Change:** {dow_data['10. change percent']}")
    else:
        st.warning("Dow Jones data not available.")

    # Seattle Weather
    seattle_data = get_weather_data("Seattle")
    if seattle_data:
        st.write(f"**Temperature in Seattle:** {seattle_data['main']['temp']} °C")
        st.write(f"**Weather:** {seattle_data['weather'][0]['description']}")
    else:
        st.warning("Seattle weather data not available.")


    st.title("World Clock")

    # Dropdown with 20 world cities
    selected_city1 = st.selectbox("Select City 1:", get_city_list(), key="city1")
    selected_city2 = st.selectbox("Select City 2:", get_city_list(), key="city2")
    selected_city3 = st.selectbox("Select City 3:", get_city_list(), key="city3")
    selected_city4 = st.selectbox("Select City 4:", get_city_list(), key="city4")

    # Get the time zone for the selected cities
    timezone1 = get_timezone(selected_city1)
    timezone2 = get_timezone(selected_city2)
    timezone3 = get_timezone(selected_city3)
    timezone4 = get_timezone(selected_city4)

    # HTML template with embedded JavaScript
    html_code = f"""
    <html>
    <head>
        <style>
            .clock-container {{
                width: 300px;
                height: 300px;
                position: relative;
                display: inline-block;
                margin: 10px;
            }}

            .hour-hand, .minute-hand, .second-hand {{
                position: absolute;
                left: 50%;
                transform-origin: bottom center;
                transform: translateX(-50%);
            }}

            .hour-hand {{
                width: 4px;
                height: 80px;
                background-color: black;
                top: 22.5%;
            }}

            .minute-hand {{
                width: 3px;
                height: 120px;
                background-color: black;
                top: 10%;
            }}

            .second-hand {{
                width: 2px;
                height: 140px;
                background-color: red;
            }}

            .clock-circle {{
                width: 100%;
                height: 100%;
                border-radius: 50%;
                border: 2px solid black;
                position: absolute;
                top: 0;
                left: 0;
            }}

            .time-text {{
                position: absolute;
                top: 70%;
                left: 50%;
                transform: translateX(-50%);
                font-size: 18px;
            }}

            .city-name {{
                position: absolute;
                top: 80%;
                left: 50%;
                transform: translateX(-50%);
                font-size: 14px;
            }}
        </style>
        <script>
            function updateClock(cityKey, cityName, timezoneOffset) {{
                var now = new Date();
                
                // Add 8 hours to the time
                now.setHours(now.getHours() + 8);
                
                // Get the time zone offset based on the selected city
                now.setMinutes(now.getMinutes() + timezoneOffset);
                
                var hours = now.getHours() % 12;
                var minutes = now.getMinutes();
                var seconds = now.getSeconds();

                var hourAngle = (hours * 30 + minutes / 2) % 360;
                var minuteAngle = (minutes * 6 + seconds / 10) % 360;
                var secondAngle = (seconds * 6) % 360;

                document.getElementById('hour-hand-' + cityKey).style.transform = 'rotate(' + hourAngle + 'deg)';
                document.getElementById('minute-hand-' + cityKey).style.transform = 'rotate(' + minuteAngle + 'deg)';
                document.getElementById('second-hand-' + cityKey).style.transform = 'rotate(' + secondAngle + 'deg)';
                
                // Display time text
                document.getElementById('time-text-' + cityKey).innerText = now.toLocaleTimeString();
                
                // Display city name
                document.getElementById('city-name-' + cityKey).innerText = cityName;
            }}

            setInterval(function() {{ updateClock('city1', '{selected_city1}', {get_timezone_offset(selected_city1)}); }}, 1000);
            setInterval(function() {{ updateClock('city2', '{selected_city2}', {get_timezone_offset(selected_city2)}); }}, 1000);
            setInterval(function() {{ updateClock('city3', '{selected_city3}', {get_timezone_offset(selected_city3)}); }}, 1000);
            setInterval(function() {{ updateClock('city4', '{selected_city4}', {get_timezone_offset(selected_city4)}); }}, 1000);
        </script>
    </head>
    <body>
        <div style="display: flex; justify-content: space-between;">
            <div class="clock-container">
                <div id="clock-circle"></div>
                <div class="hour-hand" id="hour-hand-city1"></div>
                <div class="minute-hand" id="minute-hand-city1"></div>
                <div class="second-hand" id="second-hand-city1"></div>
                <div class="time-text" id="time-text-city1"></div>
                <div class="city-name" id="city-name-city1"></div>
            </div>

            <div class="clock-container">
                <div id="clock-circle"></div>
                <div class="hour-hand" id="hour-hand-city2"></div>
                <div class="minute-hand" id="minute-hand-city2"></div>
                <div class="second-hand" id="second-hand-city2"></div>
                <div class="time-text" id="time-text-city2"></div>
                <div class="city-name" id="city-name-city2"></div>
            </div>

            <div class="clock-container">
                <div id="clock-circle"></div>
                <div class="hour-hand" id="hour-hand-city3"></div>
                <div class="minute-hand" id="minute-hand-city3"></div>
                <div class="second-hand" id="second-hand-city3"></div>
                <div class="time-text" id="time-text-city3"></div>
                <div class="city-name" id="city-name-city3"></div>
            </div>

            <div class="clock-container">
                <div id="clock-circle"></div>
                <div class="hour-hand" id="hour-hand-city4"></div>
                <div class="minute-hand" id="minute-hand-city4"></div>
                <div class="second-hand" id="second-hand-city4"></div>
                <div class="time-text" id="time-text-city4"></div>
                <div class="city-name" id="city-name-city4"></div>
            </div>
        </div>
    </body>
    </html>
    """

    # Display HTML code
    st.components.v1.html(html_code, width=1200, height=600)

# Function to get the list of 20 world cities
def get_city_list():
    return [
        "New York", "London", "Tokyo", "Sydney",
        "Dubai", "Los Angeles", "Berlin", "Singapore",
        "Mumbai", "Johannesburg", "Rio de Janeiro", "Auckland",
        "Hawaii", "UTC", "Paris", "Beijing", "Chicago", "Toronto",
        "Moscow", "Buenos Aires"
    ]

# Function to get the time zone for a city
def get_timezone(city_name):
    city_timezones = {
        "New York": "America/New_York",
        "London": "Europe/London",
        "Paris": "Europe/Paris",
        "Tokyo": "Asia/Tokyo",
        "Sydney": "Australia/Sydney",
        "Dubai": "Asia/Dubai",
        "Los Angeles": "America/Los_Angeles",
        "Berlin": "Europe/Berlin",
        "Singapore": "Asia/Singapore",
        "Mumbai": "Asia/Kolkata",
        "Johannesburg": "Africa/Johannesburg",
        "Rio de Janeiro": "America/Rio_de_Janeiro",
        "Auckland": "Pacific/Auckland",
        "Hawaii": "Pacific/Honolulu",
        "UTC": "UTC",
        "Beijing": "Asia/Shanghai",
        "Chicago": "America/Chicago",
        "Toronto": "America/Toronto",
        "Moscow": "Europe/Moscow",
        "Buenos Aires": "America/Argentina/Buenos_Aires",
    }
    return city_timezones.get(city_name, "UTC")

# Function to get the time zone offset for a city
def get_timezone_offset(city_name):
    city_timezone = get_timezone(city_name)
    utc_now = datetime.now(pytz.utc)
    if city_timezone:
        now = datetime.now(pytz.timezone(city_timezone))
        return now.utcoffset().total_seconds() / 60
    return 0


# Run the Streamlit app
if __name__ == "__main__":
    main()
    
    
    
