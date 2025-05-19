import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk
import process # Assuming process.py exists and has ai_response_to_list
from sheetf import update_name # Assuming sheetf.py exists and has update_name
from auth import auth # Assuming auth.py exists
import random
from config import creds, spreadsheet_id, sheet_id # Assuming config.py exists with these variables

def show_gtk_key_prompt(message, trigger_event_time=None):
    dialog = Gtk.Dialog(
        title="Action Required",
        parent=None, # No parent window
        flags=0 # Default flags are fine; Gtk.DialogFlags.MODAL is implicitly handled by set_modal
    )
    dialog.set_default_size(300, 120) # Slightly increased height for comfort
    dialog.set_decorated(True)    # Show window decorations (title bar, close button)
    dialog.set_modal(True)        # Make the dialog modal (blocks other windows of this app)
    dialog.set_keep_above(True)   # Keep the dialog on top of other application windows
    dialog.set_position(Gtk.WindowPosition.CENTER_ALWAYS) # Center the dialog

    # Hint to GTK to try to give focus to this window when it's mapped (shown)
    dialog.set_focus_on_map(True)

    content_area = dialog.get_content_area()
    label = Gtk.Label(label=message)
    label.set_margin_top(10) # Add some margin for the label
    label.set_margin_bottom(10)
    label.set_margin_start(10)
    label.set_margin_end(10)
    content_area.pack_start(label, True, True, 0)

    key_pressed_result = None

    # Connect the key-press-event signal to the dialog
    def on_dialog_key_press(widget, event):
        nonlocal key_pressed_result
        key_pressed_result = Gdk.keyval_name(event.keyval)
        print(f"Key '{key_pressed_result}' pressed in dialog.")
        dialog.response(Gtk.ResponseType.OK) # Any response ID will close a dialog run with run()
        return True # Indicate that the event has been handled

    dialog.connect("key-press-event", on_dialog_key_press)

    # Show the dialog and all its children
    dialog.show_all()

    # Determine the event time to use for presenting the window
    # Using the actual event time helps the window manager make better focus decisions.
    current_event_time = trigger_event_time if trigger_event_time is not None else Gdk.CURRENT_TIME

    # Present the window to the user (raises it, possibly gives focus)
    dialog.present_with_time(current_event_time)

    # After present_with_time, check and explicitly grab focus if needed.
    # It's possible that present_with_time already succeeded.
    # is_active() checks if it's the active toplevel window.
    if not dialog.is_active() or not dialog.has_focus():
        # print("Dialog not active or no focus after present_with_time. Attempting grab_focus().")
        dialog.grab_focus()

    # For debugging focus issues:
    # if dialog.has_focus():
    #     print("Debug: Dialog has focus.")
    # else:
    #     print("Debug: Dialog FAILED to grab focus.")

    # Run the dialog's own loop, which blocks until dialog.response() is called
    dialog.run()

    # Destroy the dialog widget
    dialog.destroy()

    return key_pressed_result

def on_owner_change(clip, event): # 'event' here is Gdk.EventOwnerChange
    text = clip.wait_for_text()
    if text:
        stripped_text = text.strip()
        print("Selected ➜", stripped_text)
        to_update = process.ai_response_to_list(stripped_text) # Ensure this function exists
        print("to_update: " + str(to_update))

        # Authenticate regardless of whether we update
        # Ensure 'creds' is defined in your config.py or elsewhere
        sheet = auth(random.choice(creds))

        print("Waiting for user input via GTK pop-up (key press)...")
        # Pass the time from the owner-change event
        message_on_pop="Press 'c' to skip update, any other key to continue..."
        key_name = show_gtk_key_prompt(
            message_on_pop+"\n"+str(to_update),
            trigger_event_time=event.time # Pass the actual event time
        )
        print(f"Key pressed: '{key_name}'")

        if key_name is not None and key_name.lower() != 'c':
            print("User chose to update. Running update_name...")
            if to_update:
                 # Ensure spreadsheet_id and sheet_id are defined
                 update_name(sheet, spreadsheet_id, sheet_id, to_update)
                 print("update_name finished.")
            else:
                 print("No data to update.")
        else:
            print("User chose to skip update (pressed 'c' or closed dialog).")

# Get the primary selection clipboard
clip = Gtk.Clipboard.get(Gdk.SELECTION_PRIMARY)
# Connect the "owner-change" signal
# This fires whenever the owner of the primary selection changes (e.g., new text copied)
clip.connect("owner-change", on_owner_change)

# Start the GTK main loop
print("Clipboard listener started. Waiting for selection changes...")
Gtk.main()