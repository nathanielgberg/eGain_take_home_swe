"""
eGainTrack - Package Tracking Chatbot
A command-line chatbot that helps users track packages and file claims for lost/delayed items.

Features:
- Personal name collection and validation
- Tracking number validation and status determination
- Comprehensive claim filing with details collection
- Satisfaction survey with customer support escalation
- Error handling for invalid inputs
- Support for multiple package tracking sessions

Author: Nathaniel Greenberg
"""

import re

def is_valid_tracking_number(tracking_number):
    """
    Validates tracking number format.
    
    Args:
        tracking_number (str): The tracking number to validate
        
    Returns:
        bool: True if valid (10-12 alphanumeric characters), False otherwise
    """
    # Example: valid tracking numbers are 10-12 alphanumeric chars
    return bool(re.fullmatch(r"[A-Za-z0-9]{10,12}", tracking_number))

def is_valid_name(name):
    """
    Validates user name format.
    
    Args:
        name (str): The name to validate
        
    Returns:
        bool: True if valid (letters and spaces only, not empty), False otherwise
    """
    # Check if name is not empty and contains only letters and spaces
    return bool(re.fullmatch(r"[A-Za-z\s]+", name.strip())) and len(name.strip()) > 0

def is_valid_email(email):
    """
    Validates email address format.
    
    Args:
        email (str): The email address to validate
        
    Returns:
        bool: True if valid email format, False otherwise
    """
    # Basic email validation - must contain @ and domain
    return bool(re.fullmatch(r"[^@]+@[^@]+\.[^@]+", email.strip())) and len(email.strip()) > 0

def collect_claim_details(user_name):
    """
    Collects all necessary details for filing a package claim.
    
    Args:
        user_name (str): The user's name for personalization
        
    Returns:
        dict: Dictionary containing claim details (contents, value, email, phone)
    """
    print(f"Let me collect some details for your claim, {user_name}.")
    
    # Get package contents description
    while True:
        contents = input("What was in the package? ").strip()
        if len(contents) > 0:
            break
        print("Please describe what was in the package.")
    
    # Get estimated value with currency validation
    while True:
        value = input("What's the estimated value of the package? $").strip()
        # Validate currency format (e.g., 25.99, 100, 50.50)
        if re.fullmatch(r"\d+(\.\d{2})?", value):
            break
        print("Please enter a valid amount (e.g., 25.99)")
    
    # Get email address for claim updates
    while True:
        email = input("What's your email address for claim updates? ").strip()
        if is_valid_email(email):
            break
        print("Please enter a valid email address.")
    
    # Get phone number for follow-up contact
    while True:
        phone = input("What's your phone number for follow-up? ").strip()
        # Allow various phone formats but ensure at least 10 digits
        if re.fullmatch(r"[\d\-\+\(\)\s]+", phone) and len(phone.replace(" ", "").replace("-", "").replace("(", "").replace(")", "").replace("+", "")) >= 10:
            break
        print("Please enter a valid phone number.")
    
    return {
        "contents": contents,
        "value": value,
        "email": email,
        "phone": phone
    }

def get_package_status(tracking_number, user_name=None):
    """
    Determines package status based on tracking number's last digit.
    
    Args:
        tracking_number (str): The tracking number to check
        user_name (str, optional): User's name for personalization in delivery location
        
    Returns:
        dict or None: Package status info or None if not found
    """
    # Use last digit to determine status for predictable testing
    if not tracking_number.isdigit():
        return None
    
    last_digit = int(tracking_number[-1])
    
    if last_digit <= 3:  # 0-3 = delivered successfully
        return {
            "status": "delivered",
            "location": user_name if user_name else "recipient",
            "date": "July 20"
        }
    elif last_digit <= 6:  # 4-6 = delayed but found
        return {
            "status": "delayed",
            "location": "In Transit",
            "date": "July 25"
        }
    else:  # 7-9 = lost/not found
        return None

def ask_menu(prompt, options):
    """
    Displays a menu and handles user selection with error handling.
    
    Args:
        prompt (str): The menu prompt to display
        options (dict): Dictionary of option keys and descriptions
        
    Returns:
        str: The user's valid choice
    """
    while True:
        print(prompt)
        # Display all menu options
        for key, desc in options.items():
            print(f"Press {key} {desc}")
        choice = input().strip()
        if choice in options:
            return choice
        print("Sorry, I didn't catch that. Please reply with one of the menu options.")

def get_user_name():
    """
    Collects and validates the user's name.
    
    Returns:
        str: Validated user name
    """
    while True:
        name = input("Hi there, I'm eGainTrack, your package-tracking assistant. What's your name? ").strip()
        if is_valid_name(name):
            return name.strip()
        print("Sorry, I didn't catch your name. Could you please type your first name?")

def main():
    """
    Main conversation flow for the eGainTrack chatbot.
    
    Handles the complete user interaction including:
    - Name collection and validation
    - Package tracking with status determination
    - Claim filing with detailed information collection
    - Satisfaction survey and customer support escalation
    - Multiple package tracking sessions
    """
    # Start by collecting user's name
    user_name = get_user_name()
    
    # Welcome and confirm they want to track a package
    menu_start = {'1': 'for yes', '2': 'to exit'}
    start_choice = ask_menu(f"Nice to meet you, {user_name}! Are you looking to track a package today?", menu_start)
    
    # Early exit if user doesn't want to track
    if start_choice == '2':
        print("Okay—feel free to reach out if you need anything else.")
        return
    
    print(f"Great! Let's help you track your package, {user_name}.")
    
    # Main conversation loop - allows tracking multiple packages
    while True:
        # Collect and validate tracking number
        tracking_number = input("Can you provide your tracking number? ").strip()
        if not is_valid_tracking_number(tracking_number):
            print("❌ That doesn't look like a valid tracking number. Please try again.")
            continue
        
        # Provide context about scheduled delivery
        print(f"According to our records, {user_name}, your package was scheduled to arrive on July 22.")
        print("Did it arrive by then?")
        
        # Offer options: file claim directly or check current status
        menu1 = {'1': 'if it did not arrive and you\'d like to file a claim', '2': 'if you\'d like me to check its current status'}
        choice1 = ask_menu("What would you like to do?", menu1)
        
        # Get package status based on tracking number
        status = get_package_status(tracking_number, user_name)
        
        # Handle case where package is not found in system
        if not status:
            print(f"😔 Sorry {user_name}, we couldn't find your package.")
            print("Filing a lost-package claim for you...")
            claim_details = collect_claim_details(user_name)
            print(f"Perfect! I've submitted a lost-package claim on your behalf, {user_name}.")
            print(f"You'll get an email confirmation shortly at {claim_details['email']}.")
            
            # Ask if user wants to continue or finish
            continue_tracking = ask_menu(f"Anything else I can help with today, {user_name}?", {'1': 'to track another package', '2': 'to finish'})
            if continue_tracking == '2':
                print(f"Thank you for using our service, {user_name}!")
                # Conduct satisfaction survey
                satisfaction = ask_menu("Are you satisfied with the service today?", {'1': 'for yes', '2': 'for no'})
                if satisfaction == '2':
                    print("Here is our live customer support please call at 8184241205")
                break
            continue
        
        # Handle delivered successfully case (last digit 0-3)
        if status["status"] == "delivered":
            print(f"🎉 Great news, {user_name}! Your package was delivered successfully on {status['date']}.")
            print(f"It was delivered to: {status['location']}")
            
            # Even for delivered packages, offer claim filing option
            menu_delivered = {'1': 'to file a claim (e.g., not received or damaged)', '2': 'to finish or track another package'}
            delivered_choice = ask_menu("Did you not receive your package or was it damaged?", menu_delivered)
            
            if delivered_choice == '1':
                # User wants to file claim despite "delivered" status
                print(f"Sorry to hear you had an issue with your delivered package, {user_name}.")
                claim_details = collect_claim_details(user_name)
                print(f"Perfect! I've submitted a lost-package claim on your behalf, {user_name}.")
                print(f"You'll get an email confirmation shortly at {claim_details['email']}.")
                
                # Continue or finish
                continue_tracking = ask_menu(f"Anything else I can help with today, {user_name}?", {'1': 'to track another package', '2': 'to finish'})
                if continue_tracking == '2':
                    print(f"Thank you for using our service, {user_name}!")
                    satisfaction = ask_menu("Are you satisfied with the service today?", {'1': 'for yes', '2': 'for no'})
                    if satisfaction == '2':
                        print("Here is our live customer support please call at 8184241205")
                    break
                continue
            else:
                # User is satisfied with delivery
                continue_tracking = ask_menu(f"Anything else I can help with today, {user_name}?", {'1': 'to track another package', '2': 'to finish'})
                if continue_tracking == '2':
                    print(f"Thank you for using our service, {user_name}!")
                    satisfaction = ask_menu("Are you satisfied with the service today?", {'1': 'for yes', '2': 'for no'})
                    if satisfaction == '2':
                        print("Here is our live customer support please call at 8184241205")
                    break
                continue
        
        # Handle direct claim filing (user chose option 1)
        if choice1 == '1':
            claim_details = collect_claim_details(user_name)
            print(f"Perfect! I've submitted a lost-package claim on your behalf, {user_name}.")
            print(f"You'll get an email confirmation shortly at {claim_details['email']}.")
            
            # Continue or finish
            continue_tracking = ask_menu(f"Anything else I can help with today, {user_name}?", {'1': 'to track another package', '2': 'to finish'})
            if continue_tracking == '2':
                print(f"Thank you for using our service, {user_name}!")
                satisfaction = ask_menu("Are you satisfied with the service today?", {'1': 'for yes', '2': 'for no'})
                if satisfaction == '2':
                    print("Here is our live customer support please call at 8184241205")
                break
            continue
        
        # Handle status checking (user chose option 2)
        elif choice1 == '2':
            print("Got it. One sec while I check…")
            
            if status["status"] == "delayed":
                # Package is delayed (last digit 4-6)
                print(f"Your package is currently \"{status['location']}\", with an expected delivery on {status['date']}.")
                menu2 = {'1': 'to file a claim', '2': 'to finish'}
                choice2 = ask_menu("Would you like me to file a claim now that it's delayed?", menu2)
                
                if choice2 == '1':
                    # User wants to file claim for delayed package
                    claim_details = collect_claim_details(user_name)
                    print(f"Perfect! I've submitted a lost-package claim on your behalf, {user_name}.")
                    print(f"You'll get an email confirmation shortly at {claim_details['email']}.")
                    
                    # Continue or finish
                    continue_tracking = ask_menu(f"Anything else I can help with today, {user_name}?", {'1': 'to track another package', '2': 'to finish'})
                    if continue_tracking == '2':
                        print(f"Thank you for using our service, {user_name}!")
                        satisfaction = ask_menu("Are you satisfied with the service today?", {'1': 'for yes', '2': 'for no'})
                        if satisfaction == '2':
                            print("Here is our live customer support please call at 8184241205")
                        break
                    continue
                else:
                    # User doesn't want to file claim for delayed package
                    continue_tracking = ask_menu(f"Anything else I can help with today, {user_name}?", {'1': 'to track another package', '2': 'to finish'})
                    if continue_tracking == '2':
                        print(f"Thank you for using our service, {user_name}!")
                        satisfaction = ask_menu("Are you satisfied with the service today?", {'1': 'for yes', '2': 'for no'})
                        if satisfaction == '2':
                            print("Here is our live customer support please call at 8184241205")
                        break
                    continue
            else:
                # This handles the delivered case when user chose to check status
                print(f"Your package was delivered on {status['date']} to {status['location']}.")
                continue_tracking = ask_menu(f"Anything else I can help with today, {user_name}?", {'1': 'to track another package', '2': 'to finish'})
                if continue_tracking == '2':
                    print(f"Thank you for using our service, {user_name}!")
                    satisfaction = ask_menu("Are you satisfied with the service today?", {'1': 'for yes', '2': 'for no'})
                    if satisfaction == '2':
                        print("Here is our live customer support please call at 8184241205")
                    break
                continue

if __name__ == "__main__":
    main() 