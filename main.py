from playwright.sync_api import sync_playwright
from playwright_stealth import Stealth
import pandas as pd

def scrape_costco_candy():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        # Stealth(page)

        print("Navigating to Costco candy page...")
        page.goto("https://www.costco.com/candy.html", timeout=60000)
        page.wait_for_timeout(5000)

        products = []
        page_number = 1

        while True:
            print(f"\n📄 Processing listing page {page_number}...")
            page.wait_for_timeout(3000)

            original_url = page.url

            idx = 0
            while True:
                product_elements = page.query_selector_all(
                    '.MuiTypography-root.MuiTypography-t5.MuiLink-root.MuiLink-underlineHover'
                )

                if idx >= len(product_elements):
                    break

                try:
                    element = product_elements[idx]
                    href = element.get_attribute('href')
                    if not href:
                        idx += 1
                        continue

                    full_url = "https://www.costco.com" + href
                    print(f"[{idx + 1}] Visiting: {full_url}")
                    page.goto(full_url, timeout=60000)
                    page.wait_for_timeout(4000)

                    clickable = page.query_selector(
                        '.MuiTypography-root.MuiTypography-inherit.MuiLink-root.MuiLink-underlineHover.mui-1se40y7'
                    )
                    if clickable:
                        print(f"   ➤ Clicking extra link...")
                        clickable.click()
                        page.wait_for_timeout(3000)

                    title = page.query_selector('span.product-title')
                    price = page.query_selector('span[automation-id="productPriceOutput"]')
                    description = page.query_selector('p.pdp-features')

                    products.append({
                        "title": title.inner_text().strip() if title else None,
                        "price": price.inner_text().strip() if price else None,
                        "description": description.inner_text().strip() if description else None,
                        "link": full_url
                    })

                    page.goto(original_url, timeout=60000)
                    page.wait_for_timeout(3000)
                    idx += 1

                except Exception as e:
                    print(f"❌ Error on product {idx + 1}: {e}")
                    page.goto(original_url, timeout=60000)
                    page.wait_for_timeout(3000)
                    idx += 1
                    continue

            next_button = page.query_selector('button[aria-label="Go to next page"]')
            if next_button and next_button.is_enabled():
                print("➡ Moving to next page...")
                next_button.click()
                page.wait_for_timeout(5000)
                page_number += 1
            else:
                print("❌ No more pages found. Scraping complete.")
                break

        browser.close()

        df = pd.DataFrame(products)
        df.to_csv("data/costco_candy_details.csv", index=False)
        print(f"\n✅ Finished scraping {len(products)} products. Saved to 'data/costco_candy_details.csv'.")

if __name__ == "__main__":
    scrape_costco_candy()
