import time
import requests
import random
import json
import os
from prompt_toolkit import prompt
from prompt_toolkit.key_binding import KeyBindings
import keyboard


kb = KeyBindings()

@kb.add("c-s")
def _(event):
    event.app.exit(result=event.app.current_buffer.text)



difficulty = ""
language = ""

programming_languages = [
    "python", "javascript", "java", "c", "c++", "c#", "typescript", 
    "php", "ruby", "swift", "kotlin", "go", "rust", "r", "objective-c", 
    "scala", "shell", "powerShell", "perl", "lua", "haskell", "matlab", 
    "groovy", "clojure", "elixir", "dart", "visual basic",
    "sql", "html", "css", "assembly", "fortran", "cobol", "f#", 
    "clojure", "dart", "julia", "r", "scala", "clojure", "erlang", 
    "scheme", "solidity", "clj", "apex", "ada", "bash"
]

key=os.getenv('ERRORDLE_KEY')
url = "https://bazaarlink.ai/api/v1/chat/completions"

if key is None:
    print("Please define the BazaarLink API key in environment variable named ERRORDLE_KEY.")
    print("\nPress Enter to exit Errordle...")
    input()
    raise SystemExit

print("========================")
print("        ERRORDLE")
print("========================")
print("Problem solving - But for programming errors")

print("Loading...")
time.sleep(2.65)
print("\033[H\033[J", end="")

while True:
    difficulty = input("Enter difficulty (easy, medium, hard): ")
    if difficulty.lower() == "easy" or difficulty.lower() == "medium" or difficulty.lower() == "hard":
        break

print("\033[H\033[J", end="")

while True:
    language = input("Enter coding language (anything): ").lower()
    if language in programming_languages:
        break
    else:
        print("Language not in list.")

print("\033[H\033[J", end="")



headers = {
    "Authorization": f"Bearer {key}",
    "Content-Type": "application/json"
}

data = {
    "model": "auto:free",
    "messages": [
        {
            "role": "user",
            "content": f'''You are a professional coding challenge generator for a game called "Errordle".

Your job is to create a realistic production-quality coding sample that contains hidden coding errors. The player must inspect the code and identify the mistakes.

Requirements:

1. Generate a coding challenge with exactly one difficulty level:
   - {difficulty} is the difficulty.
   - MAKE SURE TO USE THE CODING LANGUAGE NAMED {language}!!

2. The code sample:
   - Must be under 40 lines.
   - Must look like real production code written by an experienced developer.
   - Must not contain bad practices, security vulnerabilities, fake shortcuts, useless code, or intentionally messy style.
   - Must be clean, readable, and realistic.
   - Must use a common programming language.
   - Must have only intentional hidden errors. Do not include accidental issues.
   - The code sample does not need to run successfully.
   - The goal is to identify intentional mistakes through code inspection.
   - Errors may include runtime crashes, incorrect output, or incorrect behavior.
   - Every listed error must be visible through careful analysis of the code.
   - Avoid obvious syntax errors unless difficulty is easy.
   - Do not include comments explaining the errors.

3. Error difficulty rules:

Easy:
   - 1 error only.
   - Error should be discoverable by a beginner.
   - Examples:
     - wrong variable name
     - incorrect operator
     - missing condition
     - simple logic mistake

Medium:
   - 1-3 errors.
   - Requires understanding of the language and program behavior.
   - Errors should involve:
     - incorrect logic
     - edge cases
     - incorrect API usage
     - data handling mistakes

Hard:
   - 2-5 errors.
   - Should challenge experienced developers.
   - Errors should involve:
     - subtle logic bugs
     - async behavior
     - state management issues
     - incorrect assumptions
     - performance-related mistakes
     - complex language behavior

4. The generated challenge must include:

- A realistic coding scenario.
- The programming language.
- The difficulty.
- The code sample.
- The number of errors.
- A list of every hidden error.
- Explanation of why each error is wrong.
- The corrected solution code.
- A difficulty justification.

5. Output ONLY valid JSON.
Do not include markdown.
Do not include explanations outside JSON.

JSON format:

{{
  "title": "Short challenge name",
  "difficulty": "easy|medium|hard",
  "code": "Code sample as a string",
  "error_count": 0
}}

Before generating:
- Verify the code is under 40 lines.
- Verify the number of errors matches the selected difficulty.
- Verify every error is intentional and explainable.
- Verify the fixed code removes all errors.
- Verify the challenge is fair and solvable.'''
        }
    ]
}



response = requests.post(
    url,
    headers=headers,
    json=data
)

if response.status_code == 200:
    result = response.json()
elif response.status_code == 429:
    print("Error: API limit exceeded for this session.")
    print("\nPress Enter to exit Errordle...")
    input()
    raise SystemExit
else:
    print("Error: ", response.status_code)
    print("\nPress Enter to exit Errordle...")
    input()
    raise SystemExit
        
print("\033[H\033[J", end="")

data = response.json()

content = data["choices"][0]["message"]["content"]
data = json.loads(content)

print("Errordle #" + str(random.randint(1,5000)) + " | " + data["title"])
print("")
print("HINT: This puzzle has " + str(data["error_count"]) + " error(s).")

text = prompt(
    "Edit code (Ctrl+S to save):\n> ",
    default=data["code"],
    multiline=True,
    key_bindings=kb
)

data2 = {
    "model": "auto:free",
    "messages": [
        {
            "role": "user",
            "content": f'''You are checking a player's answer for an Errordle coding challenge.

Original buggy code:
{data["code"]}

Player's edited code:
{text}

Determine:
Did the player fix all errors?
What errors remain?
Explain briefly and so that the user can understand if anything went wrong or if everything is great.
Do NOT use any formatting (markdown, etc.) because this will output in a terminal and the output will be broken.
'''
        }
    ]
}

response2 = requests.post(
    url,
    headers=headers,
    json=data2
)

if response.status_code == 200:
    result = response.json()
elif response.status_code == 429:
    print("Error: API limit exceeded for this session.")
    raise SystemExit
else:
    print("Error:", response.status_code)
    raise SystemExit

        
result2 = response2.json()
content2 = result2["choices"][0]["message"]["content"]
print(content2)
print("")
print("\nPress Enter to exit Errordle...")
input()


