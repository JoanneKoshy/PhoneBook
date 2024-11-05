import streamlit as st
import sqlite3

class ContactNode:
    def __init__(self, name, number):
        self.name = name
        self.number = number
        self.next = None  

class PhoneBookLinkedList:
    def __init__(self):
        self.head = None 
        self.create_table()
        self.load_contacts_from_db()  

    def create_table(self):
        conn = sqlite3.connect("phone_book.db")
        try:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS contacts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    number TEXT NOT NULL
                )
            """)
            conn.commit()
        except Exception as e:
            st.error(f"Error creating table: {e}")
        finally:
            conn.close()

    def add_contact(self, name, number):
    
        conn = sqlite3.connect("phone_book.db")
        try:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO contacts (name, number) VALUES (?, ?)", (name, number))
            conn.commit()
            st.success(f"Contact '{name}' added to the database successfully.")
            
            new_contact = ContactNode(name, number)
            if not self.head:
                self.head = new_contact
            else:
                current = self.head
                while current.next:
                    current = current.next
                current.next = new_contact
        except Exception as e:
            st.error(f"Error adding contact: {e}")
        finally:
            conn.close()

    def load_contacts_from_db(self):

        conn = sqlite3.connect("phone_book.db")
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT name, number FROM contacts")
            rows = cursor.fetchall()
            for name, number in rows:
                new_contact = ContactNode(name, number)
                if not self.head:
                    self.head = new_contact
                else:
                    current = self.head
                    while current.next:
                        current = current.next
                    current.next = new_contact
        except Exception as e:
            st.error(f"Error loading contacts: {e}")
        finally:
            conn.close()

    def search_contact(self, name):

        current = self.head
        while current:
            if current.name == name:
                return current.number
            current = current.next
        return None 

    def display_contacts(self):
        contacts = []
        current = self.head
        while current:
            contacts.append((current.name, current.number))
            current = current.next
        return contacts

    def delete_contact(self, name):

        conn = sqlite3.connect("phone_book.db")
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM contacts WHERE name = ?", (name,))
            conn.commit()
            if cursor.rowcount == 0:
                st.error(f"Contact '{name}' not found in the database.")
                return False
            st.success(f"Contact '{name}' deleted from the database successfully.")
            

            current = self.head
            previous = None
            while current:
                if current.name == name:
                    if previous:
                        previous.next = current.next
                    else:
                        self.head = current.next
                    return True
                previous = current
                current = current.next
            return False
        except Exception as e:
            st.error(f"Error deleting contact: {e}")
            return False
        finally:
            conn.close()

st.title("Phone Book Management System")
phone_book = PhoneBookLinkedList()

tab1, tab2, tab3, tab4 = st.tabs(["Add Contact", "Display Contacts", "Search Contact", "Delete Contact"])

with tab1:
    st.subheader("Add a New Contact")
    name = st.text_input("Enter contact name", key="add_name")
    number = st.text_input("Enter contact number", key="add_number")
    
    if st.button("Add Contact"):
        if name and number:
            phone_book.add_contact(name, number)
        else:
            st.warning("Please enter both name and number.")

with tab2:
    st.subheader("Display All Contacts")
    contacts = phone_book.display_contacts()
    
    if not contacts:
        st.write("Phone book is empty.")
    else:
        for name, number in contacts:
            st.write(f"- **Name**: {name}, **Number**: {number}")

with tab3:
    st.subheader("Search for a Contact")
    search_name = st.text_input("Enter name to search", key="search_name")
    
    if st.button("Search"):
        if search_name:
            number = phone_book.search_contact(search_name)
            if number:
                st.success(f"Contact found - **Name**: {search_name}, **Number**: {number}")
            else:
                st.error(f"Contact '{search_name}' not found in the phone book.")
        else:
            st.warning("Please enter a name to search.")

with tab4:
    st.subheader("Delete a Contact")
    delete_name = st.text_input("Enter name to delete", key="delete_name")
    
    if st.button("Delete Contact"):
        if delete_name:
            success = phone_book.delete_contact(delete_name)
            if success:
                st.success(f"Contact '{delete_name}' deleted successfully.")
            else:
                st.error(f"Contact '{delete_name}' not found in the phone book.")
        else:
            st.warning("Please enter a name to delete.")
