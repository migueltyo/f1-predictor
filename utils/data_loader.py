import pandas as pd

def load_fastest_laps():
    fastest_laps = {
        "charles-leclerc": 91.992,
        "kimi-antonelli": 92.803,
        "oscar-piastri": 92.861,
        "lando-norris": 92.871,
        "max-verstappen": 93.109,
        "george-russell": 93.197,
        "lewis-hamilton": 93.408,
        "pierre-gasly": 93.421,
        "oliver-bearman": 93.487,
        "gabriel-bortoleto": 93.755,
        "franco-colapinto": 93.818,
        "nico-hulkenberg": 93.987,
        "arvid-lindblad": 94.149,
        "esteban-ocon": 94.201,
        "isack-hadjar": 94.260,
        "carlos-sainz-jr": 94.342,
        "liam-lawson": 94.532,
        "alexander-albon": 94.555,
        "valtteri-bottas": 95.290,
        "sergio-perez": 95.369,
        "lance-stroll": 95.974,
        "fernando-alonso": 96.536
    }
    return fastest_laps

def load_constructors_data():
    constructors_data = {
        "constructorId": [
            "mclaren", "mercedes", "red-bull", "ferrari", "williams",
            "racing-bulls", "aston-martin", "haas", "alpine", "audi", "cadillac"
        ],
        "points": [833, 469, 451, 398, 137, 92, 89, 79, 22, 70, 0]
    }
    return constructors_data

def load_drivers_data():
    drivers_data = {
        "driverId": [
            "lando-norris", "oscar-piastri", "george-russell", "kimi-antonelli", "max-verstappen", "isack-hadjar",
            "charles-leclerc", "lewis-hamilton", "alexander-albon", "carlos-sainz-jr", "liam-lawson", "arvid-lindblad",
            "fernando-alonso", "lance-stroll", "esteban-ocon", "oliver-bearman", "nico-hulkenberg", "gabriel-bortoleto",
            "pierre-gasly", "franco-colapinto", "valtteri-bottas", "sergio-perez"
        ],
        "points": [
            423, 410, 319, 150, 421, 51, 242, 156, 73, 64, 38, 0,
            56, 33, 38, 41, 22, 19, 0, 0, 0, 0
        ],
        "experience": [
            8, 4, 8, 2, 12, 2, 9, 20, 8, 11, 4, 1,
            23, 10, 10, 2, 13, 2, 10, 3, 13, 15
        ]
    }
    return drivers_data

def format_driver_name(name):
    return ' '.join(part.capitalize() for part in name.split('-'))

def assign_constructors_to_drivers(drivers_df):
    drivers_df["constructorId"] = [
        "mclaren", "mclaren", "mercedes", "mercedes", "red-bull", "red-bull",
        "ferrari", "ferrari", "williams", "williams", "racing-bulls", "racing-bulls",
        "aston-martin", "aston-martin", "haas", "haas", "audi", "audi",
        "alpine", "alpine", "cadillac", "cadillac"
    ]
    return drivers_df
