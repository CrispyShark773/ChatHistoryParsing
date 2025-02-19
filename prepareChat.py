import json
import sys
import os

def filter_and_format_messages(chat_data):
    filtered_messages = []
    
    for message in chat_data.get("messages", []):
        if message.get("type") == "message" and \
           "text_entities" in message and \
           message.get("from") and \
           message.get("from_id") != "null" and \
           "forwarded_from" not in message and \
           "via_bot" not in message:

            # Ensure text_entities exists and is not empty
            if not message.get("text_entities"):
                continue
            
            # Check if any text entity is of type "hashtag"
            if any(entity.get("type") == "hashtag" for entity in message["text_entities"]):
                continue

            sender = message["from"]
            text_content = "".join(entity.get("text", "") for entity in message["text_entities"] if entity.get("type") == "plain")
            
            if text_content.strip():
                filtered_messages.append(f"{{{sender}}}{text_content}")

    return filtered_messages

def main():
    if len(sys.argv) < 3:
        print("Usage: python prepareChat.py <ChatHistory.json> <output.txt> [replace]")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]
    replace = len(sys.argv) > 3 and sys.argv[3].lower() == "replace"

    try:
        with open(input_file, "r", encoding="utf-8") as f:
            chat_data = json.load(f)
    except Exception as e:
        print(f"Error reading JSON file: {e}")
        sys.exit(1)

    formatted_messages = filter_and_format_messages(chat_data)

    if not formatted_messages:
        print("No messages to export.")
        sys.exit(0)

    mode = "w" if replace else "a"
    try:
        with open(output_file, mode, encoding="utf-8") as f:
            for message in formatted_messages:
                f.write(message + "\n")
    except Exception as e:
        print(f"Error writing to file: {e}")
        sys.exit(1)

    print(f"Exported {len(formatted_messages)} messages to {output_file}.")

if __name__ == "__main__":
    main()
