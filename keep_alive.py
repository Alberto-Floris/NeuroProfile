import os
from playwright.sync_api import sync_playwright, TimeoutError


def run():
    url = os.getenv("APP_URL", "https://neuroprofile.streamlit.app/")

    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=["--no-sandbox"]
        )

        page = browser.new_page()

        try:
            print(f"Opening: {url}")
            page.goto(url, timeout=60000, wait_until="domcontentloaded")

            wake_button = 'button:has-text("Yes, get this app back up!")'

            try:
                page.wait_for_selector(wake_button, timeout=8000)
                print("App asleep → waking up...")
                page.click(wake_button)

                page.wait_for_timeout(8000)
                print("Wake-up completed (assumed success)")

            except TimeoutError:
                print("App already active.")

        except Exception as e:
            print("Error:", e)
            raise

        finally:
            browser.close()


if __name__ == "__main__":
    run()