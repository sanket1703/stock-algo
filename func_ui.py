import tkinter as tk
from tkinter import messagebox
import time
import threading
import ast
from lambda_function import (buy_order, buy_order_validator, order_validator, pre_run_checklist,
    sell_order, sell_order_validator, sync_orders, trade_sync, validate_orders)
from jobs.exchange_tradeid_job import exchange_tradeid_job


def bg_order_validator():
    # The orders keep on get validated in the background
    while True:
        order_validator()
        time.sleep(1)

# Function to execute selected function


def execute_function(selected_func, input_list, progress_label):
    # Update progress label to show which function is in progress
    progress_label.config(text=f"Executing: {selected_func}")
    progress_label.update()

    # Notify that function has started
    messagebox.showinfo("Execution Started", f"Starting {selected_func}...")

    # Execute the function in a separate thread to avoid freezing the UI
    def run(input_list):  # Ensure input_list is passed to the thread
        try:
            if selected_func == "Buy Order":
                # Safely parse the input string to a list if not empty, otherwise use an empty list
                if input_list.strip():
                    # Parse input as a Python literal (list, etc.)
                    input_list = ast.literal_eval(input_list)
                else:
                    input_list = []  # Use an empty list if input is empty
                result = buy_order(input_list)
            elif selected_func == "Sell Order":
                # Safely parse the input string to a list if not empty, otherwise use an empty list
                if input_list.strip():
                    # Parse input as a Python literal (list, etc.)
                    input_list = ast.literal_eval(input_list)
                else:
                    input_list = []  # Use an empty list if input is empty
                result = sell_order(input_list)
            elif selected_func == "Pre-Run Checklist":
                result = pre_run_checklist()  # No input needed for function_2
            elif selected_func == "Order Validator":
                result = order_validator()
            elif selected_func == "Trade Sync":
                result = trade_sync()
            elif selected_func == "Exchange Trade Id Job":
                result = exchange_tradeid_job()
            
    
            # Update progress label and notify on completion
            progress_label.config(text=f"Completed: {selected_func}")
            messagebox.showinfo("Execution Completed", result)
        except (ValueError, SyntaxError) as e:
            progress_label.config(text="Error in execution")
            messagebox.showerror("Error", f"Invalid input: {str(e)}")

    # Pass input_list explicitly to the thread for function 1, or leave it empty for function 2
    threading.Thread(target=run, args=(input_list,)).start()


# Setup the main UI
root = tk.Tk()
root.title("Fortune Alpha 13")

# Dropdown for function selection
function_choices = ["Pre-Run Checklist", "Buy Order", "Sell Order", "Order Validator", "Trade Sync", "Exchange Trade Id Job"]
selected_func = tk.StringVar()
selected_func.set(function_choices[0])  # Default selection

dropdown = tk.OptionMenu(root, selected_func, *function_choices)
dropdown.pack(pady=20)

# Input field for list (only relevant for Function 1)
list_label = tk.Label(root, text="Enter a list (e.g., [\"IDEA.NS\",\"GTLINFRA.NS\"]):")
list_label.pack(pady=5)

list_entry = tk.Entry(root)
list_entry.pack(pady=10)

# Label to display progress
progress_label = tk.Label(root, text="No function running", font=("Arial", 12))
progress_label.pack(pady=20)

# Execute button
execute_button = tk.Button(root, text="Execute", command=lambda: execute_function(
    selected_func.get(), list_entry.get(), progress_label))
execute_button.pack(pady=20)

# Enable this if you want the order validator to be constantly running in the bg
threading.Thread(target=bg_order_validator, daemon=True).start()

# Start the UI
root.mainloop()
