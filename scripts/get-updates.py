import requests
import base64
from bs4 import BeautifulSoup

all_updates = []

def get_updates(codename: str, release_code: str):
    base_response = requests.get(
        f"https://api.dariaos.com/ota/api/v1/{codename}/RELEASE/{release_code}/SOMETHING").json()
    
    if len(base_response["response"]) == 0:
        return

    response = base_response["response"][0]
    print(f"found {response['incremental']}")

    response["changes"] = base64.b64decode(response["changes"])
        
    all_updates.append(response)

    get_updates(codename, response["incremental"])

# Get DariaOS 4 -> 5 Updates
os4_updates = get_updates("zahedan", "V4.81.1.0.BOND")

updates_html = []

for update in all_updates:
    size_gb = update["size"] / (1024 ** 3)
    updates_html.append(f"""
                        <details>
                        <summary>DariaOS {update["version"]} - {update["incremental"]}</summary>

                        <h3>Download: <a href="{update["url"]}">{update["filename"]}</a></h3>
                        
                        <p>File Size: {size_gb:.2f} GB - md5sum: {update["md5sum"]} - API Level {update["api_level"]} - Channel: {update["channel"]} - Type: {update["updatetype"]}</p>

                        <h3>Changelog:</h3>
                        {update["changes"].decode("utf-8")}
                        </details>
                        """)

final_html = """
# بارگیری رام رسمی
"""

updates_html = "\n".join(updates_html)
soup = BeautifulSoup(updates_html, "html.parser")
updates_html = soup.prettify()

final_html += updates_html

with open("docs/official-rom.md", "w") as f:
    f.write(final_html)