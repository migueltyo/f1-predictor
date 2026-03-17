import os
import yaml

def get_constructor_reliability():
    # Absolute path to the races directory
    races_dir = r"C:\Users\migue\Desktop\F1 predictor\f1db-main\src\data\seasons\2025\races"

    if not os.path.exists(races_dir):
        raise FileNotFoundError(f"The directory does not exist: {races_dir}")

    # Get all race folders
    race_folders = sorted(os.listdir(races_dir))

    # Initialize a dictionary to store retirement counts for each constructor
    constructor_retirements = {}
    constructor_races = {}

    # Loop through all race folders
    for race_folder in race_folders:
        race_path = os.path.join(races_dir, race_folder, "race-results.yml")
        if not os.path.exists(race_path):
            continue

        with open(race_path, 'r') as file:
            race_results = yaml.safe_load(file)

        # Extract retirement information for each constructor
        for result in race_results:
            constructor_id = result["constructorId"]
            position = result.get("position", "")
            reason_retired = result.get("reasonRetired", "")

            # Initialize constructor's retirement and race count if not already
            if constructor_id not in constructor_retirements:
                constructor_retirements[constructor_id] = 0
                constructor_races[constructor_id] = 0
            constructor_races[constructor_id] += 1

            # Check if the driver retired
            if position in ["DNF", "DSQ"] or reason_retired:
                constructor_retirements[constructor_id] += 1

    # Calculate reliability score for each constructor
    constructor_reliability = {}
    for constructor_id in constructor_retirements:
        reliability = 1 - (constructor_retirements[constructor_id] / constructor_races[constructor_id])
        constructor_reliability[constructor_id] = reliability

    return constructor_reliability

if __name__ == "__main__":
    try:
        reliability = get_constructor_reliability()
        print(reliability)
    except Exception as e:
        print(f"Error: {e}")
