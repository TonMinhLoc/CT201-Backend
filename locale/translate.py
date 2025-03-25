import os
import subprocess
from googletrans import Translator

def translate_po_file(input_file, output_file):
    translator = Translator()

    with open(input_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    with open(output_file, 'w', encoding='utf-8') as file:
        for line in lines:
            if line.startswith('msgid'):
                original_text = line.split('"')[1]
                # Dịch chuỗi sang tiếng Việt
                translated_text = translator.translate(original_text, dest='vi').text
                file.write(line)  # Ghi lại dòng msgid gốc
                file.write(f'msgstr "{translated_text}"\n')  # Ghi lại bản dịch
            else:
                file.write(line)  # Ghi lại các dòng không cần dịch

def create_and_compile_messages(base_dir):
    locale_dir = os.path.join(base_dir, 'locale', 'vi', 'LC_MESSAGES')
    input_file = os.path.join(locale_dir, 'django.po')
    output_file = os.path.join(locale_dir, 'django_translated.po')

    # Tạo thư mục nếu chưa tồn tại
    if not os.path.exists(locale_dir):
        os.makedirs(locale_dir)
        print(f"Đã tạo thư mục {locale_dir}")

    # Lệnh tạo tệp dịch (.po)
    print("Đang tạo tệp .po...")
    subprocess.run(['django-admin', 'makemessages', '-l', 'vi'], cwd=base_dir)

    # Dịch tệp .po
    print(f"Dịch tệp {input_file} sang tiếng Việt...")
    translate_po_file(input_file, output_file)

    # Đổi tên tệp dịch mới thành django.po
    os.rename(output_file, input_file)
    print(f"Đã thay thế {input_file} bằng bản dịch mới.")

    # Biên dịch tệp dịch (.po -> .mo)
    print("Đang biên dịch tệp .po thành .mo...")
    subprocess.run(['django-admin', 'compilemessages'], cwd=base_dir)

    print("Hoàn thành!")

if __name__ == "__main__":
    # Đường dẫn tới thư mục gốc của dự án Django
    base_dir = '/Users/bimac/Documents/HK2-2024-2025/CT201/main/backend'
    create_and_compile_messages(base_dir)
