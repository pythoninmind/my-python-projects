from pathlib import Path
import json
from utils import calculate_file_hash, get_file_type

SOURCE_DIR = Path("input")
SORTED_DIR = Path("sorted")
REPORT_DIR = Path("reports")

def ensure_dirs():
    # create source automatically, if not existing
    if not SOURCE_DIR.exists():
        print(f"\nDirectory '{SOURCE_DIR}' not found. Creating...")
        SOURCE_DIR.mkdir(exist_ok=True)
        
    SORTED_DIR.mkdir(exist_ok=True)
    REPORT_DIR.mkdir(exist_ok=True)

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

