import csv, os, traceback

def write_to_csv(file_name, data):
    try:
        file_name = f"/app/data/{file_name}"
        file_exists = os.path.isfile(file_name)
        with open(file_name, mode='a', newline='') as file:
            writer = csv.DictWriter(file, fieldnames = data.keys()) 
            if not file_exists:
                writer.writeheader() 
            writer.writerow(data)
    except:
        traceback.print_exc()