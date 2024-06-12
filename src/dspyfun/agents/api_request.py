
import requests

def make_api_request(url):
    """Make a request to an API and return the response."""
    try:
        response = requests.get(url)
        # Ensure we have a successful status code (200-299 range)
        if 200 <= response.status_code < 300:
            return response.json()
        else:
            raise ValueError("API request failed with status code: {}".format(response.status_code))
    except requests.RequestException as e:
        # Handle any exceptions that occur during the request
        print(f"An error occurred: {e}")
        return None


if __name__ == "__main__":
    # Function invocation based on the provided function declaration
    result = make_api_request("https://httpbin.org/get")  # Use the specified URL for the API request
    print(result)  # Print the result of the API request
    
    