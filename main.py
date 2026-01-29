from call_engine.queue import get_contacts
from call_engine.call_processor import process_call

def main():
    contacts = get_contacts()
    for contact in contacts:
        process_call(contact)

if __name__ == "__main__":
    main()
