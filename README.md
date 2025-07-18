# eGainTrack - Package Tracking Chatbot

A command-line chatbot that helps users track packages and file claims for lost/delayed items. Built for the eGain take-home assignment to demonstrate conversation design, error handling, and user experience principles.

## Features

- **Personalized Experience**: Collects and uses user's name throughout the conversation
- **Smart Package Tracking**: Determines package status based on tracking number patterns
- **Comprehensive Claim Filing**: Collects detailed information (contents, value, contact details)
- **Flexible Status Handling**: Supports delivered, delayed, and lost package scenarios
- **Robust Error Handling**: Validates all inputs with clear error messages and re-prompting
- **Satisfaction Survey**: Collects feedback and provides customer support escalation
- **Multi-Session Support**: Users can track multiple packages in one session

## Setup/Installation Instructions

### Prerequisites
- Python 3.6 or higher
- No additional dependencies required (uses only Python standard library)

### Installation Steps

1. **Clone or download the project**
   ```bash
   # If using git
   git clone <repository-url>
   cd eGain_take_home_swe
   
   # Or simply download the lost_package_chatbot.py file
   ```

2. **Run the chatbot**
   ```bash
   python lost_package_chatbot.py
   ```

3. **Start the conversation**
   - Enter your name when prompted
   - Choose whether to track a package
   - Follow the menu-driven conversation flow

### Testing Different Scenarios

The chatbot uses the last digit of tracking numbers to determine package status:

- **Last digit 0-3**: Package delivered successfully
- **Last digit 4-6**: Package delayed but found
- **Last digit 7-9**: Package lost/not found

**Example tracking numbers for testing:**
- `1234567890` → Delivered successfully
- `1234567894` → Delayed
- `1234567897` → Lost

## Approach Explanation

### Conversation Design Philosophy

I designed this chatbot with a **human-centered approach** that prioritizes:

1. **Personalization**: Every interaction uses the user's name to create a more human connection
2. **Clear Navigation**: Menu-driven interface with numbered options for easy selection
3. **Contextual Information**: Provides relevant details (scheduled delivery date) before asking for decisions
4. **Flexible Problem Resolution**: Allows claims even for "delivered" packages, recognizing real-world scenarios

### Technical Implementation

**Core Architecture:**
- **Modular Functions**: Each feature (validation, claim collection, status checking) is separated into focused functions
- **State Management**: Uses simple variables to maintain conversation context
- **Input Validation**: Comprehensive validation for all user inputs with helpful error messages
- **Predictable Testing**: Last-digit logic allows for consistent testing of all conversation paths

**Error Handling Strategy:**
- **Proactive Validation**: Validates inputs before processing
- **Clear Feedback**: Specific error messages explain what went wrong
- **Graceful Recovery**: Re-prompts users until valid input is received
- **No Crashes**: Handles all edge cases to prevent program termination

### Conversation Flow Design

The chatbot follows a **decision tree structure** with these key principles:

1. **Progressive Disclosure**: Information is revealed as needed, not overwhelming users upfront
2. **Multiple Entry Points**: Users can file claims directly or check status first
3. **Escalation Paths**: Always provides a way to get human support if needed
4. **Loop Prevention**: Clear exit options at every decision point

### User Experience Considerations

- **Natural Language**: Conversational tone that feels human, not robotic
- **Empathetic Responses**: Acknowledges user frustration and offers solutions
- **Confirmation Steps**: Shows collected information before proceeding
- **Satisfaction Measurement**: Ends with feedback collection for continuous improvement

## Usage Examples

#enter images here

## Author

**Nathaniel Greenberg** - eGain Take Home Assignment

