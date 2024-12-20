import tkinter as tk
from tkinter import ttk, messagebox
import string

# Генерация таблицы подстановок
alphabet = string.ascii_lowercase + string.digits
substitution_table = {}
adfgvx = "ADFGVX"
index = 0
for row in adfgvx:
    for col in adfgvx:
        substitution_table[row + col] = alphabet[index]
        index += 1

reverse_table = {v: k for k, v in substitution_table.items()}

# Шифрование текста
def encrypt(text, key):
    text = text.lower().replace(" ", "")
    substituted = "".join(reverse_table.get(char, char) for char in text if char in reverse_table)

    # Таблица транспозиции
    key_order = sorted((k, i) for i, k in enumerate(key))
    columns = {k: [] for k in key_order}

    for i, char in enumerate(substituted):
        key_char = key[i % len(key)]
        columns[(key_char, key.index(key_char))].append(char)

    encrypted = "".join("".join(columns[k]) for k in key_order)
    return encrypted

# Расшифровка текста
def decrypt(ciphertext, key):
    key_order = sorted((k, i) for i, k in enumerate(key))
    col_lengths = [len(ciphertext) // len(key)] * len(key)
    for i in range(len(ciphertext) % len(key)):
        col_lengths[key_order[i][1]] += 1

    columns = {}
    start = 0
    for k, i in key_order:
        end = start + col_lengths[i]
        columns[k] = list(ciphertext[start:end])
        start = end

    rows = zip(*[columns[k] for k, _ in sorted(key_order)])
    substituted = "".join(char for row in rows for char in row)
    decrypted = "".join(substitution_table.get(substituted[i:i+2], substituted[i:i+2]) for i in range(0, len(substituted), 2))
    return decrypted.upper()

# Интерфейс пользователя
# Копирование текста в буфер обмена
def copy_to_clipboard(widget):
    text = widget.get("1.0", tk.END).strip()
    root.clipboard_clear()
    root.clipboard_append(text)
    root.update()

# Интерфейс пользователя
def process_encrypt():
    text = input_text.get("1.0", tk.END).strip()
    key = key_entry.get().strip()
    if not text or not key:
        messagebox.showerror("Ошибка", "Введите текст и ключ!")
        return
    try:
        encrypted = encrypt(text, key)
        output_text.delete("1.0", tk.END)
        output_text.insert("1.0", encrypted)
    except Exception as e:
        messagebox.showerror("Ошибка", f"Ошибка шифрования: {e}")

def process_decrypt():
    text = input_text.get("1.0", tk.END).strip()
    key = key_entry.get().strip()
    if not text or not key:
        messagebox.showerror("Ошибка", "Введите текст и ключ!")
        return
    try:
        decrypted = decrypt(text, key)
        output_text.delete("1.0", tk.END)
        output_text.insert("1.0", decrypted)
    except Exception as e:
        messagebox.showerror("Ошибка", f"Ошибка расшифровки: {e}")

# Создание окна
root = tk.Tk()
root.title("Шифр ADFGVX")
root.geometry("500x400")

# Поля ввода
frame1 = tk.Frame(root)
frame1.pack()

label1 = tk.Label(frame1, text="Введите текст:")
label1.pack(side=tk.LEFT)
copy_button1 = tk.Button(frame1, text="Копировать", command=lambda: copy_to_clipboard(input_text))
copy_button1.pack(side=tk.RIGHT)

input_text = tk.Text(root, height=5)
input_text.pack()

# Поле ввода ключа
key_frame = tk.Frame(root)
key_frame.pack()

key_label = tk.Label(key_frame, text="Ключ шифра:")
key_label.pack(side=tk.LEFT)
key_entry = tk.Entry(key_frame, width=20)
key_entry.pack(side=tk.RIGHT)

# Кнопки действий
encrypt_button = tk.Button(root, text="Зашифровать", command=process_encrypt)
encrypt_button.pack()

decrypt_button = tk.Button(root, text="Расшифровать", command=process_decrypt)
decrypt_button.pack()

# Поле вывода
frame2 = tk.Frame(root)
frame2.pack()

label2 = tk.Label(frame2, text="Результат:")
label2.pack(side=tk.LEFT)
copy_button2 = tk.Button(frame2, text="Копировать", command=lambda: copy_to_clipboard(output_text))
copy_button2.pack(side=tk.RIGHT)

output_text = tk.Text(root, height=5)
output_text.pack()

root.mainloop()