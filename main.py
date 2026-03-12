import os
import sys

# Compatibility layer: defines 'input' and 'print' behavior across versions
if sys.version_info[0] < 3:
    # Python 2.7 setup
    input_func = raw_input
else:
    # Python 3.x setup
    input_func = input

VPL_PATH = "bible.txt"
FOLDER_NAME = "verses"

def setup():
    if not os.path.exists(FOLDER_NAME):
        os.makedirs(FOLDER_NAME)

def get_verse_number(line):
    try:
        parts = line.split()
        for p in parts:
            if ":" in p:
                v_num = ''.join(c for c in p.split(":")[1] if c.isdigit())
                return int(v_num)
    except:
        pass
    return -1

def fetch_verses(reference):
    if not os.path.exists(VPL_PATH):
        return "Error: " + VPL_PATH + " not found."

    reference = reference.strip()
    results = []

    try:
        # Python 2/3 compatible file opening
        with open(VPL_PATH, 'r') as f:
            if "-" in reference:
                parts = reference.split("-")
                start_part = parts[0].strip()
                end_v = int(parts[1].strip())

                last_colon_idx = start_part.rfind(":")
                book_chap = start_part[:last_colon_idx + 1]
                start_v = int(start_part[last_colon_idx + 1:])

                for line in f:
                    if book_chap.lower() in line.lower():
                        current_v = get_verse_number(line)
                        if start_v <= current_v <= end_v:
                            results.append(line.strip())
            else:
                lower_ref = reference.lower() + " "
                for line in f:
                    if line.lower().startswith(lower_ref):
                        return line.strip()

        res_text = "\n\n".join(results)
        return res_text if res_text else "No text found for " + reference
    except Exception as e:
        return "VPL Error: " + str(e)

def save_marker(ref):
    if not ref: return
    file_name = ref.replace("-", "_").replace(":", "-") + ".jpg"
    file_path = os.path.join(FOLDER_NAME, file_name)

    if os.path.exists(file_path):
        print("\n[!] Marker already exists.")
    else:
        try:
            open(file_path, 'a').close()
            print("\n[+] Marker saved!")
        except Exception as e:
            print("\n[!] Error saving marker: " + str(e))

def list_markers():
    if not os.path.exists(FOLDER_NAME): return []
    markers = []
    files = os.listdir(FOLDER_NAME)
    for f in files:
        if f.endswith(".jpg"):
            readable = f.replace(".jpg", "").replace("-", ":").replace("_", "-")
            markers.append(readable)
    return sorted(markers)

def main():
    setup()
    while True:
        print("\n" + "="*30)
        print(" BIBLE MEMORY MANAGER (CLI)")
        print("="*30)
        print("1. Load Verse(s)")
        print("2. Save Current Reference")
        print("3. View Stored Markers")
        print("4. Exit")
        
        choice = input_func("\nChoose an option: ")

        if choice == '1':
            ref = input_func("Enter Reference (e.g., JOH 3:16): ")
            print("\n" + "-"*10)
            print(fetch_verses(ref))
            print("-"*10)
        
        elif choice == '2':
            ref = input_func("Enter Reference to save: ")
            save_marker(ref)

        elif choice == '3':
            markers = list_markers()
            if not markers:
                print("\nNo markers stored yet.")
            else:
                print("\nSTORED MARKERS:")
                for i, m in enumerate(markers):
                    # Uses .format() which works in 2.7 and 3.x
                    print("{0}. {1}".format(i + 1, m))
                
                sub_choice = input_func("\nEnter number to load (or Enter to go back): ")
                if sub_choice.isdigit():
                    idx = int(sub_choice) - 1
                    if 0 <= idx < len(markers):
                        print("\n" + "-"*10)
                        print(fetch_verses(markers[idx]))
                        print("-"*10)

        elif choice == '4':
            print("Goodbye!")
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()