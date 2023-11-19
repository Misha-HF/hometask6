import os
import shutil

IMAGE_EXTENSIONS = ('JPEG', 'PNG', 'JPG', 'SVG')
VIDEO_EXTENSIONS = ('AVI', 'MP4', 'MOV', 'MKV')
DOCS_EXTENSIONS = ('DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX')
MUSIC_EXTENSIONS = ('MP3', 'OGG', 'WAV', 'AMR')
ARCHIVE_EXTENSIONS = ('ZIP', 'GZ', 'TAR')
UNKNOWN_EXTENSIONS = set()

def normalize(name):
    transliteration_dict = {
        'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'e',
        'ж': 'zh', 'з': 'z', 'и': 'i', 'й': 'j', 'к': 'k', 'л': 'l', 'м': 'm',
        'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u',
        'ф': 'f', 'х': 'kh', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'shch',
        'ъ': '', 'ы': 'y', 'ь': '', 'э': 'e', 'ю': 'yu', 'я': 'ya',
        'є': 'je', 'і': 'i', 'ї': 'ji', 'ґ': 'g'
    }
    
    result = ''.join(transliteration_dict.get(char, char) for char in name.lower())
    result = ''.join([c if c.isalpha() or c.isdigit() or c == '.' else '_' for c in result])
    return result

def process_directory(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            normalized_name = normalize(file)
            file_extension = normalized_name.split('.')[-1].upper()

            if file_extension in IMAGE_EXTENSIONS:
                destination_folder = "images"
            elif file_extension in VIDEO_EXTENSIONS:
                destination_folder = "video"
            elif file_extension in DOCS_EXTENSIONS:
                destination_folder = "documents"
            elif file_extension in MUSIC_EXTENSIONS:
                destination_folder = "audio"
            elif file_extension in ARCHIVE_EXTENSIONS:
                destination_folder = "archives"
                unpack_folder = os.path.splitext(normalized_name)[0]
                destination_folder = os.path.join(destination_folder, unpack_folder)
                os.makedirs(destination_folder, exist_ok=True)
                shutil.unpack_archive(file_path, destination_folder)
            else:
                destination_folder = "unknown"
                UNKNOWN_EXTENSIONS.add(file_extension)

            destination_path = os.path.join(directory, destination_folder, normalized_name)
            
            # Додано перевірку та створення каталогів
            if not os.path.isdir(destination_path):
                os.makedirs(os.path.dirname(destination_path), exist_ok=True)
            
            shutil.move(file_path, destination_path)

        for dir_name in dirs:
            dir_path = os.path.join(root, dir_name)
            # Ігноруємо папку "images"
            if dir_name.lower() not in ('images', 'video', 'documents', 'audio', 'archives'):
                process_directory(dir_path)
                if not os.listdir(dir_path):
                    os.rmdir(dir_path)

if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage: python sort.py <directory>")
        sys.exit(1)

    target_directory = sys.argv[1]
    process_directory(target_directory)

    print("\nFile sorting completed.\n")

    print("Known Extensions:")
    print("Images:", IMAGE_EXTENSIONS)
    print("Video:", VIDEO_EXTENSIONS)
    print("Documents:", DOCS_EXTENSIONS)
    print("Music:", MUSIC_EXTENSIONS)
    print("Archives:", ARCHIVE_EXTENSIONS)

    print("\nUnknown Extensions:")
    print(UNKNOWN_EXTENSIONS)
