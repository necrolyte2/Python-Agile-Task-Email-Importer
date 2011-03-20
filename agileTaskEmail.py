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

# Email addresses that are ok to pull new tasks from
valid_emails = config.get( sections[1], 'valid_from_emails' ).split( ',' )
valid_emails = [email.strip() for email in valid_emails]

# Subjects that are ok to pull tasks from
valid_subjects = config.get( sections[1], 'valid_subjects' ).split( ',' )
valid_subjects = [subject.strip() for subject in valid_subjects]

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

# Which messages to delete
deletes = []

# For each message extract the id of the mail and the body
for msg_id, msg in msgs.items():
	from_address = msg.get( 'from' )
	subject = msg.get( 'subject' )
	if from_address in valid_emails and subject in valid_subjects:
		msg_body = g.get_msg_body( msg )
		# Add the task to the today list
		try:
			newTask = patapi.AddTask( msg_body, icebox = 'false' )
			print "Added task %s\n" % msg_body
			deletes.append( msg_id )
		except Exception as e:
			print "Failed to add %s\n" % msg_body
			print e
	else:
		print "From: %s Subject: %s not in" % (from_address, subject)
		print "%s or %s" % (valid_emails, valid_subjects)

# Delete all queued messages to be deleted
g.delete_msgs( deletes )

g.logout()
