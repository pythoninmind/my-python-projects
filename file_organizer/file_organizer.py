# used for path managing
from pathlib import Path
# manages JSON files
import json
# imports calculate_file_hash for digital fingerprint and get_file_type for type recognition
from utils import calculate_file_hash, get_file_type

SOURCE_DIR = Path("input")
SORTED_DIR = Path("sorted")
REPORT_DIR = Path("reports")

# creates directories input, sorted and reports, if not existing
def ensure_dirs():
    # create source automatically, if not existing
    if not SOURCE_DIR.exists():
        print(f"\nDirectory '{SOURCE_DIR}' not found. Creating...")
        SOURCE_DIR.mkdir(exist_ok=True)
        
    SORTED_DIR.mkdir(exist_ok=True)
    REPORT_DIR.mkdir(exist_ok=True)
# main logic: loops through all files in source directory, determinestype, checks for duplicates and pushes in corresponding child directories
def organize_files():
    # get function
    ensure_dirs()
    if not any(SOURCE_DIR.iterdir()):
        print(f"\nDirectory '{SOURCE_DIR}' is empty. Please insert files.")
        return
    
    duplicates = {}
    summary = {}

    for file in SOURCE_DIR.iterdir():
        if file.is_file():
            file_type = get_file_type(file)
            target_dir = SORTED_DIR / file_type
            target_dir.mkdir(exist_ok=True)

            file_hash = calculate_file_hash(file)
            if not file_hash:
                continue

            # check for duplicates
            if file_hash in duplicates:
                duplicates[file_hash].append(str(file))
                continue
            else:
                duplicates[file_hash] = [str(file)]

            # move file
            try:
                file.rename(target_dir / file.name)
            except Exception as e:
                print(f"Moving fails: {file}: {e}")

            # Summary
            summary[file_type] = summary.get(file_type, 0) + 1

    save_reports(duplicates, summary)
# writes a duplicates.json, includes filepath grouped by hash value and a summary.txt, numbers of files per type
def save_reports(duplicates, summary):
    # JSON Report for Duplicates
    with open(REPORT_DIR / "duplicates.json", "w") as f:
        json.dump(duplicates, f, indent=4)

    # TXT Summary
    with open(REPORT_DIR / "summary.txt", "w") as f:
        for file_type, count in summary.items():
            f.write(f"{file_type}: {count} Files\n")

if __name__ == "__main__":
    organize_files()

"""
File Processing Workflow (organize_files), how it works:

For every file inside the input folder, the following steps occur:
1. Determine type: get_file_type(file) identifies the file type (e.g., "Images" or "Documents"). A matching subfolder inside sorted/ is then created.
2. Check for duplicates: The function calculates the MD5/SHA hash of the file. If the exact same hash has already been registered, the file is logged as a duplicate in the list.
3. Move: The file is relocated to the new type subfolder using file.rename().
4. Count: The counter for this specific file type increases by 1 in the summary statistics.

A Critical Flaw in the Code:
The code contains a logical error regarding how duplicates are handled:
When a file is flagged as a duplicate, the script triggers a continue statement and skips immediately to the next file. Consequently, the duplicate file remains completely untouched in the input folder (it is neither deleted nor moved), even though it appears in the JSON report. 
Furthermore, the statistics (summary) completely exclude duplicates from the final count.

Need to modify the code so that duplicates are automatically deleted or moved into a separate duplicates folder.
"""
