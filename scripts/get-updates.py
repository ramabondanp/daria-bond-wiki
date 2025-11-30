import requests
import base64
import json
from bs4 import BeautifulSoup

all_server_updates = []

TRANSLATIONS = {
    "fa": {
        "title": "بارگیری رام رسمی",
        "desc_header": "توضیحات:",
        "removed_header": "رام‌های رسمی (حذف شده از سرور داریا)",
        "server_header": "رام‌های رسمی (سرور داریا)",
        "not_found": "_هیچ رام رسمی در سرور یافت نشد._",
        "download": "Download",
        "boot_recovery": "Download Boot + Recovery Image",
        "file_size": "File Size",
        "api_level": "API Level",
        "channel": "Channel",
        "type": "Type",
        "changelog": "Changelog",
        "filename": "docs/official-rom.md"
    },
    "en": {
        "title": "Official ROM Download",
        "desc_header": "Description:",
        "removed_header": "Official ROMs (Removed from Daria Server)",
        "server_header": "Official ROMs (Daria Server)",
        "not_found": "_No official ROMs found on server._",
        "download": "Download",
        "boot_recovery": "Download Boot + Recovery Image",
        "file_size": "File Size",
        "api_level": "API Level",
        "channel": "Channel",
        "type": "Type",
        "changelog": "Changelog",
        "filename": "docs/official-rom.en.md"
    }
}

def get_updates(codename: str, release_code: str):
    """Recursively fetch OTA updates from the server for a given codename and release code."""

    url = f"https://api.dariaos.com/ota/api/v1/{codename}/RELEASE/{release_code}/SOMETHING"
    try:
        base_response = requests.get(url).json()
    except Exception as e:
        print(f"Error fetching updates for {codename}: {e}")
        return

    if not base_response.get("response"):
        return

    response = base_response["response"][0]
    print(f"[{codename}] Found incremental: {response['incremental']}")

    # Decode changelog from base64
    try:
        response["changes"] = base64.b64decode(response["changes"]).decode("utf-8")
    except:
        response["changes"] = "Changelog decode failed."
        
    response["device"] = codename

    all_server_updates.append(response)

    # Recursively get previous updates
    get_updates(codename, response["incremental"])


def build_server_updates_html(updates, lang_code):
    """Generate HTML for server-hosted OTA updates."""
    t = TRANSLATIONS[lang_code]
    html_blocks = []
    for update in updates:
        size_gb = update["size"] / (1024 ** 3)
        html_blocks.append(f"""
        <details>
            <summary>DariaOS {update["version"]} - {update["incremental"]}</summary>
            <h3>{t['download']}: <a href="{update["url"]}">{update["filename"]}</a></h3>
            <p>
                {t['file_size']}: {size_gb:.2f} GB — md5sum: {update["md5sum"]} —
                {t['api_level']}: {update["api_level"]} — {t['channel']}: {update["channel"]} — {t['type']}: {update["updatetype"]}
            </p>
            <h3>{t['changelog']}:</h3>
            {update["changes"]}
        </details>
        """)
    return "\n".join(html_blocks)


def build_unlisted_updates_html(unlisted_updates, codename, lang_code):
    """Generate HTML for unlisted (manual) OTA updates filtered by codename."""
    t = TRANSLATIONS[lang_code]
    html_blocks = []
    for update in unlisted_updates:
        if update.get("device") != codename:
            continue
        size_gb = update["size"] / (1024 ** 3)
        description = update.get(f"description_{lang_code}", update.get("description_fa", ""))
        html_blocks.append(f"""
        <details {"open" if update.get("expanded", False) else ""}>
            <summary>{update["version"]}</summary>
            <h2>{t['desc_header']}</h2>
            {description}
            <h3>{t['download']}: <a href="{update["url"]}">{update["filename"]}</a></h3>
            {f'<h3>{t["boot_recovery"]}: <a href="{update["boot_img"]}">boot.img</a></h3>' if update.get("boot_img") else ""}
            <p>
                {t['file_size']}: {size_gb:.2f} GB — md5sum: {update["md5sum"]} —
                {t['api_level']}: {update["api_level"]} — {t['type']}: {update.get("updatetype", "N/A")}
            </p>
        </details>
        """)
    return "\n".join(html_blocks)


def generate_page(lang_code, devices, unlisted_updates):
    t = TRANSLATIONS[lang_code]
    final_html = f"# {t['title']}\n\n"

    for codename, info in devices.items():
        device_updates = [u for u in all_server_updates if u["device"] == codename]
        server_updates_html = build_server_updates_html(device_updates, lang_code)
        unlisted_updates_html = build_unlisted_updates_html(unlisted_updates, codename, lang_code)

        final_html += f"\n## {info['name']} ({codename})\n"
        if unlisted_updates_html:
            final_html += f"\n### {t['removed_header']}\n"
            final_html += unlisted_updates_html
        final_html += f"\n\n### {t['server_header']}\n"
        final_html += server_updates_html or t['not_found']

    # Beautify with BeautifulSoup
    final_html = BeautifulSoup(final_html, "html.parser").prettify()

    with open(t['filename'], "w", encoding="utf-8") as f:
        f.write(final_html)
    print(f"Output saved to {t['filename']}")


def main():
    devices = {
        "zahedan": {"name": "Daria Bond I", "release": "V0.00.0.0.BOND"},
        "hormoz": {"name": "Daria Bond II", "release": "V0.00.0.0.BOND2"},
        "qoqnoos": {"name": "Daria Bond II Lite", "release": "V0.00.0.0.BOND2L"}
    }

    with open("scripts/unlisted_updates.json", "r") as f:
        unlisted_updates = json.load(f).get("unlisted_updates", [])

    # Fetch updates once
    for codename, info in devices.items():
        print(f"\n=== Fetching updates for {info['name']} ({codename}) ===")
        get_updates(codename, info["release"])

    # Generate pages for both languages
    for lang in ["fa", "en"]:
        generate_page(lang, devices, unlisted_updates)

    print("\nDone!")


if __name__ == "__main__":
    main()
