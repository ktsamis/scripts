import requests

# Can only be used for the first 3 months with the free credits or you need to
# buy more

# API endpoint for the GPT-3 model
url = "https://api.openai.com/v1/engines/davinci/jobs"

# API request headers
headers = {
    "Content-Type": "application/json",
}

# Function to read API key from file
def read_api_key(file_path):
    with open(file_path, "r") as f:
        # Read API key from file and remove any leading/trailing whitespace
        api_key = f.read().strip()
    return api_key

# Read API key from file
api_key = read_api_key("api_key.txt")
headers["Authorization"] = f"Bearer {api_key}"

# Main loop to repeatedly prompt for user input and send API requests
while True:
    # Prompt user for input
    prompt = input("Enter your prompt: ")
    if prompt == "exit":
        # Exit program if user enters "exit"
        break

    # API request payload
    payload = {
        "prompt": prompt,
        "model": "davinci",
        "temperature": 0,
        "max_tokens": 100,
    }

    # Send API request
    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 200:
        # API request succeeded, display response
        response_json = response.json()
        generated_text = response_json["choices"][0]["text"]
        print(generated_text)
    else:
        # API request failed, display error message
        print("Error: API request failed", response.status_code)
