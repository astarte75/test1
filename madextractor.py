import os
import shutil
import subprocess

def find_compressed_files(include_subfolders=False):
    """Returns a list of compressed files in the current and optionally subfolders."""
    
    compressed_files = []

    if include_subfolders:
        for root, dirs, files in os.walk('.'):
            for name in files:
                if name.endswith((".zip", ".tar.gz", ".rar")):
                    compressed_files.append(os.path.join(root, name))
    else:
        for name in os.listdir():
            if name.endswith((".zip", ".tar.gz", ".rar")):
                compressed_files.append(name)

    return compressed_files


def display_compressed_files(compressed_files):
    """Displays the list of compressed files."""
    
    print("Found {} compressed files:".format(len(compressed_files)))

    for idx, filename in enumerate(compressed_files, start=1):
        print("{}. {}".format(idx, filename))
        if idx % 10 == 0:
            choice = input("Press x to exit, any other key to continue: ")
            if choice.lower() == 'x':
                return


def validate_indices(compressed_files, selections):
    """Validates the selected index numbers."""
    
    indices = []

    for selection in selections.split(','):
        try:
            index = int(selection)
            if index < 1 or index > len(compressed_files):
                raise ValueError()
            indices.append(index)
        except ValueError:
            print("Invalid index: {}".format(selection))
            return False
    
    return indices


def get_destination():
    """Prompts for destination directory."""
    
    dest_dir = input("Enter destination directory (leave blank for current directory): ")
    if not dest_dir:
        dest_dir = "."
    
    if not os.path.isdir(dest_dir):
        print("Error: Invalid directory")
        return None
    
    return dest_dir


def extract_files(compressed_files, selected_indices, destination_directory):
    """Extracts the selected compressed files to the destination directory."""
    
    if not destination_directory:
        print("Extraction cancelled, no destination provided.")
        return False

    for index in selected_indices:
        filename = compressed_files[index-1]

        try:
            if filename.endswith(".zip"):
                subprocess.run(["unzip", filename, "-d", destination_directory])
            elif filename.endswith(".tar.gz"):
                subprocess.run(["tar", "xzvf", filename, "-C", destination_directory])
            elif filename.endswith(".rar"):
                subprocess.run(["unrar", "x", filename, destination_directory])
            else:
                print("Unsupported format:")
                continue
            print("Extracted:", filename)
        except subprocess.CalledProcessError:
            print("Error extracting", filename)

    print("Done.")
    return True


def main():
    """Main entry point of the program."""
    
    include_subfolders = input("Include subfolders? (y/n): ")
    if include_subfolders.lower().startswith('y'):
        compressed_files = find_compressed_files(include_subfolders=True) 
    else:
        compressed_files = find_compressed_files()

    if not compressed_files:
        print("No compressed files found.")
        return
    
    while True:
        display_compressed_files(compressed_files)
        selections = input("Enter file indices to extract (comma-separated), or type x to exit: ")
        if selections.lower() == 'x':
            print("Exiting without extracting files.")  
            return
            
        elif selections.lower() == 'm': 
            display_compressed_files(compressed_files)
            continue

        indices = validate_indices(compressed_files, selections)  
        if not indices:
            print("Invalid indices, please try again.")
            continue

        destination = get_destination()
        if not destination:
            return

        extract_files(compressed_files, indices, destination)

        choice = input("Extract more files? (y/n): ")
        if choice.lower() != 'y':
            break


if __name__ == "__main__":
    main()
