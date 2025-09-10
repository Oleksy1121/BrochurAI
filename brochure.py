from pathlib import Path
from utils import client, MODEL, get_brochure_user_prompt
from prompts import system_prompt

def create_brochure(company_name: str, url: str, filename: str = "output/Brochure.md"):
    Path(filename).parent.mkdir(exist_ok=True)

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": get_brochure_user_prompt(company_name, url)},
        ],
    )
    result = response.choices[0].message.content

    with open(filename, "w", encoding="utf-8") as f:
        f.write(result)

    print(f"Brochure saved to {filename}")
