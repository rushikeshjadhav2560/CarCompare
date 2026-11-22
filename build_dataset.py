"""Build data/cars.json from car_catalog.py and download one photo per model.

Run:  python build_dataset.py            (downloads missing images)
      python build_dataset.py --offline  (rebuild JSON only, no network)

Photos come from Wikipedia / Wikimedia Commons (freely licensed). The author
and licence of every photo is saved with the car so the site can credit it.
Image lookups are cached in data/images.json, so re-runs are fast.
"""
import json
import re
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor
import urllib.error
import urllib.parse
import urllib.request
from html import unescape
from pathlib import Path

from car_catalog import MODELS, trims_for

ROOT = Path(__file__).parent
DATA_DIR = ROOT / "data"
IMG_DIR = ROOT / "static" / "images" / "cars"
CACHE_FILE = DATA_DIR / "images.json"
OUT_FILE = DATA_DIR / "cars.json"

API = "https://en.wikipedia.org/w/api.php"
COMMONS_API = "https://commons.wikimedia.org/w/api.php"
HEADERS = {"User-Agent": "CarCompareStudentProject/1.0 (educational car comparison demo)"}

# Fuel prices (INR) used to estimate running cost per km.
FUEL_PRICE = {"Petrol": 103, "Diesel": 90, "CNG": 85, "Hybrid": 103}
ELECTRICITY_PER_KWH = 8

# Features unlocked by a model's equipment tier (1 = basic, 5 = loaded).
FEATURE_TIERS = [
    ("powerWindows", 1), ("touchscreen", 2), ("smartphone", 2), ("rearCamera", 2),
    ("autoClimate", 3), ("cruiseControl", 3), ("sunroof", 3), ("connectedCar", 3),
    ("wirelessCharging", 3), ("camera360", 4), ("ventilatedSeats", 4), ("adas", 4),
    ("panoramicSunroof", 5), ("premiumAudio", 5), ("poweredSeats", 5),
]


def slug(text):
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def fetch(url, timeout=60, attempts=6):
    """GET a URL, waiting and retrying when Wikimedia says 'too many requests'."""
    for attempt in range(1, attempts + 1):
        try:
            req = urllib.request.Request(url, headers=HEADERS)
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                return resp.read()
        except urllib.error.HTTPError as exc:
            if exc.code not in (429, 503) or attempt == attempts:
                raise
            wait = int(exc.headers.get("Retry-After") or 0) or 10 * attempt
            print(f"  .. rate limited, waiting {wait}s")
            time.sleep(wait)


def get_json(url, params):
    query = urllib.parse.urlencode({**params, "format": "json", "formatversion": 2})
    return json.loads(fetch(f"{url}?{query}", timeout=30))


def strip_html(text):
    return re.sub(r"\s+", " ", unescape(re.sub(r"<[^>]+>", "", text or ""))).strip()


# Photos known to show the wrong car/generation - never use these.
REJECT_FILES = {
    'Mercedes_GLC_F-Cell_IMG_0063.jpg',
    'Audi_A4_B6_TDI_Cabrio_(2019-03-27_Sp_r).JPG',
    'BJEV_EC3_2023010702.jpg',
    '2011_Toyota_Corolla_Rumion_1.5X_Aerotourer_black_rear.jpg',
    'Citroen_C3_Aircross_(2017)_Facelift_1X7A7061.jpg',
    'DTM_Audi_A4_Tomczyk09_amk.jpg',
    'Audi_A6_Avant_e-tron_DSC_7425.jpg',
    'Mercedes_Benz_E-Class_W210_Police_Bahrain.jpg',
    'Mercedes-Benz_C-Class_All-Terrain_IMG_0290.jpg',
    'Mercedes-Benz_Concept_GLC_Coupe_IAA_2015.jpg',
    'MG_Comet_EV_Inside.jpg',
    'MG_hector_classic_car..jpg',
    '2007_Toyota_Corolla-Rumion_01.jpg',
    '2020_Citroën_C3_(3rd_generation)_DSC_7374.jpg',
    '2024_Citroen_e-C3.jpg',
    'Citroen_C3_Aircross_(2017)_Facelift_1X7A7060.jpg',
    "Suzuki_Alto_800_GL_2011.jpg", "Suzuki_logo_2025_(vertical).svg",
    "2022_Citroën_C5_Aircross_Automesse_Ludwigsburg_2024_IMG_1342.jpg",
    "2018_Suzuki_Vitara_(LY)_S_Turbo_wagon_(2018-11-02)_01.jpg",
    "Tata_Safari_II_front_-_PSM_2009.jpg", "2019_Hyundai_Accent_1.6L,_front_10.8.19.jpg",
    "Suzuki_Baleno_front_20071004.jpg", "Hyundai_i10_1.0_Intro_(III)_–_f_03012021.jpg",
    "Suzuki_Ertiga_NC_FL_1.5_GLX_Hybrid_Snow_White_Pearl.jpg",
}
# Extra words for the Commons search when the plain name finds older models.
SEARCH_HINTS = {
    "maruti-suzuki-baleno": "2022", "tata-safari": "2021", "hyundai-verna": "2023",
    "maruti-suzuki-alto-k10": "2022", "hyundai-grand-i10-nios": "India",
}
# Words in a model name that a photo's file name doesn't need to contain.
GENERIC_WORDS = {"ev", "electric", "n", "line", "lwb", "plus", "classic", "limousine",
                 "gran", "series", "pro", "legender", "e", "hev"}
NOT_A_CAR_PHOTO = ("logo", "interior", "dashboard", "engine", "badge", "emblem", "cockpit",
                   "steering", "seat", "map", "diagram")


# Models whose older generations look very different: the photo's file name
# must contain a year at least this recent.
MIN_YEAR = {
    "hyundai-verna": 2023, "tata-safari": 2021, "maruti-suzuki-baleno": 2022,
    "maruti-suzuki-alto-k10": 2022, "maruti-suzuki-swift": 2024, "maruti-suzuki-dzire": 2024,
    "honda-city": 2020, "honda-amaze": 2024, "toyota-fortuner": 2016, "mahindra-scorpio-n": 2022,
    "mahindra-thar": 2020, "renault-kwid": 2019, "maruti-suzuki-celerio": 2021,
}


def name_matches(file_name, model, min_year=None):
    """True if a photo's file name mentions the model, e.g. 'Hyundai_Creta_2024.png'."""
    if min_year:
        years = [int(y) for y in re.findall(r"(?<!\d)(?:19|20)\d\d(?!\d)", file_name)]
        if not years or max(years) < min_year:
            return False
    text = re.sub(r"[^a-z0-9]+", " ", file_name.lower())
    squashed = text.replace(" ", "")
    if file_name in REJECT_FILES or file_name.lower().endswith(".svg"):
        return False
    if any(word in text for word in NOT_A_CAR_PHOTO):
        return False
    tokens = [t for t in re.split(r"[^a-z0-9]+", model["name"].lower())
              if t and t not in GENERIC_WORDS]
    return all(t in text or t in squashed for t in tokens)


def wikipedia_lead_image(title, model, min_year=None):
    data = get_json(API, {"action": "query", "titles": title, "redirects": 1,
                          "prop": "pageimages", "piprop": "thumbnail|name",
                          "pithumbsize": 1000})
    for page in data.get("query", {}).get("pages", []):
        if page.get("pageimage") and page.get("thumbnail") and name_matches(page["pageimage"], model, min_year):
            return page["pageimage"], page["thumbnail"]["source"], page["title"]
    return None


def commons_search_image(query, model, min_year=None):
    data = get_json(COMMONS_API, {"action": "query", "generator": "search",
                                  "gsrsearch": f"{query} filetype:bitmap", "gsrnamespace": 6,
                                  "gsrlimit": 15, "prop": "imageinfo",
                                  "iiprop": "url", "iiurlwidth": 1000})
    pages = sorted(data.get("query", {}).get("pages", []), key=lambda p: p.get("index", 99))
    for page in pages:
        file_name = page["title"].removeprefix("File:").replace(" ", "_")
        info = (page.get("imageinfo") or [{}])[0]
        if info.get("thumburl") and name_matches(file_name, model, min_year):
            return file_name, info["thumburl"], "Wikimedia Commons search"
    return None


def find_page_image(model_id, model):
    """Return (file_name, thumb_url, source_page) for a photo of this model, or Nones."""
    min_year = MIN_YEAR.get(model_id)
    found = wikipedia_lead_image(model["wiki"], model, min_year)
    if not found:
        hint = SEARCH_HINTS.get(model_id, "")
        brand = model["brand"]
        for query in (f'{brand} {model["name"]} {hint}'.strip(), f'{brand} {model["name"]}',
                      f'{model["name"]} car'):
            found = commons_search_image(query, model, min_year)
            if found:
                break
    return found or (None, None, None)


def image_credit(file_name):
    data = get_json(COMMONS_API, {"action": "query", "titles": f"File:{file_name}",
                                  "prop": "imageinfo", "iiprop": "extmetadata|url"})
    pages = data.get("query", {}).get("pages", [])
    info = (pages[0].get("imageinfo") or [{}])[0] if pages else {}
    meta = info.get("extmetadata", {})
    return {
        "author": strip_html(meta.get("Artist", {}).get("value", "")) or "Unknown",
        "license": strip_html(meta.get("LicenseShortName", {}).get("value", "")) or "See source",
        "source": info.get("descriptionurl", f"https://commons.wikimedia.org/wiki/File:{file_name}"),
    }


def download(url, dest):
    dest.write_bytes(fetch(url))


def fetch_image(model_id, model, cache):
    """Look up, download and cache the photo for one model."""
    if model_id in cache and (ROOT / cache[model_id]["path"]).exists():
        return cache[model_id]
    file_name, thumb, page = find_page_image(model_id, model)
    if not thumb:
        return None
    ext = Path(urllib.parse.urlparse(thumb).path).suffix.lower() or ".jpg"
    dest = IMG_DIR / f"{model_id}{ext}"
    download(thumb, dest)
    entry = {"path": dest.relative_to(ROOT).as_posix(), "file": file_name,
             "page": page, **image_credit(file_name)}
    cache[model_id] = entry
    time.sleep(0.3)  # small pause to stay polite to Wikimedia servers
    return entry


def running_cost(fuel, engine, mileage):
    """Approximate fuel/energy cost in INR per km."""
    if fuel == "Electric":
        return round(engine * ELECTRICITY_PER_KWH / mileage, 2)
    return round(FUEL_PRICE[fuel] / mileage, 2)


def build():
    offline = "--offline" in sys.argv
    DATA_DIR.mkdir(exist_ok=True)
    IMG_DIR.mkdir(parents=True, exist_ok=True)
    cache = json.loads(CACHE_FILE.read_text(encoding="utf-8")) if CACHE_FILE.exists() else {}

    if not offline:
        # Download missing photos 4 at a time.
        todo = [(slug(f'{m["brand"]} {m["name"]}'), m) for m in MODELS]
        todo = [(mid, m) for mid, m in todo
                if not (mid in cache and (ROOT / cache[mid]["path"]).exists())]
        print(f"{len(todo)} models need a photo")
        lock = threading.Lock()

        def work(item):
            mid, m = item
            try:
                fetch_image(mid, m, cache)
                status = "ok" if mid in cache else "no photo found"
            except Exception as exc:  # keep going if one lookup fails
                status = f"error: {exc}"
            with lock:
                work.done += 1
                print(f"[{work.done:3}/{len(todo)}] {m['brand']} {m['name']}: {status}")
                CACHE_FILE.write_text(json.dumps(cache, indent=2), encoding="utf-8")
        work.done = 0
        with ThreadPoolExecutor(max_workers=4) as pool:
            list(pool.map(work, todo))

    cars = []
    for model in MODELS:
        model_id = slug(f'{model["brand"]} {model["name"]}')
        image = cache.get(model_id)

        trims = trims_for(model)
        levels = TRIM_LEVELS[len(trims)]
        luxury = model["variants"][0][-1] >= 40
        steps = TRIM_PRICE_STEP_LUXURY if luxury else TRIM_PRICE_STEP
        for label, fuel, trans, engine, power, torque, mileage, lakh in model["variants"]:
            # Which trims offer this powertrain: automatics usually skip the base
            # trim, CNG usually skips the top trim.
            offered = list(range(len(trims)))
            if len(trims) == 3 and trans != "Manual" and fuel != "Electric":
                offered = offered[1:]
            if fuel == "CNG" and len(offered) > 1:
                offered = offered[:-1]
            first = offered[0]
            for t in offered:
                trim, level = trims[t], levels[t]
                # The catalogue price is the cheapest trim offering this powertrain.
                price = lakh * 100000 * steps[t] / steps[first]
                tier = max(1, model["tier"] - (len(trims) - 1 - t))
                features = [key for key, need in FEATURE_TIERS if tier >= need]
                airbags = model["airbags"] if level == "Top" else min(model["airbags"], 6)
                cars.append(make_car(model, model_id, image, trim, level, label, fuel, trans,
                                     engine, power, torque, mileage, price, features, airbags))

    OUT_FILE.write_text(json.dumps(cars, indent=1, ensure_ascii=False), encoding="utf-8")
    with_img = sum(1 for c in cars if c["image"])
    print(f"\nSaved {len(cars)} cars from {len(MODELS)} models -> {OUT_FILE}")
    print(f"Cars with photos: {with_img}/{len(cars)}")


# Base / Mid / Top labels by number of trims, and price step between trims.
TRIM_LEVELS = {1: ["Top"], 2: ["Base", "Top"], 3: ["Base", "Mid", "Top"]}
TRIM_PRICE_STEP = [1.0, 1.14, 1.30]
TRIM_PRICE_STEP_LUXURY = [1.0, 1.09, 1.18]


def make_car(model, model_id, image, trim, level, label, fuel, trans, engine, power,
             torque, mileage, price, features, airbags):
    electric = fuel == "Electric"
    return {
                "id": slug(f"{model_id} {trim} {label}"),
                "modelId": model_id,
                "brand": model["brand"],
                "name": model["name"],
                "variant": f"{trim} {label}",
                "trim": trim,
                "trimLevel": level,
                "powertrain": label,
                "year": 2025,
                "price": int(round(price, -3)),
                "bodyType": model["body"],
                "fuelType": fuel,
                "transmission": trans,
                "engine": f"{engine} kWh battery" if electric else f"{engine} cc",
                "engineCc": None if electric else engine,
                "batteryKwh": engine if electric else None,
                "power": power,
                "torque": torque,
                "mileage": mileage,
                "mileageUnit": {"Electric": "km range", "CNG": "km/kg"}.get(fuel, "km/l"),
                "runningCost": running_cost(fuel, engine, mileage),
                "seating": model["seats"],
                "airbags": airbags,
                "ncap": model["ncap"],
                "length": model["length"],
                "bootSpace": model["boot"],
                "fuelTank": None if electric else model["tank"],
                "groundClearance": model["gc"],
                "features": features,
                "description": model["desc"],
                "image": f'/{image["path"]}' if image else None,
                "imageCredit": {k: image[k] for k in ("author", "license", "source")} if image else None,
    }


if __name__ == "__main__":
    build()
