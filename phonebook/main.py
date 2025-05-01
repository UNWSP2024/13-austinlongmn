# Programmer: Austin Long
# Date: 2025-05-01
# Program: Phonebook
from db import DBInterface, Entry
import tkinter
import tkinter.messagebox


class Phonebook:
    def __init__(self, phonebook: DBInterface) -> None:
        # Get database interface
        self.phonebook = phonebook

        # This will keep an in-memory representation of the current state of the entries.
        self.phonebook_list = self.phonebook.get_all_entries()

        self.main_window = tkinter.Tk()

        # Frame for the entries
        self.rows_frame = tkinter.Frame()

        # List box containing each entry
        self.list_box = tkinter.Listbox(selectmode=tkinter.SINGLE)

        # Populate list_box
        for entry in self.phonebook_list:
            self.list_box.insert(tkinter.END, str(entry))

        self.list_box.pack()

        # MARK: Operations
        self.operations_frame = tkinter.Frame()

        # Increment rows and columns
        operation_grid_col = 0
        operation_grid_row = 0

        # Create buttons for operations

        # Modifies selected entry to match input boxes
        self.modify_entry_button = tkinter.Button(
            self.operations_frame,
            text="Update selected entry",
            command=self.modify_entry,
        )
        self.modify_entry_button.grid(column=operation_grid_col, row=operation_grid_row)
        operation_grid_col += 1

        # Deletes the selected entry
        self.delete_entry_button = tkinter.Button(
            self.operations_frame,
            text="Delete selected entry",
            command=self.delete_entry,
        )
        self.delete_entry_button.grid(
            column=operation_grid_col, columnspan=2, row=operation_grid_row
        )
        operation_grid_col = 0
        operation_grid_row += 1

        # Creates a new entry with the contents of the input boxes
        self.new_entry_button = tkinter.Button(
            self.operations_frame, text="New Entry", command=self.create_entry
        )
        self.new_entry_button.grid(column=operation_grid_col, row=operation_grid_row)
        operation_grid_col += 1

        # Commits changes to the database
        self.save_button = tkinter.Button(
            self.operations_frame,
            text="Save",
            command=self.save,
            state=tkinter.DISABLED,
        )
        self.save_button.grid(column=operation_grid_col, row=operation_grid_row)
        operation_grid_col += 1

        # Rolls back the changes
        self.rollback_button = tkinter.Button(
            self.operations_frame,
            text="Revert",
            command=self.revert,
            state=tkinter.DISABLED,
        )
        self.rollback_button.grid(column=operation_grid_col, row=operation_grid_row)

        # MARK: Input
        self.input_frame = tkinter.Frame()

        input_grid_row = 0

        # Name entry box
        name_label = tkinter.Label(self.input_frame, text="Name:")
        name_label.grid(row=input_grid_row, column=0)
        self.name_entry = tkinter.Entry(self.input_frame)
        self.name_entry.grid(row=input_grid_row, column=1)
        input_grid_row += 1

        # Phone number entry box
        phone_number_label = tkinter.Label(self.input_frame, text="Phone number:")
        phone_number_label.grid(row=input_grid_row, column=0)
        self.phone_number_entry = tkinter.Entry(self.input_frame)
        self.phone_number_entry.grid(row=input_grid_row, column=1)
        input_grid_row += 1

        self.rows_frame.pack()
        self.operations_frame.pack()
        self.input_frame.pack()

        # Start
        self.main_window.minsize(16 * 30, 9 * 30)
        self.main_window.title("Phonebook")

        tkinter.mainloop()

    def refresh(self):
        """Reloads items from the database"""
        self.list_box.delete(0, tkinter.END)
        self.phonebook_list = self.phonebook.get_all_entries()
        for entry in self.phonebook_list:
            self.list_box.insert(tkinter.END, str(entry))

    def get_selected_idx(self) -> int | None:
        """Gets the selected index from the list_box.
        Returns None if none are selected.
        This function displays a dialouge box if there are none selected."""
        indicies = self.list_box.curselection()
        if len(indicies) < 1:
            tkinter.messagebox.showerror(
                title="Error", message="You must select an entry to use this operation."
            )
            return None
        return indicies[0]

    def insert_entry(self, new_entry: Entry):
        """Inserts an entry into phonebook_list and list_box. Sorts items automatically."""
        self.phonebook_list.append(new_entry)
        self.phonebook_list.sort(key=lambda e: e.get_name())

        idx = 0

        for entry in self.phonebook_list:
            if entry.get_id() == new_entry.get_id():
                break
            idx += 1

        self.list_box.insert(idx, str(new_entry))
        self.list_box.activate(idx)

    def reset_textboxes(self):
        """Resets the input boxes to empty strings."""
        self.name_entry.delete(0, tkinter.END)
        self.phone_number_entry.delete(0, tkinter.END)

    def set_changes(self, value: bool):
        """Disables appropriate buttons based on whether there are changes."""
        state = tkinter.NORMAL if value else tkinter.DISABLED

        self.save_button.configure(state=state)
        self.rollback_button.configure(state=state)

    def delete_entry(self):
        """Deletes an entry from the list_box and database"""
        index = self.get_selected_idx()
        if index == None:
            return

        entry = self.phonebook_list[index]

        if not entry:
            return

        self.phonebook.delete_entry(entry)

        del self.phonebook_list[index]
        self.list_box.delete(index)
        self.set_changes(True)

    def create_entry(self):
        """Creates an entry and adds it to list_box"""
        new_entry = self.phonebook.create_entry(
            self.name_entry.get(), self.phone_number_entry.get()
        )
        self.insert_entry(new_entry)
        self.set_changes(True)
        self.reset_textboxes()

    def modify_entry(self):
        """Modifies an entry and resorts"""
        index = self.get_selected_idx()

        if index == None:
            return

        entry = self.phonebook_list[index]

        name_input = self.name_entry.get()
        if name_input:
            entry.set_name(name_input)

        phone_number_input = self.phone_number_entry.get()
        if phone_number_input:
            entry.set_phone_number(phone_number_input)

        self.phonebook.update_entry(entry)

        self.list_box.delete(index)
        self.insert_entry(entry)
        self.set_changes(True)
        self.reset_textboxes()

    def save(self):
        """Commits to database and updates buttons"""
        self.phonebook.commit()
        self.refresh()
        self.set_changes(False)

    def revert(self):
        """Rolls back the database and updates buttons"""
        self.phonebook.rollback()
        self.refresh()
        self.set_changes(False)


if __name__ == "__main__":
    with DBInterface("phonebook.db") as phonebook:
        Phonebook(phonebook)
