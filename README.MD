# Instagram Bot (IgBot) Automation

This repository contains the code for an Instagram bot (IgBot) automation script. The script uses Selenium WebDriver to automate actions on the Instagram website. It provides functionality for logging in, sending messages, handling popups, and performing basic outreach on Instagram.

## Prerequisites

- Python 3.x
- Selenium WebDriver
- Chrome WebDriver (compatible with your Chrome browser version)

### Getting Started

#### Install the required dependencies by running the following command

` pip install -r requirements.txt `

## Features

### Login and Session Management

The script handles the login process, allowing you to provide your Instagram credentials.
It supports saving and loading the session to resume a previous session without logging in again.

### Popup Handling

The script dismisses cookie notices and handles other popups that may appear during the automation process.

### Addressee Information

You can specify the addressee (recipient) for each message using the select_addressee() method.
The script tries to select the addressee by searching for their account name or using a CSS selector if necessary.
It handles errors if the addressee cannot be selected and logs the broken addressees.

### Message Sending

The script sends messages to the selected addressees.
It checks if there are any prior messages sent to the addressee before sending a message if enabled.
The messages are sent using the send_message() method.

### Error Handling

The script includes error check functions to handle common login errors and account suspension.
It logs any errors encountered during the automation process and provides appropriate messages.

## Customization

#### You can customize the process in any way, according to your requirements

- Start by adding an Instagram account with a username and password using our Graphical User Interface (GUI).
- Upload an Address List that contains usernames and names. The list should have the following headings: {username, name}.
- Upload a Message List of automated messages to send. We recommend having four messages without a name value appended, and four messages with the name value appended. To include the name dynamically in the message, use {name} within the uploaded message list. The heading for the message list should be {message}.
- Once you have set up the account and uploaded the address and message lists, you can start the process and watch the bot in action!

#### Message Examples

- Hey {name}, how are you today?

##### Feel free to customize the messages and add more variations based on your preferences
