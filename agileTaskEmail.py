from PyImap import PyImap

import sys

# imap username which is your full email address
user = ''
# imap password
password = ''
# The label/folder that will contain new task emails
imap_folder = ''

# Path to pyAgileTaskAPI(https://github.com/necrolyte2/pyAgileTaskAPI)
path_to_agiletaskapi = ''
# Your Agile Task API Key
api_key = ''

sys.path.append( path_to_agiletaskapi )
from AgileTaskAPI import AgileTaskAPI

# Initialize the Imap Interface
g = PyImap( )

# Login to Imap
g.login( user, password )

# Initialize the Python Agile Task API
patapi = AgileTaskAPI( api_key )

# Get mail from a specific folder/label
msgs = g.get_mail( imap_folder )

# For each message extract the id of the mail and the body
for msg_id, msg_body in msgs.items():
	# Add the task to the today list
	try:
		newTask = patapi.AddTask( msg_body, icebox = 'false' )
		g.delete_msgs( list( msg_id ) )
	except:
		print "Failed to add %s" % msg_body

g.logout()
