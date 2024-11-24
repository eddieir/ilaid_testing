import requests
import math
import time
import json
import logging

# Configure logging
logging.basicConfig(
    filename="iss_tracker.log",  # Log output file
    level=logging.DEBUG,         # Log level (DEBUG for detailed logs)
    format="%(asctime)s - %(levelname)s - %(message)s"  # Log message format
)

# Haversine formula to calculate the distance between two geographic points
def haversine(lat1, lon1, lat2, lon2):
    if None in [lat1, lon1, lat2, lon2]:
        return None
    R = 6371.0
    lat1_rad, lon1_rad = math.radians(lat1), math.radians(lon1)
    lat2_rad, lon2_rad = math.radians(lat2), math.radians(lon2)
    dlat, dlon = lat2_rad - lat1_rad, lon2_rad - lon1_rad
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = R * c 
    logging.debug(f"Calculated distance: {distance} km between ({lat1}, {lon1}) and ({lat2}, {lon2}).")
    return distance  # Distance in kilometers

# Function to get the current ISS position
def get_iss_position():
    try:
        start_time = time.time()
        response = requests.get("http://api.open-notify.org/iss-now.json")
        response_time = time.time() - start_time
        response.raise_for_status()  # This raises an HTTPError for bad responses
        try:
            data = response.json()  # This could raise a ValueError for invalid JSON
            logging.info(f"API responded in {response_time:.2f} seconds.")
        except ValueError:
            print("Error parsing JSON response")
            return None, None , None
        if 'iss_position' in data:
            lat = data['iss_position'].get('latitude')
            lon = data['iss_position'].get('longitude')
            if lat and lon:
                timestamp = int(data['timestamp']) if 'timestamp' in data else None
                logging.debug(f"Received ISS position: latitude={lat}, longitude={lon}.")
                return float(lat), float(lon), timestamp
        logging.warning("API response does not contain valid ISS position data.")
        return None, None, int(data['timestamp']) if 'timestamp' in data else None  # Return timestamp even if no position data
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching ISS position: {e}")
        return None, None, None

# Function to save results to a JSON file
def save_results_to_json(results, filename="iss_speed_results.json"):
    try:
        with open(filename, 'w') as f:
            json.dump(results, f, indent=4)
        logging.info(f"Results saved to {filename}.")
    except Exception as e:
        logging.error(f"Error saving results to {filename}: {e}")

# Function to calculate the speed of the ISS
def calculate_speed(distance, time_diff):
    if time_diff == 0 or distance is None:
        return None
    return distance / time_diff

# Main function to track ISS speed
def track_iss_speed(max_runtime=30, poll_interval=1, output_file="iss_speed_results.json"):
    logging.info("Starting ISS speed tracking.")
    prev_lat, prev_lon, prev_timestamp = get_iss_position()
    prev_time = time.time()
    if prev_lat is None or prev_lon is None or prev_timestamp is None:
        logging.error("Invalid initial ISS position. Exiting.")
        save_results_to_json([], output_file)  # Save empty results if initial position fails
        return []
    results = []
    save_results_to_json(results, output_file)  # Save initial empty file
    start_time = time.time()
    while time.time() - start_time < max_runtime:
        time.sleep(poll_interval)
        curr_lat, curr_lon, curr_timestamp = get_iss_position()
        if curr_lat is None or curr_lon is None or curr_timestamp is None:
            logging.warning("Invalid ISS position. Skipping this poll.")
            continue
        curr_time = time.time()
        distance = haversine(prev_lat, prev_lon, curr_lat, curr_lon)
        time_diff = (curr_time - prev_time) / 3600
        speed = calculate_speed(distance, time_diff)
        if speed is not None:
            iss_data = {
                "timestamp": curr_timestamp,
                "message": "success",
                "iss_position": {
                    "latitude": f"{curr_lat:.4f}",
                    "longitude": f"{curr_lon:.4f}"
                }
            }
            results.append(iss_data)
            logging.info(f"Recorded ISS data: {iss_data}")
            save_results_to_json(results, output_file)  # Save results after every poll
        prev_lat, prev_lon, prev_time, prev_timestamp = curr_lat, curr_lon, curr_time, curr_timestamp
    logging.info("Tracking complete.")
    return results

# Run the program
if __name__ == "__main__":
    track_iss_speed()
