import requests
import xlsxwriter
from bs4 import BeautifulSoup

main_url = 'https://www.edimdoma.ru'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}

data = [['Наименование', 'Список', 'Cсылка']]


# Function to fetch HTML content from a URL
def get_html(url):
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.text


# Fetch HTML content from the website
try:
    html_content = get_html(main_url)

    # Parse HTML content using Beautiful Soup
    soup = BeautifulSoup(html_content, 'html.parser')

    # Extract recipe information
    categories = soup.find_all('div', class_='popular-recipes__group')
    for category in categories:
        category_name = category.find('a', class_='popular-recipes__group-title-link').text.strip()
        subcategories = category.find_all('a', href=True)
        for subcategory in subcategories:
            subcategory_name = subcategory.text.strip()
            subcategory_url = main_url + subcategory['href']
            data.append([subcategory_name, category_name, subcategory_url])

    # Write data to Excel file
    with xlsxwriter.Workbook('dishes_list.xlsx') as workbook:
        worksheet = workbook.add_worksheet()

        for row_num, row_data in enumerate(data):
            worksheet.write_row(row_num, 0, row_data)

    print("Data scraped and saved to recipes.xlsx successfully.")

except requests.exceptions.HTTPError as err:
    print(f"HTTP error occurred: {err}")

except requests.exceptions.RequestException as e:
    print(f"An error occurred: {e}")
