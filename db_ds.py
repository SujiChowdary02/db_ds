'''import tkinter as tk
import mysql.connector
from tkinter import filedialog
import time
import csv

# Function to save data from CSV file to the database
def save_csv_to_db():
    file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
    if file_path:
        try:
            with open(file_path, 'r') as file:
                csv_reader = csv.reader(file)
                next(csv_reader)  # Skip header if present
                for row in csv_reader:
                    cursor.execute("INSERT INTO datasets (name, data) VALUES (%s, %s)", (row[0], row[1]))
                db.commit()
                status_label.config(text="Data from CSV file saved successfully!")
                refresh_data()  # Update displayed data after saving
        except (mysql.connector.Error, csv.Error) as err:
            status_label.config(text=f"Error saving data from CSV file: {err}")
    else:
        status_label.config(text="Please select a CSV file.")


# Function to save data to the database
def save_to_db():
    name = entry_name.get()
    data = entry_data.get()
    if name and data:
        try:
            cursor.execute("INSERT INTO datasets (name, data) VALUES (%s, %s)", (name, data))
            db.commit()
            status_label.config(text="Data saved successfully!")
            refresh_data()  # Update displayed data after saving
        except mysql.connector.Error as err:
            status_label.config(text=f"Error saving data: {err}")
    else:
        status_label.config(text="Please enter both name and data.")

# Function to retrieve all datasets from the database
def retrieve_all():
    try:
        cursor.execute("SELECT * FROM datasets")
        results = cursor.fetchall()
        display_results(results)
    except mysql.connector.Error as err:
        status_label.config(text=f"Error retrieving data: {err}")

# Function to search and retrieve specific dataset from the database
def search_dataset():
    search_term = entry_search.get()
    if search_term:
        try:
            cursor.execute("SELECT * FROM datasets WHERE name LIKE %s", (f'%{search_term}%',))
            results = cursor.fetchall()
            display_results(results)
        except mysql.connector.Error as err:
            status_label.config(text=f"Error searching data: {err}")
    else:
        status_label.config(text="Please enter a search term.")

# Function to display results in the text widget
def display_results(results):
    if results:
        result_text = "ID\tName\tData\n"
        for row in results:
            result_text += f"{row[0]}\t{row[1]}\t{row[2]}\n"
        display_text.delete(1.0, tk.END)
        display_text.insert(tk.END, result_text)
    else:
        display_text.delete(1.0, tk.END)
        display_text.insert(tk.END, "No datasets found.")

# Function to refresh displayed data
def refresh_data():
    retrieve_all()

# Connect to MySQL
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="dsdatabase"
)

# Create a cursor
cursor = db.cursor()

# GUI Setup
root = tk.Tk()
root.title("Dataset Management")

label_name = tk.Label(root, text="Name:")
label_name.pack()

entry_name = tk.Entry(root)
entry_name.pack()

label_data = tk.Label(root, text="Data:")
label_data.pack()

entry_data = tk.Entry(root)
entry_data.pack()

save_button = tk.Button(root, text="Save", command=save_to_db)
save_button.pack()

status_label = tk.Label(root, text="")
status_label.pack()

retrieve_all_button = tk.Button(root, text="Retrieve All", command=retrieve_all)
retrieve_all_button.pack()

search_label = tk.Label(root, text="Search by Name:")
search_label.pack()

entry_search = tk.Entry(root)
entry_search.pack()

search_button = tk.Button(root, text="Search", command=search_dataset)
search_button.pack()

display_text = tk.Text(root, height=10, width=40)
display_text.pack()

refresh_button = tk.Button(root, text="Refresh", command=refresh_data)
refresh_button.pack()

upload_button = tk.Button(root, text="Upload CSV", command=save_csv_to_db)
upload_button.pack()


root.mainloop()

# Close the cursor and database connection when the application closes
cursor.close()
db.close()
'''

import tkinter as tk
from tkinter import filedialog
import mysql.connector


# Function to retrieve and display a specific dataset from the database based on search
def search_and_display_dataset():
    search_term = dataset_search.get()
    try:
        # Establish connection to MySQL
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="dsdatabase"
        )

        cursor = connection.cursor()

        # Retrieve the specified dataset from MySQL based on search
        select_query = "SELECT name, data FROM datasets WHERE name LIKE %s"
        cursor.execute(select_query, (f'%{search_term}%',))

        datasets = cursor.fetchall()

        connection.close()

        if datasets:
            dataset_listbox.delete(0, tk.END)
            for dataset in datasets:
                dataset_listbox.insert(tk.END, dataset[0])
        else:
            status_label.config(text="Dataset not found!")

    except Exception as e:
        status_label.config(text=f"Error: {str(e)}")


# Function to download a dataset when searched by the user
def download_searched_dataset():
    selected_dataset = dataset_listbox.get(tk.ACTIVE)
    try:
        # Establish connection to MySQL
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="dsdatabase"
        )

        cursor = connection.cursor()

        # Retrieve the selected dataset from MySQL
        select_query = "SELECT data FROM datasets WHERE name = %s"
        cursor.execute(select_query, (selected_dataset,))

        dataset_content = cursor.fetchone()

        connection.close()

        if dataset_content:
            file_path = filedialog.asksaveasfilename(defaultextension=".csv", initialfile=selected_dataset)
            if file_path:
                with open(file_path, 'w') as file:
                    file.write(dataset_content[0])
                status_label.config(text=f"Dataset '{selected_dataset}' downloaded successfully!")
        else:
            status_label.config(text="Dataset not found!")

    except Exception as e:
        status_label.config(text=f"Error: {str(e)}")

# Function to save dataset to MySQL database
def save_to_database():
    name = dataset_name.get()
    file_path = file_path_var.get()
    
    try:
        with open(file_path, 'r') as file:
            dataset_content = file.read()
            
            # Establish connection to MySQL
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="root",
                database="dsdatabase"
            )
            
            cursor = connection.cursor()
            
            # Save dataset name and content to MySQL
            insert_query = "INSERT INTO datasets (name, data) VALUES (%s, %s)"
            cursor.execute(insert_query, (name, dataset_content))
            
            connection.commit()
            connection.close()
            
            status_label.config(text="Dataset saved to database!")
            
    except Exception as e:
        status_label.config(text=f"Error: {str(e)}")


# Function to retrieve all datasets from the database
def retrieve_all_datasets():
    try:
        # Establish connection to MySQL
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="dsdatabase"
        )
        
        cursor = connection.cursor()
        
        # Retrieve all datasets from MySQL
        select_query = "SELECT name FROM datasets"
        cursor.execute(select_query)
        
        datasets = cursor.fetchall()
        
        # Display retrieved datasets in a listbox
        dataset_listbox.delete(0, tk.END)
        for dataset in datasets:
            dataset_listbox.insert(tk.END, dataset[0])
        
        connection.close()
        
    except Exception as e:
        status_label.config(text=f"Error: {str(e)}")


# Function to retrieve a specific dataset from the database
def retrieve_selected_dataset():
    selected_dataset = dataset_listbox.get(tk.ACTIVE)
    
    try:
        # Establish connection to MySQL
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="dsdatabase"
        )
        
        cursor = connection.cursor()
        
        # Retrieve the selected dataset from MySQL
        select_query = "SELECT content FROM datasets WHERE name = %s"
        cursor.execute(select_query, (selected_dataset,))
        
        dataset_content = cursor.fetchone()
        
        connection.close()
        
        if dataset_content:
            retrieved_content.delete(1.0, tk.END)
            retrieved_content.insert(tk.END, dataset_content[0])
        else:
            status_label.config(text="Dataset not found!")
        
    except Exception as e:
        status_label.config(text=f"Error: {str(e)}")


# GUI setup
root = tk.Tk()
root.title("Dataset Management")

dataset_name_label = tk.Label(root, text="Dataset Name:")
dataset_name_label.pack()

dataset_name = tk.Entry(root)
dataset_name.pack()

file_path_var = tk.StringVar()

def choose_file():
    file_path = filedialog.askopenfilename()
    file_path_var.set(file_path)

choose_file_button = tk.Button(root, text="Choose CSV File", command=choose_file)
choose_file_button.pack()

save_button = tk.Button(root, text="Save to Database", command=save_to_database)
save_button.pack()

retrieve_all_button = tk.Button(root, text="Retrieve All Datasets", command=retrieve_all_datasets)
retrieve_all_button.pack()

dataset_listbox = tk.Listbox(root)
dataset_listbox.pack()

retrieve_selected_button = tk.Button(root, text="Retrieve Selected Dataset", command=retrieve_selected_dataset)
retrieve_selected_button.pack()

retrieved_content_label = tk.Label(root, text="Retrieved Dataset Content:")
retrieved_content_label.pack()

retrieved_content = tk.Text(root, height=10, width=50)
retrieved_content.pack()

status_label = tk.Label(root, text="")
status_label.pack()

search_label = tk.Label(root, text="Search by Name:")
search_label.pack()

dataset_search = tk.Entry(root)
dataset_search.pack()

search_button = tk.Button(root, text="Search", command=search_and_display_dataset)
search_button.pack()

# Download button for the searched dataset
download_searched_button = tk.Button(root, text="Download Searched Dataset", command=download_searched_dataset)
download_searched_button.pack()

root.mainloop()







