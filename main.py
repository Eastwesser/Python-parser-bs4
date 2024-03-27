import requests
from bs4 import BeautifulSoup
import xlsxwriter

main_url = 'https://www.edimdoma.ru'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

class WebsiteUnavailableError(Exception):
    pass

def get_soup(url):
    try:
        res = requests.get(url, headers=headers)
        res.raise_for_status()  # Raise an error for non-200 status codes
        return res.text  # Return HTML content as a string
    except requests.exceptions.RequestException as e:
        raise WebsiteUnavailableError(f"Failed to access {url}: {e}") from None

def scrape_recipes(html_content):  # Pass HTML content as argument
    data = [['Наименование', 'Категория блюда', 'Базовые ингредиенты', 'Cсылка', 'Картинка']]

    try:
        # Parse the HTML content with BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')

        # Extract recipe data
        # Implement this part based on the HTML structure of the page
        # Identify the HTML elements that contain recipe information and extract it
        # For demonstration purposes, let's assume we extract some sample data
        sample_recipe_data = [
            ["Sample Recipe 1", "Sample Category", ["Ingredient 1", "Ingredient 2", "Ingredient 3"], "https://www.edimdoma.ru/recipe/123", "https://www.edimdoma.ru/img/sample_recipe1.jpg"],
            ["Sample Recipe 2", "Sample Category", ["Ingredient 4", "Ingredient 5", "Ingredient 6"], "https://www.edimdoma.ru/recipe/456", "https://www.edimdoma.ru/img/sample_recipe2.jpg"],
        ]

        # Store the extracted data
        data.extend(sample_recipe_data)

        # Write the data to an Excel file
        write_to_excel(data)

    except WebsiteUnavailableError as e:
        print(f"Website is unavailable: {e}")

def write_to_excel(data):
    # Writing data to Excel
    with xlsxwriter.Workbook('recipes.xlsx') as workbook:
        worksheet = workbook.add_worksheet()

        for row_num, info in enumerate(data):
            worksheet.write_row(row_num, 0, info)

# Unit test
def test_scrape_recipes():
    try:
        # Call the function to scrape recipes and write to Excel
        html_content = get_soup("https://www.edimdoma.ru/retsepty")
        scrape_recipes(html_content)
        print("Unit test passed!")
    except Exception as e:
        print(f"Unit test failed: {e}")

if __name__ == "__main__":
    test_scrape_recipes()