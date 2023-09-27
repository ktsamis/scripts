import requests
import xml.etree.ElementTree as ET
from colorama import Fore, Style, init

ITEMS_PER_PAGE = 13


def get_rss_feed(url, error_color, reset_color):
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"{error_color}Error: Unable to fetch the RSS feed from {url}: {e}{reset_color}")
        return []
    except Exception as e:
        print(f"{error_color}Error: An unexpected error occurred while fetching {url}: {e}{reset_color}")
        return []

    try:
        root = ET.fromstring(response.text)
    except ET.ParseError as e:
        print(f"{error_color}Error: Unable to parse the XML from {url}: {e}{reset_color}")
        return []

    items = root.findall("./channel/item")
    return [{child.tag: child.text for child in item} for item in items]


def display_items(items, title_color, link_color, summary_color, reset_color):
    if not items:
        print("No items to display.")
        return

    filtered_items = [item for item in items if item.get("description")]
    total_pages = (len(filtered_items) - 1) // ITEMS_PER_PAGE + 1

    if total_pages == 0:
        print("No items to display with summaries.")
        return

    page_number = 1
    while True:
        print(f"Page {page_number} of {total_pages}")

        start_index = (page_number - 1) * ITEMS_PER_PAGE
        end_index = start_index + ITEMS_PER_PAGE
        for i in range(start_index, min(end_index, len(filtered_items))):
            item = filtered_items[i]
            print(f"{title_color}Title:{reset_color}", item["title"])
            print(f"{link_color}Link:{reset_color}", item["link"])
            print(f"{summary_color}Summary:{reset_color}", item.get("description", ""))
            print("")

        if page_number >= total_pages:  # If on the last page, exit the loop (and function)
            break
        elif page_number < total_pages:
            user_input = input("Press 'n' for next page, 'p' for previous page, 'q' to quit: ").lower()
            if user_input == 'n':
                page_number += 1
            elif user_input == 'p' and page_number > 1:
                page_number -= 1
            elif user_input == 'q' or user_input == '\x1b':  # '\x1b' is the escape character
                break


if __name__ == "__main__":
    init(autoreset=True)

    try:
        with open("config.txt", "r") as config_file:
            config = {"urls": []}
            for line in config_file.readlines():
                key, value = line.strip().split('=')
                if key == "url":
                    config["urls"].append(value)
                else:
                    config[key] = value

            if not config["urls"]:
                raise ValueError("No URL found in config.txt")

            color_map = {
                "red": Fore.RED,
                "green": Fore.GREEN,
                "yellow": Fore.YELLOW,
                "blue": Fore.BLUE,
                "magenta": Fore.MAGENTA,
                "cyan": Fore.CYAN,
                "white": Fore.WHITE,
                "reset": Style.RESET_ALL
            }

            title_color = color_map.get(config.get("title_color", "reset"))
            link_color = color_map.get(config.get("link_color", "reset"))
            summary_color = color_map.get(config.get("summary_color", "reset"))
            error_color = color_map.get(config.get("error_color", "reset"))
            reset_color = Style.RESET_ALL

    except FileNotFoundError:
        print(f"{Fore.RED}Error: config.txt file not found!{Style.RESET_ALL}")
        exit()
    except ValueError as ve:
        print(f"{Fore.RED}Error: {ve}{Style.RESET_ALL}")
        exit()

    all_items = []
    for url in config["urls"]:
        all_items.extend(get_rss_feed(url, error_color, reset_color))

    if all_items:
        display_items(all_items, title_color, link_color, summary_color, reset_color)
    else:
        print("No items to display.")

