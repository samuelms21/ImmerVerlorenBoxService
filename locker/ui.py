import abc
from abc import abstractmethod
from locker.services import LockerService
import argparse
from .dto import *
from tkinter import *
from tkinter import ttk, messagebox
from kink import di, inject
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class Graph(abc.ABC):
    @abstractmethod
    def run(self, report_dto):
        pass


class ItemTypeVsDurationGraph(Graph):
    def run(self, item_type_vs_duration_report_dto):
        plt.figure(figsize=(6, 4))
        x1 = item_type_vs_duration_report_dto.electronics[0]
        y1 = item_type_vs_duration_report_dto.electronics[1]
        plt.plot(x1, y1, label='electronics', color='green', linewidth=2,
                 marker=".", markersize=10)

        x2 = item_type_vs_duration_report_dto.food_and_beverage[0]
        y2 = item_type_vs_duration_report_dto.food_and_beverage[1]
        plt.plot(x2, y2, label='food_and_beverage', color='red', linewidth=2,
                 marker=".", markersize=10)

        x3 = item_type_vs_duration_report_dto.clothing[0]
        y3 = item_type_vs_duration_report_dto.clothing[1]
        plt.plot(x3, y3, label='clothing', color='blue', linewidth=2,
                 marker=".", markersize=10)

        x4 = item_type_vs_duration_report_dto.pharmacy[0]
        y4 = item_type_vs_duration_report_dto.pharmacy[1]
        plt.plot(x4, y4, label='pharmacy', color='yellow', linewidth=2,
                 marker=".", markersize=10)

        plt.title("Item Type VS Duration\nReport",
                  fontdict={'fontname': 'Arial'})
        plt.xlabel("Duration in Locker (Minutes)",
                  fontdict={'fontname': 'Arial'})
        plt.ylabel("Amount of items",
                  fontdict={'fontname': 'Arial'})

        plt.legend()
        plt.show()


class ItemSizeVSDurationGraph(Graph):
    def run(self, item_size_vs_duration_report_dto):
        plt.figure(figsize=(6, 4))
        x1 = item_size_vs_duration_report_dto.large[0]
        y1 = item_size_vs_duration_report_dto.large[1]
        plt.plot(x1, y1, label='Large', color='green', linewidth=2,
                 marker=".", markersize=10)

        x2 = item_size_vs_duration_report_dto.medium[0]
        y2 = item_size_vs_duration_report_dto.medium[1]
        plt.plot(x2, y2, label='Medium', color='red', linewidth=2,
                 marker=".", markersize=10)

        x3 = item_size_vs_duration_report_dto.small[0]
        y3 = item_size_vs_duration_report_dto.small[1]
        plt.plot(x3, y3, label='Small', color='blue', linewidth=2,
                 marker=".", markersize=10)

        plt.title("Item Size VS Duration\nReport",
                  fontdict={'fontname': 'Arial'})
        plt.xlabel("Duration in Locker (Minutes)",
                  fontdict={'fontname': 'Arial'})
        plt.ylabel("Amount of items",
                  fontdict={'fontname': 'Arial'})

        plt.legend()
        plt.show()


@inject
class LockerUI:
    def __init__(self, _locker_service: LockerService):
        self.locker_service = _locker_service

    def back_to_main_menu(self, root, main_menu_frame):
        main_menu_frame.destroy()
        root.destroy()
        self.locker_service.arduino_locker.close_all_lockers()
        self.main_menu()

    def delete_all_rows_from_treeview(self, treeview):
        for item in treeview.get_children():
            treeview.delete(item)

    def update_treeview(self, treeview):
        all_users_from_repository = self.locker_service.get_all_users()
        users_for_display = []
        for user in all_users_from_repository:
            users_for_display.append((f'{user.user_id}', f'{user.name}', f'{user.email}'))

        for user_info in users_for_display:
            treeview.insert('', END, values=user_info)

    def operator_report(self):
        item_type_vs_duration_report_dto, item_size_vs_duration_report_dto = self.locker_service.operator_report()

        if self.locker_service.operator_report() == -1:
            messagebox.showerror(title="Error", message="No package data to analyze.")
        else:
            electronics_x = item_type_vs_duration_report_dto.electronics[0]
            electronics_y = item_type_vs_duration_report_dto.electronics[1]
            food_and_beverage_x = item_type_vs_duration_report_dto.food_and_beverage[0]
            food_and_beverage_y = item_type_vs_duration_report_dto.food_and_beverage[1]
            clothing_x = item_type_vs_duration_report_dto.clothing[0]
            clothing_y = item_type_vs_duration_report_dto.clothing[1]
            pharmacy_x = item_type_vs_duration_report_dto.pharmacy[0]
            pharmacy_y = item_type_vs_duration_report_dto.pharmacy[1]
            large_x = item_size_vs_duration_report_dto.large[0]
            large_y = item_size_vs_duration_report_dto.large[1]
            medium_x = item_size_vs_duration_report_dto.medium[0]
            medium_y = item_size_vs_duration_report_dto.medium[1]
            small_x = item_size_vs_duration_report_dto.small[0]
            small_y = item_size_vs_duration_report_dto.small[1]

            root = Tk()
            root.title("Report | ImmerVerloren Box Service")

            figure1 = plt.Figure(figsize=(6, 5), dpi=100)

            ax1 = figure1.add_subplot(211)
            ax1.plot(electronics_x, electronics_y, color='green', linewidth=2, marker='.',
                     label='electronics')
            ax1.plot(food_and_beverage_x, food_and_beverage_y, color='red', linewidth=2,
                     marker='.', label='food_and_beverage')
            ax1.plot(clothing_x, clothing_y, color='blue', linewidth=2,
                     marker='.', label='clothing')
            ax1.plot(pharmacy_x, pharmacy_y, color='yellow', linewidth=2,
                     marker='.', label='pharmacy')
            ax1.legend()

            ax2 = figure1.add_subplot(212)
            ax2.plot(large_x, large_y, color='green', linewidth=2,
                     label='Large', marker='.')
            ax2.plot(medium_x, medium_y, color='red', linewidth=2,
                     label='Medium', marker='.')
            ax2.plot(small_x, small_y, color='blue', linewidth=2,
                     label='Small', marker='.')
            ax2.legend()
            ax2.set_xlabel("Duration in Locker (Minutes)")

            line1 = FigureCanvasTkAgg(figure1, root)
            line1.get_tk_widget().pack(side=LEFT, fill=BOTH)

            root.mainloop()


    def open_operator_page(self, root, main_menu_frame, header_text,
                           subheading_font, body_font):
        main_menu_frame.destroy()
        header_text.grid(column=1, row=0, padx=10, pady=10)
        # Make Operator Frame
        operator_frame = LabelFrame(root, font=subheading_font,
                                    text="Operator", padx=15, pady=10)
        operator_frame.grid(column=1, row=1)

        ####################################################################
        # All Users Table
        # Define columns
        columns = ("user_id", "name", "email")
        tree = ttk.Treeview(operator_frame, columns=columns, show='headings')

        # Define headings
        tree.heading('user_id', text="User ID")
        tree.heading('name', text="Name")
        tree.heading('email', text="Email")

        # Generate Sample Data
        all_users_from_repository = self.locker_service.get_all_users()
        users_for_display = []
        if all_users_from_repository:
            for user in all_users_from_repository:
                users_for_display.append((f'{user.user_id}', f'{user.name}', f'{user.email}'))
        else:
            users_for_display = []

        # Add data to treeview
        for user_info in users_for_display:
            tree.insert('', END, values=user_info)

        def item_selected(event):
            for selected_item in tree.selection():
                item = tree.item(selected_item)
                record = item['values']
                # Show a message
                showinfo(title="Information", message=",".join(record))

        tree.bind('<<TreeviewSelect>>', item_selected)
        tree.grid(column=1, row=2, sticky='nsew')

        # Add a scrollbar
        scrollbar = ttk.Scrollbar(operator_frame, orient=VERTICAL,
                                  comman=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.grid(column=2, row=2, sticky='ns')
        ##########################################################################

        # Register / Remove User by Operator
        # Register/Remove User Frame
        register_remove_user_frame = LabelFrame(operator_frame,
                                                font=subheading_font,
                                                text="Register/Remove User",
                                                padx=15, pady=10,
                                                bd=5)
        register_remove_user_frame.grid(columnspan=3, column=1, row=3,
                                        padx=15, pady=10)

        input_user_name_label = Label(register_remove_user_frame, font=body_font,
                                      padx=5, pady=5, text="Name")
        input_user_name = Entry(register_remove_user_frame, font=body_font,
                                width=30)
        input_user_name_label.grid(column=1, row=4)
        input_user_name.grid(column=1, row=5, pady=5, padx=10)

        input_email_label = Label(register_remove_user_frame, font=body_font,
                                      padx=5, pady=5, text="Email")
        input_email = Entry(register_remove_user_frame, font=body_font,
                                width=30)
        input_email_label.grid(column=1, row=6)
        input_email.grid(column=1, row=7, pady=5, padx=10)

        register_button_color = "#38b000"
        register_button = Button(register_remove_user_frame,
                                 font=body_font, bg=register_button_color,
                                 fg="white", bd=3,
                                 width=10, padx=5, pady=5, text="Register",
                                 command=lambda : self.register_new_user(input_user_name, input_email, tree))
        register_button.grid(column=0, row=8)

        report_button_color = "#0077b6"
        report_button = Button(register_remove_user_frame,
                               font=body_font, bg=report_button_color,
                               fg="white", bd=3,
                               width=18, padx=5, pady=5, text="Report",
                               command=self.operator_report)
        report_button.grid(column=1, row=8)

        remove_button_color = "#ea0c20"
        remove_button = Button(register_remove_user_frame,
                               font=body_font, bg=remove_button_color,
                               fg="white", bd=3,
                               width=10, padx=5, pady=5, text="Remove",
                               command=lambda:self.remove_user(input_user_name, input_email, tree))
        remove_button.grid(column=2, row=8)

        # Back to main menu button
        back_to_main_menu_button = Button(root, text="Back to Main Menu",
                                          command=lambda: self.back_to_main_menu(root, main_menu_frame),
                                          font=body_font, padx=15, pady=3)
        back_to_main_menu_button.grid(column=1, row=2, pady=10)

    def register_new_user(self, name_entry, email_entry, treeview):
        name = name_entry.get()
        email = email_entry.get()

        if not name or not email:
            messagebox.showerror(title="Error", message="Please fill all required fields.")
            return

        name_and_email_dto = UserNameAndEmailDTO(name, email)
        register_status = self.locker_service.register_new_user(name_and_email_dto)
        if register_status == -1:
            messagebox.showerror(title="Error", message="User is already registered.")
        else:
            self.delete_all_rows_from_treeview(treeview)
            self.update_treeview(treeview)
            messagebox.showinfo(title="Registration Successful",
                                  message="User successfully registered!")

    def remove_user(self, name_entry, email_entry, treeview):
        name = name_entry.get()
        email = email_entry.get()

        if not name or not email:
            messagebox.showerror(title="Error", message="Please fill all required fields.")
            return

        name_and_email_dto = UserNameAndEmailDTO(name, email)
        remove_status = self.locker_service.remove_user(name_and_email_dto)
        if remove_status == -1:
            messagebox.showerror(title="Error", message="User not found.")
        else:
            self.delete_all_rows_from_treeview(treeview)
            self.update_treeview(treeview)
            messagebox.showinfo(title="Removal Successful",
                                message="User successfully removed!")

    def main_menu(self):
        root = Tk()
        root.title("ImmerVerloren Box Service")

        header_font = "Bahnschrift 25 bold"
        body_font = "Bahnschrift 11"
        subheading_font = "Bahnschrift 12"

        header_text = Label(root, text="ImmerVerloren Box Service"
                            , bg="#29335C", fg="white"
                            , padx=20, pady=20
                            , font=header_font)
        header_text.grid(column=1, row=0, padx=10, pady=10)

        # Main Menu
        main_menu_frame = LabelFrame(root, text="Main Menu",
                                     padx=15, pady=15, font=subheading_font,
                                     fg="#29335C")
        main_menu_frame.grid(columnspan=3, rowspan=5, column=1, row=1,
                             padx=25, pady=20)

        # Operator Button
        operator_button = Button(main_menu_frame, text="Operator", width=30, height=2,
                                 font=body_font,
                                 command= lambda: self.open_operator_page(
                                     root, main_menu_frame, header_text,
                                     subheading_font, body_font))
        operator_button.grid(column=1, row=2, pady=5)

        # Staff / Mahasiswa Button
        staff_mahasiswa_button = Button(main_menu_frame,
                                        text="Staff / Mahasiswa CIT",
                                        width=30, height=2, font=body_font,
                                        command=lambda: self.open_staff_mahasiswa_page(root, main_menu_frame, header_text,
                                                                                       subheading_font, body_font))
        staff_mahasiswa_button.grid(column=1, row=3, pady=5)

        # Kurir Button
        kurir_button = Button(main_menu_frame, text="Kurir", width=30, height=2,
                              font=body_font, command=lambda: self.open_courier_page(root, main_menu_frame, header_text,
                                                                             subheading_font, body_font))
        kurir_button.grid(column=1, row=4, pady=5)
        root.mainloop()

    def open_courier_page(self, root, main_menu_frame, header_text,
                           subheading_font, body_font):
        main_menu_frame.destroy()
        header_text.grid(column=0, row=0, columnspan=2, padx=10, pady=10)
        # Locker Frame
        locker_frame = LabelFrame(root, text="Courier",
                                   padx=15, pady=10, font=subheading_font,
                                   fg="#29335C")
        locker_frame.grid(column=0, row=1)

        occupied_lockers = [locker[0] for locker in self.locker_service.get_all_occupied_lockers()]

        for locker in [1,2,3,4]:
            if locker not in occupied_lockers:
                self.locker_service.arduino_locker.open_or_close_specific_locker(locker, True)

        def check_if_available(i):
            if occupied_lockers:
                if i in occupied_lockers:
                    return DISABLED
                else:
                    return NORMAL
            return NORMAL

        locker_no_label = Label(locker_frame, text="Locker number :",
                                font=body_font, padx=10, pady=10)
        locker_no_value_label = Label(locker_frame, text="Choose a locker",
                                      font=body_font, padx=10, pady=10)

        item_size_label = Label(locker_frame, text="Item size :",
                                font=body_font, padx=10, pady=10, justify= RIGHT)
        item_size_value_label = Label(locker_frame, text="Choose a locker",
                                      font=body_font, padx=10, pady=10)

        # Locker 1
        locker_no_and_size_var = StringVar()
        locker_1_large = Radiobutton(locker_frame, text="Locker 1\nLarge",
                                     indicator=0, value="1_Large", state=check_if_available(1),
                                     width=20, height=5, font=body_font, variable=locker_no_and_size_var,
                                     command=lambda:
                                     self.update_item_size_and_locker_no(1, "Large",
                                                                         locker_no_value_label, item_size_value_label))
        locker_1_large.grid(column=0, row=2)

        # Locker 2
        locker_2_medium = Radiobutton(locker_frame, text="Locker 2\nMedium",
                                      indicator=0, value="2_Medium", state=check_if_available(2),
                                      width=20, height=5, font=body_font, variable=locker_no_and_size_var,
                                      command=lambda: self.update_item_size_and_locker_no(2, "Medium",
                                                                          locker_no_value_label, item_size_value_label)
                                      )
        locker_2_medium.grid(column=1, row=2)

        # Locker 3
        locker_3_small = Radiobutton(locker_frame, text="Locker 3\nSmall",
                                      indicator=0, value="3_Small", state=check_if_available(3),
                                     width=20, height=5, font=body_font, variable=locker_no_and_size_var,
                                     command=lambda: self.update_item_size_and_locker_no(3, "Small",
                                                                          locker_no_value_label, item_size_value_label))
        locker_3_small.grid(column=0, row=3)

        # Locker 4
        locker_4_small = Radiobutton(locker_frame, text="Locker 4\nSmall",
                                      indicator=0, value="4_Small", state=check_if_available(4),
                                     width=20, height=5, font=body_font, variable=locker_no_and_size_var,
                                     command=lambda: self.update_item_size_and_locker_no(4, "Small",
                                                                          locker_no_value_label, item_size_value_label))
        locker_4_small.grid(column=1, row=3)

        current_lockers = [locker_1_large, locker_2_medium, locker_3_small, locker_4_small]

        # Input Fields and Radio Buttons
        package_info_frame = LabelFrame(root, text="Package Info",
                                   padx=15, pady=27, font=subheading_font,
                                   fg="#29335C")
        package_info_frame.grid(column=1, row=1)

        post_box_id_label = Label(package_info_frame, text="Post Box ID :",
                                  font=body_font, padx=10, pady=10)
        post_box_id_entry = Entry(package_info_frame, font=body_font, width=20, bd=3)
        post_box_id_label.grid(column=0, row=4, sticky=E)
        post_box_id_entry.grid(column=1, row=4, sticky=W)

        item_type_label = Label(package_info_frame, text="Item type :",
                                  font=body_font, padx=10, pady=10)

        item_type_var = StringVar()
        item_type_food_and_beverage = Radiobutton(package_info_frame, text="Food and Beverage", value="food_and_beverage",
                                                  font=body_font, variable=item_type_var)
        item_type_electronics = Radiobutton(package_info_frame, text="Electronics", value="electronics",
                                            font=body_font, variable=item_type_var)
        item_type_clothing = Radiobutton(package_info_frame, text="Clothing", value="clothing",
                                         font=body_font, variable=item_type_var)
        item_type_pharmacy = Radiobutton(package_info_frame, text="Pharmacy", value="pharmacy",
                                         font=body_font, variable=item_type_var)

        item_type_label.grid(column=0, row=5, sticky=E)
        item_type_food_and_beverage.grid(column=1, row=5, sticky=W,pady=5)
        item_type_electronics.grid(column=1, row=6, sticky=W, pady=5)
        item_type_clothing.grid(column=1, row=7, sticky=W, pady=5)
        item_type_pharmacy.grid(column=1, row=8, sticky=W, pady=5)

        locker_no_label.grid(column=0, row=9, sticky=E)
        locker_no_value_label.grid(column=1, row=9, sticky=W)
        item_size_label.grid(column=0, row=10, sticky=E)
        item_size_value_label.grid(column=1, row=10, sticky=W)

        drop_and_close = Button(package_info_frame, text="Drop and Close",
                                font=body_font, padx=10, pady=10,
                                bg="#0077b6", fg="white",
                                command=lambda: self.drop_and_close(post_box_id_entry, locker_no_and_size_var.get(),
                                                                    item_type_var, body_font, root, main_menu_frame))
        drop_and_close.grid(column=0, row=11, columnspan=2)

        # Back to Main Menu Button
        back_to_main_menu_button = Button(root, text="Back to Main Menu",
                                          command=lambda: self.back_to_main_menu(root, main_menu_frame),
                                          font=body_font, padx=15, pady=3)
        back_to_main_menu_button.grid(column=1, row=2, pady=10)

    def update_item_size_and_locker_no(self, locker_no, item_size, locker_no_label_value,
                                       item_size_label_value):
        locker_no_label_value.configure(text = locker_no)
        item_size_label_value.configure(text = item_size)

    def drop_and_close(self, post_box_id_entry, locker_no_and_size_var, item_type, body_font, root, main_menu_frame):
        post_box_id = post_box_id_entry.get()
        if not post_box_id:
            messagebox.showerror(title="Error", message="Please fill in the Post Box ID to drop your package.")
        else:
            item_type = item_type.get()
            try:
                locker_no = int(str(locker_no_and_size_var)[:1])
                item_size = locker_no_and_size_var[2:]
            except ValueError:
                locker_no = None
                item_size = None

            if not item_type:
                messagebox.showerror(title="Error", message="Please select one of the item types to proceed.")
            else:
                new_item_size = None

                if locker_no is None and new_item_size is None:
                        item_size_window = Tk()
                        item_size_window.title("ImmerVerloren Box Service")

                        item_size_label = Label(item_size_window, text="Input item size below:",
                                                font=body_font)
                        item_size_label.grid(column=1, row=0, padx=10, pady=10)
                        item_size_entry = Entry(item_size_window, font=body_font,
                                                bd=5, width=15)
                        item_size_entry.grid(column=1, row=1, padx=10, pady=10)

                        def get_item_size():
                            new_item_size = item_size_entry.get()
                            if new_item_size not in ["Large", "Medium", "Small"]:
                                messagebox.showerror(title="Error", message="Invalid item size.\n"
                                                                            "Available item sizes:"
                                                                            "\n * Large"
                                                                            "\n * Medium"
                                                                            "\n * Small")
                                return
                            received_package_dto = ReceivedPackageFromUIDTO(post_box_id, item_type, new_item_size,
                                                                            locker_no)
                            if post_box_id:
                                drop_status = self.locker_service.drop_package_in_locker(received_package_dto)
                                if drop_status == -1:
                                    messagebox.showerror(title="Error", message="Post Box ID does not exist.\n"
                                                                                "Please report to the nearest security officer.")
                                    item_size_window.destroy()
                                else:
                                    message = f"Package is successfully delivered!\n" \
                                              f"Below are your package delivery details:\n" \
                                              f"Post Box ID: {post_box_id}\n" \
                                              f"Item type: {item_type}\n" \
                                              f"Item size: {new_item_size}\n"
                                    messagebox.showinfo(title="Drop Successful",
                                                        message=message)
                                    item_size_window.destroy()
                                    self.back_to_main_menu(root, main_menu_frame)
                            else:
                                messagebox.showerror(title="Error", message="Please fill in all required fields.")
                                item_size_window.destroy()


                        enter_item_size_btn = Button(item_size_window, text="Enter",
                                                     font=body_font,
                                                     command=get_item_size)
                        enter_item_size_btn.grid(column=1, row=2, padx=5, pady=5)
                else:
                    received_package_dto = ReceivedPackageFromUIDTO(post_box_id, item_type, item_size,
                                                                locker_no)
                    if post_box_id:
                        drop_status = self.locker_service.drop_package_in_locker(received_package_dto)
                        if drop_status == -1:
                            messagebox.showerror(title="Error", message="Post Box ID does not exist."
                                                                        "\nPlease report to the nearest security officer.")
                        else:
                            message = f"Package is successfully delivered!\n" \
                                      f"Below are your package delivery details:\n" \
                                      f"Post Box ID: {post_box_id}\n" \
                                      f"Locker No: {locker_no}\n" \
                                      f"Item type: {item_type}\n" \
                                      f"Item size: {item_size}\n"

                            messagebox.showinfo(title="Drop Successful",
                                            message=message)
                            self.back_to_main_menu(root, main_menu_frame)
                    else:
                        messagebox.showerror(title="Error", message="Please fill in all required fields.")

    def open_staff_mahasiswa_page(self, root, main_menu_frame, header_text, subheading_font, body_font):
        main_menu_frame.destroy()
        header_text.grid(column=0, row=0, columnspan=3, padx=10, pady=10)
        # Staff/Mahasiswa Frame
        staff_mahasiswa_frame= LabelFrame(root, text="Staff/Mahasiswa",
                                  padx=15, pady=10, font=subheading_font,
                                  fg="#29335C", height=20, width=40)
        staff_mahasiswa_frame.grid(column=0, row=1, columnspan=3)

        # Input User ID and PIN
        user_id_label = Label(staff_mahasiswa_frame, text="User ID:", bd=4, font=body_font)
        user_id_entry = Entry(staff_mahasiswa_frame, bd=4, font=body_font)
        user_id_label.grid(column=0, row=2, sticky=E)
        user_id_entry.grid(column=1, row=2, sticky=W, padx=10, pady=10)

        pin_label = Label(staff_mahasiswa_frame, text="PIN:", bd=4, font=body_font)
        pin_entry = Entry(staff_mahasiswa_frame, bd=4, font=body_font, show="*")
        pin_label.grid(column=0, row=3, sticky=E)
        pin_entry.grid(column=1, row=3, sticky=W, padx=10, pady=10)

        open_button = Button(staff_mahasiswa_frame, text="Open", bg="#38b000", fg="white", font=body_font,
                              width=9, padx=10, pady=5,
                              command=lambda: self.open_locker_and_validate_user_id_and_pin(
                                  user_id_entry.get(), pin_entry.get()
                              ))
        open_button.grid(column=0, row=4, sticky=W)

        close_button = Button(staff_mahasiswa_frame, text="Close", bg="#ea0c20", fg="white", font=body_font,
                              width=9, padx=10, pady=5, command=self.locker_service.arduino_locker.close_all_lockers)
        close_button.grid(column=1, row=4, sticky=E)

        back_to_main_menu_button = Button(root, text="Back to Main Menu",
                                          command=lambda: self.back_to_main_menu(root, main_menu_frame),
                                          font=body_font, padx=15, pady=3)
        back_to_main_menu_button.grid(column=1, row=2, pady=10)

    def open_locker_and_validate_user_id_and_pin(self, user_id_entry, pin_entry):
        if not user_id_entry:
            messagebox.showerror(title="Error", message="Please enter your User ID to proceed.")
        else:
            # User ID is not empty
            pickup_package_dto = PickupPackageDTO(user_id_entry, pin_entry)
            pickup_status = self.locker_service.pickup_package_from_locker(pickup_package_dto)
            if pickup_status is None:
                pickup_message = '''
                Package pickup successful.\n
                Thank you for using our services!
                '''
                messagebox.showinfo(title="Pickup Successful!", message=pickup_message)
            elif pickup_status == -2:
                special_pickup_message = '''
                The package you want to pickup is at the security office.\n
                Thank you for using our services!
                '''
                messagebox.showinfo(title="Pickup Package", message=special_pickup_message)
            elif pickup_status == -1:
                error_message = '''
                The User ID or PIN that you have entered is invalid\n
                Please try again.
                '''
                messagebox.showerror(title="Error", message=error_message)
            elif pickup_status == -3:
                info_message = '''
                You do not have any packages waiting for you.\n
                Thank you for using our services!
                '''
                messagebox.showinfo(title="No packages for now!", message=info_message)
            elif pickup_status == -4:
                info_message = '''
                You have packages waiting 
                for you inside one of our lockers.\n
                Please enter the 
                required PIN to pickup your package.\n
                Thank you for using our services!
                '''
                messagebox.showinfo(title="You have packages waiting for you.", message=info_message)

    def run(self):
        self.locker_service.setup()
        self.main_menu()
