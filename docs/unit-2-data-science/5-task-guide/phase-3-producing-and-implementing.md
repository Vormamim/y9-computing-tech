# Phase 3: Producing and Implementing

!!! warning "Headings"

    Remember to add headings as needed for each of the following.


As with before, we'll look at what it specifically in the task, then visit certain areas on a separate page which need further explanation.

??? note "Python, Pandas, Matplotlib"

    Use Python Pandas to read and manipulate data. Create relevant charts and visualisations using Matplotlib. This can first be done in your `main.py` **file,** however, eventually you want to **add this to the** `data_module.py` **file** as functions, which are then imported into your `main.py` file.


??? note "User Interface"

    How does the user find and generate the data to assess your findings? In a separate Python program, create an intuitive text-based or graphical user interface (GUI) which allows for an accessible User Experience (UX). Call the program `main.py`for the user interface, then move any functions to another file to import (e.g. `data_module.py`).

    **Note:** When not using Jupyter Notebook, if you need to output a dataframe you need to remember to use the print function, for example: `print(big_mac_df)`.


??? note "Example UI and Module"

    ## main.py

    ```python title="main.py"
    from data_module import (
        display_dataset_preview,
        display_visualisation,
        search_data,
        update_data_entry,
        save_changes
    )

    def main_menu():
        while True:
            print("\n=== Data Viewer Interface ===")
            print("1. View dataset")
            print("2. View visualisation")
            print("3. Search or filter data")
            print("4. Update a data entry")
            print("5. Save changes")
            print("6. Exit")

            choice = input("Select an option (1-6): ").strip()

            if choice == '1':
                display_dataset_preview()
            elif choice == '2':
                display_visualisation()
            elif choice == '3':
                search_data()
            elif choice == '4':
                update_data_entry()
            elif choice == '5':
                save_changes()
                print("Changes saved.")
            elif choice == '6':
                print("Exiting program.")
                break
            else:
                print("Invalid selection. Please choose a number between 1 and 6.")

    if __name__ == "__main__":
        main_menu()
    ```

    ## data\_module.py

    ```python title="data_module.py"
    # data_module.py
    import pandas as pd

    def display_dataset_preview():
        # Use pandas here
        pass

    def update_data_entry():
        # Use pandas here
        pass

    # etc...
    ```

    The above is **just an example.** It is up to you to create your `main.py` UI and your `data_module.py` functions.

    ### Why if \_\_name\_\_ == "\_\_main\_\_":

    When Python runs a file, it sets a special built-in variable called `__name__`.

    * If the file is being **run directly** (e.g., `python main.py`), then `__name__` is set to `"__main__"`.
    * If the file is being **imported as a module** (e.g., `import main`), then `__name__` is set to `"main"` (the file name, without `.py`).
