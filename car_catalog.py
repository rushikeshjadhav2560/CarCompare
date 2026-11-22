"""CarCompare master catalogue (Indian market, 2025).

Each model has shared specs (body, size, safety) and one or more powertrain
variants. `build_dataset.py` expands every variant into its own car record,
so a model with 3 variants becomes 3 comparable cars.

Variant tuple:
    (label, fuel, transmission, engine, power_bhp, torque_nm, mileage, price_lakh)
      - engine  : displacement in cc, or battery size in kWh for Electric
      - mileage : km/l (Petrol/Diesel/Hybrid), km/kg (CNG), or range in km (Electric)

NOTE: Prices and specs are approximate, illustrative values for a student
project. Verify with official manufacturer sources before relying on them.
"""


def M(brand, name, wiki, body, seats, airbags, ncap, length, boot, tank, gc,
      tier, desc, variants):
    return {
        "brand": brand, "name": name, "wiki": wiki, "body": body,
        "seats": seats, "airbags": airbags, "ncap": ncap, "length": length,
        "boot": boot, "tank": tank, "gc": gc, "tier": tier, "desc": desc,
        "variants": variants,
    }


P, D, C, E, H = "Petrol", "Diesel", "CNG", "Electric", "Hybrid"

MODELS = [
    # ------------------------------------------------------------ MARUTI SUZUKI
    M("Maruti Suzuki", "Alto K10", "Maruti Suzuki Alto K10", "Hatchback", 5, 6, None, 3530, 214, 27, 160, 1,
      "India's most affordable entry hatchback, easy to drive and cheap to run.", [
        ("1.0 Petrol MT", P, "Manual", 998, 66, 89, 24.39, 3.70),
        ("1.0 Petrol AGS", P, "AMT", 998, 66, 89, 24.90, 5.31),
        ("1.0 CNG MT", C, "Manual", 998, 56, 82, 33.85, 5.90)]),
    M("Maruti Suzuki", "S-Presso", "Maruti Suzuki S-Presso", "Hatchback", 5, 6, None, 3565, 240, 27, 180, 1,
      "A tall-boy micro hatch with SUV-like seating position.", [
        ("1.0 Petrol MT", P, "Manual", 998, 66, 89, 24.12, 4.27),
        ("1.0 Petrol AGS", P, "AMT", 998, 66, 89, 25.30, 5.21),
        ("1.0 CNG MT", C, "Manual", 998, 56, 82, 32.73, 5.92)]),
    M("Maruti Suzuki", "Celerio", "Maruti Suzuki Celerio", "Hatchback", 5, 6, None, 3695, 313, 32, 170, 2,
      "A frugal city hatchback with one of the best mileage figures in India.", [
        ("1.0 Petrol MT", P, "Manual", 998, 66, 89, 25.24, 5.64),
        ("1.0 Petrol AGS", P, "AMT", 998, 66, 89, 26.68, 6.39),
        ("1.0 CNG MT", C, "Manual", 998, 56, 82, 34.43, 6.89)]),
    M("Maruti Suzuki", "WagonR", "Maruti Suzuki Wagon R", "Hatchback", 5, 6, None, 3655, 341, 32, 165, 2,
      "A practical, roomy family hatchback with a big boot.", [
        ("1.0 Petrol MT", P, "Manual", 998, 66, 89, 24.35, 5.79),
        ("1.2 Petrol AGS", P, "AMT", 1197, 89, 113, 24.43, 6.94),
        ("1.0 CNG MT", C, "Manual", 998, 56, 82, 34.05, 6.89)]),
    M("Maruti Suzuki", "Swift", "Suzuki Swift", "Hatchback", 5, 6, None, 3860, 265, 37, 163, 3,
      "A fun-to-drive hatchback with an efficient 3-cylinder Z-series engine.", [
        ("1.2 Petrol MT", P, "Manual", 1197, 81, 112, 24.80, 6.49),
        ("1.2 Petrol AGS", P, "AMT", 1197, 81, 112, 25.75, 7.80),
        ("1.2 CNG MT", C, "Manual", 1197, 69, 102, 32.85, 8.20)]),
    M("Maruti Suzuki", "Dzire", "Suzuki Dzire", "Sedan", 5, 6, 5, 3995, 382, 37, 163, 3,
      "India's best-selling compact sedan, now with a 5-star safety rating.", [
        ("1.2 Petrol MT", P, "Manual", 1197, 81, 112, 24.79, 6.84),
        ("1.2 Petrol AGS", P, "AMT", 1197, 81, 112, 25.71, 8.24),
        ("1.2 CNG MT", C, "Manual", 1197, 69, 102, 33.73, 8.79)]),
    M("Maruti Suzuki", "Baleno", "Suzuki Baleno", "Hatchback", 5, 6, None, 3990, 318, 37, 170, 3,
      "A spacious premium hatchback with head-up display and 360 camera.", [
        ("1.2 Petrol MT", P, "Manual", 1197, 89, 113, 22.35, 6.70),
        ("1.2 Petrol AGS", P, "AMT", 1197, 89, 113, 22.94, 7.95),
        ("1.2 CNG MT", C, "Manual", 1197, 77, 98, 30.61, 8.45)]),
    M("Maruti Suzuki", "Ignis", "Suzuki Ignis", "Hatchback", 5, 6, None, 3700, 260, 32, 180, 2,
      "A quirky, compact urban crossover hatch.", [
        ("1.2 Petrol MT", P, "Manual", 1197, 82, 113, 20.89, 5.85),
        ("1.2 Petrol AGS", P, "AMT", 1197, 82, 113, 20.89, 6.90)]),
    M("Maruti Suzuki", "Fronx", "Suzuki Fronx", "SUV", 5, 6, None, 3995, 308, 37, 190, 3,
      "A coupe-styled crossover with an optional turbo-petrol engine.", [
        ("1.2 Petrol MT", P, "Manual", 1197, 89, 113, 21.79, 7.59),
        ("1.0 Turbo Petrol AT", P, "Automatic", 998, 99, 148, 20.01, 11.98),
        ("1.2 CNG MT", C, "Manual", 1197, 77, 98, 28.51, 8.54)]),
    M("Maruti Suzuki", "Brezza", "Maruti Suzuki Brezza", "SUV", 5, 6, 4, 3995, 328, 48, 198, 3,
      "A practical compact SUV with low running costs.", [
        ("1.5 Petrol MT", P, "Manual", 1462, 102, 137, 17.38, 8.69),
        ("1.5 Petrol AT", P, "Automatic", 1462, 102, 137, 19.80, 11.14),
        ("1.5 CNG MT", C, "Manual", 1462, 87, 122, 25.51, 9.64)]),
    M("Maruti Suzuki", "Grand Vitara", "Maruti Suzuki Grand Vitara", "SUV", 5, 6, None, 4345, 373, 45, 210, 4,
      "A mid-size SUV with a strong-hybrid option that returns 27+ km/l.", [
        ("1.5 Petrol MT", P, "Manual", 1462, 102, 137, 21.11, 11.42),
        ("1.5 Petrol AT", P, "Automatic", 1462, 102, 137, 20.58, 13.67),
        ("1.5 Strong Hybrid eCVT", H, "Automatic", 1490, 114, 122, 27.97, 16.99),
        ("1.5 CNG MT", C, "Manual", 1462, 87, 122, 26.60, 13.48)]),
    M("Maruti Suzuki", "Ertiga", "Suzuki Ertiga", "MUV", 7, 6, 3, 4395, 209, 45, 185, 2,
      "India's favourite 7-seater family MPV.", [
        ("1.5 Petrol MT", P, "Manual", 1462, 102, 137, 20.51, 8.97),
        ("1.5 Petrol AT", P, "Automatic", 1462, 102, 137, 20.30, 11.97),
        ("1.5 CNG MT", C, "Manual", 1462, 87, 122, 26.11, 10.88)]),
    M("Maruti Suzuki", "XL6", "Suzuki XL6", "MUV", 6, 6, None, 4445, 209, 45, 180, 3,
      "A premium 6-seater MPV with captain chairs.", [
        ("1.5 Petrol MT", P, "Manual", 1462, 102, 137, 20.97, 11.71),
        ("1.5 Petrol AT", P, "Automatic", 1462, 102, 137, 20.27, 13.31)]),
    M("Maruti Suzuki", "Ciaz", "Suzuki Ciaz", "Sedan", 5, 6, None, 4490, 510, 43, 170, 2,
      "A comfortable mid-size sedan with a huge rear seat.", [
        ("1.5 Petrol MT", P, "Manual", 1462, 103, 138, 20.65, 9.41),
        ("1.5 Petrol AT", P, "Automatic", 1462, 103, 138, 20.04, 11.15)]),
    M("Maruti Suzuki", "Jimny", "Suzuki Jimny", "SUV", 4, 6, None, 3985, 211, 40, 210, 2,
      "A compact, go-anywhere 4x4 with a ladder frame.", [
        ("1.5 Petrol MT 4x4", P, "Manual", 1462, 103, 134, 16.94, 12.76),
        ("1.5 Petrol AT 4x4", P, "Automatic", 1462, 103, 134, 16.39, 13.71)]),
    M("Maruti Suzuki", "Invicto", "Maruti Suzuki Invicto", "MUV", 7, 6, None, 4755, 239, 52, 185, 5,
      "Maruti's flagship strong-hybrid MPV.", [
        ("2.0 Strong Hybrid eCVT", H, "Automatic", 1987, 184, 188, 23.24, 25.51)]),
    M("Maruti Suzuki", "Eeco", "Maruti Suzuki Eeco", "MUV", 7, 6, None, 3675, 540, 32, 160, 1,
      "A no-frills van for families and small businesses.", [
        ("1.2 Petrol MT", P, "Manual", 1197, 80, 104, 19.71, 5.70),
        ("1.2 CNG MT", C, "Manual", 1197, 71, 95, 26.78, 6.70)]),
    M("Maruti Suzuki", "e Vitara", "Suzuki e Vitara", "SUV", 5, 7, None, 4275, 306, 0, 185, 5,
      "Maruti's first electric SUV, built on a dedicated EV platform.", [
        ("49 kWh", E, "Automatic", 49, 142, 189, 426, 17.49),
        ("61 kWh", E, "Automatic", 61, 172, 189, 543, 22.49)]),

    # ------------------------------------------------------------ HYUNDAI
    M("Hyundai", "Grand i10 Nios", "Hyundai Grand i10 Nios", "Hatchback", 5, 6, None, 3815, 260, 37, 165, 2,
      "A well-finished small hatch with a smooth engine.", [
        ("1.2 Petrol MT", P, "Manual", 1197, 82, 114, 20.70, 5.98),
        ("1.2 Petrol AMT", P, "AMT", 1197, 82, 114, 20.10, 7.28),
        ("1.2 CNG MT", C, "Manual", 1197, 68, 95, 27.00, 7.68)]),
    M("Hyundai", "i20", "Hyundai i20", "Hatchback", 5, 6, 3, 3995, 311, 37, 165, 3,
      "A premium hatchback with sunroof and connected features.", [
        ("1.2 Petrol MT", P, "Manual", 1197, 82, 115, 20.35, 7.04),
        ("1.2 Petrol IVT", P, "CVT", 1197, 87, 115, 19.65, 9.38)]),
    M("Hyundai", "i20 N Line", "Hyundai i20 N Line", "Hatchback", 5, 6, 3, 3995, 311, 37, 165, 3,
      "A sporty turbo hatch with stiffer suspension and red accents.", [
        ("1.0 Turbo Petrol DCT", P, "DCT", 998, 118, 172, 20.00, 11.10)]),
    M("Hyundai", "Aura", "Hyundai Aura", "Sedan", 5, 6, None, 3995, 402, 37, 165, 2,
      "A compact sedan with a comfortable, feature-rich cabin.", [
        ("1.2 Petrol MT", P, "Manual", 1197, 82, 114, 20.50, 6.54),
        ("1.2 Petrol AMT", P, "AMT", 1197, 82, 114, 20.10, 8.37),
        ("1.2 CNG MT", C, "Manual", 1197, 68, 95, 28.00, 7.55)]),
    M("Hyundai", "Exter", "Hyundai Exter", "SUV", 5, 6, None, 3815, 391, 37, 185, 3,
      "A micro SUV with dashcam and sunroof at an entry price.", [
        ("1.2 Petrol MT", P, "Manual", 1197, 82, 114, 19.40, 6.00),
        ("1.2 Petrol AMT", P, "AMT", 1197, 82, 114, 19.20, 7.97),
        ("1.2 CNG MT", C, "Manual", 1197, 68, 95, 27.10, 8.43)]),
    M("Hyundai", "Venue", "Hyundai Venue", "SUV", 5, 6, None, 3995, 350, 45, 190, 3,
      "A popular compact SUV with petrol, turbo and diesel options.", [
        ("1.2 Petrol MT", P, "Manual", 1197, 82, 114, 17.50, 7.94),
        ("1.0 Turbo Petrol DCT", P, "DCT", 998, 118, 172, 18.30, 11.86),
        ("1.5 Diesel MT", D, "Manual", 1493, 114, 250, 23.40, 10.71)]),
    M("Hyundai", "Venue N Line", "Hyundai Venue", "SUV", 5, 6, None, 3995, 350, 45, 190, 4,
      "The sportier, turbo-only version of the Venue.", [
        ("1.0 Turbo Petrol DCT", P, "DCT", 998, 118, 172, 18.30, 12.15)]),
    M("Hyundai", "Verna", "Hyundai Verna", "Sedan", 5, 6, 5, 4535, 528, 45, 165, 4,
      "A stylish sedan with ADAS and a powerful turbo option.", [
        ("1.5 Petrol MT", P, "Manual", 1497, 113, 144, 18.60, 11.07),
        ("1.5 Petrol IVT", P, "CVT", 1497, 113, 144, 19.60, 14.23),
        ("1.5 Turbo Petrol DCT", P, "DCT", 1482, 158, 253, 20.60, 14.93)]),
    M("Hyundai", "Creta", "Hyundai Creta", "SUV", 5, 6, None, 4330, 433, 50, 190, 4,
      "India's best-selling mid-size SUV with a huge range of engines.", [
        ("1.5 Petrol MT", P, "Manual", 1497, 113, 144, 17.40, 11.11),
        ("1.5 Petrol IVT", P, "CVT", 1497, 113, 144, 17.70, 15.37),
        ("1.5 Diesel MT", D, "Manual", 1493, 114, 250, 21.80, 12.69),
        ("1.5 Diesel AT", D, "Automatic", 1493, 114, 250, 19.10, 16.46),
        ("1.5 Turbo Petrol DCT", P, "DCT", 1482, 158, 253, 18.40, 19.99)]),
    M("Hyundai", "Creta N Line", "Hyundai Creta", "SUV", 5, 6, None, 4330, 433, 50, 190, 4,
      "A sportier Creta with the 160 PS turbo engine as standard.", [
        ("1.5 Turbo Petrol DCT", P, "DCT", 1482, 158, 253, 18.00, 16.93)]),
    M("Hyundai", "Creta Electric", "Hyundai Creta Electric", "SUV", 5, 6, None, 4340, 433, 0, 190, 5,
      "The electric Creta with up to 473 km claimed range.", [
        ("42 kWh", E, "Automatic", 42, 133, 200, 390, 17.99),
        ("51.4 kWh", E, "Automatic", 51.4, 169, 200, 473, 21.49)]),
    M("Hyundai", "Alcazar", "Hyundai Alcazar", "SUV", 7, 6, None, 4560, 180, 50, 200, 5,
      "A 6/7-seat SUV based on the Creta, with captain seats option.", [
        ("1.5 Turbo Petrol DCT", P, "DCT", 1482, 158, 253, 18.00, 18.67),
        ("1.5 Diesel AT", D, "Automatic", 1493, 114, 250, 18.10, 18.06)]),
    M("Hyundai", "Tucson", "Hyundai Tucson", "SUV", 5, 6, 5, 4630, 540, 54, 181, 5,
      "A premium SUV with level-2 ADAS and a plush cabin.", [
        ("2.0 Petrol AT", P, "Automatic", 1999, 154, 192, 13.00, 29.27),
        ("2.0 Diesel AT", D, "Automatic", 1997, 184, 416, 18.00, 31.65)]),
    M("Hyundai", "Ioniq 5", "Hyundai Ioniq 5", "SUV", 5, 6, None, 4635, 527, 0, 160, 5,
      "A futuristic electric crossover with ultra-fast charging.", [
        ("72.6 kWh RWD", E, "Automatic", 72.6, 214, 350, 631, 46.05)]),

    # ------------------------------------------------------------ TATA
    M("Tata", "Tiago", "Tata Tiago", "Hatchback", 5, 2, 4, 3765, 242, 35, 170, 2,
      "A budget-friendly first car with a 4-star safety rating.", [
        ("1.2 Petrol MT", P, "Manual", 1199, 85, 113, 19.00, 5.00),
        ("1.2 Petrol AMT", P, "AMT", 1199, 85, 113, 19.43, 6.85),
        ("1.2 CNG MT", C, "Manual", 1199, 72, 95, 26.49, 6.00)]),
    M("Tata", "Tiago EV", "Tata Tiago EV", "Hatchback", 5, 2, None, 3769, 240, 0, 166, 2,
      "One of India's most affordable electric cars.", [
        ("19.2 kWh MR", E, "Automatic", 19.2, 60, 110, 250, 7.99),
        ("24 kWh LR", E, "Automatic", 24, 74, 114, 315, 10.14)]),
    M("Tata", "Tigor", "Tata Tigor", "Sedan", 5, 2, 4, 3993, 419, 35, 170, 2,
      "A compact sedan with a solid build and big boot.", [
        ("1.2 Petrol MT", P, "Manual", 1199, 85, 113, 19.28, 6.00),
        ("1.2 CNG MT", C, "Manual", 1199, 72, 95, 26.49, 7.60)]),
    M("Tata", "Tigor EV", "Tata Tigor", "Sedan", 5, 2, 4, 3993, 316, 0, 172, 2,
      "An electric compact sedan popular with fleet and private buyers.", [
        ("26 kWh", E, "Automatic", 26, 74, 170, 315, 12.49)]),
    M("Tata", "Altroz", "Tata Altroz", "Hatchback", 5, 6, 5, 3990, 345, 37, 165, 3,
      "A 5-star safety hatchback with petrol, diesel and CNG.", [
        ("1.2 Petrol MT", P, "Manual", 1199, 87, 115, 19.33, 6.89),
        ("1.2 Petrol DCA", P, "DCT", 1199, 87, 115, 18.50, 8.85),
        ("1.5 Diesel MT", D, "Manual", 1497, 89, 200, 23.64, 8.89),
        ("1.2 CNG MT", C, "Manual", 1199, 72, 103, 26.20, 7.89)]),
    M("Tata", "Punch", "Tata Punch", "SUV", 5, 2, 5, 3827, 366, 37, 187, 2,
      "A tough micro SUV with a 5-star safety rating.", [
        ("1.2 Petrol MT", P, "Manual", 1199, 87, 115, 20.09, 6.00),
        ("1.2 Petrol AMT", P, "AMT", 1199, 87, 115, 18.80, 7.10),
        ("1.2 CNG MT", C, "Manual", 1199, 72, 103, 26.99, 7.30)]),
    M("Tata", "Punch EV", "Tata Punch EV", "SUV", 5, 6, 5, 3857, 366, 0, 190, 3,
      "A small electric SUV with up to 421 km claimed range.", [
        ("25 kWh MR", E, "Automatic", 25, 81, 114, 315, 9.99),
        ("35 kWh LR", E, "Automatic", 35, 120, 190, 421, 13.29)]),
    M("Tata", "Nexon", "Tata Nexon", "SUV", 5, 6, 5, 3995, 382, 44, 208, 4,
      "A compact SUV with a strong focus on safety and value.", [
        ("1.2 Turbo Petrol MT", P, "Manual", 1199, 118, 170, 17.44, 8.00),
        ("1.2 Turbo Petrol DCA", P, "DCT", 1199, 118, 170, 17.18, 11.70),
        ("1.5 Diesel MT", D, "Manual", 1497, 113, 260, 23.23, 10.00),
        ("1.5 Diesel AMT", D, "AMT", 1497, 113, 260, 24.08, 11.40),
        ("1.2 Turbo CNG MT", C, "Manual", 1199, 99, 170, 24.00, 9.00)]),
    M("Tata", "Nexon EV", "Tata Nexon EV", "SUV", 5, 6, 5, 3994, 350, 0, 205, 4,
      "India's best-selling electric SUV.", [
        ("30 kWh MR", E, "Automatic", 30, 127, 215, 275, 12.49),
        ("45 kWh LR", E, "Automatic", 45, 142, 215, 489, 13.99)]),
    M("Tata", "Curvv", "Tata Curvv", "SUV", 5, 6, 5, 4308, 500, 44, 208, 5,
      "A coupe-SUV with a sloping roof and a large 500-litre boot.", [
        ("1.2 Turbo Petrol MT", P, "Manual", 1199, 118, 170, 17.00, 10.00),
        ("1.2 Turbo Petrol DCA", P, "DCT", 1199, 118, 170, 15.00, 12.00),
        ("1.5 Diesel MT", D, "Manual", 1497, 116, 260, 22.00, 11.50)]),
    M("Tata", "Curvv EV", "Tata Curvv", "SUV", 5, 6, 5, 4310, 500, 0, 190, 5,
      "The electric coupe-SUV with up to 585 km claimed range.", [
        ("45 kWh", E, "Automatic", 45, 148, 215, 502, 17.49),
        ("55 kWh", E, "Automatic", 55, 165, 215, 585, 19.25)]),
    M("Tata", "Harrier", "Tata Harrier", "SUV", 5, 7, 5, 4605, 445, 50, 205, 5,
      "A bold mid-size SUV built on Land Rover-derived architecture.", [
        ("2.0 Diesel MT", D, "Manual", 1956, 168, 350, 16.80, 15.00),
        ("2.0 Diesel AT", D, "Automatic", 1956, 168, 350, 14.60, 19.15)]),
    M("Tata", "Harrier EV", "Tata Harrier", "SUV", 5, 7, 5, 4607, 502, 0, 205, 5,
      "An electric Harrier with optional dual-motor all-wheel drive.", [
        ("65 kWh RWD", E, "Automatic", 65, 235, 315, 538, 21.49)]),
    M("Tata", "Safari", "Tata Safari", "SUV", 7, 7, 5, 4668, 420, 50, 200, 5,
      "A 6/7-seat flagship SUV with a 5-star safety rating.", [
        ("2.0 Diesel MT", D, "Manual", 1956, 168, 350, 16.30, 15.50),
        ("2.0 Diesel AT", D, "Automatic", 1956, 168, 350, 14.50, 19.99)]),

    # ------------------------------------------------------------ MAHINDRA
    M("Mahindra", "XUV 3XO", "Mahindra XUV 3XO", "SUV", 5, 6, 5, 3990, 364, 42, 201, 4,
      "A compact SUV with panoramic sunroof and ADAS.", [
        ("1.2 Turbo Petrol MT", P, "Manual", 1197, 110, 200, 18.89, 7.99),
        ("1.2 TGDi Petrol AT", P, "Automatic", 1197, 129, 230, 17.96, 13.05),
        ("1.5 Diesel MT", D, "Manual", 1497, 115, 300, 20.60, 9.99),
        ("1.5 Diesel AMT", D, "AMT", 1497, 115, 300, 21.20, 11.99)]),
    M("Mahindra", "Bolero", "Mahindra Bolero", "SUV", 7, 2, None, 3995, 370, 60, 180, 1,
      "A rugged, no-nonsense workhorse SUV.", [
        ("1.5 Diesel MT", D, "Manual", 1493, 75, 210, 16.00, 9.79)]),
    M("Mahindra", "Bolero Neo", "Mahindra Bolero Neo", "SUV", 7, 2, 1, 3995, 384, 50, 160, 1,
      "A more modern, comfortable take on the Bolero.", [
        ("1.5 Diesel MT", D, "Manual", 1493, 100, 260, 17.29, 9.95)]),
    M("Mahindra", "Thar", "Mahindra Thar", "SUV", 4, 2, 4, 3985, 225, 57, 226, 2,
      "An iconic lifestyle off-roader with real 4x4 ability.", [
        ("1.5 Diesel MT RWD", D, "Manual", 1497, 117, 300, 15.20, 11.50),
        ("2.0 Turbo Petrol AT 4x4", P, "Automatic", 1997, 150, 320, 12.40, 15.25),
        ("2.2 Diesel MT 4x4", D, "Manual", 2184, 130, 300, 15.20, 14.75),
        ("2.2 Diesel AT 4x4", D, "Automatic", 2184, 130, 300, 15.20, 16.25)]),
    M("Mahindra", "Thar Roxx", "Mahindra Thar Roxx", "SUV", 5, 6, 5, 4428, 447, 57, 225, 4,
      "A 5-door Thar with a premium, family-friendly cabin.", [
        ("2.0 Turbo Petrol AT", P, "Automatic", 1997, 174, 380, 12.40, 16.99),
        ("2.2 Diesel MT", D, "Manual", 2184, 150, 330, 15.20, 13.99),
        ("2.2 Diesel AT 4x4", D, "Automatic", 2184, 172, 370, 15.20, 20.99)]),
    M("Mahindra", "Scorpio Classic", "Mahindra Scorpio", "SUV", 7, 2, None, 4456, 460, 60, 209, 1,
      "The classic, tough Scorpio with a commanding stance.", [
        ("2.2 Diesel MT", D, "Manual", 2184, 130, 300, 15.00, 13.62)]),
    M("Mahindra", "Scorpio N", "Mahindra Scorpio N", "SUV", 7, 6, 5, 4662, 460, 57, 187, 4,
      "A modern body-on-frame SUV with optional 4x4.", [
        ("2.0 Turbo Petrol MT", P, "Manual", 1997, 200, 370, 12.12, 13.99),
        ("2.0 Turbo Petrol AT", P, "Automatic", 1997, 200, 380, 11.00, 17.69),
        ("2.2 Diesel MT", D, "Manual", 2184, 172, 370, 15.42, 14.39),
        ("2.2 Diesel AT 4x4", D, "Automatic", 2184, 172, 400, 14.50, 21.25)]),
    M("Mahindra", "XUV700", "Mahindra XUV700", "SUV", 7, 7, 5, 4695, 240, 60, 200, 5,
      "A feature-packed 7-seat SUV with powerful engines and ADAS.", [
        ("2.0 Turbo Petrol MT", P, "Manual", 1999, 197, 380, 13.00, 13.99),
        ("2.0 Turbo Petrol AT", P, "Automatic", 1999, 197, 380, 11.60, 19.20),
        ("2.2 Diesel MT", D, "Manual", 2184, 182, 420, 17.00, 14.59),
        ("2.2 Diesel AT", D, "Automatic", 2184, 182, 450, 16.00, 20.00)]),
    M("Mahindra", "XUV400 EV", "Mahindra XUV400", "SUV", 5, 6, 5, 4200, 378, 0, 190, 3,
      "A quick electric SUV with a large boot.", [
        ("34.5 kWh EC", E, "Automatic", 34.5, 148, 310, 375, 15.49),
        ("39.4 kWh EL", E, "Automatic", 39.4, 148, 310, 456, 17.69)]),
    M("Mahindra", "BE 6", "Mahindra BE 6", "SUV", 5, 7, 5, 4371, 455, 0, 207, 5,
      "A sporty electric SUV on Mahindra's INGLO platform.", [
        ("59 kWh", E, "Automatic", 59, 228, 380, 556, 18.90),
        ("79 kWh", E, "Automatic", 79, 282, 380, 682, 26.90)]),
    M("Mahindra", "XEV 9e", "Mahindra XEV 9e", "SUV", 5, 7, 5, 4789, 663, 0, 207, 5,
      "A large electric coupe-SUV with a triple-screen dashboard.", [
        ("59 kWh", E, "Automatic", 59, 228, 380, 542, 21.90),
        ("79 kWh", E, "Automatic", 79, 282, 380, 656, 30.50)]),
    M("Mahindra", "Marazzo", "Mahindra Marazzo", "MUV", 7, 2, 4, 4585, 190, 45, 200, 2,
      "A comfortable 7/8-seat MPV with a refined diesel.", [
        ("1.5 Diesel MT", D, "Manual", 1497, 121, 300, 17.30, 14.59)]),

    # ------------------------------------------------------------ KIA
    M("Kia", "Sonet", "Kia Sonet", "SUV", 5, 6, None, 3995, 385, 45, 205, 4,
      "A feature-rich compact SUV with many engine choices.", [
        ("1.2 Petrol MT", P, "Manual", 1197, 82, 115, 18.40, 8.00),
        ("1.0 Turbo Petrol DCT", P, "DCT", 998, 118, 172, 19.20, 12.70),
        ("1.5 Diesel MT", D, "Manual", 1493, 114, 250, 22.30, 9.80),
        ("1.5 Diesel AT", D, "Automatic", 1493, 114, 250, 18.60, 13.50)]),
    M("Kia", "Syros", "Kia Syros", "SUV", 5, 6, 5, 3995, 465, 45, 190, 5,
      "A boxy, roomy compact SUV with ventilated rear seats.", [
        ("1.0 Turbo Petrol MT", P, "Manual", 998, 118, 172, 18.20, 9.00),
        ("1.0 Turbo Petrol DCT", P, "DCT", 998, 118, 172, 17.68, 13.30),
        ("1.5 Diesel AT", D, "Automatic", 1493, 114, 250, 17.65, 15.00)]),
    M("Kia", "Seltos", "Kia Seltos", "SUV", 5, 6, 3, 4365, 433, 50, 190, 5,
      "A sporty-looking SUV with a technology-focused interior.", [
        ("1.5 Petrol MT", P, "Manual", 1497, 113, 144, 17.00, 11.13),
        ("1.5 Petrol IVT", P, "CVT", 1497, 113, 144, 17.70, 15.00),
        ("1.5 Turbo Petrol DCT", P, "DCT", 1482, 158, 253, 17.90, 19.20),
        ("1.5 Diesel MT", D, "Manual", 1493, 114, 250, 20.70, 12.70),
        ("1.5 Diesel AT", D, "Automatic", 1493, 114, 250, 19.10, 16.60)]),
    M("Kia", "Carens", "Kia Carens", "MUV", 7, 6, 3, 4540, 216, 45, 195, 4,
      "A versatile 6/7-seat MPV with SUV styling.", [
        ("1.5 Petrol MT", P, "Manual", 1497, 113, 144, 15.70, 11.41),
        ("1.5 Turbo Petrol DCT", P, "DCT", 1482, 158, 253, 16.00, 16.50),
        ("1.5 Diesel AT", D, "Automatic", 1493, 114, 250, 18.00, 17.00)]),
    M("Kia", "Carnival", "Kia Carnival", "MUV", 7, 8, None, 5155, 627, 72, 172, 5,
      "A luxurious limousine-style MPV with power sliding doors.", [
        ("2.2 Diesel AT", D, "Automatic", 2151, 190, 441, 14.85, 63.90)]),
    M("Kia", "EV6", "Kia EV6", "SUV", 5, 8, None, 4695, 490, 0, 160, 5,
      "A sleek electric crossover with all-wheel drive.", [
        ("84 kWh AWD", E, "Automatic", 84, 325, 605, 663, 65.97)]),
    M("Kia", "EV9", "Kia EV9", "SUV", 6, 10, None, 5015, 333, 0, 176, 5,
      "A flagship 6-seat electric SUV.", [
        ("99.8 kWh AWD", E, "Automatic", 99.8, 379, 700, 561, 129.90)]),

    # ------------------------------------------------------------ HONDA
    M("Honda", "Amaze", "Honda Amaze", "Sedan", 5, 6, None, 3995, 416, 35, 172, 3,
      "A compact sedan with ADAS and a smooth CVT.", [
        ("1.2 Petrol MT", P, "Manual", 1199, 89, 110, 18.65, 8.10),
        ("1.2 Petrol CVT", P, "CVT", 1199, 89, 110, 19.46, 9.35)]),
    M("Honda", "City", "Honda City", "Sedan", 5, 6, None, 4583, 506, 40, 165, 4,
      "A spacious sedan known for its refined engine and ride.", [
        ("1.5 Petrol MT", P, "Manual", 1498, 119, 145, 17.80, 11.82),
        ("1.5 Petrol CVT", P, "CVT", 1498, 119, 145, 18.40, 13.05)]),
    M("Honda", "City e:HEV", "Honda City", "Sedan", 5, 6, None, 4583, 410, 40, 165, 5,
      "A strong-hybrid City with exceptional fuel economy.", [
        ("1.5 Strong Hybrid eCVT", H, "Automatic", 1498, 125, 253, 27.13, 19.00)]),
    M("Honda", "Elevate", "Honda Elevate", "SUV", 5, 6, None, 4312, 458, 40, 220, 4,
      "A practical mid-size SUV with high ground clearance.", [
        ("1.5 Petrol MT", P, "Manual", 1498, 119, 145, 15.31, 11.69),
        ("1.5 Petrol CVT", P, "CVT", 1498, 119, 145, 16.92, 13.71)]),

    # ------------------------------------------------------------ TOYOTA
    M("Toyota", "Glanza", "Toyota Glanza", "Hatchback", 5, 6, None, 3990, 318, 37, 170, 3,
      "Toyota's premium hatchback, with a long standard warranty.", [
        ("1.2 Petrol MT", P, "Manual", 1197, 89, 113, 22.35, 6.86),
        ("1.2 Petrol AMT", P, "AMT", 1197, 89, 113, 22.94, 8.66),
        ("1.2 CNG MT", C, "Manual", 1197, 77, 98, 30.61, 8.65)]),
    M("Toyota", "Urban Cruiser Taisor", "Toyota Urban Cruiser Taisor", "SUV", 5, 6, None, 3995, 308, 37, 190, 3,
      "A stylish crossover with a peppy turbo-petrol option.", [
        ("1.2 Petrol MT", P, "Manual", 1197, 89, 113, 21.70, 7.74),
        ("1.0 Turbo Petrol AT", P, "Automatic", 998, 99, 148, 20.00, 12.87),
        ("1.2 CNG MT", C, "Manual", 1197, 77, 98, 28.50, 8.71)]),
    M("Toyota", "Urban Cruiser Hyryder", "Toyota Urban Cruiser Hyryder", "SUV", 5, 6, None, 4365, 373, 45, 210, 4,
      "A mid-size SUV with a highly efficient strong-hybrid.", [
        ("1.5 Petrol MT", P, "Manual", 1462, 102, 137, 21.12, 11.34),
        ("1.5 Strong Hybrid eCVT", H, "Automatic", 1490, 114, 122, 27.97, 16.81),
        ("1.5 CNG MT", C, "Manual", 1462, 87, 122, 26.60, 13.71)]),
    M("Toyota", "Rumion", "Toyota Rumion", "MUV", 7, 6, None, 4420, 209, 45, 185, 2,
      "A 7-seat MPV with Toyota service and reliability.", [
        ("1.5 Petrol MT", P, "Manual", 1462, 102, 137, 20.51, 10.54),
        ("1.5 Petrol AT", P, "Automatic", 1462, 102, 137, 20.11, 13.08),
        ("1.5 CNG MT", C, "Manual", 1462, 87, 122, 26.11, 11.59)]),
    M("Toyota", "Innova Crysta", "Toyota Innova Crysta", "MUV", 7, 7, None, 4735, 300, 55, 178, 3,
      "A legendary, near-indestructible family MPV.", [
        ("2.4 Diesel MT", D, "Manual", 2393, 148, 343, 12.00, 19.99)]),
    M("Toyota", "Innova Hycross", "Toyota Innova Hycross", "MUV", 7, 6, None, 4755, 239, 52, 185, 5,
      "A monocoque MPV with a 23+ km/l strong-hybrid.", [
        ("2.0 Petrol CVT", P, "CVT", 1987, 172, 205, 16.13, 19.94),
        ("2.0 Strong Hybrid eCVT", H, "Automatic", 1987, 184, 188, 23.24, 26.31)]),
    M("Toyota", "Fortuner", "Toyota Fortuner", "SUV", 7, 7, None, 4795, 296, 80, 225, 4,
      "The king of full-size body-on-frame SUVs in India.", [
        ("2.7 Petrol AT", P, "Automatic", 2694, 164, 245, 10.00, 33.78),
        ("2.8 Diesel MT", D, "Manual", 2755, 201, 420, 14.40, 35.37),
        ("2.8 Diesel AT 4x4", D, "Automatic", 2755, 201, 500, 14.20, 43.66)]),
    M("Toyota", "Fortuner Legender", "Toyota Fortuner", "SUV", 7, 7, None, 4795, 296, 80, 225, 5,
      "A sharper-styled, better-equipped Fortuner.", [
        ("2.8 Diesel AT 4x4", D, "Automatic", 2755, 201, 500, 14.20, 44.11)]),
    M("Toyota", "Hilux", "Toyota Hilux", "Pickup", 5, 7, None, 5325, None, 80, 220, 3,
      "A tough lifestyle pickup truck with 4x4.", [
        ("2.8 Diesel MT 4x4", D, "Manual", 2755, 201, 420, 13.00, 30.40)]),
    M("Toyota", "Camry", "Toyota Camry", "Sedan", 5, 9, None, 4920, 524, 50, 145, 5,
      "A smooth, quiet luxury hybrid sedan.", [
        ("2.5 Strong Hybrid eCVT", H, "Automatic", 2487, 227, 221, 25.49, 48.00)]),
    M("Toyota", "Land Cruiser 300", "Toyota Land Cruiser (J300)", "SUV", 7, 10, None, 4985, 175, 110, 230, 5,
      "The ultimate go-anywhere luxury SUV.", [
        ("3.3 Twin-Turbo Diesel AT", D, "Automatic", 3346, 304, 700, 11.00, 210.00)]),
    M("Toyota", "Vellfire", "Toyota Alphard", "MUV", 7, 6, None, 5005, 148, 60, 160, 5,
      "A chauffeur-driven luxury MPV with business-class seats.", [
        ("2.5 Strong Hybrid eCVT", H, "Automatic", 2487, 190, 240, 19.28, 122.30)]),

    # ------------------------------------------------------------ SKODA
    M("Skoda", "Kylaq", "Skoda Kylaq", "SUV", 5, 6, 5, 3995, 446, 45, 189, 4,
      "Skoda's first sub-4m SUV with a punchy turbo engine.", [
        ("1.0 TSI MT", P, "Manual", 999, 114, 178, 19.68, 7.89),
        ("1.0 TSI AT", P, "Automatic", 999, 114, 178, 19.05, 11.40)]),
    M("Skoda", "Kushaq", "Skoda Kushaq", "SUV", 5, 6, 5, 4225, 385, 50, 155, 4,
      "A fun-to-drive SUV with a 5-star safety rating.", [
        ("1.0 TSI MT", P, "Manual", 999, 114, 178, 19.76, 10.99),
        ("1.0 TSI AT", P, "Automatic", 999, 114, 178, 18.09, 14.00),
        ("1.5 TSI DSG", P, "DCT", 1498, 148, 250, 18.86, 16.89)]),
    M("Skoda", "Slavia", "Skoda Slavia", "Sedan", 5, 6, 5, 4541, 521, 45, 179, 4,
      "A driver-focused sedan with a punchy turbo engine.", [
        ("1.0 TSI MT", P, "Manual", 999, 114, 178, 20.32, 10.34),
        ("1.0 TSI AT", P, "Automatic", 999, 114, 178, 18.73, 13.69),
        ("1.5 TSI DSG", P, "DCT", 1498, 148, 250, 19.36, 16.39)]),
    M("Skoda", "Kodiaq", "Škoda Kodiaq", "SUV", 7, 9, None, 4758, 281, 58, 155, 5,
      "A premium 7-seat SUV with all-wheel drive.", [
        ("2.0 TSI DSG 4x4", P, "DCT", 1984, 201, 320, 14.86, 46.89)]),
    M("Skoda", "Superb", "Škoda Superb", "Sedan", 5, 9, None, 4869, 625, 66, 156, 5,
      "A luxurious executive sedan with enormous rear legroom.", [
        ("2.0 TSI DSG", P, "DCT", 1984, 187, 320, 15.00, 54.00)]),

    # ------------------------------------------------------------ VOLKSWAGEN
    M("Volkswagen", "Virtus", "Volkswagen Virtus", "Sedan", 5, 6, 5, 4561, 521, 45, 179, 4,
      "A sporty sedan with German build quality and 5-star safety.", [
        ("1.0 TSI MT", P, "Manual", 999, 114, 178, 20.08, 11.56),
        ("1.0 TSI AT", P, "Automatic", 999, 114, 178, 18.12, 14.88),
        ("1.5 TSI DSG", P, "DCT", 1498, 148, 250, 19.62, 16.86)]),
    M("Volkswagen", "Taigun", "Volkswagen Taigun", "SUV", 5, 6, 5, 4221, 385, 50, 188, 4,
      "A compact, sharp-handling SUV.", [
        ("1.0 TSI MT", P, "Manual", 999, 114, 178, 19.87, 11.70),
        ("1.0 TSI AT", P, "Automatic", 999, 114, 178, 18.15, 15.19),
        ("1.5 TSI DSG", P, "DCT", 1498, 148, 250, 19.01, 17.15)]),
    M("Volkswagen", "Tiguan R-Line", "Volkswagen Tiguan", "SUV", 5, 9, None, 4539, 652, 58, 167, 5,
      "A sporty premium SUV with 4MOTION all-wheel drive.", [
        ("2.0 TSI DSG 4MOTION", P, "DCT", 1984, 201, 320, 12.58, 49.00)]),

    # ------------------------------------------------------------ MG
    M("MG", "Comet EV", "MG Comet EV", "Hatchback", 4, 2, None, 2974, None, 0, 165, 2,
      "An ultra-compact 2-door city EV that's easy to park.", [
        ("17.3 kWh", E, "Automatic", 17.3, 41, 110, 230, 6.99)]),
    M("MG", "Windsor EV", "MG Windsor EV", "SUV", 5, 6, None, 4295, 604, 0, 186, 4,
      "A spacious electric crossover with reclining rear seats.", [
        ("38 kWh", E, "Automatic", 38, 134, 200, 332, 13.99),
        ("52.9 kWh Pro", E, "Automatic", 52.9, 134, 200, 449, 18.39)]),
    M("MG", "ZS EV", "MG ZS EV", "SUV", 5, 6, None, 4323, 448, 0, 177, 4,
      "A practical electric SUV with a 461 km claimed range.", [
        ("50.3 kWh", E, "Automatic", 50.3, 174, 280, 461, 17.99)]),
    M("MG", "Astor", "MG ZS (2017)", "SUV", 5, 6, None, 4323, 488, 48, 180, 4,
      "A feature-loaded SUV with an AI personal assistant.", [
        ("1.5 Petrol MT", P, "Manual", 1498, 108, 144, 15.43, 9.99),
        ("1.5 Petrol CVT", P, "CVT", 1498, 108, 144, 14.82, 14.50)]),
    M("MG", "Hector", "MG Hector", "SUV", 5, 6, None, 4699, 587, 60, 192, 5,
      "A large SUV with a 14-inch portrait touchscreen.", [
        ("1.5 Turbo Petrol MT", P, "Manual", 1451, 141, 250, 13.79, 13.99),
        ("1.5 Turbo Petrol CVT", P, "CVT", 1451, 141, 250, 12.34, 18.08),
        ("2.0 Diesel MT", D, "Manual", 1956, 168, 350, 15.58, 17.30)]),
    M("MG", "Hector Plus", "MG Hector", "SUV", 7, 6, None, 4699, 155, 60, 192, 5,
      "A 6/7-seat version of the Hector.", [
        ("2.0 Diesel MT", D, "Manual", 1956, 168, 350, 15.58, 19.49)]),
    M("MG", "Gloster", "Maxus D90", "SUV", 7, 6, None, 4985, 343, 75, 210, 5,
      "A big full-size SUV with twin-turbo diesel and 4x4.", [
        ("2.0 Twin-Turbo Diesel AT 4x4", D, "Automatic", 1996, 212, 478, 12.04, 39.57)]),

    # ------------------------------------------------------------ RENAULT / NISSAN
    M("Renault", "Kwid", "Renault Kwid", "Hatchback", 5, 2, 1, 3731, 279, 28, 184, 2,
      "An affordable hatch with SUV-inspired styling.", [
        ("1.0 Petrol MT", P, "Manual", 999, 67, 91, 21.46, 4.70),
        ("1.0 Petrol AMT", P, "AMT", 999, 67, 91, 22.30, 5.45)]),
    M("Renault", "Triber", "Renault Triber", "MUV", 7, 4, 4, 3990, 84, 40, 182, 2,
      "India's most affordable 7-seater with removable third-row seats.", [
        ("1.0 Petrol MT", P, "Manual", 999, 71, 96, 18.29, 6.10),
        ("1.0 Petrol AMT", P, "AMT", 999, 71, 96, 18.29, 7.70)]),
    M("Renault", "Kiger", "Renault Kiger", "SUV", 5, 4, 4, 3991, 405, 40, 205, 3,
      "A value-packed compact SUV with a turbo option.", [
        ("1.0 Petrol MT", P, "Manual", 999, 71, 96, 19.17, 6.10),
        ("1.0 Turbo Petrol CVT", P, "CVT", 999, 99, 152, 18.24, 10.00)]),
    M("Nissan", "Magnite", "Nissan Magnite", "SUV", 5, 6, 4, 3994, 336, 40, 205, 3,
      "A well-equipped compact SUV at a very low price.", [
        ("1.0 Petrol MT", P, "Manual", 999, 71, 96, 19.35, 6.14),
        ("1.0 Turbo Petrol CVT", P, "CVT", 999, 99, 152, 17.40, 9.99)]),

    # ------------------------------------------------------------ CITROEN
    M("Citroen", "C3", "Citroën C3 (2022)", "Hatchback", 5, 6, None, 3981, 315, 30, 180, 2,
      "A comfortable hatch with a soft, bump-absorbing ride.", [
        ("1.2 Petrol MT", P, "Manual", 1199, 81, 115, 19.30, 6.16),
        ("1.2 Turbo Petrol AT", P, "Automatic", 1199, 109, 205, 17.60, 9.99)]),
    M("Citroen", "eC3", "Citroën C3 (2022)", "Hatchback", 5, 2, None, 3981, 315, 0, 170, 2,
      "An affordable electric hatchback with a comfy ride.", [
        ("29.2 kWh", E, "Automatic", 29.2, 56, 143, 320, 12.76)]),
    M("Citroen", "Basalt", "Citroën Basalt", "SUV", 5, 6, None, 4352, 470, 45, 180, 3,
      "A coupe-SUV with adjustable under-thigh support.", [
        ("1.2 Turbo Petrol MT", P, "Manual", 1199, 109, 190, 19.50, 9.99),
        ("1.2 Turbo Petrol AT", P, "Automatic", 1199, 109, 205, 18.70, 12.80)]),
    M("Citroen", "Aircross", "Citroën C3 Aircross (2023)", "SUV", 7, 6, None, 4323, 444, 45, 200, 3,
      "A 5+2 seat SUV with removable third row.", [
        ("1.2 Petrol MT", P, "Manual", 1199, 81, 115, 18.50, 8.49),
        ("1.2 Turbo Petrol AT", P, "Automatic", 1199, 109, 205, 17.60, 12.49)]),

    # ------------------------------------------------------------ JEEP
    M("Jeep", "Compass", "Jeep Compass", "SUV", 5, 6, 5, 4405, 438, 60, 178, 4,
      "A premium SUV with real off-road capability.", [
        ("2.0 Diesel MT", D, "Manual", 1956, 168, 350, 17.10, 18.99),
        ("2.0 Diesel AT 4x4", D, "Automatic", 1956, 168, 350, 15.30, 28.29)]),
    M("Jeep", "Meridian", "Jeep Meridian", "SUV", 7, 6, None, 4769, 170, 60, 214, 5,
      "A 7-seat premium SUV with a plush cabin.", [
        ("2.0 Diesel AT", D, "Automatic", 1956, 168, 350, 15.00, 24.99)]),
    M("Jeep", "Wrangler", "Jeep Wrangler (JL)", "SUV", 5, 6, None, 4882, 533, 81, 260, 4,
      "An icon of off-roading with removable doors and roof.", [
        ("2.0 Turbo Petrol AT 4x4", P, "Automatic", 1995, 268, 400, 11.40, 67.65)]),
    M("Jeep", "Grand Cherokee", "Jeep Grand Cherokee (WL)", "SUV", 5, 8, None, 4914, 1067, 87, 215, 5,
      "A luxury SUV with advanced 4x4 systems.", [
        ("2.0 Turbo Petrol AT 4x4", P, "Automatic", 1995, 268, 400, 10.00, 67.50)]),

    # ------------------------------------------------------------ BYD
    M("BYD", "Atto 3", "BYD Atto 3", "SUV", 5, 7, None, 4455, 440, 0, 175, 5,
      "A well-equipped electric SUV with a Blade battery.", [
        ("60.48 kWh", E, "Automatic", 60.48, 201, 310, 521, 24.99)]),
    M("BYD", "Seal", "BYD Seal", "Sedan", 5, 9, None, 4800, 400, 0, 120, 5,
      "A fast, sleek electric sports sedan.", [
        ("82.56 kWh RWD", E, "Automatic", 82.56, 308, 360, 650, 41.00)]),
    M("BYD", "eMax 7", "BYD e6", "MUV", 7, 6, None, 4710, 180, 0, 170, 5,
      "An electric 6/7-seat family MPV.", [
        ("71.8 kWh", E, "Automatic", 71.8, 201, 310, 530, 26.90)]),
    M("BYD", "Sealion 7", "BYD Sealion 7", "SUV", 5, 11, None, 4830, 500, 0, 150, 5,
      "A premium electric SUV-coupe.", [
        ("82.56 kWh", E, "Automatic", 82.56, 308, 380, 567, 48.90)]),

    # ------------------------------------------------------------ BMW
    M("BMW", "3 Series Gran Limousine", "BMW 3 Series (G20)", "Sedan", 5, 6, None, 4823, 480, 59, 140, 5,
      "A long-wheelbase sports sedan made for India.", [
        ("330Li Petrol AT", P, "Automatic", 1998, 255, 400, 15.39, 62.60)]),
    M("BMW", "5 Series LWB", "BMW 5 Series (G60)", "Sedan", 5, 8, None, 5175, 500, 68, 140, 5,
      "A long-wheelbase executive luxury sedan.", [
        ("530Li Petrol AT", P, "Automatic", 1998, 255, 400, 12.00, 72.90)]),
    M("BMW", "X1", "BMW X1 (U11)", "SUV", 5, 8, None, 4500, 476, 54, 180, 5,
      "BMW's entry luxury SUV.", [
        ("sDrive18i Petrol AT", P, "Automatic", 1499, 134, 230, 16.00, 49.50)]),
    M("BMW", "X3", "BMW X3 (G45)", "SUV", 5, 8, None, 4755, 570, 65, 200, 5,
      "A dynamic mid-size luxury SUV.", [
        ("xDrive20 Petrol AT", P, "Automatic", 1998, 255, 400, 13.00, 75.80)]),
    M("BMW", "X5", "BMW X5 (G05)", "SUV", 5, 8, None, 4922, 650, 83, 214, 5,
      "A powerful, luxurious full-size SUV.", [
        ("xDrive40i Petrol AT", P, "Automatic", 2998, 375, 520, 12.00, 97.00)]),
    M("BMW", "X7", "BMW X7", "SUV", 7, 8, None, 5181, 326, 83, 221, 5,
      "BMW's flagship 7-seat luxury SUV.", [
        ("xDrive40i Petrol AT", P, "Automatic", 2998, 375, 520, 11.29, 130.00)]),
    M("BMW", "i4", "BMW i4", "Sedan", 5, 8, None, 4783, 470, 0, 125, 5,
      "An electric gran coupe with a 590 km range.", [
        ("eDrive40", E, "Automatic", 70.2, 335, 430, 590, 72.50)]),
    M("BMW", "iX1 LWB", "BMW X1 (U11)", "SUV", 5, 8, None, 4616, 490, 0, 180, 5,
      "A long-wheelbase electric luxury SUV.", [
        ("eDrive20L", E, "Automatic", 66.4, 201, 250, 531, 49.00)]),

    # ------------------------------------------------------------ MERCEDES-BENZ
    M("Mercedes-Benz", "A-Class Limousine", "Mercedes-Benz A-Class (W177)", "Sedan", 5, 7, None, 4549, 420, 43, 140, 5,
      "The most affordable Mercedes sedan.", [
        ("A 200 Petrol AT", P, "Automatic", 1332, 161, 270, 17.50, 46.05)]),
    M("Mercedes-Benz", "C-Class", "Mercedes-Benz C-Class (W206)", "Sedan", 5, 7, None, 4793, 455, 66, 140, 5,
      "A mini S-Class with a high-tech cabin.", [
        ("C 200 Petrol AT", P, "Automatic", 1496, 201, 300, 16.90, 59.40)]),
    M("Mercedes-Benz", "E-Class LWB", "Mercedes-Benz E-Class (W214)", "Sedan", 5, 8, None, 5092, 540, 66, 145, 5,
      "A long-wheelbase luxury sedan for the rear seat.", [
        ("E 200 Petrol AT", P, "Automatic", 1999, 255, 400, 15.00, 78.50)]),
    M("Mercedes-Benz", "GLA", "Mercedes-Benz GLA", "SUV", 5, 7, None, 4412, 425, 51, 165, 5,
      "A compact luxury crossover.", [
        ("GLA 200 Petrol AT", P, "Automatic", 1332, 161, 270, 17.40, 50.50)]),
    M("Mercedes-Benz", "GLC", "Mercedes-Benz GLC", "SUV", 5, 7, None, 4716, 620, 62, 180, 5,
      "A best-selling mid-size luxury SUV.", [
        ("GLC 300 Petrol AT", P, "Automatic", 1999, 255, 400, 14.70, 76.80)]),
    M("Mercedes-Benz", "GLE", "Mercedes-Benz GLE", "SUV", 5, 9, None, 4924, 630, 85, 180, 5,
      "A powerful, comfortable full-size luxury SUV.", [
        ("GLE 300d Diesel AT", D, "Automatic", 1993, 265, 550, 12.00, 99.00)]),
    M("Mercedes-Benz", "GLS", "Mercedes-Benz GLS", "SUV", 7, 9, None, 5209, 355, 90, 216, 5,
      "The 'S-Class of SUVs' with seven luxurious seats.", [
        ("GLS 450 Petrol AT", P, "Automatic", 2999, 375, 500, 10.00, 132.00)]),
    M("Mercedes-Benz", "EQB", "Mercedes-Benz EQB", "SUV", 7, 7, None, 4684, 495, 0, 170, 5,
      "A compact electric luxury SUV with 7 seats.", [
        ("EQB 350 4MATIC", E, "Automatic", 70.5, 288, 520, 535, 72.20)]),

    # ------------------------------------------------------------ AUDI
    M("Audi", "A4", "Audi A4 (B9)", "Sedan", 5, 8, None, 4762, 460, 54, 140, 5,
      "A refined entry luxury sedan with quattro DNA.", [
        ("40 TFSI Petrol AT", P, "Automatic", 1984, 201, 320, 17.40, 46.02)]),
    M("Audi", "A6", "Audi A6 (C8)", "Sedan", 5, 8, None, 4939, 530, 73, 140, 5,
      "A tech-loaded executive luxury sedan.", [
        ("45 TFSI Petrol AT", P, "Automatic", 1984, 241, 370, 14.11, 65.72)]),
    M("Audi", "Q3", "Audi Q3", "SUV", 5, 6, None, 4484, 530, 60, 170, 5,
      "A compact luxury SUV with quattro AWD.", [
        ("40 TFSI quattro AT", P, "Automatic", 1984, 187, 320, 14.90, 44.25)]),
    M("Audi", "Q5", "Audi Q5", "SUV", 5, 8, None, 4682, 520, 70, 200, 5,
      "A comfortable, well-rounded luxury SUV.", [
        ("45 TFSI quattro AT", P, "Automatic", 1984, 261, 370, 13.47, 65.51)]),
    M("Audi", "Q7", "Audi Q7", "SUV", 7, 8, None, 5063, 295, 85, 220, 5,
      "A 7-seat luxury SUV with a V6 engine.", [
        ("55 TFSI quattro AT", P, "Automatic", 2995, 335, 500, 11.00, 88.66)]),
    M("Audi", "Q8 e-tron", "Audi Q8 e-tron", "SUV", 5, 8, None, 4915, 569, 0, 176, 5,
      "A luxurious electric SUV with quattro AWD.", [
        ("55 quattro", E, "Automatic", 114, 402, 664, 582, 115.00)]),

    # ------------------------------------------------------------ VOLVO / LAND ROVER / LEXUS
    M("Volvo", "XC60", "Volvo XC60", "SUV", 5, 7, None, 4708, 483, 71, 216, 5,
      "A safe, elegant Scandinavian luxury SUV.", [
        ("B5 Mild Hybrid AT", P, "Automatic", 1969, 247, 360, 11.20, 70.90)]),
    M("Volvo", "XC90", "Volvo XC90", "SUV", 7, 7, None, 4953, 302, 71, 238, 5,
      "Volvo's flagship 7-seat SUV, renowned for safety.", [
        ("B5 Mild Hybrid AT", P, "Automatic", 1969, 247, 360, 10.50, 101.90)]),
    M("Volvo", "EX40", "Volvo XC40", "SUV", 5, 7, None, 4440, 452, 0, 175, 5,
      "A compact electric luxury SUV with twin motors.", [
        ("Twin Motor AWD", E, "Automatic", 78, 402, 670, 475, 56.10)]),
    M("Land Rover", "Defender", "Land Rover Defender (L663)", "SUV", 5, 6, None, 5018, 786, 90, 291, 5,
      "A modern legend of off-roading and luxury.", [
        ("110 P300 Petrol AT", P, "Automatic", 1997, 296, 400, 9.00, 104.00)]),
    M("Land Rover", "Range Rover Evoque", "Range Rover Evoque", "SUV", 5, 6, None, 4371, 591, 67, 212, 5,
      "A stylish compact luxury SUV.", [
        ("P250 Petrol AT", P, "Automatic", 1997, 247, 365, 11.00, 69.50)]),
    M("Land Rover", "Range Rover Velar", "Range Rover Velar", "SUV", 5, 6, None, 4797, 513, 82, 213, 5,
      "A sleek, minimalist luxury SUV.", [
        ("P250 Petrol AT", P, "Automatic", 1997, 247, 365, 10.00, 87.90)]),
    M("Lexus", "ES 300h", "Lexus ES", "Sedan", 5, 10, None, 4975, 454, 50, 150, 5,
      "A whisper-quiet luxury hybrid sedan.", [
        ("2.5 Hybrid eCVT", H, "Automatic", 2487, 215, 221, 22.50, 64.00)]),

    # ------------------------------------------------------------ OTHERS
    M("Force", "Gurkha", "Force Gurkha", "SUV", 4, 2, None, 3965, 500, 63, 233, 1,
      "A hardcore off-roader with locking differentials.", [
        ("2.6 Diesel MT 4x4", D, "Manual", 2596, 138, 320, 12.00, 16.75)]),
    M("Isuzu", "D-Max V-Cross", "Isuzu D-Max", "Pickup", 5, 6, None, 5332, None, 55, 240, 3,
      "A lifestyle pickup with a tough diesel engine.", [
        ("1.9 Diesel MT 4x2", D, "Manual", 1898, 161, 360, 12.50, 25.52),
        ("1.9 Diesel AT 4x4", D, "Automatic", 1898, 161, 360, 12.00, 30.96)]),
]


# ---------------------------------------------------------------- TRIM LEVELS
# Every powertrain above is offered in these trims (Base -> Top). Names follow
# each brand's usual naming. Prices and features per trim are approximate.
BRAND_TRIMS = {
    "Maruti Suzuki": ["LXi", "VXi", "ZXi+"],
    "Hyundai": ["E", "S", "SX(O)"],
    "Tata": ["Smart", "Creative", "Fearless+"],
    "Mahindra": ["MX", "AX5", "AX7"],
    "Kia": ["HTE", "HTK+", "GTX+"],
    "Honda": ["V", "VX", "ZX"],
    "Toyota": ["E", "G", "V"],
    "Skoda": ["Classic", "Signature", "Prestige"],
    "Volkswagen": ["Comfortline", "Highline", "GT Plus"],
    "MG": ["Style", "Select", "Sharp Pro"],
    "Renault": ["RXE", "RXL", "RXZ"],
    "Nissan": ["XE", "XL", "XV Premium"],
    "Citroen": ["Live", "Feel", "Shine"],
    "Jeep": ["Sport", "Longitude", "Limited (O)"],
    "BYD": ["Dynamic", "Premium", "Superior"],
    "BMW": ["Luxury Line", "M Sport"],
    "Mercedes-Benz": ["Progressive", "AMG Line"],
    "Audi": ["Premium Plus", "Technology"],
    "Volvo": ["Plus", "Ultimate"],
    "Land Rover": ["S", "HSE"],
    "Lexus": ["Exquisite", "Luxury"],
    "Isuzu": ["Hi-Lander", "Z Prestige"],
    "Force": ["Standard"],
}
# Maruti's premium NEXA showroom models use a different naming scheme.
NEXA_MODELS = {"Baleno", "Ignis", "Ciaz", "XL6", "Fronx", "Grand Vitara", "Jimny", "Invicto", "e Vitara"}
NEXA_TRIMS = ["Sigma", "Delta", "Alpha"]
# Single-trim exceptions (flagships sold in one fully loaded version).
SINGLE_TRIM = {"Invicto", "Carnival", "EV6", "EV9", "Ioniq 5", "Land Cruiser 300", "Vellfire",
               "Camry", "Fortuner Legender", "Kodiaq", "Superb", "Tiguan R-Line", "Gloster",
               "Wrangler", "Grand Cherokee", "Seal", "Sealion 7", "Comet EV", "Creta N Line",
               "i20 N Line", "Venue N Line"}


def trims_for(model):
    """Trim names for a model, Base first."""
    if model["name"] in SINGLE_TRIM:
        return ["Signature"] if model["brand"] != "MG" else ["Plush"]
    if model["brand"] == "Maruti Suzuki" and model["name"] in NEXA_MODELS:
        return NEXA_TRIMS
    return BRAND_TRIMS[model["brand"]]
