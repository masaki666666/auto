import requests
import pandas as pd
import re
from bs4 import BeautifulSoup

# Initialize an empty DataFrame
df = pd.DataFrame()

# Open the file containing the URLs
with open('urls.txt', 'r') as file:
    urls = file.readlines()

# For each URL in the list
for url in urls:
    # Strip any trailing newline character
    url = url.strip()

    # Fetch the website content
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    header_tags = soup.find_all("th")
    data_tags = soup.find_all("td")
    header = [tag.get("class")[0] for tag in header_tags if tag.get("class")]

    data_html = ''.join(map(str, data_tags))
    records_html = re.split('<td class="place">', data_html)[1:]

    for record_html in records_html:
        record_html = '<td class="place">' + record_html  # Add the splitting string back to each record
        record_soup = BeautifulSoup(record_html, "html.parser")
        record_tags = record_soup.find_all("td")

        data = {}

        for tag in record_tags:
            if tag.get("class") and tag.get("class")[0] in header:
                if tag.get("class")[0] == "waku" and tag.img and 'alt' in tag.img.attrs:
                    waku_number = re.findall(r'\d+', tag.img.attrs['alt'])
                    data[tag.get("class")[0]] = waku_number[0] if waku_number else None
                elif tag.get("class")[0] == "corner":
                    corner_passes = tag.find_all("li")
                    if corner_passes and len(corner_passes) >= 2:
                        data["corner_3"] = corner_passes[0].text.strip()
                        data["corner_4"] = corner_passes[1].text.strip()
                elif tag.get("class")[0] == "h_weight":
                    weight_data = tag.text.split('<span>')[0] if '<span>' in tag.text else tag.text
                    data[tag.get("class")[0]] = weight_data.strip()
                else:
                    data[tag.get("class")[0]] = tag.text.strip()

        df = df.append(data, ignore_index=True)

# Export the DataFrame to a CSV file
df.to_csv('output.csv', index=False)