from PyImap import PyImap

import sys
import ConfigParser
import ssl

config = ConfigParser.RawConfigParser()
config.read( "%s/%s", (sys.path[0],'settings.cfg') )

# imap username which is your full email address
user = config.get( 'AgileTaskEmail', 'imap_user' )
# imap password
password = config.get( 'AgileTaskEmail', 'imap_password' )
# The label/folder that will contain new task emails
imap_folder = config.get( 'AgileTaskEmail', 'imap_folder' )
# Imap Server
host = config.get( 'AgileTaskEmail', 'imap_host' )
# Imap Port
port = config.getint( 'AgileTaskEmail', 'imap_port' )
# Timeout
timeout = config.getfloat( 'AgileTaskEmail', 'imap_timeout' )

# Email addresses that are ok to pull new tasks from
valid_emails = config.get( 'AgileTaskEmail', 'valid_from_emails' ).split( ',' )
valid_emails = [email.strip() for email in valid_emails]

# Subjects that are ok to pull tasks from
valid_subjects = config.get( 'AgileTaskEmail', 'valid_subjects' ).split( ',' )
valid_subjects = [subject.strip() for subject in valid_subjects]

# Path to pyAgileTaskAPI(https://github.com/necrolyte2/pyAgileTaskAPI)
#path_to_agiletaskapi = config.get( 'pyAgileTaskApi', 'path_to_agiletaskapi' )

# Your Agile Task API Key
api_key = config.get( 'pyAgileTaskApi', 'api_key' )

#print "User: %s\nPass: %s\nFolder: %s\nPath: %s\nKey: %s\n" % (user, password, imap_folder, path_to_agiletaskapi, api_key)

try:
    from agiletaskapi.AgileTaskAPI import AgileTaskAPI
except ImportError:
    print "You need to install pyAgileTaskAPI"
    sys.exit( -1 )

# Initialize the Imap Interface
g = PyImap( host, port, timeout )

# Login to Imap
g.login( user, password )

# Get mail from a specific folder/label
msgs = g.get_mail( imap_folder )

# Initialize the Python Agile Task API
patapi = AgileTaskAPI( api_key )
 
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
