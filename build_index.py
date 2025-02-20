import json
import sys
sys.setrecursionlimit(5000)  # Increase limit to allow deep nesting

def build_index(input_file, output_file):
    trie = {}

    with open(input_file, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            
            # Extract key (prefix) and store full sentence
            words = line.split()  # Use words as search keys
            for word in words:
                node = trie
                for char in word.lower():  # Convert to lowercase for case-insensitive search
                    if char not in node:
                        node[char] = {}
                    node = node[char]
                if "_messages" not in node:
                    node["_messages"] = []
                if line not in node["_messages"]:
                    node["_messages"].append(line)  # Store unique results

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(trie, f, ensure_ascii=False)

    print(f"Search index saved to {output_file}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python build_index.py <input.txt> <output.json>")
        sys.exit(1)

    build_index(sys.argv[1], sys.argv[2])
