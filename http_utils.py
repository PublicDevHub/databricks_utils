# http_utils.py
import requests
import json
import time

def fetch_json(url, max_retries=3, backoff_factor=1.0):
    """
    Fetch JSON data from a URL with error handling and retries.
    
    Parameters:
        url (str): The URL to fetch data from.
        max_retries (int): Maximum number of retry attempts.
        backoff_factor (float): Time (in seconds) to wait between retries, exponentially increasing.
        
    Returns:
        dict or None: Parsed JSON data if successful, otherwise None.
    """
    retries = 0
    while retries < max_retries:
        try:
            response = requests.get(url)
            # Check if the response status is OK
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Warning: Received status code {response.status_code} for URL {url}")
        
        except requests.RequestException as e:
            print(f"Warning: Request failed for URL {url}. Error: {e}")
        
        except json.JSONDecodeError:
            print(f"Warning: Received invalid JSON data for URL {url}")
        
        # Increment the retry count and apply exponential backoff
        retries += 1
        time.sleep(backoff_factor * (2 ** retries))
    
    # Return None if all retries failed
    print(f"Error: All retries failed for URL {url}")
    return None