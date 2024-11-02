from datetime import datetime, time
import pytz
from loguru import logger

def check_end_of_market():
    
    # Define the specific time
    target_time = time(15, 25)  # 3:25 PM

    # Get the current time in IST
    ist = pytz.timezone('Asia/Kolkata')
    current_time = datetime.now(ist).time()

    # Check if the current time is after 3:25 PM
    if current_time >= target_time:
        # Execute your code here
        logger.info("It's after 3:25 PM IST. Modify Order will be executing.")
    else:
        logger.info("It's before 3:25 PM IST. Modify Order will not be executed.")
