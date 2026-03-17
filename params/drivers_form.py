import os
import yaml

def get_drivers_form():
    # Construct the absolute path to the races directory
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    races_dir = os.path.join(base_dir, 'f1db-main', 'src', 'data', 'seasons', '2025', 'races')

    if not os.path.exists(races_dir):
        raise FileNotFoundError(f"The directory does not exist: {races_dir}")

    race_folders = sorted(os.listdir(races_dir))[-5:]

    drivers_positions = {}

    for race_folder in race_folders:
        race_path = os.path.join(races_dir, race_folder, "race-results.yml")
        if not os.path.exists(race_path):
            continue  # Skip if the file doesn't exist

        with open(race_path, 'r') as file:
            race_results = yaml.safe_load(file)

        for result in race_results:
            driver_id = result["driverId"]
            position = result["position"]

            # Convert non-numeric positions to 22
            if position in ["DNF", "DSQ"] or not str(position).isdigit():
                position = 22
            else:
                position = int(position)

            if driver_id not in drivers_positions:
                drivers_positions[driver_id] = []
            drivers_positions[driver_id].append(position)

    drivers_form = {}
    for driver_id, positions in drivers_positions.items():
        avg_position = sum(positions) / len(positions)
        drivers_form[driver_id] = avg_position

    return drivers_form

if __name__ == "__main__":
    try:
        form = get_drivers_form()
        print(form)
    except Exception as e:
        print(f"Error: {e}")
