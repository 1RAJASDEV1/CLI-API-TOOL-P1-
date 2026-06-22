import requests

while True:

    city = input("\nEnter city name (or 'quit' to exit): ")

    if city.lower() == "quit":
        print("Goodbye!")
        break

    try:
        # Geocoding API
        geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}"

        geo_response = requests.get(geo_url, timeout=10)
        geo_response.raise_for_status() # except requests.exceptions.HTTPError:  print("API returned an error.")

        geo_data = geo_response.json()

        if "results" not in geo_data:
            print("City not found")
            continue

        latitude = geo_data["results"][0]["latitude"]
        longitude = geo_data["results"][0]["longitude"]

        # Weather API
        weather_url = (
            f"https://api.open-meteo.com/v1/forecast?"
            f"latitude={latitude}&longitude={longitude}"
            f"&current=temperature_2m"
        )

        weather_response = requests.get(weather_url, timeout=10)
        weather_response.raise_for_status()  # except requests.exceptions.HTTPError:  print("API returned an error.")

        weather_data = weather_response.json()

        temperature = weather_data["current"]["temperature_2m"]

        print(f"\nCity: {city}")
        print(f"Latitude: {latitude}")
        print(f"Longitude: {longitude}")
        print(f"Current Temperature: {temperature}°C")

        # Save to file
        with open("weather_log.txt", "a") as file:
            file.write(
                f"City: {city}, "
                f"Latitude: {latitude}, "
                f"Longitude: {longitude}, "
                f"Temperature: {temperature}°C\n"
            )

        print("Data saved to weather_log.txt")

    except requests.exceptions.ConnectionError:
        print("Internet connection error.")

    except requests.exceptions.Timeout:
        print("Request timed out.")

    except requests.exceptions.HTTPError:
        print("API returned an error.")

    except Exception as e:
        print("Unexpected error:", e)