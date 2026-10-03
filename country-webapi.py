import requests

# This program demonstrates how to use the REST Countries API to get information 
# about a country based on its name.
# It defines a function `get_country_info` that takes a country name as input, 
# makes a GET request to the API, and prints out details about the country 
# such as its capital, population

def get_country_info(country_name: str):

    # The base URL for the API
    # We will append the country name to this URL to get information about that specific country
    # Notice the version (v3.1) and the endpoint (name)
    base_url = "https://restcountries.com/v3.1/name/"
    
    # We append the country name to the path
    api_url = f"{base_url}{country_name}"
    # For example, if country_name is "France", the full URL will be:
    # https://restcountries.com/v3.1/name/France
    
    # Parameters to pass in the query string (?fullText=true)
    # This tells the API we want an exact name match, not just a partial one
    query_params = {
        "fullText": "false"
    }

    try:
        # Making the GET request
        response = requests.get(api_url, params=query_params)

        # Check if the request was successful (HTTP Status Code 200)
        if response.status_code == 200:
            # Parse the response data into a Python list/dictionary
            data = response.json()
            
            # Extract specific data from the JSON structure
            country = data[0]
            name = country['name']['common']
            capital = country['capital'][0]
            population = country['population']
            currencies = country['currencies']
            flag = country['flags']['alt']            
            print(f"Country: {name}")
            print(f"Capital: {capital}")
            print(f"Population: {population:,}")
            print(f"Currencies: {', '.join(currencies.keys())}")
            print(f"Flag: {flag}")
            print("-" * 40)

        else:
            print(f"Error: Could not find country. Status Code: {response.status_code}")

    except Exception as e:
        print(f"An error occurred: {e}")


def main(): 
    running : bool = True
    while running:
        # Example usage of the function
        country = input("Enter the name of a country: ")
        get_country_info(country)
        cont = input("Do you want to search for another country? (yes/no): ").strip().lower()
        if cont != "yes":
            running = False

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"An error occurred: {e}")

