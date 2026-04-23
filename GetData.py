import requests
import time
import csv
import os

def get_soil_data(lat, lon, retries=3):
    url = "https://rest.isric.org/soilgrids/v2.0/properties/query"
    properties = ["phh2o", "clay", "soc", "sand", "silt", "nitrogen"]
    params = {
        "lon": lon, "lat": lat,
        "property": properties,
        "depth": "0-5cm", "value": "mean"
    }
    for i in range(retries):
        try:
            response = requests.get(url, params=params, timeout=20)
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 404:
                return None
        except Exception as e:
            if i == retries - 1:
                print(f"\nError at {lat}, {lon}: {e}")
            else:
                time.sleep(1)
    return None

def process_data(data):
    if not data or "properties" not in data:
        return None
    results = {"lat": data["geometry"]["coordinates"][1], "lon": data["geometry"]["coordinates"][0]}
    layers = data["properties"].get("layers", [])
    has_valid_data = False
    for layer in layers:
        name = layer["name"]
        val = layer["depths"][0]["values"]["mean"]
        if val is not None:
            has_valid_data = True
            if name in ["phh2o", "clay", "sand", "silt", "nitrogen"]:
                results[name] = val / 10
            elif name == "soc":
                results[name] = val / 10
            else:
                results[name] = val
        else:
            results[name] = None
    return results if has_valid_data else None

# --- Configuration ---
LAT_MIN, LAT_MAX = 22.0, 31.7
LON_MIN, LON_MAX = 24.7, 36.9
STEP = 0.5 
MAX_RECORDS = 300

output_file = "egypt_soil_dataset.csv"
fieldnames = ["lat", "lon", "phh2o", "clay", "soc", "sand", "silt", "nitrogen"]

# Check for existing progress
existing_coords = set()
file_exists = os.path.isfile(output_file) and os.path.getsize(output_file) > 0

if file_exists:
    with open(output_file, mode="r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            existing_coords.add((float(row["lat"]), float(row["lon"])))
    print(f"Resuming: Found {len(existing_coords)} existing records.")

print(f"Targeting Egypt (Step: {STEP}). Output: {output_file}")
print(f"Will stop after {MAX_RECORDS} new records.")

with open(output_file, mode="a", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    if not file_exists:
        writer.writeheader()
    
    session_count = 0
    lat = LAT_MIN
    while lat <= LAT_MAX and session_count < MAX_RECORDS:
        lon = LON_MIN
        while lon <= LON_MAX and session_count < MAX_RECORDS:
            # Rounding to match floating point precision issues during resume
            curr_lat, curr_lon = round(lat, 2), round(lon, 2)
            
            if (curr_lat, curr_lon) in existing_coords:
                lon += STEP
                continue

            print(f"[{session_count + 1}/{MAX_RECORDS}] Fetching {curr_lat}, {curr_lon}...", end="\r")
            
            raw_data = get_soil_data(curr_lat, curr_lon)
            processed = process_data(raw_data)
            
            if processed:
                writer.writerow(processed)
                f.flush() # Force save to disk immediately
                session_count += 1
            
            lon += STEP
            time.sleep(0.1)
        lat += STEP

print(f"\n\nDone! Downloaded {session_count} new records.")
