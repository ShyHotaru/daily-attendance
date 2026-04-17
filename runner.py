import datetime
import json
import webbrowser

from catalog import full_catalog
from paths import FLAGS_DIR, SELECTED_FILE


def run() -> None:
    FLAGS_DIR.mkdir(parents=True, exist_ok=True)
    today = datetime.date.today().strftime("%Y%m%d")
    today_flag = FLAGS_DIR / f"{today}.flag"

    for f in FLAGS_DIR.glob("*.flag"):
        if f.name != today_flag.name:
            try:
                f.unlink()
            except OSError:
                pass

    if today_flag.exists() or not SELECTED_FILE.exists():
        return

    with open(SELECTED_FILE, encoding="utf-8") as f:
        selected_ids = json.load(f)

    catalog = {g["id"]: g for g in full_catalog()}
    for gid in selected_ids:
        game = catalog.get(gid)
        if game:
            webbrowser.open(game["url"])

    today_flag.write_text("opened", encoding="utf-8")
