import json
from pathlib import Path

from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

DATA_FILE = Path(__file__).parent / "data" / "cars.json"
if not DATA_FILE.exists():
    raise SystemExit("data/cars.json not found. Run:  python build_dataset.py")
CARS = json.loads(DATA_FILE.read_text(encoding="utf-8"))
CARS_BY_ID = {c["id"]: c for c in CARS}

FEATURES = {
    "powerWindows": "Power windows",
    "touchscreen": "Touchscreen infotainment",
    "smartphone": "Android Auto / Apple CarPlay",
    "rearCamera": "Rear parking camera",
    "autoClimate": "Automatic climate control",
    "cruiseControl": "Cruise control",
    "sunroof": "Sunroof",
    "connectedCar": "Connected car tech",
    "wirelessCharging": "Wireless phone charger",
    "camera360": "360° camera",
    "ventilatedSeats": "Ventilated front seats",
    "adas": "ADAS (driver assistance)",
    "panoramicSunroof": "Panoramic sunroof",
    "premiumAudio": "Premium sound system",
    "poweredSeats": "Powered driver seat",
}

SORTS = {
    "price_asc": (lambda c: c["price"], False),
    "price_desc": (lambda c: c["price"], True),
    "power": (lambda c: c["power"], True),
    "economy": (lambda c: c["runningCost"], False),
    # Default: cars with photos first, then brand A–Z.
    "name": (lambda c: (c["image"] is None, c["brand"], c["name"], c["price"]), False),
}


def int_arg(name, default=0):
    try:
        return int(request.args.get(name, default))
    except ValueError:
        return default


def matches(car, q="", brand="", fuel="", body="", transmission="", trim="", min_price=0, max_price=0):
    text = f'{car["brand"]} {car["name"]} {car["variant"]} {car["fuelType"]}'.lower()
    return ((not q or all(word in text for word in q.split()))
            and (not brand or car["brand"].lower() == brand)
            and (not fuel or car["fuelType"].lower() == fuel)
            and (not body or car["bodyType"].lower() == body)
            and (not transmission or car["transmission"].lower() == transmission)
            and (not trim or car["trimLevel"].lower() == trim)
            and car["price"] >= min_price
            and (not max_price or car["price"] <= max_price))


@app.route("/")
def home():
    return render_template("index.html")


@app.get("/api/cars")
def cars():
    args = {k: request.args.get(k, "").strip().lower()
            for k in ("q", "brand", "fuel", "body", "transmission", "trim")}
    items = [c for c in CARS if matches(c, **args, min_price=int_arg("minPrice"),
                                        max_price=int_arg("maxPrice"))]
    key, reverse = SORTS.get(request.args.get("sort", ""), SORTS["name"])
    return jsonify(sorted(items, key=key, reverse=reverse))


MODEL_SORTS = {
    "price_asc": (lambda m: m["priceMin"], False),
    "price_desc": (lambda m: m["priceMax"], True),
    "power": (lambda m: m["powerMax"], True),
    "economy": (lambda m: m["runningCostMin"], False),
    "name": (lambda m: (m["image"] is None, m["brand"], m["name"]), False),
}


def summarise_model(variants):
    """One card's worth of data for a model, built from its (matching) variants."""
    first = variants[0]
    unique = lambda key: sorted({v[key] for v in variants})
    return {
        "modelId": first["modelId"],
        "brand": first["brand"],
        "name": first["name"],
        "bodyType": first["bodyType"],
        "description": first["description"],
        "image": first["image"],
        "seating": first["seating"],
        "ncap": first["ncap"],
        "priceMin": min(v["price"] for v in variants),
        "priceMax": max(v["price"] for v in variants),
        "powerMin": min(v["power"] for v in variants),
        "powerMax": max(v["power"] for v in variants),
        "runningCostMin": min(v["runningCost"] for v in variants),
        "fuelTypes": unique("fuelType"),
        "trims": [t for t in ("Base", "Mid", "Top") if any(v["trimLevel"] == t for v in variants)],
        "transmissions": unique("transmission"),
        "variantCount": len(variants),
        # Cheapest matching variant is what "+ Compare" adds from the card.
        "defaultVariantId": min(variants, key=lambda v: v["price"])["id"],
    }


@app.get("/api/models")
def models():
    """Same filters as /api/cars, but grouped into one entry per model."""
    args = {k: request.args.get(k, "").strip().lower()
            for k in ("q", "brand", "fuel", "body", "transmission", "trim")}
    grouped = {}
    for car in CARS:
        if matches(car, **args, min_price=int_arg("minPrice"), max_price=int_arg("maxPrice")):
            grouped.setdefault(car["modelId"], []).append(car)
    items = [summarise_model(v) for v in grouped.values()]
    key, reverse = MODEL_SORTS.get(request.args.get("sort", ""), MODEL_SORTS["name"])
    return jsonify(sorted(items, key=key, reverse=reverse))


@app.get("/api/cars/<car_id>")
def car_detail(car_id):
    car = CARS_BY_ID.get(car_id)
    if not car:
        return jsonify({"error": "Car not found."}), 404
    siblings = sorted((c for c in CARS if c["modelId"] == car["modelId"]), key=lambda c: c["price"])
    return jsonify({"car": car, "variants": siblings})


@app.get("/api/meta")
def meta():
    return jsonify({
        "count": len(CARS),
        "models": len({c["modelId"] for c in CARS}),
        "brands": sorted({c["brand"] for c in CARS}),
        "bodyTypes": sorted({c["bodyType"] for c in CARS}),
        "fuelTypes": sorted({c["fuelType"] for c in CARS}),
        "transmissions": sorted({c["transmission"] for c in CARS}),
        "trimLevels": ["Base", "Mid", "Top"],
        "features": FEATURES,
    })


@app.get("/api/compare")
def compare():
    ids = [value for value in request.args.get("ids", "").split(",") if value]
    if not 2 <= len(ids) <= 3:
        return jsonify({"error": "Select between 2 and 3 cars to compare."}), 400
    selected = [CARS_BY_ID[i] for i in ids if i in CARS_BY_ID]
    if len(selected) != len(ids):
        return jsonify({"error": "One or more selected cars were not found."}), 404
    return jsonify(selected)


# How much each metric counts for each buying priority (weights add up to 1).
PRIORITY_WEIGHTS = {
    "balanced":    {"economy": .30, "power": .25, "features": .25, "value": .20},
    "economy":     {"economy": .60, "power": .10, "features": .15, "value": .15},
    "performance": {"economy": .10, "power": .60, "features": .15, "value": .15},
    "features":    {"economy": .15, "power": .10, "features": .60, "value": .15},
    "value":       {"economy": .20, "power": .10, "features": .10, "value": .60},
}


@app.get("/api/recommend")
def recommend():
    budget = int_arg("budget")
    if budget <= 0:
        return jsonify({"error": "Enter a budget greater than zero."}), 400
    body = request.args.get("body", "").strip().lower()
    fuel = request.args.get("fuel", "").strip().lower()
    seats = int_arg("seats")
    weights = PRIORITY_WEIGHTS.get(request.args.get("priority", ""), PRIORITY_WEIGHTS["balanced"])

    pool = [c for c in CARS if matches(c, body=body, fuel=fuel) and c["seating"] >= seats]
    # Only consider cars from 40% of the budget upwards, so a 30 lakh budget
    # doesn't recommend a 5 lakh hatchback.
    candidates = [c for c in pool if budget * 0.4 <= c["price"] <= budget]

    if not candidates:
        cheapest = min(pool, key=lambda c: c["price"], default=None)
        message = "No cars match these filters."
        if cheapest and cheapest["price"] > budget:
            message = (f"Nothing within your budget. The most affordable match is the "
                       f"{cheapest['brand']} {cheapest['name']} at ₹{cheapest['price']:,}.")
        elif cheapest:
            message = "Your budget is higher than every match. Try raising the filters or lowering the budget."
        return jsonify({"results": [], "message": message})

    metrics = {c["id"]: {
        "economy": -c["runningCost"],
        "power": c["power"],
        "features": len(c["features"]) + c["airbags"] / 2 + (c["ncap"] or 0),
        "value": budget - c["price"],
    } for c in candidates}

    def normalise(key):
        values = [m[key] for m in metrics.values()]
        low, high = min(values), max(values)
        return {cid: 1.0 if high == low else (m[key] - low) / (high - low)
                for cid, m in metrics.items()}

    scaled = {key: normalise(key) for key in weights}
    scored = sorted(candidates, key=lambda c: sum(weights[k] * scaled[k][c["id"]] for k in weights),
                    reverse=True)

    # Keep only the best variant of each model so results are varied.
    results, seen = [], set()
    for car in scored:
        if car["modelId"] in seen:
            continue
        seen.add(car["modelId"])
        cid = car["id"]
        reasons = []
        if scaled["economy"][cid] >= .9:
            reasons.append(f"Very low running cost (≈ ₹{car['runningCost']}/km)")
        if scaled["power"][cid] >= .8:
            reasons.append(f"Among the most powerful ({car['power']} bhp)")
        if scaled["features"][cid] >= .8:
            reasons.append(f"Loaded with features and {car['airbags']} airbags")
        if car["ncap"] == 5:
            reasons.append("5-star safety rating")
        saving = budget - car["price"]
        reasons.append(f"₹{saving:,} under your budget" if saving else "Exactly on budget")
        score = sum(weights[k] * scaled[k][cid] for k in weights)
        results.append({"car": car, "score": round(score * 100), "reasons": reasons[:4]})
        if len(results) == 6:
            break

    return jsonify({"results": results, "considered": len(candidates)})


if __name__ == "__main__":
    app.run(debug=True)
