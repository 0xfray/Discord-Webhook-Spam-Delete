import requests
import time
import re

def send_message_loop(webhook_url, message):
    print("Sending messages in a loop until rate-limited...")
    while True:
        response = requests.post(webhook_url, json={"content": message})
        if response.status_code == 429:
            retry_after = response.json().get("retry_after", 0) / 1000
            print(f"Rate-limited. Retrying after {retry_after} seconds.")
            time.sleep(retry_after)
        elif not response.ok:
            print(f"Failed to send message. HTTP Status: {response.status_code}")
            break
        else:
            print("Message sent successfully!")

def delete_webhook(webhook_url):
    print("Attempting to delete the webhook...")
    response = requests.delete(webhook_url)
    if response.status_code == 404:
        print("Error: This webhook does not exist or is already deleted.")
    elif not response.ok:
        print(f"Failed to delete the webhook. HTTP Status: {response.status_code}")
    else:
        print("Webhook successfully deleted.")

def send_message_and_delete(webhook_url, message):
    print("Sending your message 10 times...")
    for i in range(10):
        response = requests.post(webhook_url, json={"content": message})
        if not response.ok:
            print(f"Failed to send message #{i + 1}. HTTP Status: {response.status_code}")
            break
        print(f"Message #{i + 1} sent successfully!")
    delete_webhook(webhook_url)

def validate_webhook_url(webhook_url):
    if not webhook_url.startswith("https://discord.com/api/webhooks/") or not re.match(r"^https://discord\.com/api/webhooks/\d+/[\w-]+$", webhook_url):
        return False
    return True

def main():
    print("Discord Webhook Tool | 0xfray ")
    print("1. Send a message to the webhook in a loop until rate-limited")
    print("2. Delete the webhook")
    print("3. Send the same message 10 times and then delete the webhook")
    try:
        choice = int(input("Enter your choice (1/2/3): ").strip())
    except ValueError:
        print("Invalid input. Please enter 1, 2, or 3.")
        return
    webhook_url = input("Enter the Discord webhook URL: ").strip()
    if not validate_webhook_url(webhook_url):
        print("This is not a valid Discord webhook URL.")
        return
    if choice == 1:
        message = input("Enter the message to send: ").strip()
        send_message_loop(webhook_url, message)
    elif choice == 2:
        delete_webhook(webhook_url)
    elif choice == 3:
        message = input("Enter the message to send: ").strip()
        send_message_and_delete(webhook_url, message)
    else:
        print("Invalid choice. Please enter 1, 2, or 3.")

if __name__ == "__main__":
    main()
