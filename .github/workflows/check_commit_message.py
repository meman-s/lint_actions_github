import sys
import os
from openai import OpenAI


OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)

with open("commit_messages.txt", "r", encoding="utf-8") as f:
    commit_messages = f.readlines()

PROMPT = f"""
You need to check commit messages for compliance with a strict format.

Commit format:
1. It must start with an emoji.
2. After the emoji, there must be a whitespace.
2. After the whitespace, there must be a code repository in parentheses.
3. After the category, there must be a colon, whitespace and a description.
4. The emoji must match the commit message.

Examples of correct commits:
🔥 (requests): Remove async_request_disk_folder_move_to function
🏷️ (commands): Add return type annotation to disk_folder_upload_file command
♻️ (rest_api): Add APICommand classes to __init__.py exports

Here are the commit messages to check:
{commit_messages}

Output "VALID" if all commit messages follow the format.
If there are errors, output "INVALID: <list of errors>".
"""


response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a commit message validator."},
        {"role": "user", "content": PROMPT}
    ]
)

result = response.choices[0].message.content.strip()

if "VALID" in result:
    print("✅ Commit messages are valid")
    sys.exit(0)
else:
    print("❌ Commit messages have problems:")
    print(result)
    sys.exit(1)
