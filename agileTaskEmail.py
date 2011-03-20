from PyImap import PyImap

import ConfigParser
config = ConfigParser.RawConfigParser()
config.read( 'settings.cfg' )
sections = config.sections()
print sections

import sys

# imap username which is your full email address
user = config.get( sections[1], 'imap_user' )
# imap password
password = config.get( sections[1], 'imap_password' )
# The label/folder that will contain new task emails
imap_folder = config.get( sections[1], 'imap_folder' )
# Imap Server
host = config.get( sections[1], 'imap_host' )
# Imap Port
port = config.getint( sections[1], 'imap_port' )
# Timeout
timeout = config.getfloat( sections[1], 'imap_timeout' )

# Path to pyAgileTaskAPI(https://github.com/necrolyte2/pyAgileTaskAPI)
path_to_agiletaskapi = config.get( sections[0], 'path_to_agiletaskapi' )

# Your Agile Task API Key
api_key = config.get( sections[0], 'api_key' )

print "User: %s\nPass: %s\nFolder: %s\nPath: %s\nKey: %s\n" % (user, password, imap_folder, path_to_agiletaskapi, api_key)

sys.path.append( path_to_agiletaskapi )
from AgileTaskAPI import AgileTaskAPI

# Initialize the Imap Interface
g = PyImap( host, port, timeout )

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
