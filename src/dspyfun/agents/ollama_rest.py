import requests

def fetch_from_httpbin():
    """
    Fetches a simple GET request data from http://httpbin.org/get and
returns the JSON response.

    Returns:
        dict or None: The JSON response if successful, otherwise `None`.
    """
    try:
        # Make an HTTP GET request to https://httpbin.org/get
        response = requests.get('https://httpbin.org/get')

        # Check for a successful response (HTTP status code 200)
        if response.status_code == 200:
            return response.json()  # Return the JSON-encoded content of the response
        else:
            print(f"Error {response.status_code}: Unable to fetch data")
            return None
    except requests.exceptions.RequestException as e:
        # Handle any request exceptions (e.g., network issues)
        print(f"An error occurred: {str(e)}")
        return None

# Example usage
if __name__ == "__main__":
    result = fetch_from_httpbin()
    if result is not None:
        print("Fetched data from httpbin.org:", result)