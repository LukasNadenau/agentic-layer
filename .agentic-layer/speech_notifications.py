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


# Success messages - randomly selected when workflow completes successfully
SUCCESS_MESSAGES = [
    "Mission accomplished! I am ready for your next command.",
    "Workflow completed successfully. All systems nominal. Standing by.",
    "Victory! The code gods smile upon us. I am ready.",
    "All phases complete. Your code is pristine. Ready for action.",
    "Success across the board! Everything passed. Ready when you are.",
    "Flawless execution! All checks passed. Awaiting your next move.",
    "Boom! Nailed it! Workflow complete. What's next, boss?",
    "Green lights everywhere! Workflow successful. I am ready to serve.",
]

# Error messages - randomly selected when workflow encounters an error
ERROR_MESSAGES = [
    "Houston, we have a problem. An error has occurred.",
    "Abort! Abort! Something went wrong. Please check the logs.",
    "Error detected. Workflow failed. I need your attention.",
    "Red alert! The workflow encountered an error.",
    "Oops! Hit a snag. An error stopped the workflow.",
    "Failure is not an option, but it happened anyway. Error occurred.",
    "Code gremlins detected! An error has halted progress.",
    "Plot twist! An unexpected error appeared. Check the output.",
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
    except Exception as e:
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
