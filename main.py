import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk
import process
from sheetf import *
from auth import auth
import random
from config import *
def on_owner_change(clip, event):
    text = clip.wait_for_text()
    if text:
        print("Selected ➜", text.strip())
        to_update = process.ai_response_to_list(text.strip())
        print("to_update" + str(to_update))
        # Authenticate regardless of whether we update
        sheet = auth(random.choice(creds))
        
        # Prompt user for input before deciding to update
        # WARNING: Using input() blocks the Gtk main loop.
        # In a proper Gtk application, a dialog should be used instead.
        # Assuming console interaction is acceptable for this script based on context.
        user_input = input("Selection received. Press 'c' to skip updating this selection, any other key to update: ")

        # Check user input. Skip update if 'c' is pressed (case-insensitive check).
        if user_input.lower() != 'c':
            print("User chose to update. Running update_name...")
            # Call the update function
            update_name(sheet, spreadsheet_id, sheet_id, to_update)
            print("update_name finished.")
        else:
            # User chose to skip
            print("User chose to skip update.")
clip = Gtk.Clipboard.get(Gdk.SELECTION_PRIMARY)
clip.connect("owner-change", on_owner_change)   # fires whenever selection changes
Gtk.main()
