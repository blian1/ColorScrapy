"""
Description: Extract and print color names and hex values from a webpage using HTML parsing.
Author: Boyuan Lian
Date: 2024/10/16
"""
from html.parser import HTMLParser
import urllib.request


class ColorHexParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_color_name = False
        self.in_hex_value = False
        self.current_color_name = None
        self.colors = {}


    def handle_starttag(self, tag, attrs):
        if tag == 'a':  # Look for <a> tags with specific classes
            for attr in attrs:
                # Check if the class attribute is 'tw' or 'tb' to identify color names
                if attr[0] == 'class' and ('tw' in attr[1] or 'tb' in attr[1]):
                    self.in_color_name = True
                # Check if href attribute starts with '/' to identify hex value links
                if attr[0] == 'href' and attr[1].startswith('/'):
                    self.in_hex_value = True


    def handle_data(self, data):
        if self.in_color_name:
            # Store the color name
            self.current_color_name = data.strip()
            self.in_color_name = False

        if self.in_hex_value and self.current_color_name:
            hex_value = data.strip()
            self.colors[self.current_color_name] = hex_value
            self.in_hex_value = False

    def handle_endtag(self, tag):
        if tag == 'a':
            self.in_color_name = False
            self.in_hex_value = False


myparser = ColorHexParser()

with urllib.request.urlopen('https://www.colorhexa.com/color-names') as response:
    html = response.read().decode()

myparser.feed(html)


for color_name, hex_value in myparser.colors.items():
    print(f"{color_name} {hex_value}")

print(f"Total colors: {len(myparser.colors)}")

