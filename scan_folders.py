import os
import pathlib
import csv
import time
import pandas as pd
import multiprocessing
import config

def file_enumerator(folder_paths, input_queue): # Walks through each folder and enqueues file paths.

    

    for folder_path in folder_paths:
        for root, _, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                input_queue.put(file_path)
    num_workers = multiprocessing.cpu_count()
    for _ in range(num_workers):
        input_queue.put(None)


def worker(input_queue, output_queue): # Processes file paths from the input queue.
    
    while True:
        file_path = input_queue.get()
        if file_path is None:
            break
        try:
            file_stat = os.stat(file_path)
            file_type = pathlib.Path(file_path).suffix
            file_size = file_stat.st_size
            result = {
                "File Path": file_path,
                "Filename": os.path.basename(file_path),
                "Created Date": pd.to_datetime(file_stat.st_ctime, unit='s'),
                "Modified Date": pd.to_datetime(file_stat.st_mtime, unit='s'),
                "Type": file_type,
                "Size (Bytes)": file_size
            }
            output_queue.put(result)
        except Exception:
            continue
    output_queue.put(None)


def writer(output_queue, csv_filename, num_workers): # Reads processed file info from the output queue and writes it to a CSV.

    fieldnames = ["File Path", "Filename", "Created Date", "Modified Date", "Type", "Size (Bytes)"]
    with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
        csv_writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        csv_writer.writeheader()
        flush_counter = 0
        finished_workers = 0
        while finished_workers < num_workers:
            result = output_queue.get()
            if result is None:
                finished_workers += 1
                continue
            csv_writer.writerow(result)
            flush_counter += 1
            if flush_counter % 100 == 0:
                csvfile.flush()
        csvfile.flush()


def main():
    start_time = time.time()

    # List of folder paths to analyze. Check config.py
    folder_paths = config.folders

    csv_filename = f"file_details_{time.strftime('%Y%m%d')}.csv"
    num_workers = multiprocessing.cpu_count()

    # Use queues with a maxsize to prevent unbounded memory usage. 1kk = ~500mb
    input_queue = multiprocessing.Queue(maxsize=1000000)
    output_queue = multiprocessing.Queue(maxsize=1000000)

    enumerator = multiprocessing.Process(target=file_enumerator, args=(folder_paths, input_queue))
    enumerator.start()
    
    workers = []
    for _ in range(num_workers):
        p = multiprocessing.Process(target=worker, args=(input_queue, output_queue))
        p.start()
        workers.append(p)

    writer_process = multiprocessing.Process(target=writer, args=(output_queue, csv_filename, num_workers))
    writer_process.start()

    enumerator.join()
    for p in workers:
        p.join()
    writer_process.join()

    end_time = time.time()
    print(f"Total execution time: {end_time - start_time:.2f} seconds")


if __name__ == "__main__":
    multiprocessing.freeze_support()  # For Windows support
    main()
