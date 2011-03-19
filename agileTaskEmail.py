from PyGmail import PyGmail

import sys
sys.path.append( '/Users/tyghe/Programming/pyAgileTaskApi' )
from AgileTaskAPI import AgileTaskAPI
 
# Gmail username which is your full email address(AKA whatever is in the top right of your gmail screen)
user = ''
# Gmail password
password = ''
# The label that will contain new task emails
gmail_label = ''

# Initialize the Gmail Imap Interface
g = PyGmail( )

# Login to gmail
g.login( user, password )

# Initialize the Python Agile Task API
patapi = AgileTaskAPI( '' )

# Get mail from a specific folder/label
msgs = g.get_mail( gmail_label )

# For each message extract the id of the mail and the body
for msg_id, msg_body in msgs.items():
	# Add the task to the today list
	try:
		newTask = patapi.AddTask( msg_body, icebox = 'false' )
		g.delete_msgs( list( msg_id ) )
	except:
		print "Failed to add %s" % msg_body

g.logout()
