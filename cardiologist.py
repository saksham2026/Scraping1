import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_data():
    url = 'https://www.maxhealthcare.in/doctor/cardiologists-in-delhi'
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find all div elements with class "d-flex"
        div_elements = soup.find_all('div', class_='d-flex')

        data_list = []

        for div in div_elements:
            # Check if there is exactly one class within the div
            if len(div.get('class', [])) == 1 and 'd-flex' in div.get('class', []):
                # Extract href from the first <a> tag within the div
                a_tag = div.find('a', href=True)
                href = a_tag['href'] if a_tag else None

                # Extract text from the first <h4> tag within the div
                h4_tag = div.find('h4')
                text = h4_tag.text.strip() if h4_tag else None

                # Store the data in a dictionary
                data = {'href': href, 'text': text}
                data_list.append(data)

        return data_list

    else:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")
        return None

def save_to_excel(data_list, filename='output2.xlsx'):
    df = pd.DataFrame(data_list)
    df.to_excel(filename, index=False)
    print(f"Data has been successfully saved to '{filename}'.")

if __name__ == '__main__':
    result = scrape_data()

    if result:
        save_to_excel(result)
