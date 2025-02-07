# FS_file_analyzer
Analyses a series of directories defined by the user and returns the potential savings by deleting files older than X years


## Overview
This tool provides a detailed analysis of disk space usage by examining file ages within specified directories. It categorizes files based on their age—determining how much space could be saved by deleting files older than 1, 3, 5, and 10 years (customizable). The analysis results are visualized in a series of bar graphs, saved as an image file, which makes it easy to interpret the potential savings across multiple directories.

## Features
Multi-Folder Analysis: Analyze multiple folders simultaneously for a comprehensive overview.
Customizable Age Thresholds: Easily adjust the age thresholds for analyzing file ages.
Graphical Output: Visualizes disk space usage in bar graphs, grouped by folder, with results saved as a PNG image.
Efficiency: Utilizes pandas for data handling and matplotlib for generating graphics, optimized for large datasets.


## Prerequisites

Before running this script, ensure you have the following installed:
- Python 3.6 or higher
- Pandas library
- Matplotlib library
- Numpy library

You can install the required packages using pip:
```
pip install pandas matplotlib numpy
```

## Usage
To use this tool, follow these steps:

- Edit the config.py file and setup your target directories and age thresholds you want in the final report

#### Prepare Your Data:
- Run the scan_folders.py script. Ensure the resulting .csv file is generated in the same folder as the script

#### Run the processing script:
- Run the process_data.py script which will process the resulting .csv file and generate an image file with the results

#### Visualize the results.
- Check the output PNG image space_saved_by_folder.png for the graphical results.
