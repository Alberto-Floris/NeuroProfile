import os
from playwright.sync_api import sync_playwright


def run():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        url = os.getenv("APP_URL", "https://quizpygym.streamlit.app/")
        print(f"Visito: {url}")
        page.goto(url, timeout=60_000)

        button_selector = 'button:has-text("Yes, get this app back up!")'

        try:
            page.wait_for_selector(button_selector, timeout=15_000)
            page.click(button_selector)
            print("App era in sleep → risvegliata con successo!")
        except Exception as e:
            if "Timeout" in type(e).__name__:
                print("App già attiva, nessuna azione necessaria.")
            else:
                raise

        browser.close()


if __name__ == "__main__":
    run()