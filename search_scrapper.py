from playwright.sync_api import sync_playwright
import pandas as pd

def search_and_scrape_chocolate():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        print("🔍 Navigating to Costco home page...")
        page.goto("https://www.costco.com", timeout=60000)
        page.wait_for_timeout(3000)

        print("🔎 Searching for 'chocolate'...")
        page.wait_for_selector('input[aria-describedby="typeahead-search-field-description"]', timeout=10000)
        search_box = page.query_selector('input[aria-describedby="typeahead-search-field-description"]')
        search_box.fill("chocolate")
        search_box.press("Enter")
        page.wait_for_timeout(5000)

        products = []
        page_number = 1

        while True:
            print(f"\n📄 Processing results page {page_number}...")

            # Re-fetch links every time
            product_elements = page.query_selector_all(
                '.MuiTypography-root.MuiTypography-inherit.MuiLink-root.MuiLink-underlineHover.mui-1se40y7'
            )
            print(f"🔗 Found {len(product_elements)} products on this page.")

            hrefs = []
            for el in product_elements:
                href = el.get_attribute("href")
                if href:
                    full_url = href
                    hrefs.append(full_url)

            for idx, url in enumerate(hrefs):
                try:
                    print(f"   ➤ Visiting product {idx + 1}: {url}")
                    page.goto(url, timeout=60000)
                    page.wait_for_load_state("load")
                    page.wait_for_timeout(3000)

                    title = page.query_selector('span.product-title')
                    price = page.query_selector('span[automation-id="productPriceOutput"]')
                    description = page.query_selector('p.pdp-features') or page.query_selector('div.product-info-description p')

                    products.append({
                        "title": title.inner_text().strip() if title else None,
                        "price": price.inner_text().strip() if price else None,
                        "description": description.inner_text().strip() if description else None,
                        "link": url
                    })

                except Exception as e:
                    print(f"   ❌ Failed to scrape product {idx + 1}: {e}")
                    continue

            # ✅ Try to click the next page
            next_button = page.query_selector('button[aria-label="Go to next page"]')
            if next_button and next_button.is_enabled():
                print("➡ Moving to next page...")
                next_button.click()
                page.wait_for_timeout(5000)
                page_number += 1
            else:
                print("✅ No more pages.")
                break

        browser.close()

        # Save to CSV
        df = pd.DataFrame(products)
        df.to_csv("data/costco_chocolate_search_results.csv", index=False)
        print(f"\n✅ Done! Scraped {len(products)} products. File saved to 'data/costco_chocolate_search_results.csv'.")

if __name__ == "__main__":
    search_and_scrape_chocolate()
