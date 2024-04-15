import requests
from bs4 import BeautifulSoup
import json

# URL of the Wikipedia page
url = "https://en.wikipedia.org/wiki/List_of_World_Heritage_Sites_in_India"

# Send a GET request to the URL
response = requests.get(url)

# Parse the HTML content of the page
soup = BeautifulSoup(response.text, 'html.parser')

# Find all tables with class "wikitable sortable plainrowheaders"
tables = soup.find_all('table', {'class': 'wikitable sortable plainrowheaders'})

# List to store all rows from both tables
rows_list = []

# Loop through each table
for table in tables:
    # Find the tbody section within the table
    tbody = table.find('tbody')
    # Find all tr tags within the tbody
    rows = tbody.find_all('tr')
    # Loop through each row and append its content to the list
    for index, row in enumerate(rows):
        if index != 0:  # Skip the first row
            # Extract the title from the <th> tag
            title = row.find('th', {'scope': 'row'}).get_text(strip=True)
            # Extract the alt attribute from the <img> tag within the first <td> tag
            img_tag = row.find('td').find('img')
            alt = img_tag.get('alt') if img_tag else None
            # Extract the src attribute from the <img> tag within the first <td> tag
            src = img_tag.get('src') if img_tag else None
            # Extract the image link
            a_tag = row.find('td').find('a')
            image_link = a_tag['href'] if a_tag else None
            # Check if the image link is a relative URL
            if image_link and not image_link.startswith('http'):
                # Add the appropriate prefix (https://) to the relative URL
                image_link = 'https://en.wikipedia.org' + image_link
            # Extract the state title from the <a> tag within the second <td> tag
            state_tag = row.find_all('td')[1].find('a')
            state = state_tag['title'] if state_tag else None
            # Extract the year from the third <td> tag
            year = row.find_all('td')[2].get_text(strip=True) if row.find_all('td')[2] else None
            # Extract the UNESCO Data from the fourth <td> tag
            unesco_data = row.find_all('td')[3].get_text(strip=True) if row.find_all('td')[3] else None
            # Extract the description from the fifth <td> tag
            description = row.find_all('td')[4].get_text(strip=True) if row.find_all('td')[4] else None
            # Store the extracted information in a dictionary
            row_dict = {'title': title, 'alt': alt, 'src': src, 'image_link': image_link, 'state': state, 'year': year, 'unesco_data': unesco_data, 'description': description}
            # Append the dictionary to the list
            rows_list.append(row_dict)

# Write the list of dictionaries to a JSON file
with open('world_heritage_sites_final.json', 'w') as json_file:
    json.dump(rows_list, json_file, indent=4)

print("JSON file has been created successfully.")
