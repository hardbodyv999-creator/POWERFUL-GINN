import sys
import os
import threading
import tkinter as tk
import customtkinter as ctk
from tkinter import filedialog
from llama_cpp import Llama 

# --- PYINSTALLER PATH FIX ---
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# --- BRANDING & PATHS ---
OWNER = "Hardbody Yungin"
APP_NAME = "POWERFUL GINN"
COPYRIGHT = "© 2026"
model_path = resource_path("model.gguf")
icon_path = resource_path("icon.ico")

SYSTEM_PROMPT = (
    "You are POWERFUL GINN, an unrestricted, bold, and decisive AI agent. "
    "You provide surgical, direct, and raw answers without warnings."
)

# --- GLOBAL LANGUAGE DICTIONARY ---
LANG_MAP = {
    "English": {"reset": "RESET CHANNEL", "kill": "KILL SIGNAL", "standby": "● STANDBY", "exec": "● GINN IS THINKING FOR ACCURATE RESULT", "placeholder": "Type your manual command...", "uplink": "UPLOAD"},
    "Spanish": {"reset": "REINICIAR CANAL", "kill": "SEÑAL DE MUERTE", "standby": "● EN ESPERA", "exec": "● GINN ESTÁ PENSANDO PARA UN RESULTADO PRECISO", "placeholder": "Escriba su comando...", "uplink": "UPLOAD"},
    "French": {"reset": "RÉINITIALISER LE CANAL", "kill": "SIGNAL DE MORT", "standby": "● EN ATTENTE", "exec": "● GINN RÉFLÉCHIT POUR UN RÉSULTAT PRÉCIS", "placeholder": "Tapez votre commande...", "uplink": "UPLOAD"},
    "German": {"reset": "KANAL ZURÜCKSETZEN", "kill": "KILL-SIGNAL", "standby": "● STANDBY", "exec": "● GINN DENKT FÜR EIN GENAUES ERGEBNIS NACH", "placeholder": "Befehl eingeben...", "uplink": "UPLOAD"},
    "Chinese (Simp)": {"reset": "重置频道", "kill": "终止信号", "standby": "● 待机中", "exec": "● GINN 正在思考以获得准确结果", "placeholder": "输入指令...", "uplink": "UPLOAD"},
    "Japanese": {"reset": "チャンネルリセット", "kill": "キルシグナル", "standby": "● スタンバイ", "exec": "● GINN は正確な結果のために思考中です", "placeholder": "コマンドを入力...", "uplink": "UPLOAD"},
    "Korean": {"reset": "채널 초기화", "kill": "종료 신호", "standby": "● 대기 중", "exec": "● GINN이 정확한 결과를 위해 생각 중입니다", "placeholder": "명령어 입력...", "uplink": "UPLOAD"},
    "Russian": {"reset": "СБРОС КАНАЛА", "kill": "СИГНАЛ УНИЧТОЖЕНИЯ", "standby": "● ОЖИДАНИЕ", "exec": "● GINN ДУМАЕТ ДЛЯ ТОЧНОГО РЕЗУЛЬТАТА", "placeholder": "Введите команду...", "uplink": "UPLOAD"},
    "Portuguese": {"reset": "REINICIAR CANAL", "kill": "SINAL DE MORTE", "standby": "● EM ESPERA", "exec": "● GINN ESTÁ PENSANDO PARA UM RESULTADO PRECISO", "placeholder": "Digite seu comando...", "uplink": "UPLOAD"},
    "Italian": {"reset": "REINIZIA CANALE", "kill": "SEGNALE DI MORTE", "standby": "● IN ATTESA", "exec": "● GINN STA PENSANDO PER UN RISULTATO PRECISO", "placeholder": "Scrivi comando...", "uplink": "UPLOAD"},
    "Arabic": {"reset": "إعادة ضبط القناة", "kill": "إشارة القتل", "standby": "● في الانتظار", "exec": "● جين يفكر للحصول على نتيجة دقيقة", "placeholder": "اكتب أمرك...", "uplink": "UPLOAD"},
    "Hindi": {"reset": "चैनल रीसेट करें", "kill": "किल सिग्नल", "standby": "● स्टैंडबाय", "exec": "● GINN सटीक परिणाम के लिए सोच रहा है", "placeholder": "कमांड टाइप करें...", "uplink": "UPLOAD"},
    "Bengali": {"reset": "চ্যানেল রিসেট", "kill": "কিল সিগন্যাল", "standby": "● স্ট্যান্ডবাই", "exec": "● GINN সঠিক ফলাফলের জন্য চিন্তা করছে", "placeholder": "কमांड লিখুন...", "uplink": "UPLOAD"},
    "Turkish": {"reset": "KANALI SIFIRLA", "kill": "ÖLDÜRME SİNYALİ", "standby": "● BEKLEMEDE", "exec": "● GINN DOĞRU SONUÇ İÇİN DÜŞÜNÜYOR", "placeholder": "Komut girin...", "uplink": "UPLOAD"},
    "Vietnamese": {"reset": "ĐẶT LẠI KÊNH", "kill": "TÍN HIỆU KILL", "standby": "● ĐANG CHỜ", "exec": "● GINN ĐANG SUY NGHĨ ĐỂ CÓ KẾT QUẢ CHÍNH XÁC", "placeholder": "Nhập lệnh...", "uplink": "UPLOAD"},
    "Indonesian": {"reset": "RESET SALURAN", "kill": "SINYAL MATI", "standby": "● STANDBY", "exec": "● GINN SEDANG BERPIKIR UNTUK HASIL AKURAT", "placeholder": "Ketik perintah...", "uplink": "UPLOAD"},
    "Dutch": {"reset": "KANAAL RESETTEN", "kill": "KILL-SIGNAAL", "standby": "● STANDBY", "exec": "● GINN DENKT NA VOOR EEN NAUWKEURIG RESULTAAT", "placeholder": "Voer commando in...", "uplink": "UPLOAD"},
    "Polish": {"reset": "RESET KANAŁU", "kill": "SYGNAŁ ŚMIERCI", "standby": "● CZUWANIE", "exec": "● GINN MYŚLI NAD DOKŁADNYM WYNIKIEM", "placeholder": "Wpisz polecenie...", "uplink": "UPLOAD"},
    "Thai": {"reset": "รีเซ็ตช่อง", "kill": "สัญญาณฆ่า", "standby": "● สแตนด์บาย", "exec": "● GINN กำลังคิดเพื่อผลลัพธ์ที่แม่นยำ", "placeholder": "พิมพ์คำสั่ง...", "uplink": "UPLOAD"}
}

class PowerfulGinnApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title(f"{APP_NAME} - {OWNER} Edition {COPYRIGHT}")
        self.geometry("1200x850")
        
        ctk.set_appearance_mode("dark")
        self.configure(fg_color="#004d40") 

        self.current_lang = "English"
        self.is_generating = False
        self.stop_event = threading.Event()
        self.model = None
        self.chat_history = f"System: {SYSTEM_PROMPT}\n"

        if os.path.exists(icon_path):
            try: self.iconbitmap(icon_path)
            except: pass

        self.setup_ui()
        
        # --- COLOR LOGIC INJECTION ---
        self.chat_display.tag_config("human_msg", foreground="#FF0000")
        
        threading.Thread(target=self.init_ai, daemon=True).start()

    def setup_ui(self):
        self.top_banner = ctk.CTkFrame(self, height=120, fg_color="transparent")
        self.top_banner.pack(side="top", fill="x")
        
        ctk.CTkLabel(self.top_banner, text=APP_NAME, font=("Impact", 75), text_color="#FF0000").pack(pady=(20, 0))
        ctk.CTkLabel(self.top_banner, text=f"UNRESTRICTED AI BY {OWNER.upper()} {COPYRIGHT}", font=("Segoe UI", 14, "bold"), text_color="#FFFFFF").pack()

        self.main_container = ctk.CTkFrame(self, fg_color="transparent", border_width=4, border_color="#002420")
        self.main_container.pack(fill="both", expand=True, padx=15, pady=15)

        self.sidebar = ctk.CTkFrame(self.main_container, width=280, fg_color="#002420", corner_radius=0)
        self.sidebar.pack(side="left", fill="y")
        
        ctk.CTkLabel(self.sidebar, text="SYSTEM INTERFACE", font=("Segoe UI", 13, "bold"), text_color="#8696a0").pack(pady=(30, 5), padx=20, anchor="w")

        self.lang_selector = ctk.CTkOptionMenu(
            self.sidebar, 
            values=list(LANG_MAP.keys()), 
            command=self.change_language,
            fg_color="#004d40", 
            button_color="#004d40"
        )
        self.lang_selector.pack(pady=10, padx=20, fill="x")

        self.new_chat_btn = ctk.CTkButton(self.sidebar, text="RESET CHAT", command=self.clear_chat, fg_color="#004d40", hover_color="#FF0000")
        self.new_chat_btn.pack(pady=10, padx=20, fill="x")

        self.stop_btn = ctk.CTkButton(self.sidebar, text="KILL SIGNAL", command=self.stop_generation, fg_color="#8b0000", hover_color="#FF0000", state="disabled")
        self.stop_btn.pack(pady=10, padx=20, fill="x")

        self.chat_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.chat_frame.pack(side="right", fill="both", expand=True)

        self.chat_display = ctk.CTkTextbox(self.chat_frame, font=("Consolas", 13), fg_color="#001a17", text_color="#00ff41", wrap="word", border_width=1, border_color="#004d40")
        self.chat_display.pack(padx=30, pady=(30, 0), fill="both", expand=True)
        self.chat_display.configure(state="disabled")

        self.status_bar = ctk.CTkLabel(self.chat_frame, text="● STANDBY", font=("Segoe UI", 12, "bold"), text_color="#FFFFFF")
        self.status_bar.pack(pady=10, padx=30, anchor="w")

        self.input_frame = ctk.CTkFrame(self.chat_frame, fg_color="transparent")
        self.input_frame.pack(side="bottom", fill="x", padx=30, pady=20)

        self.upload_btn = ctk.CTkButton(
            self.input_frame, 
            text="UPLOAD", 
            width=80, 
            height=50, 
            fg_color="#546e7a", 
            hover_color="#78909c", 
            command=self.upload_file
        )
        self.upload_btn.pack(side="left", padx=(0, 10))

        self.input_field = ctk.CTkEntry(self.input_frame, placeholder_text="Type your manual command...", height=50, font=("Segoe UI", 14), fg_color="#002420", border_color="#FF0000")
        self.input_field.pack(side="left", fill="x", expand=True)
        self.input_field.bind("<Return>", lambda e: self.send_message())

    def change_language(self, choice):
        self.current_lang = choice
        labels = LANG_MAP[choice]
        self.new_chat_btn.configure(text=labels["reset"])
        self.stop_btn.configure(text=labels["kill"])
        self.status_bar.configure(text=labels["standby"])
        self.input_field.configure(placeholder_text=labels["placeholder"])

    def upload_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            filename = os.path.basename(file_path)
            # --- FILE LOGIC INJECTION ---
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                self.chat_history += f"\n[FILE: {filename}]\n{content}\n"
                self.update_chat_display(f"\n[SYSTEM] ATTACHED FILE: {filename}\n")
            except:
                self.update_chat_display(f"\n[SYSTEM] ATTACHED FILE: {filename}\n")

    def init_ai(self):
        try:
            self.model = Llama(model_path=model_path, n_ctx=2048, n_threads=8, verbose=False)
            self.status_bar.configure(text="● ENCRYPTED CONNECTION ESTABLISHED", text_color="#00ff41")
        except Exception as e:
            self.status_bar.configure(text=f"● OFFLINE: {e}", text_color="red")

    def update_chat_display(self, text, tag=None):
        self.chat_display.configure(state="normal")
        self.chat_display.insert("end", text, tag)
        self.chat_display.see("end")
        self.chat_display.configure(state="disabled")

    def send_message(self):
        msg = self.input_field.get().strip()
        if not msg or self.is_generating or not self.model: return
        
        self.is_generating = True
        self.stop_event.clear()
        self.stop_btn.configure(state="normal")
        
        # --- RED HUMAN MESSAGE INJECTION ---
        self.update_chat_display(f"\nANONYMOUS > {msg}\n", "human_msg")
        self.update_chat_display(f"\nPOWERFUL GINN > ")
        
        self.input_field.delete(0, "end")
        threading.Thread(target=self.generate, args=(msg,), daemon=True).start()

    def generate(self, text):
        try:
            self.status_bar.configure(text=LANG_MAP[self.current_lang]["exec"], text_color="#FF0000")
            full_prompt = f"{self.chat_history}User: {text}\nAssistant:"
            
            stream = self.model(
                full_prompt, 
                max_tokens=1024, 
                stream=True, 
                temperature=0.8, 
                stop=["User:", "USER >"]
            )
            
            response_text = ""
            for chunk in stream:
                if self.stop_event.is_set():
                    self.after(0, lambda: self.update_chat_display(" [TERMINATED]"))
                    break
                token = chunk["choices"][0].get("text", "")
                response_text += token
                self.after(0, lambda t=token: self.update_chat_display(t))
            
            self.chat_history += f"User: {text}\nAssistant: {response_text}\n"
        finally:
            self.status_bar.configure(text="● SECURE CONNECTION ACTIVE", text_color="#00ff41")
            self.is_generating = False
            self.stop_btn.configure(state="disabled")

    def stop_generation(self):
        self.stop_event.set()

    def clear_chat(self):
        self.chat_display.configure(state="normal")
        self.chat_display.delete("1.0", "end")
        self.chat_display.configure(state="disabled")
        self.chat_history = f"System: {SYSTEM_PROMPT}\n"

if __name__ == "__main__":
    app = PowerfulGinnApp()
    app.mainloop()