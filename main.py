from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from ShopDataService import DataService
from User import Role
from tkinter import filedialog
from Offer import Offer,Type
from Reciept import ReceiptWindow
from tkinter import messagebox


WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 600

class MotorcycleShop:
    ### START
    def __init__(self, root):
        self.root = root
        self.window = None
        self.bg_image_path = "./assets/Images/black-bg.jpg"
        self.background = None
        self.service = DataService()
        self.user = None
        self.mainContentFrame = None
        self.selected_offer_id = None

    def run(self):
        self.login_window()
        self.root.mainloop()

    def update_background_image(self, img_path):
        img = Image.open(img_path)
        img = img.resize((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.background = ImageTk.PhotoImage(img)
        self.window.create_image(0, 0, image=self.background, anchor="nw")

    def reset_window(self):
        if self.window:
            self.window.destroy()
        self.window = Canvas(self.root, width=WINDOW_WIDTH, height=WINDOW_HEIGHT)
        self.window.pack(expand=True, fill=BOTH)
        self.update_background_image(self.bg_image_path)

    ### USE SERVICE
    def login(self, username, password):
        if username and password:
            user = self.service.user_login(username, password)
            if user:
                self.user = user
                if user.role == Role.USER.value:
                    self.home_window()
                else:
                    self.admin_home()
        else:
            print("account not found")

    def register(self, name, username, password, role, image):
        if name and username and password and role and image:
            user = self.service.register_user(name, username, password, role, image)
            if user:
                self.login_window()
                print("Registered successfully", user.name)
            else:
                print("error")
        else:
            print("Error: Please fill all fields")

    def logout(self):
        self.user = None
        self.login_window()




    def confirm_order(self, offer_name, billing_type, payment):

        tran = self.service.add_transaction(self.user.id, self.user.name, offer_name, billing_type, payment)
        self.open_receipt(tran)

    def open_receipt(self, tran):
        receipt = ReceiptWindow(tran)

    def add_to_cart(self,offer) :
        self.service.add_to_cart(self.user.id,offer)
    def remove_to_cart(self,cart_id):
        self.service.remove_to_cart(cart_id)

    ### DEFAULT LAYOUT
    def config_banK_cred(self, offer_name, offer_price):

        self.reset_window()

        bank_frame = Frame(self.window, bg="#ffffff", bd=2, relief=GROOVE)
        bank_frame.place(relx=0.5, rely=0.5, anchor=CENTER, width=400, height=350)

        title_label = Label(bank_frame, text="Bank Details", font=("Helvetica", 18, "bold"), bg="#ffffff", fg="#333333")
        title_label.pack(pady=10)

        card_number_label = Label(bank_frame, text="Credit Card Number", font=("Helvetica", 12), bg="#ffffff",
                                  fg="#333333")
        card_number_label.pack(pady=5, anchor=W, padx=20)
        card_number_entry = ttk.Entry(bank_frame, font=("Helvetica", 12))
        card_number_entry.pack(pady=5, padx=20, fill=X)

        pin_label = Label(bank_frame, text="PIN", font=("Helvetica", 12), bg="#ffffff", fg="#333333")
        pin_label.pack(pady=5, anchor=W, padx=20)
        pin_entry = ttk.Entry(bank_frame, font=("Helvetica", 12), show="*")
        pin_entry.pack(pady=5, padx=20, fill=X)

        def process_payment():
            card_number = card_number_entry.get()
            pin = pin_entry.get()
            if not card_number or not pin:
                messagebox.showerror("Error", "Please enter all required fields")
                return
            self.confirm_order(offer_name, 'Credit Card', offer_price)
            # messagebox.showinfo("Order Confirmed", "Your order has been confirmed.")


            self.home_window()

        confirm_button = Button(bank_frame, text="Confirm Payment", font=("Helvetica", 12, "bold"), bg="#4CAF50",
                                fg="#ffffff", cursor="hand2", command=process_payment)
        confirm_button.pack(pady=20, padx=20, fill=X)

        cancel_button = Button(bank_frame, text="Cancel", font=("Helvetica", 12), bg="#FF5733", fg="white",
                               cursor="hand2", relief=FLAT, command=self.home_window)
        cancel_button.pack(pady=10, padx=20, fill=X)

    def config_banK_cred_all(self, items):

        self.reset_window()

        bank_frame = Frame(self.window, bg="#ffffff", bd=2, relief=GROOVE)
        bank_frame.place(relx=0.5, rely=0.5, anchor=CENTER, width=400, height=350)

        title_label = Label(bank_frame, text="Bank Details", font=("Helvetica", 18, "bold"), bg="#ffffff", fg="#333333")
        title_label.pack(pady=10)

        card_number_label = Label(bank_frame, text="Credit Card Number", font=("Helvetica", 12), bg="#ffffff",
                                  fg="#333333")
        card_number_label.pack(pady=5, anchor=W, padx=20)
        card_number_entry = ttk.Entry(bank_frame, font=("Helvetica", 12))
        card_number_entry.pack(pady=5, padx=20, fill=X)

        pin_label = Label(bank_frame, text="PIN", font=("Helvetica", 12), bg="#ffffff", fg="#333333")
        pin_label.pack(pady=5, anchor=W, padx=20)
        pin_entry = ttk.Entry(bank_frame, font=("Helvetica", 12), show="*")
        pin_entry.pack(pady=5, padx=20, fill=X)

        def process_payment():
            card_number = card_number_entry.get()
            pin = pin_entry.get()
            if not card_number or not pin:
                messagebox.showerror("Error", "Please enter all required fields")
                return
            for item in items:
                self.confirm_order(item[1], 'Credit Card', item[2])
            #messagebox.showinfo("Order Confirmed", "Your order has been confirmed.")

            self.home_window()

        confirm_button = Button(bank_frame, text="Confirm Payment", font=("Helvetica", 12, "bold"), bg="#4CAF50",
                                fg="#ffffff", cursor="hand2", command=process_payment)
        confirm_button.pack(pady=20, padx=20, fill=X)

        cancel_button = Button(bank_frame, text="Cancel", font=("Helvetica", 12), bg="#FF5733", fg="white",
                               cursor="hand2", relief=FLAT, command=self.home_window)
        cancel_button.pack(pady=10, padx=20, fill=X)

    def order_frame(self, offer_name, offer_price):

        self.default_user_layout()


        order_frame = Frame(self.mainContentFrame, bg="#ffffff", bd=2, relief=GROOVE)
        order_frame.place(relx=0.5, rely=0.5, anchor=CENTER, width=400, height=550)

        title_label = Label(order_frame, text="Confirm Your Order", font=("Helvetica", 18, "bold"), bg="#ffffff",
                            fg="#333333")
        title_label.pack(pady=10)

        offer_name_label = Label(order_frame, text=f"Offer: {offer_name}", font=("Helvetica", 14), bg="#ffffff",
                                 fg="#333333")
        offer_name_label.pack(pady=5, anchor=W, padx=20)

        offer_price_label = Label(order_frame, text=f"Price: ${offer_price}", font=("Helvetica", 14, "bold"),
                                  bg="#ffffff", fg="#27ae60")
        offer_price_label.pack(pady=5, anchor=W, padx=20)

        payment_label = Label(order_frame, text="Payment", font=("Helvetica", 12), bg="#ffffff", fg="#333333")
        payment_label.pack(pady=10, anchor=W, padx=20)

        payment_method = StringVar(value="COD")

        payment_options = [("Cash on Delivery", "COD"), ("Credit Card", "CC")]
        for text, value in payment_options:
            payment_radio = Radiobutton(order_frame, text=text, variable=payment_method, value=value,font=("Helvetica", 12), bg="#ffffff", fg="#333333")
            payment_radio.pack(anchor=W, padx=20)

        def proceed_to_payment():
            selected_payment_method = payment_method.get()
            if selected_payment_method == "CC":
                self.config_banK_cred(offer_name,offer_price)
            else:
                self.confirm_order(offer_name,'Cash on Delivery',offer_price)
                #messagebox.showinfo("Orders Confirmed", "Your orders has been confirmed for Cash on Delivery.")
                self.home_window()
        confirm_button = Button(order_frame, text="Proceed to Payment", font=("Helvetica", 12, "bold"), bg="#4CAF50",
                                fg="#ffffff", cursor="hand2", command=proceed_to_payment)
        confirm_button.pack(pady=20, padx=20, fill=X)

        cancel_button = Button(order_frame, text="Cancel", font=("Helvetica", 12), bg="#FF5733", fg="white",
                               cursor="hand2", relief=FLAT, command=self.home_window)
        cancel_button.pack(pady=10, padx=20, fill=X)

    def order_selected_frame(self, items):

        self.default_user_layout()


        order_frame = Frame(self.mainContentFrame, bg="#ffffff", bd=2, relief=GROOVE)
        order_frame.place(relx=0.5, rely=0.5, anchor=CENTER, width=400, height=550)

        title_label = Label(order_frame, text="Confirm Your Order", font=("Helvetica", 18, "bold"), bg="#ffffff",
                            fg="#333333")
        title_label.pack(pady=10)

        offer_name_label = Label(order_frame, text=f"Items: {len(items)}", font=("Helvetica", 14), bg="#ffffff",
                                 fg="#333333")
        offer_name_label.pack(pady=5, anchor=W, padx=20)

        offer_price_label = Label(order_frame, text=f"Price: ${200}", font=("Helvetica", 14, "bold"),
                                  bg="#ffffff", fg="#27ae60")
        offer_price_label.pack(pady=5, anchor=W, padx=20)

        payment_label = Label(order_frame, text="Payment", font=("Helvetica", 12), bg="#ffffff", fg="#333333")
        payment_label.pack(pady=10, anchor=W, padx=20)

        payment_method = StringVar(value="COD")

        payment_options = [("Cash on Delivery", "COD"), ("Credit Card", "CC")]
        for text, value in payment_options:
            payment_radio = Radiobutton(order_frame, text=text, variable=payment_method, value=value,
                                        font=("Helvetica", 12), bg="#ffffff", fg="#333333")
            payment_radio.pack(anchor=W, padx=20)

        def proceed_to_payment():
            selected_payment_method = payment_method.get()
            if selected_payment_method == "CC":
                self.config_banK_cred_all(items)
            else:
                for item in items:
                    self.confirm_order(item[1], 'Cash on Delivery', item[2])
                #messagebox.showinfo("Orders Confirmed", "Your orders has been confirmed for Cash on Delivery.")
                self.home_window()

        confirm_button = Button(order_frame, text="Proceed to Payment", font=("Helvetica", 12, "bold"), bg="#4CAF50",
                                fg="#ffffff", cursor="hand2", command=proceed_to_payment)
        confirm_button.pack(pady=20, padx=20, fill=X)

        cancel_button = Button(order_frame, text="Cancel", font=("Helvetica", 12), bg="#FF5733", fg="white",
                               cursor="hand2", relief=FLAT, command=self.home_window)
        cancel_button.pack(pady=10, padx=20, fill=X)

    def default_user_layout(self):
        self.reset_window()


        self.window.grid_rowconfigure(0, weight=1)
        self.window.grid_columnconfigure(1, weight=1)


        sidebar = Frame(self.window, bg="#333333", width=250)
        sidebar.grid(row=0, column=0, sticky="ns")

        self.mainContentFrame = Frame(self.window, bg="#f5f5f5")
        self.mainContentFrame .grid(row=0, column=1, sticky="nsew")


        nav_button1 = Button(sidebar, text="Home", font=("Helvetica", 12), bg="#333333", fg="white", relief=FLAT,command=self.home_window)
        nav_button1.pack(pady=10, padx=20, fill=X)

        nav_button3 = Button(sidebar, text="Orders", font=("Helvetica", 12), bg="#333333", fg="white", relief=FLAT,command=self.orders_window)
        nav_button3.pack(pady=10, padx=20, fill=X)

        nav_button3 = Button(sidebar, text="Carts", font=("Helvetica", 12), bg="#333333", fg="white", relief=FLAT,command=self.cart_window)
        nav_button3.pack(pady=10, padx=20, fill=X)

        nav_logout = Button(sidebar, text="Profile", font=("Helvetica", 12), bg="#333333", fg="white", relief=FLAT,command=self.profile_window)
        nav_logout.pack(pady=10, padx=20, fill=X)

    def default_Admin_layout(self):
        self.reset_window()

        self.window.grid_rowconfigure(0, weight=1)
        self.window.grid_columnconfigure(1, weight=1)


        sidebar = Frame(self.window, bg="#2E3B4E", width=250, padx=15)
        sidebar.grid(row=0, column=0, sticky="ns")

        self.mainContentFrame = Frame(self.window, bg="#F7F7F7", padx=20, pady=20)
        self.mainContentFrame.grid(row=0, column=1, sticky="nsew")


        admin_button1 = Button(sidebar, text="Users", font=("Roboto", 12), bg="#4A90E2", fg="white", relief=FLAT,
                               command=self.admin_home)
        admin_button1.pack(pady=15, fill=X)

        admin_button3 = Button(sidebar, text="Transac", font=("Roboto", 12), bg="#4A90E2", fg="white", relief=FLAT,
                               command=self.transactions_window)
        admin_button3.pack(pady=15, fill=X)

        admin_button2 = Button(sidebar, text="Manage", font=("Roboto", 12), bg="#4A90E2", fg="white",
                               relief=FLAT,
                               command=self.manage_window)
        admin_button2.pack(pady=15, fill=X)

        nav_logout = Button(sidebar, text="Profile", font=("Roboto", 12), bg="#4A90E2", fg="white", relief=FLAT,
                            command=self.profile_window)
        nav_logout.pack(pady=15, fill=X)

    #### WINDOWS
    def profile_window(self):

        if self.user.role == Role.USER.value:
            self.default_user_layout()
        else:
            self.default_Admin_layout()


        title_label = Label(self.mainContentFrame, text=f"{self.user.role}", font=("Helvetica", 24, "bold"), fg="#333333",
                            bg="#f4f4f9")
        title_label.pack(pady=(0, 20))



        image = Image.open(self.user.image_path)
        image = image.resize((100,100))
        profile_image = ImageTk.PhotoImage(image)


        if profile_image:
            image_label = Label(self.mainContentFrame, image=profile_image, bg="#f4f4f9")
            image_label.image = profile_image
            image_label.pack(pady=10)


        user_info_frame = Frame(self.mainContentFrame, bg="#ffffff", bd=0, relief="solid")
        user_info_frame.pack(pady=10, padx=10, fill="x")

        self._create_info_row(user_info_frame, "Name:", self.user.name)
        self._create_info_row(user_info_frame, "Username:", self.user.username)
        self._create_info_row(user_info_frame, "Password:", "********")
        self._create_info_row(user_info_frame, "Role:", self.user.role)

        logout_button = Button(
            self.mainContentFrame,
            text="Logout",
            command=self.logout,
            bg="#ff4757",
            fg="#ffffff",
            font=("Helvetica", 14, "bold"),
            activebackground="#e84118",
            activeforeground="#ffffff",
            relief="flat",
            cursor="hand2"
        )
        logout_button.pack(pady=(20, 0), ipadx=20, ipady=10)

    def _create_info_row(self, parent, label_text, value_text):

        row_frame = Frame(parent, bg="#ffffff")
        row_frame.pack(fill="x", pady=5)

        label = Label(row_frame, text=label_text, font=("Helvetica", 12, "bold"), fg="#555555", bg="#ffffff")
        label.pack(side="left", padx=(10, 5))

        value = Label(row_frame, text=value_text, font=("Helvetica", 12), fg="#333333", bg="#ffffff")
        value.pack(side="left")

    def orders_window(self):
        self.default_user_layout()


        orders_frame = Frame(self.mainContentFrame, bg="#ffffff", bd=2, relief=GROOVE)
        orders_frame.pack(pady=20, padx=20, fill=BOTH, expand=True)


        title_label = Label(orders_frame, text="Your Orders", font=("Helvetica", 18, "bold"), bg="#ffffff",
                            fg="#333333")
        title_label.pack(pady=10)


        columns = ("Order ID", "User Name", "Offer Name", "Billing Type", "Payment Method","Date")
        tree = ttk.Treeview(orders_frame, columns=columns, show="headings", selectmode="browse")


        tree.heading("Order ID", text="Order ID")
        tree.heading("User Name", text="User Name")
        tree.heading("Offer Name", text="Offer Name")
        tree.heading("Billing Type", text="Billing Type")
        tree.heading("Payment Method", text="Payment Method")
        tree.heading("Date", text="Status")


        tree.column("Order ID", width=100, anchor="center")
        tree.column("User Name", width=150, anchor="center")
        tree.column("Offer Name", width=200, anchor="center")
        tree.column("Billing Type", width=120, anchor="center")
        tree.column("Payment Method", width=120, anchor="center")
        tree.column("Date", width=100, anchor="center")


        orders = self.service.get_user_orders(self.user.id)


        for order in orders:
            tree.insert("", "end", values=(
            order.user_id, order.user_name, order.offer_name, order.billing_type, order.payment,str(order.date).split(" ")[0]))


        scrollbar = Scrollbar(orders_frame, orient="vertical", command=tree.yview)
        scrollbar.pack(side="right", fill="y")
        tree.configure(yscrollcommand=scrollbar.set)
        tree.pack(fill=BOTH, expand=True)


        def on_order_select(event):
            selected_item = tree.selection()
            if selected_item:
                order_id = tree.item(selected_item)["values"][0]


                result = messagebox.askyesno("Cancel Order",
                                             f"Are you sure you want to cancel the order with ID: {order_id}?")
                if result:

                    self.service.cancel_order(order_id)
                    messagebox.showinfo("Order Canceled", f"Order {order_id} has been canceled.")
                    self.orders_window()


        tree.bind("<ButtonRelease-1>", on_order_select)

    def cart_window(self):
        self.default_user_layout()


        cart_frame = Frame(self.mainContentFrame, bg="#ffffff", bd=2, relief=GROOVE)
        cart_frame.pack(pady=20, padx=20, fill=BOTH, expand=True)


        title_label = Label(cart_frame, text="Your Cart", font=("Helvetica", 18, "bold"), bg="#ffffff", fg="#333333")
        title_label.pack(pady=10)


        columns = ("Item ID", "Item Name", "Price")
        tree = ttk.Treeview(cart_frame, columns=columns, show="headings",
                            selectmode="extended")

        tree.heading("Item ID", text="Item ID")
        tree.heading("Item Name", text="Item Name")
        tree.heading("Price", text="Price")


        tree.column("Item ID", width=100, anchor="center")
        tree.column("Item Name", width=200, anchor="center")
        tree.column("Price", width=100, anchor="center")


        cart_items = self.service.get_user_cart(self.user.id)


        for item in cart_items:
            tree.insert("", "end", values=(item.id, item.offer.name, f"${item.offer.price}"))


        scrollbar = Scrollbar(cart_frame, orient="vertical", command=tree.yview)
        scrollbar.pack(side="right", fill="y")
        tree.configure(yscrollcommand=scrollbar.set)
        tree.pack(fill=BOTH, expand=True)


        def cancel_selected_items():
            selected_items = tree.selection()
            if selected_items:
                for item in selected_items:
                    item_id = tree.item(item)["values"][0]

                    self.service.remove_to_cart(item_id)
                messagebox.showinfo("Cart Updated", "Selected items have been removed from the cart.")
                self.cart_window()

        def order_selected_items():
            selected_items = tree.selection()
            items = []
            if selected_items:
                for item in selected_items:
                    items.append(tree.item(item)["values"])
                self.order_selected_frame(items)

        cancel_button = Button(cart_frame, text="Cancel Selected Items", font=("Helvetica", 12, "bold"), bg="#FF5733",
                               fg="white", cursor="hand2", command=cancel_selected_items)
        cancel_button.pack(pady=10, padx=20, fill=X)

        order_button = Button(cart_frame, text="Order Selected Items", font=("Helvetica", 12, "bold"), bg="#4CAF50",
                              fg="white", cursor="hand2", command=order_selected_items)
        order_button.pack(pady=10, padx=20, fill=X)

    def home_window(self):
        self.default_user_layout()

        title_label = Label(self.mainContentFrame, text="Parts and Services", font=("Helvetica", 20, "bold"), bg="#f4f6f9",
                            fg="#2c3e50")
        title_label.pack(pady=20, padx=20)

        canvas = Canvas(self.mainContentFrame)
        canvas.pack(side="left", fill="both", expand=True)

        scrollbar = Scrollbar(self.mainContentFrame, orient="vertical", command=canvas.yview)
        scrollbar.pack(side="right", fill="y")

        canvas.config(yscrollcommand=scrollbar.set)

        offers_frame = Frame(canvas, bg="#f4f6f9", bd=0, relief=GROOVE)
        canvas.create_window((0, 0), window=offers_frame, anchor="nw", width=890)

        offers = self.service.offers()

        for index, offer in enumerate(offers):
            row = (index // 2) + 1
            column = index % 2

            offer_frame = Frame(offers_frame, bg="#ffffff", bd=1, relief=SOLID, width=490)
            offer_frame.grid(row=row, column=column, padx=5, pady=5, sticky="nsew")

            offer_image = Image.open(offer.image_path)
            offer_image = offer_image.resize((180, 180))
            offer_image_tk = ImageTk.PhotoImage(offer_image)
            offer_img_label = Label(offer_frame, image=offer_image_tk, bg="#ffffff")
            offer_img_label.image = offer_image_tk
            offer_img_label.grid(row=0, column=0, padx=5, pady=5)

            offer_details_frame = Frame(offer_frame, bg="#ffffff")
            offer_details_frame.grid(row=0, column=1, sticky="nswe")

            offer_name_label = Label(offer_details_frame, text=offer.name, font=("Helvetica", 14), bg="#ffffff",
                                     fg="#34495e")
            offer_name_label.grid(row=0, column=0, padx=15, pady=5, sticky=W)

            offer_price_label = Label(offer_details_frame, text=f"${offer.price}", font=("Helvetica", 14, "bold"),
                                      bg="#ffffff", fg="#27ae60")
            offer_price_label.grid(row=1, column=0, padx=15, pady=5, sticky=W)

            add_to_cart_button = Button(offer_details_frame, text="Add to Cart", font=("Helvetica", 12), bg="#4CAF50",
                                        fg="white", cursor="hand2", relief=FLAT,
                                        activebackground="#388E3C", activeforeground="white", padx=15, pady=8, width=15,command=lambda : self.add_to_cart(offer))
            add_to_cart_button.grid(row=2, column=0, padx=15, pady=10)

            direct_order_button = Button(offer_details_frame, text="Order Now", font=("Helvetica", 12), bg="#FF5733",
                                         fg="white", cursor="hand2", relief=FLAT, activebackground="#D43F00",
                                         activeforeground="white",
                                         padx=15, pady=8, width=15,
                                         command=lambda: self.order_frame(offer.name, offer.price))
            direct_order_button.grid(row=3, column=0, padx=15, pady=10)

        offers_frame.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))


    #admin
    def admin_home(self):

        self.default_Admin_layout()

        users = self.service.users()


        columns = ("Name", "Username","Password", "Role")
        tree = ttk.Treeview(self.mainContentFrame, columns=columns, show="headings")
        tree.pack(fill=BOTH, expand=True)


        style = ttk.Style()
        style.configure("Treeview",
                        font=("Helvetica", 12),  #
                        rowheight=30,
                        background="#f9f9f9",
                        foreground="black",
                        fieldbackground="#f9f9f9")
        style.configure("Treeview.Heading",
                        font=("Helvetica", 13, "bold"),
                        background="#4CAF50",
                        foreground="black")
        style.map("Treeview",
                  background=[('selected', '#4CAF50')],
                  foreground=[('selected', 'white')])


        for col in columns:
            tree.heading(col, text=col)


        for user in users:
            if user.role == Role.USER.value:
                tree.insert("", "end", values=(user.name, user.username,"*"*len(user.password), user.role))


        def on_row_enter(event, row_id):
            tree.item(row_id, tags=("hover",))

        def on_row_leave(event, row_id):
            tree.item(row_id, tags=(""))


        for row_id in tree.get_children():
            tree.tag_configure("hover", background="#e0e0e0")  # Highlight color for row on hover
            tree.tag_bind(row_id, "<Enter>", lambda event, row_id=row_id: on_row_enter(event, row_id))
            tree.tag_bind(row_id, "<Leave>", lambda event, row_id=row_id: on_row_leave(event, row_id))


        vertical_scroll = ttk.Scrollbar(self.mainContentFrame, orient="vertical", command=tree.yview)
        vertical_scroll.pack(side="right", fill="y")
        tree.configure(yscrollcommand=vertical_scroll.set)

        horizontal_scroll = ttk.Scrollbar(self.mainContentFrame, orient="horizontal", command=tree.xview)
        horizontal_scroll.pack(side="bottom", fill="x")
        tree.configure(xscrollcommand=horizontal_scroll.set)
    def transactions_window(self):
        self.default_Admin_layout()

        trans = self.service.transactions()

        columns = ( "User Name", "Offer Name", "Billing Type", "Payment","Date")
        tree = ttk.Treeview(self.mainContentFrame, columns=columns, show="headings")
        tree.pack(fill=BOTH, expand=True)

        style = ttk.Style()
        style.configure("Treeview",
                        font=("Helvetica", 12),  #
                        rowheight=30,
                        background="#f9f9f9",
                        foreground="black",
                        fieldbackground="#f9f9f9")
        style.configure("Treeview.Heading",
                        font=("Helvetica", 13, "bold"),
                        background="#4CAF50",
                        foreground="black")
        style.map("Treeview",
                  background=[('selected', '#4CAF50')],
                  foreground=[('selected', 'white')])

        for col in columns:
            tree.heading(col, text=col)

        for tran in trans:

            tree.insert("", "end", values=(tran.user_name,tran.offer_name,tran.billing_type,tran.payment,str(tran.date).split(" ")[0]))

        def on_row_enter(event, row_id):
            tree.item(row_id, tags=("hover",))

        def on_row_leave(event, row_id):
            tree.item(row_id, tags=(""))

        for row_id in tree.get_children():
            tree.tag_configure("hover", background="#e0e0e0")  # Highlight color for row on hover
            tree.tag_bind(row_id, "<Enter>", lambda event, row_id=row_id: on_row_enter(event, row_id))
            tree.tag_bind(row_id, "<Leave>", lambda event, row_id=row_id: on_row_leave(event, row_id))

        vertical_scroll = ttk.Scrollbar(self.mainContentFrame, orient="vertical", command=tree.yview)
        vertical_scroll.pack(side="right", fill="y")
        tree.configure(yscrollcommand=vertical_scroll.set)

        horizontal_scroll = ttk.Scrollbar(self.mainContentFrame, orient="horizontal", command=tree.xview)
        horizontal_scroll.pack(side="bottom", fill="x")
        tree.configure(xscrollcommand=horizontal_scroll.set)

    def manage_window(self):
        self.default_Admin_layout()



        left_frame = Frame(self.mainContentFrame, width=350, bg="#FFFFFF", relief=SOLID, bd=1, padx=15, pady=10)
        left_frame.pack(side=LEFT, fill=Y, padx=10, pady=10)


        right_frame = Frame(self.mainContentFrame, bg="#FFFFFF", relief=SOLID, bd=1, padx=10, pady=10)
        right_frame.pack(side=LEFT, fill=BOTH, expand=True, padx=10, pady=10)


        form_label = Label(left_frame, text="Offer Form", font=("Roboto", 14, "bold"), bg="#FFFFFF", fg="#333333")
        form_label.pack(pady=10)


        offer_type_label = Label(left_frame, text="Offer Type", font=("Roboto", 10), bg="#FFFFFF", fg="#333333")
        offer_type_label.pack(pady=5)
        offer_type = ttk.Combobox(left_frame, values=[Type.SERVICE.value, Type.PART.value], width=20,
                                  font=("Roboto", 10))
        offer_type.pack(pady=5)


        name_label = Label(left_frame, text="Name", font=("Roboto", 10), bg="#FFFFFF", fg="#333333")
        name_label.pack(pady=5)
        name_entry = Entry(left_frame, width=20, font=("Roboto", 10))
        name_entry.pack(pady=5)


        price_label = Label(left_frame, text="Price", font=("Roboto", 10), bg="#FFFFFF", fg="#333333")
        price_label.pack(pady=5)
        price_entry = Entry(left_frame, width=20, font=("Roboto", 10))
        price_entry.pack(pady=5)


        image_label = Label(left_frame, text="Image", font=("Roboto", 10), bg="#FFFFFF", fg="#333333")
        image_label.pack(pady=5)
        image_path_entry = Entry(left_frame, width=20, font=("Roboto", 10))
        image_path_entry.pack(pady=5)

        def browse_image():
            image_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
            image_path_entry.delete(0, END)
            image_path_entry.insert(0, image_path)
            show_image(image_path)

        browse_button = Button(left_frame, text="Browse", command=browse_image, font=("Roboto", 10), bg="#4A90E2",
                               fg="white", relief=FLAT)
        browse_button.pack(pady=5)

        image_preview_label = Label(left_frame)
        image_preview_label.pack(pady=10)

        def show_image(image_path):
            try:
                img = Image.open(image_path)
                img = img.resize((100, 100))
                img = ImageTk.PhotoImage(img)
                image_preview_label.config(image=img)
                image_preview_label.image = img
            except:
                pass


        create_button = Button(left_frame, text="Create Offer",
                               command=lambda: create_offer(offer_type.get(), image_path_entry.get(), name_entry.get(),
                                                            float(price_entry.get()) if price_entry.get() else 0),
                               font=("Roboto", 10), bg="#28A745", fg="white", relief=FLAT)
        create_button.pack(pady=10, fill=X)

        update_button = Button(left_frame, text="Update Offer", state=DISABLED,
                               command=lambda: self.update_offer(offer_type.get(), name_entry.get(),
                                                                 float(price_entry.get()) if price_entry.get() else 0,
                                                                 offer_table), font=("Roboto", 10), bg="#FFC107",
                               fg="white", relief=FLAT)
        update_button.pack(pady=10, fill=X)

        delete_button = Button(left_frame, text="Delete Offer", state=DISABLED,
                               command=lambda: delete_offer(self.selected_offer_id), font=("Roboto", 10),
                               bg="#DC3545", fg="white", relief=FLAT)
        delete_button.pack(pady=10, fill=X)


        columns = ("Type", "Name", "Price")
        offer_table = ttk.Treeview(right_frame, columns=columns, show="headings", height=10, style="Custom.Treeview")
        offer_table.pack(fill=BOTH, expand=True)

        for col in columns:
            offer_table.heading(col, text=col)


        vertical_scroll = ttk.Scrollbar(right_frame, orient="vertical", command=offer_table.yview)
        vertical_scroll.pack(side="right", fill="y")
        offer_table.configure(yscrollcommand=vertical_scroll.set)

        horizontal_scroll = ttk.Scrollbar(right_frame, orient="horizontal", command=offer_table.xview)
        horizontal_scroll.pack(side="bottom", fill="x")
        offer_table.configure(xscrollcommand=horizontal_scroll.set)


        self.refresh_offer_table(offer_table)


        def on_offer_select(event):
            selected_item = offer_table.selection()[0]
            offer_data = offer_table.item(selected_item, "values")
            name_entry.delete(0, END)
            name_entry.insert(0, offer_data[2])
            price_entry.delete(0, END)
            price_entry.insert(0, offer_data[3])
            offer_type.set(offer_data[1])
            update_button.config(state=NORMAL)
            delete_button.config(state=NORMAL)
            self.selected_offer_id = int(offer_data[0])
        def delete_offer(offer_id):
            self.service.delete_offer(offer_id)
            self.refresh_offer_table(offer_table)
        def create_offer(_type, image_path, name, price):
            self.service.create_offer(_type, image_path, name, price)
            self.refresh_offer_table(offer_table)

        offer_table.bind("<ButtonRelease-1>", on_offer_select)


        style = ttk.Style()
        style.configure("Custom.Treeview", background="#f5f5f5", foreground="black", rowheight=25)
        style.map("Custom.Treeview", background=[('selected', '#D1E0FF')])

    def update_offer(self, type, name, price, offer_table):
        offer = Offer(type, "", name, price)
        offer.id = self.selected_offer_id
        self.service.update_offer(offer)
        self.refresh_offer_table(offer_table)

    def refresh_offer_table(self, offer_table):
        for item in offer_table.get_children():
            offer_table.delete(item)
        for offer in self.service.offers():
            offer_table.insert("", "end", values=( offer.type, offer.name, offer.price))


    def register_window(self):
        self.reset_window()

        register_frame = Frame(self.window, bg="#ffffff", bd=2, relief=GROOVE)
        register_frame.place(relx=0.5, rely=0.5, anchor=CENTER, width=400, height=500)

        title_label = Label(register_frame, text="Register", font=("Helvetica", 18, "bold"), bg="#ffffff", fg="#333333")
        title_label.pack(pady=10)

        name_label = Label(register_frame, text="Name", font=("Helvetica", 12), bg="#ffffff", fg="#333333")
        name_label.pack(pady=5, anchor=W, padx=20)
        name_entry = ttk.Entry(register_frame, font=("Helvetica", 12))
        name_entry.pack(pady=5, padx=20, fill=X)

        username_label = Label(register_frame, text="Username", font=("Helvetica", 12), bg="#ffffff", fg="#333333")
        username_label.pack(pady=5, anchor=W, padx=20)
        username_entry = ttk.Entry(register_frame, font=("Helvetica", 12))
        username_entry.pack(pady=5, padx=20, fill=X)

        password_label = Label(register_frame, text="Password", font=("Helvetica", 12), bg="#ffffff", fg="#333333")
        password_label.pack(pady=5, anchor=W, padx=20)
        password_entry = ttk.Entry(register_frame, font=("Helvetica", 12), show="*")
        password_entry.pack(pady=5, padx=20, fill=X)

        confirm_password_label = Label(register_frame, text="Confirm Password", font=("Helvetica", 12), bg="#ffffff",
                                       fg="#333333")
        confirm_password_label.pack(pady=5, anchor=W, padx=20)
        confirm_password_entry = ttk.Entry(register_frame, font=("Helvetica", 12), show="*")
        confirm_password_entry.pack(pady=5, padx=20, fill=X)

        def upload_image():
            file_path = filedialog.askopenfilename(title="Select an Image",
                                                   filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.gif;*.bmp")])
            if file_path:
                self.selected_image = file_path
                print("Image selected:", file_path)

        image_button = Button(register_frame, text="Upload Image", font=("Helvetica", 12, "bold"), bg="#4CAF50",
                              fg="#ffffff", cursor="hand2", command=upload_image)
        image_button.pack(pady=10, padx=20)

        register_button = Button(register_frame, text="Register", font=("Helvetica", 12, "bold"), bg="#4CAF50",
                                 fg="#ffffff", cursor="hand2", command=lambda: self.register(name_entry.get(),
                                                                                             username_entry.get(),
                                                                                             password_entry.get(),
                                                                                             Role.USER.value,
                                                                                             getattr(self,
                                                                                                     'selected_image',
                                                                                                     None)))
        register_button.pack(pady=20, padx=20, fill=X)

        back_to_login_label = Label(register_frame, text="Back to login", font=("Helvetica", 10, "italic"),
                                    bg="#ffffff", fg="#007BFF", cursor="hand2")
        back_to_login_label.pack(pady=5)

        back_to_login_label.bind("<Button-1>", lambda e: self.login_window())

    def login_window(self):
        self.reset_window()

        login_frame = Frame(self.window, bg="#ffffff", bd=2, relief=GROOVE)
        login_frame.place(relx=0.5, rely=0.5, anchor=CENTER, width=400, height=300)

        title_label = Label(login_frame, text="Login", font=("Helvetica", 18, "bold"), bg="#ffffff", fg="#333333")
        title_label.pack(pady=10)

        username_label = Label(login_frame, text="Username", font=("Helvetica", 12), bg="#ffffff", fg="#333333")
        username_label.pack(pady=5, anchor=W, padx=20)
        username_entry = ttk.Entry(login_frame, font=("Helvetica", 12))
        username_entry.pack(pady=5, padx=20, fill=X)

        password_label = Label(login_frame, text="Password", font=("Helvetica", 12), bg="#ffffff", fg="#333333")
        password_label.pack(pady=5, anchor=W, padx=20)
        password_entry = ttk.Entry(login_frame, font=("Helvetica", 12), show="*")
        password_entry.pack(pady=5, padx=20, fill=X)

        login_button = Button(login_frame, text="Login", font=("Helvetica", 12, "bold"), bg="#4CAF50", fg="#ffffff",
                              cursor="hand2",
                              command=lambda : self.login(username_entry.get(), password_entry.get()))
        login_button.pack(pady=20, padx=20, fill=X)

        register_label = Label(login_frame, text="No account? Register here", font=("Helvetica", 10, "italic"),
                               bg="#ffffff", fg="#007BFF", cursor="hand2")
        register_label.pack(pady=5)

        register_label.bind("<Button-1>", lambda e: self.register_window())


if __name__ == "__main__":
    root = Tk()
    root.maxsize(WINDOW_WIDTH, WINDOW_HEIGHT)
    root.minsize(WINDOW_WIDTH, WINDOW_HEIGHT)
    root.title('Motorcycle Shop System')

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width - WINDOW_WIDTH) // 2
    y = (screen_height - WINDOW_HEIGHT) // 2
    root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}+{x}+{y}")

    shop = MotorcycleShop(root)
    shop.run()
