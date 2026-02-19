import subprocess
import time
from playwright.sync_api import sync_playwright

def verify_pwa():
    # Start a simple HTTP server in the background
    server_process = subprocess.Popen(["python3", "-m", "http.server", "8080"])

    # Give the server a moment to start
    time.sleep(2)

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            # Navigate to the app
            page.goto("http://localhost:8080/")

            # Check for manifest link
            manifest_link = page.locator('link[rel="manifest"]')
            if manifest_link.count() > 0:
                print("Manifest link found.")
            else:
                print("Manifest link NOT found.")

            # Take a screenshot
            page.screenshot(path="verification/pwa_screenshot.png")
            print("Screenshot taken.")

            # Check if title is correct
            title = page.title()
            print(f"Page title: {title}")

    finally:
        # Kill the server
        server_process.kill()

if __name__ == "__main__":
    verify_pwa()
