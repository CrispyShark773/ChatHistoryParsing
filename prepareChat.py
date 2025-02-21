import json
import sys
import os

# Define filtering dictionaries
dict_id = {
    # "user1965673897": True
}

dict_content = {
    # "小支星": True,
    # "小只星": True,
    # "小嘟星": True,
    # "支宝": True
}

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
            sender_id = message["from_id"]
            text_content = "".join(entity.get("text", "") for entity in message["text_entities"] if entity.get("type") == "plain")

            # Skip empty messages
            if not text_content.strip():
                continue

            # Filtering logic
            match_id = bool(dict_id) and sender_id in dict_id
            match_content = bool(dict_content) and any(keyword in text_content for keyword in dict_content)

            if dict_id or dict_content:  # Apply filters only if at least one dictionary is non-empty
                if not (match_id or match_content):
                    continue  # Skip messages that do not match any filter

            filtered_messages.append(f"{{{sender}}}{text_content}")

    return filtered_messages

def main():
    if len(sys.argv) < 3:
        print("Usage: python prepareChat.py <ChatHistory.json> <output.txt> [--replace]")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]
    replace = "--replace" in sys.argv  # Check for the new --replace argument

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
