import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import threading
import time
import random
import json
import os

class StudentProductivityToolkit:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Productivity Toolkit")
        self.root.geometry("500x400")
        
        self.create_menu()
        self.current_frame = None
        self.load_timer_frame()

    def create_menu(self):
        menu_bar = tk.Menu(self.root)
        self.root.config(menu=menu_bar)

        menu_bar.add_command(label="Timer Belajar", command=self.load_timer_frame)
        menu_bar.add_command(label="Catatan Harian", command=self.load_notes_frame)
        menu_bar.add_command(label="To-Do List", command=self.load_todo_frame)
        menu_bar.add_command(label="Motivational Quotes", command=self.load_quote_frame)
        menu_bar.add_command(label="Kalkulator", command=self.load_calculator_frame)
        menu_bar.add_command(label="Keluar", command=self.exit_app)

    def switch_frame(self, frame_class):
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = frame_class(self.root)

    def load_timer_frame(self):
        self.switch_frame(TimerFrame)

    def load_notes_frame(self):
        self.switch_frame(NotesFrame)

    def load_todo_frame(self):
        self.switch_frame(ToDoFrame)

    def load_quote_frame(self):
        self.switch_frame(QuoteFrame)

    def load_calculator_frame(self):
        self.switch_frame(CalculatorFrame)

    def exit_app(self):
        if messagebox.askyesno("Keluar", "Yakin ingin keluar dari aplikasi?"):
            self.root.destroy()

# TIMER BELAJAR
class TimerFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.pack(fill="both", expand=True, padx=10, pady=10)

        ttk.Label(self, text="Timer Belajar", font=("Arial", 16)).grid(row=0, column=0, columnspan=2, pady=10)

        ttk.Label(self, text="Durasi (detik):").grid(row=1, column=0, sticky="e")
        self.entry = ttk.Entry(self, width=10)
        self.entry.grid(row=1, column=1, sticky="w")
        self.entry.insert(0, "0")

        self.start_button = ttk.Button(self, text="Mulai", command=self.start_timer)
        self.start_button.grid(row=2, column=0, columnspan=2, pady=5)

        self.time_label = ttk.Label(self, text="", font=("Arial", 14))
        self.time_label.grid(row=3, column=0, columnspan=2, pady=10)

    def start_timer(self):
        try:
            duration = int(self.entry.get())
            threading.Thread(target=self.run_timer, args=(duration,)).start()
        except ValueError:
            messagebox.showerror("Error", "Masukkan angka yang valid")

    def run_timer(self, duration):
        for i in range(duration, -1, -1):
            self.time_label.config(text=f"Waktu tersisa: {i} detik")
            time.sleep(1)
        self.time_label.config(text="Waktu habis!")

# CATATAN HARIAN
class NotesFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.pack(fill="both", expand=True, padx=10, pady=10)

        ttk.Label(self, text="Catatan Harian", font=("Arial", 16)).grid(row=0, column=0, pady=10)

        self.text_area = tk.Text(self, height=15, width=50)
        self.text_area.grid(row=1, column=0, pady=10)

        self.load_notes()

        ttk.Button(self, text="Simpan", command=self.save_notes).grid(row=2, column=0, pady=5)
        
    def save_notes(self):
        notes = self.text_area.get("1.0", tk.END).strip()
        with open("notes.txt", "w") as file:
            file.write(notes)
        messagebox.showinfo("Info", "Catatan berhasil disimpan")

    def load_notes(self):
        if os.path.exists("notes.txt"):
            with open("notes.txt", "r") as file:
                self.text_area.insert(tk.END, file.read())

# TO - DO LIST
class ToDoFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        # Mengatur frame agar dapat mengisi seluruh ruang yang tersedia
        self.pack(fill="both", expand=True, padx=10, pady=10)

        # Menambahkan label "To-Do List" di bagian atas
        ttk.Label(self, text="To-Do List", font=("Arial", 16)).grid(row=0, column=0, columnspan=2, pady=10)

        # Menambahkan listbox untuk menampilkan daftar tugas
        self.listbox = tk.Listbox(self, width=40, height=10, selectmode=tk.SINGLE)
        self.listbox.grid(row=1, column=0, columnspan=2)

        # Menambahkan entry field untuk input tugas baru
        self.entry = ttk.Entry(self, width=30)
        self.entry.grid(row=2, column=0, pady=5)

        # Menambahkan tombol "Tambah" untuk menambah tugas baru
        ttk.Button(self, text="Tambah", command=self.add_task).grid(row=2, column=1, pady=5)

        # Menambahkan tombol "Hapus" untuk menghapus tugas yang dipilih
        ttk.Button(self, text="Hapus", command=self.delete_task).grid(row=3, column=1, pady=5)

        # Menambahkan tombol "Selesaikan" untuk menandai tugas yang selesai
        ttk.Button(self, text="Selesaikan", command=self.complete_task).grid(row=4, column=0, pady=5)

        # Menambahkan tombol "Hapus Semua" untuk menghapus semua tugas
        ttk.Button(self, text="Hapus Semua", command=self.clear_all).grid(row=4, column=1, pady=5)

        # Memuat tugas yang telah disimpan sebelumnya saat aplikasi dijalankan
        self.load_tasks()

    def add_task(self):
        # Mengambil teks dari entry field dan menghapus spasi ekstra
        task = self.entry.get().strip()
        if task:
            # Menambahkan tugas ke listbox jika ada input
            self.listbox.insert(tk.END, task)
            # Mengosongkan entry field setelah tugas ditambahkan
            self.entry.delete(0, tk.END)
            # Menyimpan daftar tugas setelah penambahan
            self.save_tasks()

    def delete_task(self):
        try:
            # Mengambil indeks tugas yang dipilih
            selected_task = self.listbox.curselection()[0]
            # Menghapus tugas yang dipilih dari listbox
            self.listbox.delete(selected_task)
            # Menyimpan perubahan setelah menghapus tugas
            self.save_tasks()
        except IndexError:
            # Menampilkan pesan error jika tidak ada tugas yang dipilih
            messagebox.showerror("Error", "Pilih tugas untuk dihapus")

    def complete_task(self):
        try:
            # Mengambil indeks tugas yang dipilih
            selected_task = self.listbox.curselection()[0]
            # Menandai tugas yang selesai dengan mengubah latar belakangnya menjadi hijau muda
            self.listbox.itemconfig(selected_task, {'bg':'lightgreen'})
            # Menyimpan perubahan setelah menandai tugas selesai
            self.save_tasks()
        except IndexError:
            # Menampilkan pesan error jika tidak ada tugas yang dipilih
            messagebox.showerror("Error", "Pilih tugas untuk ditandai selesai")

    def clear_all(self):
        # Menanyakan konfirmasi dari pengguna sebelum menghapus semua tugas
        if messagebox.askyesno("Hapus Semua", "Yakin ingin menghapus semua tugas?"):
            # Menghapus semua tugas di listbox
            self.listbox.delete(0, tk.END)
            # Menyimpan perubahan setelah menghapus semua tugas
            self.save_tasks()

    def save_tasks(self):
        # Mengambil semua tugas dari listbox dan menyimpannya dalam bentuk list
        tasks = self.listbox.get(0, tk.END)
        # Menyimpan daftar tugas ke file JSON
        with open("tasks.json", "w") as file:
            json.dump(tasks, file)

    def load_tasks(self):
        # Mengecek apakah file tasks.json ada
        if os.path.exists("tasks.json"):
            # Membaca file tasks.json dan memuat tugas-tugas yang ada ke listbox
            with open("tasks.json", "r") as file:
                for task in json.load(file):
                    self.listbox.insert(tk.END, task)

# MOTIVATIONAL QUOTE GENERATOR
class QuoteFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.pack(fill="both", expand=True, padx=10, pady=10)

        ttk.Label(self, text="Motivational Quotes", font=("Arial", 16)).grid(row=0, column=0, pady=10)

        self.quote_label = ttk.Label(self, text="", font=("Arial", 12), wraplength=400)
        self.quote_label.grid(row=1, column=0, pady=10)

        ttk.Button(self, text="Tampilkan Kutipan", command=self.show_quote).grid(row=2, column=0, pady=5)

    def show_quote(self):
        quotes = [
            "Believe in yourself!",
            "Keep pushing forward!",
            "Success is the sum of small efforts, repeated day in and day out.",
            "Don’t watch the clock; do what it does. Keep going.",
            "The future depends on what you do today."
        ]
        self.quote_label.config(text=random.choice(quotes))

# KALKULATOR SEDERHANA
class CalculatorFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.pack(fill="both", expand=True, padx=10, pady=10)

        ttk.Label(self, text="Kalkulator", font=("Arial", 16)).grid(row=0, column=0, columnspan=4, pady=10)

        self.entry = ttk.Entry(self, font=("Arial", 14), justify="right")
        self.entry.grid(row=1, column=0, columnspan=4, sticky="we", padx=5, pady=5)

        buttons = [
            ('7', 2, 0), ('8', 2, 1), ('9', 2, 2), ('/', 2, 3),
            ('4', 3, 0), ('5', 3, 1), ('6', 3, 2), ('*', 3, 3),
            ('1', 4, 0), ('2', 4, 1), ('3', 4, 2), ('-', 4, 3),
            ('C', 5, 0), ('0', 5, 1), ('=', 5, 2), ('+', 5, 3),
        ]

        for (text, row, col) in buttons:
            ttk.Button(self, text=text, command=lambda t=text: self.on_button_click(t)).grid(
                row=row, column=col, padx=5, pady=5, sticky="nsew"
            )

        for i in range(6):
            self.rowconfigure(i, weight=1)
        for i in range(4):
            self.columnconfigure(i, weight=1)

    def on_button_click(self, char):
        if char == "C":
            self.entry.delete(0, tk.END)
        elif char == "=":
            try:
                expression = self.entry.get()
                result = eval(expression)
                self.entry.delete(0, tk.END)
                self.entry.insert(tk.END, str(result))
            except Exception:
                messagebox.showerror("Error", "Ekspresi tidak valid")
        else:
            self.entry.insert(tk.END, char)

if __name__ == "__main__":
    root = tk.Tk()
    app = StudentProductivityToolkit(root)
    root.mainloop()
