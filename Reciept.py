import tkinter as tk
from tkinter import Toplevel

class ReceiptWindow:
    def __init__(self, tran):
        self.tran = tran
        self.window = Toplevel()
        self.window.title("Receipt")
        self.window.overrideredirect(True)
        self.center_window(450, 400)
        self.window.configure(bg="#f0f4f8")
        self.style_receipt()

    def center_window(self, width, height):
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        position_top = int(screen_height / 2 - height / 2)
        position_left = int(screen_width / 2 - width / 2)
        self.window.geometry(f'{width}x{height}+{position_left}+{position_top}')

    def style_receipt(self):
        frame = tk.Frame(self.window, padx=20, pady=20, bg="#f0f4f8")
        frame.pack(expand=True)

        title_label = tk.Label(frame, text="Receipt", font=("Helvetica", 20, "bold"), bg="#f0f4f8", fg="#333")
        title_label.grid(row=0, column=0, columnspan=2, pady=20)

        details = [
            ("User Name:", self.tran.user_name),
            ("Offer Name:", self.tran.offer_name),
            ("Billing Type:", self.tran.billing_type),
            ("Payment:", f"${self.tran.payment}"),
            ("Date:", self.tran.date)
        ]

        for i, (label, value) in enumerate(details, start=1):
            label_widget = tk.Label(frame, text=label, font=("Helvetica", 12), bg="#f0f4f8", fg="#555")
            value_widget = tk.Label(frame, text=value, font=("Helvetica", 12), bg="#f0f4f8", fg="#2d8b5e")
            label_widget.grid(row=i, column=0, sticky="e", padx=10, pady=5)
            value_widget.grid(row=i, column=1, sticky="w", padx=10, pady=5)

        close_button = tk.Button(frame, text="Close", command=self.window.destroy,
                                 font=("Helvetica", 12), bg="#2d8b5e", fg="white",
                                 relief="flat", padx=20, pady=10,
                                 activebackground="#1d6c47", activeforeground="white")
        close_button.grid(row=len(details)+1, column=0, columnspan=2, pady=20)

        frame.config(bd=5, relief="solid", highlightbackground="#ccc", highlightthickness=1)
