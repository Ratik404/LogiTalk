import threading
from socket import *
from customtkinter import *
from random import choice

yes=False
no=True

adjectives = [
    "Швидкий", "Темний", "Легкий", "Сильний", "Вогняний", "Холодний", "Яскравий", "Мудрий", "Злий", "Добрий",
    "Глибокий", "Кольоровий", "Тихий", "Шалений", "Летючий", "Срібний", "Золотий", "Старий", "Новий", "Веселий",
    "Сумний", "Твердий", "М'який", "Різкий", "Блискучий", "Темпераментний", "Мрійливий", "Солодкий", "Гіркий", "Сірий",
    "Казковий", "Лісовий", "Морський", "Небесний", "Прозорий", "Буйний", "Легковажний", "Зухвалий", "Спокійний", "Вірний",
    "Броньований", "Пряний", "Чистий", "Могутній", "Легендарний", "Потаємний", "Стриманий", "Неочікуваний", "Безстрашний", "Величний"
]

nouns = [
    "Дракон", "Лев", "Вовк", "Вогонь", "Ліс", "Моряк", "Шторм", "Меч", "Маг", "Лицар",
    "Фенікс", "Тигр", "Яструб", "Грім", "Місяць", "Зірка", "Хижак", "Рицар", "Кіт", "Ворон",
    "Мороз", "Буревій", "Гроза", "Вітрило", "Кристал", "Чарівник", "Борець", "Рейнджер", "Король", "Принц",
    "Самурай", "Ніндзя", "Орк", "Ельф", "Гоблін", "Гладіатор", "Гігант", "Тролль", "Кентавр", "Русалка",
    "Паладин", "Берсерк", "Сокол", "Орел", "Лицарка", "Привид", "Чаклун", "Ангел", "Демон", "Вартовий"
]

class MainWindow(CTk):
    def __init__(self):
        super().__init__()
        self.geometry('400x300')
        self.label = None
        self.def_mode = False
        self.theme_mode = "light"

        # menu frame
        self.menu_frame = CTkFrame(self, width=30, height=300)
        self.menu_frame.pack_propagate(False)
        self.menu_frame.place(x=0, y=0)
        self.is_show_menu = False
        self.speed_animate_menu = -5
        self.btn = CTkButton(self, text='▶️', command=self.toggle_show_menu, width=30)
        self.btn.place(x=0, y=0)

        # main chat UI
        self.chat_field = CTkTextbox(self, font=('Arial', 14, 'bold'), state='disable')
        self.chat_field.place(x=0, y=0)
        self.message_entry = CTkEntry(self, placeholder_text='Введіть повідомлення:', height=40)
        self.message_entry.place(x=0, y=0)
        self.send_button = CTkButton(self, text='>', width=50, height=40, command=self.send_message)
        self.send_button.place(x=0, y=0)

        self.username = choice(adjectives) + ' ' + choice(nouns)
        try:
            self.sock = socket(AF_INET, SOCK_STREAM)
            self.sock.connect(('localhost', 8080))
            hello = f"TEXT@{self.username}@[SYSTEM] {self.username} приєднався(лась) до чату!\n"
            self.sock.send(hello.encode('utf-8'))
            threading.Thread(target=self.recv_message, daemon=True).start()
        except Exception as e:
            self.add_message(f"Не вдалося підключитися до сервера: {e}")

        self.adaptive_ui()

    def toggle_show_menu(self):
        if self.is_show_menu:
            self.is_show_menu = False
            self.speed_animate_menu *= -1
            self.btn.configure(text='▶️')
            self.show_menu()
        else:
            self.is_show_menu = True
            self.speed_animate_menu *= -1
            self.btn.configure(text='◀️')
            self.show_menu()
            self.label = CTkLabel(self.menu_frame, text='Імʼя')
            self.label.pack(pady=10)
            self.entry = CTkEntry(self.menu_frame)
            self.entry.pack(pady=10)
            self.saveNameBtn = CTkButton(self.menu_frame, text='Зберегти', command=self.saveName)
            self.saveNameBtn.pack(pady=5)

            self.theme_button = CTkButton(self.menu_frame, width=80, height=40, text='Тема', command=self.toggle_theme)
            if self.def_mode:
                self.theme_button.configure(state="disabled")
            self.theme_button.place(x=10, y=200)

            self.clear_button = CTkButton(self.menu_frame, width=80, height=40, text='Очистка', command=self.clear_chat)
            self.clear_button.place(x=10, y=250)

            self.lang_btn = CTkButton(self.menu_frame, width=80, height=40, text='Файна Українська',command=self.set_lang)
            self.lang_btn.place(x=100, y=250)

    def show_menu(self):
        self.menu_frame.configure(width=self.menu_frame.winfo_width() + self.speed_animate_menu)
        if not self.menu_frame.winfo_width() >= 200 and self.is_show_menu:
            self.after(10, self.show_menu)
        elif self.menu_frame.winfo_width() >= 40 and not self.is_show_menu:
            self.after(10, self.show_menu)
            for attr in ('label', 'entry', 'saveNameBtn', 'theme_button', 'clear_button'):
                if hasattr(self, attr):
                    try:
                        getattr(self, attr).destroy()
                    except:
                        pass

    def toggle_theme(self):
        if self.def_mode:
            return
        if self.theme_mode == "dark":
            set_appearance_mode('light')
            self.theme_mode = "light"
            self.theme_button.configure(text='Темна тема')
        else:
            set_appearance_mode('dark')
            self.theme_mode = "dark"
            self.theme_button.configure(text='Світла тема ')

    def clear_chat(self):
        self.chat_field.configure(state='normal')
        self.chat_field.delete("1.0", END)
        self.chat_field.configure(state='disable')

    def saveName(self):
        if self.def_mode:
            return
        new_nick = self.entry.get()
        if new_nick:
            self.add_message(f"Користувач {self.username} змінив нік на {new_nick}")
            message = f"Користувач{self.username} змінив нік на{new_nick}"
            data = f"TEXT@{self.username}@{message}\n"
            try:
                self.sock.sendall(data.encode())
            except:
                pass
            self.username = new_nick

    def set_lang(self):
        global yes
        if yes == False:
            yes = True
            self.clear_button.configure(text='Хай горить')
            self.message_entry.configure(placeholder_text='Надряпай щось')
            self.lang_btn.configure(text='Українська')
            self.label.configure(text='Прізьвисько')
            self.saveNameBtn.configure(text='Переписати паспорт')
        elif yes == True:
            yes = False
            self.clear_button.configure(text='Очистка')
            self.message_entry.configure(placeholder_text='Введіть повідомлення')
            self.lang_btn.configure(text='Файна Українська')
            self.label.configure(text="Ім'я")
            self.saveNameBtn.configure(text='Зберегти')

    def _apply_def_style(self):
        set_appearance_mode('dark')
        self.theme_mode = 'dark'
        for widget in self.winfo_children():
            self._style_widget(widget)

    def _style_widget(self, widget):
        try:
            widget.configure(fg_color="black", text_color="green", border_color="green")
        except:
            pass
        for child in widget.winfo_children():
            self._style_widget(child)

    def adaptive_ui(self):
        self.menu_frame.configure(height=self.winfo_height())
        self.chat_field.place(x=self.menu_frame.winfo_width())
        self.chat_field.configure(width=self.winfo_width() - self.menu_frame.winfo_width(),
                                  height=self.winfo_height() - 40)
        self.send_button.place(x=self.winfo_width() - 50, y=self.winfo_height() - 40)
        self.message_entry.place(x=self.menu_frame.winfo_width(), y=self.send_button.winfo_y())
        self.message_entry.configure(
            width=self.winfo_width() - self.menu_frame.winfo_width() - self.send_button.winfo_width())
        self.after(50, self.adaptive_ui)

    def add_message(self, text):
        self.chat_field.configure(state='normal')
        if self.def_mode:
            self.chat_field.insert(END, "def_\n")
            self.chat_field.configure(text_color="green")
        else:
            self.chat_field.insert(END, text + '\n')
        self.chat_field.configure(state='disable')

    def send_message(self):
        message = self.message_entry.get().strip()
        if message == "/def_":
            self.def_mode = True
            self.username = "def_"
            if hasattr(self, 'theme_button'):
                self.theme_button.configure(state="disabled")
            self._apply_def_style()
            self.add_message("[SYSTEM] Режим def_ активовано")
        else:
            if self.def_mode:
                data = f"TEXT@{self.username}@def_\n"
            else:
                data = f"TEXT@{self.username}@{message}\n"
            try:
                self.sock.sendall(data.encode())
            except:
                pass
            if self.def_mode:
                self.add_message("def_")
            else:
                self.add_message(f"{self.username}: {message}")
        self.message_entry.delete(0, END)

    def recv_message(self):
        buffer = ""
        while True:
            try:
                chunk = self.sock.recv(4096)
                if not chunk:
                    break
                buffer += chunk.decode()
                while "\n" in buffer:
                    line, buffer = buffer.split("\n", 1)
                    self.handle_line(line.strip())
            except:
                break
        self.sock.close()

    def handle_line(self, line):
        if not line:
            return
        parts = line.split("@", 3)
        msg_type = parts[0]
        if msg_type == "TEXT":
            if len(parts) >= 3:
                author = parts[1]
                message = parts[2]
                if self.def_mode:
                    self.add_message("def_")
                else:
                    self.add_message(f"{author}: {message}")
        elif msg_type == "IMAGE":
            if len(parts) >= 4:
                author = parts[1]
                filename = parts[2]
                if self.def_mode:
                    self.add_message("def_")
                else:
                    self.add_message(f"{author} надіслав(ла) зображення: {filename}")
        else:
            if self.def_mode:
                self.add_message("def_")
            else:
                self.add_message(line)


win = MainWindow()
win.mainloop()

