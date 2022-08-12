
# Base structure and comments provided by Professor Mark Baldwin for ICS 32 Class
# Modified by Ragib Sakib to fit the purpose of the ds_messenger

import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
import ds_messenger
from ds_messenger import DirectMessenger, DirectMessage, DirectMessengerError


class Body(tk.Frame):
    """
    A subclass of tk.Frame that is responsible for drawing all of the widgets
    in the body portion of the root frame.
    """
    def __init__(self, root, select_all_callback=None, select_new_callback=None, info_callback=None):
        tk.Frame.__init__(self, root)
        self.root = root
        self._select_all_callback = select_all_callback
        self._select_new_callback = select_new_callback
        self._info_callback = info_callback

        # A list of the DirectMessage objects available in the current user
        self._messages = []
        # A list of the users that have sent messages to the current user
        self._users = []
        # A dictionary of users assigned to their list of messages
        self._user_dict = {}
        # A variable to hold the currently selected user
        self.selected_user = None
        
        # After all initialization is complete, call the _draw method to pack the widgets
        # into the Body instance 
        self._draw()
    
    def node_select(self, event):
        """
        Update the entry_editor with the full post entry when the corresponding node in the user_tree
        is selected.
        """
        # Credit to @ChumiestBucket for this canvas wipe code
        # Weblink: https://stackoverflow.com/questions/51856163/how-can-i-clear-or-overwrite-a-tkinter-canvas
        self.viewer.delete('all')
        self.y = 10
        #selections are not 0-based, so subtract one.
        index = int(self.user_tree.selection()[0])
        if len(self._users) == 1:
            index += 1
        self.selected_user = self._users[index]
        self._update_message_view(self._user_dict[self.selected_user])
    
    def get_text_entry(self) -> str:
        """
        Returns the text that is currently displayed in the entry_editor widget.
        """
        return self.entry_editor.get('1.0', 'end').rstrip()

    def set_text_entry(self, text:str):
        """
        Sets the text to be displayed in the entry_editor widget.
        NOTE: This method is useful for clearing the widget, just pass an empty string.
        """
        #This deletes all current text in the self.entry_editor widget
        self.entry_editor.delete('1.0', 'end')
        #and this inserts the value contained within the text parameter.
        self.entry_editor.insert('1.0', text)

    def set_all_messages_and_users(self):
        """
        Populates all users in the treeview and assigns every message to its user
        """
        # These messages are from oldest to newest
        self._messages = self._select_all_callback()
        self._insert_users(self._messages)
        self._assign_messages()

    def set_new_messages_and_users(self):
        """
        Populates new users in the treeview and assigns every message to its user, is called when refresh button is clicked
        """
        try:
            server, username = self._info_callback()
            assert username != None and server != None, "Can't refresh without logging in first"
            self._users = []
            self.selected_user = None
            # Clear the user tree
            for item in self.user_tree.get_children():
                self.user_tree.delete(item)
            # Credit to @ChumiestBucket for this canvas wipe code
            # Weblink: https://stackoverflow.com/questions/51856163/how-can-i-clear-or-overwrite-a-tkinter-canvas
            self.viewer.delete('all')
            self.y = 10
            
            # These messages are from oldest to newest
            messages = self._select_new_callback()
            for message in messages:
                self._messages.append(message)
            self._insert_users(messages)
            self._assign_messages()
        except AssertionError as e:
            tk.messagebox.showinfo(title='Error', message=e)
            return

    def _assign_messages(self):
        """
        Assigns messages to their user in _user_dict
        """
        # Assign users as dict keys to empty lists
        for user in self._users:
            if user not in self._user_dict.keys():
                self._user_dict[user] = []

        for message in self._messages:
            if message not in self._user_dict[message.recipient]:
                self._user_dict[message.recipient].append(message)

    def _update_message_view(self, messages:list):
        """
        Takes a list of messages and populates the message view with them
        """
        # Credit to @Mat.C for this method of updating text on a canvas widget
        # Weblink: https://stackoverflow.com/questions/55675124/how-to-make-a-scrollbar-for-a-label-list-python-tkinter
        for message in messages:
            self.viewer.create_text(5, self.y, text=message.message, font="Arial 12", anchor=tk.NW)
            self.y+=20

    def insert_user(self):
        """
        Takes a list of messages and inserts a list of users to the post_tree widget.
        """
        try:
            user = tk.simpledialog.askstring(title="Recipient", prompt="Who do you want to send a message to?")
            assert user != None
            assert user not in self._users
            
            # Insert the username to the 0 index of the user list
            self._users.insert(0, user)

            # Assign it an empty list
            self._assign_messages()
            if len(self._users) > 2:
                # Insert user into the posttree as negative so that it appears on top
                self._insert_user_tree(-len(self._users), user)
            else:
                self._insert_user_tree(-2, user)
        except AssertionError:
            return
        
    def _insert_users(self, message_list):
        """
        Takes a list of messages and inserts a list of users to the post_tree widget.
        """
        # Make the class list of users filled with unique ID's
        for message in self._messages:
            if message.recipient in self._users:
                self._users.remove(message.recipient)
            self._users.append(message.recipient)

        # Insert every user into the posttree at a negative index
        for index, user in enumerate(self._users):
            self._insert_user_tree(index-len(self._users), user)

    def reset_ui(self):
        """
        Resets all UI widgets to their default state. Useful for when clearing the UI is neccessary such
        as when a new DSU file is loaded, for example.
        """
        # Set all class variables to empty or None
        self.set_text_entry("")
        self._messages = []
        self._users = []
        self._user_dict = {}
        self.selected_user = None
        # Clear the user tree
        for item in self.user_tree.get_children():
            self.user_tree.delete(item)
        # Credit to @ChumiestBucket for this canvas wipe code
        # Weblink: https://stackoverflow.com/questions/51856163/how-can-i-clear-or-overwrite-a-tkinter-canvas
        self.viewer.delete('all')
        self.y = 10

    def _insert_user_tree(self, id, user):
        """
        Inserts a post entry into the user_tree widget.
        """
        if user != self.user_tree:
            # If username too long, then shorten it
            if len(user) > 25:
                user = user[:24] + "..."
            
            self.user_tree.insert('', id, id, text=user)
    
    def _draw(self):
        """
        Call only once upon initialization to add widgets to the frame
        """
        # Draw the left side of the gui
        user_frame = tk.Frame(master=self, width=250, bg="lightblue")
        user_frame.pack(fill=tk.BOTH, side=tk.LEFT)
        # Fill it with a Treeview and bind the treeview to the node select function
        self.user_tree = ttk.Treeview(user_frame, show='tree')
        self.user_tree.bind("<<TreeviewSelect>>", self.node_select)
        self.user_tree.pack(fill=tk.BOTH, side=tk.TOP, expand=True, padx=5, pady=5)

        # Draw the right side of the gui
        entry_frame = tk.Frame(master=self, bg="")
        entry_frame.pack(fill=tk.BOTH, side=tk.TOP, expand=True)

        # Split the right side into two boxes
        message_viewer_frame = tk.Frame(master=entry_frame, bg="lightblue")
        message_viewer_frame.pack(fill=tk.BOTH, side=tk.TOP, expand=True)
        entry_editor_frame = tk.Frame(master=entry_frame, bg="lightblue", height=100)
        entry_editor_frame.pack(fill=tk.BOTH, side=tk.BOTTOM, expand=False)

        # Make a frame for the message viewer and its scroll bar
        viewer_frame = tk.Frame(master=message_viewer_frame, bg="red")
        viewer_frame.pack(fill=tk.BOTH, side=tk.TOP, expand=True, padx=5, pady=5)
        scroll_frame = tk.Frame(master=viewer_frame, bg="blue", width=10)
        scroll_frame.pack(fill=tk.BOTH, side=tk.RIGHT, expand=False)
        # Make a frame for the entry editor
        editor_frame = tk.Frame(master=entry_editor_frame, bg="yellow", height=10)
        editor_frame.pack(fill=tk.BOTH, side=tk.BOTTOM, expand=False, padx=5, pady=5)

        # Fill the message viewer frame with a Canvas widget
        # Credit to @Gary02127 and @Shish on StackOverflow for providing an example of how to make a scrollbar for a Canvas widget
        # Weblink: https://stackoverflow.com/questions/7727804/tkinter-using-scrollbars-on-a-canvas
        self.viewer = tk.Canvas(viewer_frame, scrollregion=(0,0,0,0), bg="white")
        self.viewer.pack(fill=tk.BOTH, side=tk.LEFT, expand=True, padx=0, pady=0)
        # Create a Y variable to hold the current spot for text to appear
        # Credit to @Mat.C for this method of updating text on a canvas widget
        # Weblink: https://stackoverflow.com/questions/55675124/how-to-make-a-scrollbar-for-a-label-list-python-tkinter
        self.y = 10
        
        # Fill the scrollbar frame with a Scrollbar widget and link it to the message viewer
        viewer_scrollbar = tk.Scrollbar(master=scroll_frame, command=self.viewer.yview, bg="darkblue")
        self.viewer.config(yscrollcommand=viewer_scrollbar.set)
        viewer_scrollbar.pack(fill=tk.Y, side=tk.LEFT, expand=False, padx=0, pady=0)

        # Fill the Entry Editor frame with a Text widget
        self.entry_editor = tk.Text(master=editor_frame, height=2)
        self.entry_editor.pack(fill=tk.X)


class Footer(tk.Frame):
    """
    A subclass of tk.Frame that is responsible for drawing all of the widgets
    in the footer portion of the root frame.
    """
    def __init__(self, root, messenger_callback=None, send_callback=None, add_callback=None, refresh_callback=None):
        tk.Frame.__init__(self, root)
        self.root = root
        self._messenger_callback = messenger_callback
        self._send_callback = send_callback
        self._add_callback = add_callback
        self._refresh_callback = refresh_callback
        
        # After all initialization is complete, call the _draw method to pack the widgets
        # into the Footer instance 
        self._draw()
    
    def add_click(self):
        """
        Calls the callback function specified in the online_callback class attribute, if
        available, when the add_u_button has been clicked.
        """
        self._add_callback()

    def send_click(self):
        """
        Calls the callback function specified in the send_callback class attribute, if
        available, when the send_button has been clicked.
        """
        self._send_callback()

    def refresh_click(self):
        """
        Calls the callback function specified in the refresh_callback class attribute, if
        available, when the send_button has been clicked and refreshes message status
        """
        self.sent_label.configure(bg="lightpink", text="No new message has been made")
        self._refresh_callback()

    def sent_status(self, sent_bool:bool):
        if sent_bool == True:
            self.sent_label.configure(bg="lightblue", text="Message has been sent")
        else:
            self.sent_label.configure(bg="pink", text="Message has not been sent")

    def update_status(self):
        """
        Updates the text that is displayed in the username and server label widgets
        """
        server, username = self._messenger_callback()
        self.server_label.configure(text="Current Server: {}".format(server))
        self.user_label.configure(text="Current User: {}".format(username))
    
    def _draw(self):
        """
        Call only once upon initialization to add widgets to the frame
        """
        # Draw the send button
        send_button = tk.Button(master=self, text="Send", width=15, bg="lightpink")
        send_button.configure(command=self.send_click)
        send_button.pack(fill=tk.BOTH, side=tk.RIGHT, padx=5, pady=5)

        # Draw the add user button
        add_u_button = tk.Button(master=self, text="Add User", width=25, bg="lightpink")
        add_u_button.configure(command=self.add_click)
        add_u_button.pack(fill=tk.BOTH, side=tk.LEFT, padx=15, pady=10)

        # Draw the refresh user button
        add_u_button = tk.Button(master=self, text="Refresh", width=15, bg="lightpink")
        add_u_button.configure(command=self.refresh_click)
        add_u_button.pack(fill=tk.BOTH, side=tk.RIGHT, padx=5, pady=5)

        # Add labels for current username and server address and if a message sent
        self.user_label = tk.Label(master=self, text="Current User: {}".format(None), bg="lightblue")
        self.user_label.pack(fill=tk.BOTH, side=tk.BOTTOM, padx=5, pady=5)
        self.server_label = tk.Label(master=self, text="Current Server: {}".format(None), bg="lightblue")
        self.server_label.pack(fill=tk.BOTH, side=tk.BOTTOM, padx=5, pady=0)
        self.sent_label = tk.Label(master=self, text="No Messages sent".format(None), bg="lightpink")
        self.sent_label.pack(fill=tk.BOTH, side=tk.BOTTOM, padx=5, pady=5)

class MainApp(tk.Frame):
    """
    A subclass of tk.Frame that is responsible for drawing all of the widgets
    in the main portion of the root frame. Also manages all method calls for
    the NaClProfile class.
    """
    def __init__(self, root):
        tk.Frame.__init__(self, root)
        self.root = root

        # Initialize a new NaClProfile and assign it to a class attribute.
        self._current_messenger = DirectMessenger()

        # After all initialization is complete, call the _draw method to pack the widgets
        # into the root frame
        self._draw()

    def _get_current_info(self):
        """
        Returns the current server and Username
        """
        return self._current_messenger.dsuserver, self._current_messenger.username

    def _retrieve_new_messages(self) -> list:
        """
        Retrieves a list of only new DirectMessage objects from the server and returns it
        """
        return self._current_messenger.retrieve_new()

    def _retrieve_all_messages(self) -> list:
        """
        Retrieves a list of all DirectMessage objects from the server and returns it
        """
        return self._current_messenger.retrieve_all()

    def new_login(self):
        """
        Sends a login request to the server that will either
        log into a current user or make a new user
        """
        try:
            # Give prompts to fill in information for new .dsu file
            # Credit: I got the idea of using prompts from Luis E Morales in ICS 32
            username = tk.simpledialog.askstring(parent=self.root, title="Profile Details", prompt="Enter Username")
            assert username != None
            password = tk.simpledialog.askstring(title="Profile Details", prompt="Enter Password", initialvalue="password")
            assert password != None
            # Credit to @Da_Pz on StackOverflow for the initialvalue option, which is not written anywhere else
            server = tk.simpledialog.askstring(title="Profile Details", prompt="Enter Server", initialvalue="168.235.86.101")
            assert server != None

            # Set the class messenger as a DirectMessenger object with the previous information
            self._current_messenger = DirectMessenger(server, username, password)

            # Raise an error if something went wrong
            if self._current_messenger.error != None:
                raise DirectMessengerError

            # Reset the UI
            self.body.reset_ui()
            
            # Update the footer status
            self.footer.update_status()

            # Update the post tree in body
            self.body.set_all_messages_and_users()

        except DirectMessengerError:
            tk.messagebox.showinfo(title='Error', message=self._current_messenger.error)
        except AssertionError:
            return

    def send_message(self):
        """
        Sends Message in the textbox to the selected user
        """
        try:
            # Make sure that the user can connect to the server
            assert self._current_messenger.error == None, "Please properly connect to the server or login first"
            # Make sure that the user has selected a recipient
            assert self.body.selected_user != None, "Please select a user to send a message to"
            
            # Define the message and recipient
            message = self.body.get_text_entry()
            recipient = self.body.selected_user

            # Reset the text entry box
            self.body.set_text_entry("")

            # Send it with the class's messenger attributes
            sent = self._current_messenger.send(message, recipient)

            # Update the sent status accordingly
            self.footer.sent_status(sent)
            
            # If it returns false then raise an error
            if sent == False:
                raise DirectMessengerError
        except DirectMessengerError:
            tk.messagebox.showinfo(title='Error', message="Something went wrong sending your file")
            return
        except AssertionError as e:
            tk.messagebox.showinfo(title='Error', message=e)
            return
        
    
    def close(self):
        """
        Closes the program when the 'Close' menu item is clicked
        """
        self.root.destroy()
    
    def _draw(self):
        """
        Call only once, upon initialization to add widgets to root frame
        """
        # Build a menu and add it to the root frame.
        menu_bar = tk.Menu(self.root)
        self.root['menu'] = menu_bar
        menu_file = tk.Menu(menu_bar)
        menu_bar.add_cascade(menu=menu_file, label='File')
        menu_file.add_command(label='Login/Register', command=self.new_login)
        menu_file.add_command(label='Close', command=self.close)

        # The Body and Footer classes must be initialized and packed into the root window.
        self.body = Body(self.root, self._retrieve_all_messages, self._retrieve_new_messages, self._get_current_info)
        self.body.pack(fill=tk.BOTH, side=tk.TOP, expand=True)
        self.footer = Footer(self.root, self._get_current_info, self.send_message, self.body.insert_user, self.body.set_new_messages_and_users)
        # Just to change the color of the bottom
        self.footer.configure(bg="lightblue")
        self.footer.pack(fill=tk.BOTH, side=tk.BOTTOM)

if __name__ == "__main__":
    # All Tkinter programs start with a root window. We will name ours 'main'.
    main = tk.Tk()
    
    # 'title' assigns a text value to the Title Bar area of a window.
    main.title("Distributed Social Messenger")

    # This is just an arbitrary starting point. You can change the value around to see how
    # the starting size of the window changes. I just thought this looked good for our UI.
    main.geometry("920x480")

    # adding this option removes some legacy behavior with menus that modern OSes don't support. 
    main.option_add('*tearOff', False)

    # Initialize the MainApp class, which is the starting point for the widgets used in the program.
    # All of the classes that we use, subclass Tk.Frame, since our root frame is main, we initialize 
    # the class with it.
    MainApp(main)

    # Update to make sure our windows are stay the minimum size
    # minsize prevents the root window from resizing too small. Feel free to comment it out and see how
    # the resizing behavior of the window changes.
    main.update()
    main.minsize(main.winfo_width(), main.winfo_height())
    # And finally, start up the event loop for the program
    main.mainloop()
