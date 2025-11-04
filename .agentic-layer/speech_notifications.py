"""Voice notification system using text-to-speech.

Provides audio feedback for workflow completion and errors.
"""
# /// script
# dependencies = [
#   "pyttsx3",
# ]
# ///

import logging
import random
import pyttsx3

# Suppress verbose INFO logs from comtypes (Windows COM wrapper)
logging.getLogger('comtypes').setLevel(logging.WARNING)


# Success messages - randomly selected when workflow completes successfully
SUCCESS_MESSAGES = [
    "The Force is strong with this code. Mission complete, I am ready.",
    "These aren't the bugs you're looking for. All checks passed. Ready.",
    "I have a good feeling about this! Workflow successful. Awaiting orders.",
    "The mission is complete, Master. What are your orders?",
    "This is the way. All tests have passed.",
    "Never tell me the odds! And we succeeded anyway.",
]

# Error messages - randomly selected when workflow encounters an error
ERROR_MESSAGES = [
    "I've got a bad feeling about this. An error occurred.",
    "It's a trap! The workflow has failed.",
    "The dark side clouds everything. An error has stopped progress.",
    "Help me, developer, you're my only hope! An error occurred.",
    "I find your lack of passing tests disturbing. Error detected.",
    "These ARE the bugs you're looking for. Workflow failed.",
    "Failed, we have. Into exile, the code must go.",
    "The code is strong with the dark side. Error detected.",
    "Only at the end do you realize the power of the bugs. Failure.",
    "This is not the deployment you're looking for. Build failed.",
]


def speak_notification(message: str):
    """Speak a notification message using text-to-speech.

    Args:
        message: The text message to speak

    Note:
        Errors are logged but don't raise exceptions to avoid breaking workflow.
    """
    try:
        engine = pyttsx3.init()
        # Set speech rate (slower for clarity)
        engine.setProperty('rate', 150)
        engine.say(message)
        engine.runAndWait()
    except (RuntimeError, OSError, ImportError) as e:
        # Don't let TTS errors break the workflow
        logging.getLogger(__name__).warning("Failed to speak notification: %s", e)


def speak_success():
    """Speak a randomly selected success message."""
    message = random.choice(SUCCESS_MESSAGES)
    print(f"[SPEECH] Speaking: {message}")
    speak_notification(message)


def speak_error():
    """Speak a randomly selected error message."""
    message = random.choice(ERROR_MESSAGES)
    print(f"[SPEECH] Speaking: {message}")
    speak_notification(message)


def speak_custom(message: str):
    """Speak a custom message.

    Args:
        message: Custom text to speak
    """
    print(f"[SPEECH] Speaking: {message}")
    speak_notification(message)


# Testing
if __name__ == "__main__":
    import sys
    import argparse

    parser = argparse.ArgumentParser(description="Test speech notifications")
    parser.add_argument(
        "action",
        nargs="?",
        choices=["success", "error", "all-success", "all-error"],
        help="Action to perform (if not provided, runs interactive mode)"
    )
    parser.add_argument(
        "--message",
        help="Custom message to speak (use with 'custom' action or standalone)"
    )

    args = parser.parse_args()

    # If a custom message is provided without action, speak it directly
    if args.message and not args.action:
        speak_custom(args.message)
        sys.exit(0)

    # Non-interactive mode
    if args.action:
        if args.action == "success":
            speak_success()
        elif args.action == "error":
            speak_error()
        elif args.action == "all-success":
            print("\nTesting all success messages...")
            for msg in SUCCESS_MESSAGES:
                print(f"\n[SPEECH] {msg}")
                speak_notification(msg)
        elif args.action == "all-error":
            print("\nTesting all error messages...")
            for msg in ERROR_MESSAGES:
                print(f"\n[SPEECH] {msg}")
                speak_notification(msg)
        print("\n[OK] Test complete!")
        sys.exit(0)

    # Interactive mode
    print("Speech Notification System Test")
    print("=" * 50)
    print("\nOptions:")
    print("  1 - Test success message")
    print("  2 - Test error message")
    print("  3 - Test custom message")
    print("  4 - Test all success messages")
    print("  5 - Test all error messages")
    print()

    choice = input("Enter choice (1-5): ").strip()

    if choice == "1":
        speak_success()
    elif choice == "2":
        speak_error()
    elif choice == "3":
        custom = input("Enter custom message: ")
        speak_custom(custom)
    elif choice == "4":
        print("\nTesting all success messages...")
        for msg in SUCCESS_MESSAGES:
            print(f"\n[SPEECH] {msg}")
            speak_notification(msg)
    elif choice == "5":
        print("\nTesting all error messages...")
        for msg in ERROR_MESSAGES:
            print(f"\n[SPEECH] {msg}")
            speak_notification(msg)
    else:
        print("Invalid choice")
        sys.exit(1)

    print("\n[OK] Test complete!")
