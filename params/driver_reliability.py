import os
import yaml

def get_driver_reliability():
    # Absolute path to the races directory
    races_dir = r"C:\Users\migue\Desktop\F1 predictor\f1db-main\src\data\seasons\2025\races"

    if not os.path.exists(races_dir):
        raise FileNotFoundError(f"The directory does not exist: {races_dir}")

    # Get all race folders
    race_folders = sorted(os.listdir(races_dir))

    # Initialize a dictionary to store retirement counts for each driver
    driver_retirements = {}
    driver_races = {}

    # Loop through all race folders
    for race_folder in race_folders:
        race_path = os.path.join(races_dir, race_folder, "race-results.yml")
        if not os.path.exists(race_path):
            continue

        with open(race_path, 'r') as file:
            race_results = yaml.safe_load(file)

        # Extract retirement information for each driver
        for result in race_results:
            driver_id = result["driverId"]
            position = result.get("position", "")
            reason_retired = result.get("reasonRetired", "")

            # Initialize driver's retirement and race count if not already
            if driver_id not in driver_retirements:
                driver_retirements[driver_id] = 0
                driver_races[driver_id] = 0
            driver_races[driver_id] += 1

            # Check if the driver retired
            if position in ["DNF", "DSQ"] or reason_retired:
                driver_retirements[driver_id] += 1

    # Calculate reliability score for each driver
    driver_reliability = {}
    for driver_id in driver_retirements:
        reliability = 1 - (driver_retirements[driver_id] / driver_races[driver_id])
        driver_reliability[driver_id] = reliability

    return driver_reliability

if __name__ == "__main__":
    try:
        reliability = get_driver_reliability()
        print(reliability)
    except Exception as e:
        print(f"Error: {e}")
