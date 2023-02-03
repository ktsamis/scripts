import requests
import xml.etree.ElementTree as ET

def get_rss_feed(url):
    """
    Makes an HTTP GET request to the given URL and returns the parsed RSS feed
    as a list of dictionaries.  Each dictionary represents an item in the feed,
    with the keys being the tag names and the values being the tag text.
    """
    # Make an HTTP GET request to the URL
    response = requests.get(url)

    # Parse the response as XML
    root = ET.fromstring(response.text)

    # Find all the "item" elements in the RSS feed
    items = root.findall("./channel/item")

    # Return the items as a list of dictionaries
    return [{child.tag: child.text for child in item} for item in items]

if __name__ == "__main__":
    """
    The main program that reads the URL of the RSS feed from a config file,
    gets the RSS feed, and prints the title, link, and summary of each item.
    """
    # Read the URL of the RSS feed from the config file
    with open("config.txt", "r") as config_file:
        url = config_file.readline().strip()

    # Get the RSS feed
    items = get_rss_feed(url)

    # Print the title, link, and summary of each item
    for item in items:
        print("Title:", item["title"])
        print("Link:", item["link"])
        print("Summary:", item.get("description", ""))
        print("")
