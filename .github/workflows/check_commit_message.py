import os
import sys
import requests

API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-mnli"
HF_API_KEY = os.getenv("HF_API_KEY")

with open("commit_messages.txt", "r", encoding="utf-8") as file:
    commit_messages = file.read().strip().split('\n')

commit_messages = [msg for msg in commit_messages if not msg.lower().startswith("merge")]

PROMPT_TEMPLATE = """
You need to check the following commit message for compliance with a strict format.

Commit format:
1. It must start with an emoji.
2. After the emoji, there must be a whitespace.
3. After the whitespace, there must be a code repository in parentheses.
4. After the category, there must be a colon, whitespace, and a description.
5. The emoji must match the commit message.

Examples of correct commits:
🔥 (requests): Remove async_request_disk_folder_move_to function
🏷️ (commands): Add return type annotation to disk_folder_upload_file command
♻️ (rest_api): Add APICommand classes to __init__.py exports

Commit message to check:
"{commit_message}"

Output only "VALID" if the commit message follows the format.
If there are errors, output "INVALID: <list of errors>".
"""

headers = {"Authorization": f"Bearer {HF_API_KEY}"}

VALID = True

for message in commit_messages:
    prompt = PROMPT_TEMPLATE.format(commit_message=message)
    payload = {"inputs": prompt}
    print(payload)
    response = requests.post(API_URL, headers=headers,
                             json=payload, timeout=30)
    result = response.json()
    print(result)

    output = result.get("generated_text", "") if isinstance(
        result, dict) else str(result)

    if "VALID" in output:
        print(f"✅ Commit message is valid: {message}")
    else:
        print(f"❌ Invalid commit message: {message}")
        print(f"Reason: {output}")
        VALID = False

if VALID:
    sys.exit(0)
else:
    sys.exit(1)
