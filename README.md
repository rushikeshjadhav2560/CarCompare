# CarCompare – Vehicle Comparison

A Python (Flask) website for exploring and comparing **270+ cars** (140+ models, 25+ brands) from the Indian market, each with a real photo.

## Features
- **Compare** engine, power, torque, mileage/range, running cost, price, size, safety and 15 features for 2–3 cars side by side. The best value in each row is highlighted.
- **Browse by body type**: hatchbacks, sedans, SUVs, MUVs and pickups. Filter by brand, fuel (Petrol / Diesel / CNG / Hybrid / Electric), gearbox and price, and sort the results.
- **Recommend cars for a budget**: pick a budget, body type, fuel, seats and priority (balanced, running cost, performance, features, price). The app scores every car in range and explains each pick.
- **Save favourite comparisons**: saved in the browser and reopened with one click.
- **Image-first design**: photo cards, a rotating hero slideshow, a detail popup with a large photo, every variant and full specs, and photos in the comparison table.

## Run it (Windows, VS Code)
```
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python app.py
```
Open http://127.0.0.1:5000

`data/cars.json` and the photos in `static/images/cars/` are already included, so you don't need internet access to run the site (except for Google Fonts).

## Project structure
```
CarCompare/
├── app.py               Flask app + JSON APIs + recommendation engine
├── car_catalog.py       Master list of models and their variants (edit cars here)
├── build_dataset.py     Builds data/cars.json and downloads one photo per model
├── data/
│   ├── cars.json        Generated car dataset (274 cars)
│   └── images.json      Photo cache (file name, author, licence, source)
├── static/
│   ├── images/cars/     Downloaded car photos
│   ├── css/style.css
│   └── js/script.js
└── templates/index.html
```

## Adding or editing cars
1. Edit `car_catalog.py`: add a model with `M(...)` and its variants.
2. Run `python build_dataset.py`. It rebuilds `data/cars.json` and downloads photos only for new models. Use `--offline` to skip downloads.
3. Restart `python app.py`.

## API endpoints
| Endpoint | Description |
|---|---|
| `GET /api/models?q=&brand=&fuel=&body=&transmission=&maxPrice=&sort=` | One entry per model (price range, fuels, variant count) for the Explore grid |
| `GET /api/cars?q=&brand=&fuel=&body=&transmission=&maxPrice=&sort=` | Search and filter individual variants |
| `GET /api/cars/<id>` | One car plus all variants of its model |
| `GET /api/meta` | Counts, brands, body types, fuel types, feature labels |
| `GET /api/compare?ids=a,b,c` | 2–3 cars for comparison |
| `GET /api/recommend?budget=&body=&fuel=&seats=&priority=` | Top 6 recommendations |

## How the recommendation works
For every car within 40–100% of the budget, the app measures four things: **running cost** (₹/km from mileage and fuel price), **power**, **features** (feature count + airbags + safety rating) and **value** (money left from the budget). Each is scaled from 0 to 1 against the other candidates and combined using weights for the chosen priority. Only the best variant of each model is shown, so the results stay varied.

## Data and photo credits
- Prices and specifications are **approximate, illustrative values** for a student project. Check official manufacturer sources before relying on them.
- Car photos come from **Wikimedia Commons** under free licences (mostly CC BY-SA). The author and licence of each photo appear in the car's detail popup and are stored in `data/images.json`. Some photos show a different model year or market version of the car.
