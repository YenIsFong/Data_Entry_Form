import tkinter as tk
from tkinter import ttk, filedialog, messagebox

import pandas as pd
import numpy as np
from openpyxl import load_workbook
from Backend import *

#################################################################################################
## Global Functions

def get_user_input():
    user_inputs = []
    for i, entry in enumerate(entries):
        user_input = entry.get()  # or entries[i].get()
        user_inputs.append(user_input)
    return user_inputs

def SaveNewError():
    user_inputs = get_user_input()
    try:
        result = addError(user_inputs[0],user_inputs[1],float(user_inputs[2]))
        if result is False:
            raise Exception("Error already exists")
        
        # errors = getErrorList()
        # errors.append("Add new error")
        # combo['values'] = errors
        # selected_error_var.set("Add new error")
        messagebox.showinfo("Success", f"{user_inputs[0]} successfully added.")
        error_tab(frame1) # Go back ErrorTab

    except Exception as e:
        print(e)
        if str(e) == "Error already exists":
            messagebox.showerror("Error", "Error already exists.")
        else:
            messagebox.showerror("Error", "Please enter a number for frequency.")
    # Get the ErrorString
    # Call addError(ErrorString):
    
            # def addNewAction(ErrorString, newActionString,Frequency):

def save_action(error_name,givenActionName,freq):
    """Retrieves user input and saves a new action for the selected error."""

    if not givenActionName.strip():
        messagebox.showerror("Error", "Action name cannot be empty.")
        return

    result = addNewAction(error_name, givenActionName, freq)  # Default frequency is 1

    if result:
        messagebox.showinfo("Success", "Action added successfully!")

###############################################################################################

def error_tab(frame1):
    dic = {"Issue": 3, 
            "Action Taken": 4, 
            "Frequency": 5
            }
    
    global combo, sops, labels, entries, comboboxlist, buttons, tk_list
    buttons = []
    labels = []
    entries = []
    sops = []
    comboboxlist = []
    tk_list = []
    
    errors = getErrorList()
    errors.append("Delete error")
    errors.append("Add new error")


    # Clear existing widgets
    for widget in frame1.winfo_children():
        widget.destroy()

    # Create combo box
    global selected_error_var
    selected_error_var = tk.StringVar()
    combo = ttk.Combobox(frame1, values=errors, state="readonly", width=40, textvariable=selected_error_var)
    combo.grid(row=2, column=0, sticky='W')
    # Optionally, remove or adjust this if you want a different default:
    combo.current(len(errors)-1)
    
    def Display_Selected_Error():
        # display all things to query
        for key, value in dic.items():
            label = tk.Label(frame1, text=key)
            label.grid(row=value, column=0, sticky='W')
            labels.append(label)
            provided = tk.StringVar()
            entry = tk.Entry(frame1, width=35, textvariable=provided)
            entry.grid(row=value, column=1, sticky='WE')
            entries.append(entry)
        button = tk.Button(frame1, text="Save", width=5, height=1, command=SaveNewError)
        # button.place(relx=0.5, rely=0.5, anchor="se")
        button.grid(row=6, column=1)
        buttons.append(button)
        
    def DeleteAction():
        
        label = tk.Label(frame1, text="Please Select Which Error to Delete: ")
        label.grid(row=3, column=0, sticky='W')  
        labels.append(label)
        

        # Create a combo box, values= getActionList(ComboBoxValue)
        errorlist = getErrorList()
        
        ErrorComboBox = ttk.Combobox(frame1, values=errorlist, state="readonly", width=40)
        ErrorComboBox.grid(row=3, column=1, sticky='W')
        ErrorComboBox.current(len(errorlist)-1)
        comboboxlist.append(ErrorComboBox) # append to list to destory everytime we reset
        
        def update_delete_error(event):
            print("Okay cool")
        ErrorComboBox.bind("<<ComboboxSelected>>", update_delete_error)
        
        
        def confirm_delete_error():
            selected_error = ErrorComboBox.get()
            if not selected_error:
                messagebox.showerror("Error", "Please select an action to delete.")
                return

            confirmation = messagebox.askyesno("Confirm Deletion", f"Are you sure you want to delete '{selected_error}'?")
            if confirmation:
                deleteError(selected_error)
                messagebox.showinfo("Success", f"Action '{selected_error}' deleted successfully.")
                ErrorComboBox['values'] = getErrorList()  # Refresh the combobox
        
        delete_button = tk.Button(frame1, text="Delete Action", command=confirm_delete_error, width=15)
        delete_button.grid(row=4, column=1)
        buttons.append(delete_button)
        
        
    def display_Current(ComboBoxValue):
        # display all things to query
        label = tk.Label(frame1, text=ComboBoxValue)
        label.grid(row=3, column=0, sticky='W')  
        labels.append(label)
        
        label1 = tk.Label(frame1, text="Increment or Decrement Frequency")
        label1.grid(row=3, column=1, sticky='W')  
        labels.append(label1)

        # Create a combo box, values= getActionList(ComboBoxValue)
        actions = getActionList(ComboBoxValue)
        actions.append("Delete Action")
        actions.append("Add Action")        

        label = tk.Label(frame1, text="Action Taken")
        label.grid(row=4, column=0, sticky='W')
        labels.append(label)
        ActionComboBox = ttk.Combobox(frame1, values=actions, state="readonly", width=40)
        ActionComboBox.grid(row=4, column=1, sticky='W')
        ActionComboBox.current(len(actions)-1)
        comboboxlist.append(ActionComboBox) # append to list to destory everytime we reset
        
        def update_Action(event):
            global tk_list  # Declare tk_list as a global variable again
            current_Action = ActionComboBox.current()
            ActionValue = actions[current_Action]
            for item in tk_list:
                item.destroy()
            tk_list = []
            match ActionValue: 
                case "Add Action":
                    # Clear any previous widgets before adding new ones
                    global label, frequency_label, plus_button, minus_button

                    # print("Okay this is the Default value")

                    # Label for entering new action
                    labelf = tk.Label(frame1, text="Enter Action to Add:")
                    labelf.grid(row=5, column=0, sticky='W')
                    tk_list.append(labelf)

                    # Entry field for new action
                    providedf = tk.StringVar()
                    entryq = tk.Entry(frame1, width=35, textvariable=providedf)
                    entryq.grid(row=5, column=1, sticky='W')
                    tk_list.append(entryq)

                    # Create the "Save Action" button
                    save_action_button = tk.Button(
                        frame1, text="Save Action", width=20, 
                        command=lambda: save_action(ComboBoxValue, providedf.get(), 1)  # Corrected variable reference
                    )
                    save_action_button.grid(row=6, column=1, pady=10, sticky="W")  # Align with Entry
                    tk_list.append(save_action_button)
                    
                case "Delete Action":
                    # Label for selecting action to delete
                    delete_label = tk.Label(frame1, text="Select Action to Delete:")
                    delete_label.grid(row=5, column=0, sticky='W')
                    tk_list.append(delete_label)

                    # Get the list of actions for the selected error
                    newactionlist = getActionList(ComboBoxValue)

                    # Create a combobox with available actions
                    delete_action_combobox = ttk.Combobox(frame1, values=newactionlist, state="readonly", width=40)
                    delete_action_combobox.grid(row=5, column=1, sticky='W')
                    tk_list.append(delete_action_combobox)

                    # Delete Button
                    def confirm_delete():
                        selected_action = delete_action_combobox.get()
                        if not selected_action:
                            messagebox.showerror("Error", "Please select an action to delete.")
                            return

                        confirmation = messagebox.askyesno("Confirm Deletion", f"Are you sure you want to delete '{selected_action}'?")
                        if confirmation:
                            deleteAction(ComboBoxValue, selected_action)
                            messagebox.showinfo("Success", f"Action '{selected_action}' deleted successfully.")
                            delete_action_combobox['values'] = getActionList(ComboBoxValue)  # Refresh the combobox

                    delete_button = tk.Button(frame1, text="Delete Action", command=confirm_delete, width=15)
                    delete_button.grid(row=6, column=1, sticky='W', pady=10)
                    tk_list.append(delete_button)

                
                case _:
                    # Label for frequency
                    labeld = tk.Label(frame1, text="Frequency")
                    labeld.grid(row=5, column=0, sticky='W')
                    tk_list.append(labeld)

                    # Frequency Label
                    frequency_label = tk.Label(
                        frame1,
                        text=getActionFrequency(ComboBoxValue, ActionValue),
                        font=('Helvetica', 20),
                        anchor='w'
                    )
                    frequency_label.grid(row=5, column=1, sticky='W', padx=(5, 0))  # Move it closer
                    tk_list.append(frequency_label)

                    # Function to update the label
                    def update_label():
                        frequency_label.config(text=getActionFrequency(ComboBoxValue, ActionValue))

                    # Button frame placement
                    button_frame = tk.Frame(frame1)
                    button_frame.grid(row=6, column=1, sticky='W', padx=10)  # Adjust column for proper alignment
                    tk_list.append(button_frame)  # Append the frame to tk_list

                    # Plus Button
                    plus_button = tk.Button(
                        button_frame, text="+", font=('Helvetica', 12),
                        width=5, height=2,  # Bigger buttons
                        command=lambda: [IncrementActionCount(ComboBoxValue, ActionValue), update_label()]
                    )
                    plus_button.pack(side="left", padx=5)  # Keep buttons close
                    tk_list.append(plus_button)  # Append the plus button to tk_list


                    # Minus Button
                    minus_button = tk.Button(
                        button_frame, text="-", font=('Helvetica', 12),
                        width=5, height=2,  # Bigger buttons
                        command=lambda: [DecrementActionCount(ComboBoxValue, ActionValue), update_label()]
                    )
                    minus_button.pack(side="left", padx=5)  # Keep buttons close
                    tk_list.append(minus_button)  # Append the minus button to tk_list

        ActionComboBox.bind("<<ComboboxSelected>>", update_Action)

    def error_page(event):
        global labels, entries, comboboxlist, buttons, tk_list
        
        # Remove existing widgets
        for label in labels:
            label.destroy()
        for entry in entries:
            entry.destroy()
        for item in comboboxlist:
            item.destroy()
        for item in buttons:
            item.destroy()
        for item in tk_list:
            item.destroy()
        labels = []
        entries = []
        comboboxlist = []
        buttons = []
        tk_list = []

        # Get the selected value directly from the combo box
        value = selected_error_var.get()
        print(f"Selected error: {value}")  # Debugging output

        # Check if the value is "Add new error" or something else
        if value == "Add new error":
            print("Only ADD")
            Display_Selected_Error()  # Function to add new error
        elif value == "Delete error":
            print("ONLY DELETE")
            DeleteAction()
        else:
            print("REST")
            display_Current(value)  # Function to display current error and actions

    # Bind combo box selection to error_page function
    combo.bind("<<ComboboxSelected>>", error_page)
    
def Action_Order_Tab(frame2):
    global labels, comboboxlist, order_vars
    labels = []
    comboboxlist = []
    order_vars = []  # Stores StringVar objects for combobox values

    errors = getErrorList()

    # Clear existing widgets
    for widget in frame2.winfo_children():
        widget.destroy()

    # Create a canvas and a frame within it
    canvas = tk.Canvas(frame2, width=800, height=600)
    scrollbar = tk.Scrollbar(frame2, orient=tk.VERTICAL, command=canvas.yview)
    
    scroll_frame = tk.Frame(canvas)

    # Attach scrollbar and frame
    scroll_window = canvas.create_window((0, 0), window=scroll_frame, anchor="nw")

    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # Function to update scroll region
    def update_scroll_region(event=None):
        """Ensures canvas recognizes new content and updates scrolling"""
        canvas.update_idletasks()
        canvas.configure(scrollregion=canvas.bbox("all"))

    scroll_frame.bind("<Configure>", update_scroll_region)

    # Enable scrolling with the mouse wheel
    def on_mousewheel(event):
        canvas.yview_scroll(-1 * (event.delta // 120), "units")

    canvas.bind("<MouseWheel>", on_mousewheel)  # Windows
    canvas.bind("<Button-4>", lambda e: canvas.yview_scroll(-1, "units"))  # Linux Scroll Up
    canvas.bind("<Button-5>", lambda e: canvas.yview_scroll(1, "units"))   # Linux Scroll Down

    # Create combo box for error selection
    selected_error_var = tk.StringVar()
    error_combo = ttk.Combobox(scroll_frame, values=errors, state="readonly", width=40, textvariable=selected_error_var)
    error_combo.grid(row=0, column=0, sticky='W')
    error_combo.current(len(errors) - 1)
    
    ## Create a label
    UserName_label = tk.Label(scroll_frame, text="User:")
    UserName_label.grid(row=0, column=1, sticky='W')

    # Create an entry field
    UserName_var = tk.StringVar()
    UserName_entry = tk.Entry(scroll_frame, textvariable=UserName_var, width=40)
    UserName_entry.grid(row=0, column=2, sticky='W')

    def update_action_order(event):
        """Updates the action order comboboxes dynamically"""
        for label in labels:
            label.destroy()
        for combo in comboboxlist:
            combo.destroy()
        labels.clear()
        comboboxlist.clear()
        order_vars.clear()

        selected_error = selected_error_var.get()
        if selected_error == "Add new error":
            return

        actions = getActionList(selected_error)
        num_actions = len(actions)
        available_orders = [""] + list(range(1, num_actions + 1))  # Include blank option

        def update_combobox_options(*args):
            """Dynamically updates combobox options to prevent duplicates while keeping blank option."""
            selected_values = [var.get() for var in order_vars if var.get()]  # Get all selected values

            for i, var in enumerate(order_vars):
                current_value = var.get()
                possible_values = [str(x) for x in available_orders if str(x) not in selected_values or str(x) == current_value]

                comboboxlist[i]["values"] = possible_values  # Update combobox options

        for i, action in enumerate(actions):
            label = tk.Label(scroll_frame, text=f"{action} Order:")
            label.grid(row=i+1, column=0, sticky='W')
            labels.append(label)

            order_var = tk.StringVar()
            action_combo = ttk.Combobox(scroll_frame, values=[str(x) for x in available_orders], state="readonly", textvariable=order_var, width=5)
            action_combo.grid(row=i+1, column=1, sticky='W')
            comboboxlist.append(action_combo)
            order_vars.append(order_var)  # Store the StringVar

            # Bind function to update combobox dynamically when a selection is made
            order_var.trace_add("write", update_combobox_options)

        update_scroll_region()  # Refresh scroll region after adding new widgets

    # Function to retrieve selected values and validate them
    def get_selected_values():
        selected_values = [var.get() for var in order_vars]

        # Validate selections: No empty values allowed
        if "" in selected_values:
            messagebox.showerror("Invalid Selection", "Please select a valid order for all actions. No blank values allowed!")
            return

        # Validate uniqueness: No duplicate orders allowed
        if len(selected_values) != len(set(selected_values)):
            messagebox.showerror("Invalid Selection", "Duplicate orders are not allowed! Please choose unique values.")
            return



        # Get the selected error name
        selected_error = selected_error_var.get()

        print("Selected Error:", selected_error)  # Debugging
        print("Selected Values:", selected_values)  # Debugging

        UserName = UserName_var.get()
        if UserName == "":
            messagebox.showerror("Invalid Selection", "Please Input New UserName!")
            return

        if UserName in getUser(selected_error):
            messagebox.showerror("Invalid Selection", "UserName Already Exist!")
            return

        # UserName="Anthony"
        addOrder(selected_error, selected_values, UserName)

        # Call backend function to update CSV
        # updateCSVActionOrder(selected_error, selected_values)

        messagebox.showinfo("Success", "Action order updated successfully!")

    # Bind error selection to update function
    error_combo.bind("<<ComboboxSelected>>", update_action_order)

    # Create a button to retrieve values
    get_values_button = tk.Button(scroll_frame, text="Enter Order Of Actions", command=get_selected_values)
    get_values_button.grid(row=100, column=0, columnspan=2, pady=10)

    update_scroll_region()  # Initial update
    
import tkinter as tk
from tkinter import ttk

def Action_Order_Query_Tab(frame3):
    global labels, comboboxlist, order_vars, database
    labels = []
    database = []
    comboboxlist = []
    order_vars = []

    # Clear previous content
    for widget in frame3.winfo_children():
        widget.destroy()

    # --- Create canvas + scrollbar wrapper ---
    canvas = tk.Canvas(frame3, height=500)
    scrollbar = ttk.Scrollbar(frame3, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    scrollable_frame = tk.Frame(canvas)
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

    def on_configure(event):
        canvas.configure(scrollregion=canvas.bbox("all"))

    scrollable_frame.bind("<Configure>", on_configure)

    # Mousewheel scrolling support
    def _on_mousewheel(event):
        canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def _bind_mousewheel(event):
        canvas.bind_all("<MouseWheel>", _on_mousewheel)

    def _unbind_mousewheel(event):
        canvas.unbind_all("<MouseWheel>")

    scrollable_frame.bind("<Enter>", _bind_mousewheel)
    scrollable_frame.bind("<Leave>", _unbind_mousewheel)

    # --- Your logic starts here ---
    errors = getErrorList()
    print("Errors:", errors)

    selected_error_var = tk.StringVar()
    error_combo = ttk.Combobox(scrollable_frame, values=errors, state="readonly", width=40, textvariable=selected_error_var)
    error_combo.grid(row=2, column=0, sticky='W', padx=10, pady=5)
    error_combo.current(len(errors) - 1)

    def display_User(event):
        for label in labels:
            label.destroy()
        for combo in comboboxlist:
            combo.destroy()
        for item in database:
            item.destroy()
        database.clear()
        labels.clear()
        comboboxlist.clear()
        order_vars.clear()

        selected_error = selected_error_var.get()
        print("Selected error:", selected_error)
        if selected_error == "Add new error":
            return

        user_label = tk.Label(scrollable_frame, text="Select User:")
        user_label.grid(row=4, column=0, sticky='W', padx=10)
        labels.append(user_label)

        users = getUser(selected_error)
        selected_user_var = tk.StringVar()
        user_combo = ttk.Combobox(scrollable_frame, values=users, state="readonly", width=40, textvariable=selected_user_var)
        user_combo.grid(row=4, column=1, sticky='W', padx=10)
        comboboxlist.append(user_combo)
        order_vars.append(selected_user_var)

        def display_action_order(event):
            for item in database:
                item.destroy()
            database.clear()

            SelectedUser = selected_user_var.get()
            sortedActionOrder = getActionOrderdict(selected_error, SelectedUser)
            print(f"Selected Error: {selected_error}")
            print(f"Selected User Variable: {SelectedUser}")
            row_num = 5
            for action, order in sortedActionOrder.items():
                order_label = tk.Label(scrollable_frame, text=f"{order}.")
                order_label.grid(row=row_num, column=0, padx=10, pady=2, sticky='W')
                database.append(order_label)

                action_label = tk.Label(scrollable_frame, text=action)
                action_label.grid(row=row_num, column=1, padx=10, pady=2, sticky='W')
                database.append(action_label)

                row_num += 1

        user_combo.bind("<<ComboboxSelected>>", display_action_order)

    error_combo.bind("<<ComboboxSelected>>", display_User)

def create_gui():
    global frame1,frame2,frame3
    root = tk.Tk()
    # root.geometry('600x450')
    root.geometry('700x500')  # Sets the window size to 1000x700 pixels
    root.title('Self-Update Platform')
    root.resizable(True, True)  # Allows the user to resize the window horizontally and vertically
    
    notebook = ttk.Notebook(root)
    notebook.pack(pady=10, expand=True)

    frame1 = ttk.Frame(notebook, width=600, height=400)
    frame2 = ttk.Frame(notebook, width=40000, height=400)
    frame3 = ttk.Frame(notebook, width=600, height=400)

    frame1.pack(fill='both', expand=True)
    frame2.pack(fill='both', expand=True)
    frame3.pack(fill='both', expand=True)

    notebook.add(frame1, text='Error Entry')
    notebook.add(frame2, text='Action Order')
    notebook.add(frame3, text='View Action Order')

    return root, frame1, frame2, frame3
def main():
    root, frame1, frame2, frame3 = create_gui()
    error_tab(frame1)
    Action_Order_Tab(frame2)
    Action_Order_Query_Tab(frame3)
    root.mainloop()

if __name__ == "__main__":
    main()