# Costco Chocolate Web Scraper

This Python project uses [Playwright](https://playwright.dev/python/) to automate a search for "chocolate" on [Costco.com](https://www.costco.com), visit each product on the search results pages, extract key details, and save them into a CSV file.

## 📌 Features

- Automates chocolate search on Costco.com.
- Visits each product in the search results and extracts:
  - Product Title
  - Price
  - Description
  - Product Link
- Iterates through all result pages (pagination supported).
- Saves the final output into `data/costco_chocolate_search_results.csv`.

## 🚀 Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/rida-louchachha/web_scrapping_cosco.git
cd web_scrapping_cosco
```

### 2. Create and activate virtual environment

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

If you don’t have a `requirements.txt` yet, create one with the following:

```
playwright
pandas
```

Then run:

```bash
playwright install
```

### 4. Run the scraper

```bash
python search_scrapper.py
```

The scraped product data will be saved to:

```
data/costco_chocolate_search_results.csv
```

## 📁 Project Structure

```
├── data/
│   └── costco_chocolate_search_results.csv     # Output CSV file
├── main.py                                     # Optional logic (entry point if needed)
├── search_scrapper.py                          # Main scraper logic
├── README.md                                   # Project documentation
└── requirements.txt                            # Python dependencies
```

## 🛠️ Notes

- The script uses Playwright in visible mode (`headless=False`) for debugging. Change to `headless=True` for background scraping.
- The scraper uses CSS selectors specific to Costco's website structure. If their UI changes, you might need to update the selectors.

## 👤 Author

**Rida Louchachha**  
📧 [ridalouchachha2580@gmail.com](mailto:ridalouchachha2580@gmail.com)
