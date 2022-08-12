This whole project was coded and tested by Ragib Sakib



Credit to Professor Mark Baldwin and his staff for providing a lot of the skeleton code for this project
	ds_messenger.py:
		-line 50 - DirectMessage class skeleton
		-line 73 - DirectMessenger class skeleton
	ds_protocol.py:
		-line 50 - extract_json function skeleton
	The entirety of ds_GUI was a skeleton that he provided

Credit to @BrownieInMotion on StackOverflow for providing an example of how to use json.dumps()
Weblink - https://stackoverflow.com/questions/64761547/using-python-f-string-in-a-json-list-of-data
	ds_protocol.py:
		-line 87
		-line 99
		-line 110

Credit to @ChumiestBucket for code to wipe a tkinter canvas widget
Weblink: https://stackoverflow.com/questions/51856163/how-can-i-clear-or-overwrite-a-tkinter-canvas
	ds_GUI.py:
		-line 43
		-line 91
		-line 179
		
Credit to @Mat.C for providing a method of updating text on a canvas widget
Weblink: https://stackoverflow.com/questions/55675124/how-to-make-a-scrollbar-for-a-label-list-python-tkinter	
		-line 124
		-line 233
			
Credit to @Gary02127 and @Shish on StackOverflow for providing an example of how to make a scrollbar for a Canvas widget
Weblink: https://stackoverflow.com/questions/7727804/tkinter-using-scrollbars-on-a-canvas
	ds_GUI.py:
		-line 228

Credit to @Da_Pz on StackOverflow for the initialvalue option of tk.simpledialog, which is not written anywhere else
Weblink: https://stackoverflow.com/questions/49190088/adding-default-value-in-simpledialog-askstring-using-tkinter-in-python-3
	ds_GUI.py:
		-line 373

Credit: I got the idea of using prompts from Luis E Morales in ICS 32
	ds_GUI.py:
		-line 135
		-line 368 to line 373



Now all of my citations are out of the way, time to give a rundown of how to use my program

HOW TO USE THIS PROGRAM:
	1. Run ds_GUI.py, this is the main GUI/access point for this program

	2. Click "file" and hit the "login/register" option, 3 prompts will then appear asking for username, password, and server
		-If this isn't done, the program will simply not proceed and throw error dialog boxes if you try to do any actions

	3. After logging in, all users who have sent you a message will appear on the left box
		-These users are formatted NEWEST on TOP and OLDEST on BOTTOM, similar to say Instagram

	4. If the user list is empty or you want to add a new user click the "Add User" button on the left, a 
	prompt will then appear asking for the recipient's username
		-After doing this, the name will show up on the left user view

	5. To Send a message simply click on one of users in the user view, type into the text box, and click "Send"
		-Sent message are NOT shown, only received messages are sent

	6. This program DOES NOT update in realtime. To check if you received any new messages, you have to click the "Refresh" button
		-After clicking this button, if there are any users that have not sent you a message in your user view, they
		will be purged

	7. Most Importantly: Have Fun


