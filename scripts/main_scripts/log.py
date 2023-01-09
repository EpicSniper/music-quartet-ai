import logging
import os
import datetime

# Set up logging
log_file = os.path.join(os.path.abspath(os.path.dirname(__file__)), '../..', 'Log.txt')
logging.basicConfig(filename=log_file, level=logging.INFO)

def logMessage(message):
  # Get the current date and time
  now = datetime.datetime.now()

  # Format the message with the date and time
  formatted_message = f'{now:%Y-%m-%d %H:%M:%S}: {message}'

  logging.info(formatted_message)