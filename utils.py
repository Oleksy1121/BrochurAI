import json
import os
from dotenv import load_dotenv
from openai import OpenAI
from scraper import Website
from prompts import link_system_prompt, system_prompt

load_dotenv(override=True)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
MODEL = "gpt-4o-mini"


def get_links_user_prompt(website: Website) -> str:
    user_prompt = f"Here is the list of links on the website of {website.url}:\n"
    user_prompt += "Please decide which of these are relevant web links for a brochure about the company.\n"
    user_prompt += "\n".join(website.links)
    return user_prompt


def get_links(url: str) -> dict:
    website = Website(url)
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": link_system_prompt},
            {"role": "user", "content": get_links_user_prompt(website)}
        ],
        response_format={"type": "json_object"},
    )
    return json.loads(response.choices[0].message.content)


def get_brochure_user_prompt(company_name: str, url: str, max_chars: int = 20000) -> str:
    from scraper import Website
    details = "Landing page:\n" + Website(url).get_contents()
    links = get_links(url)
    for link in links["links"]:
        details += f"\n\n{link['type']}\n"
        details += Website(link["url"]).get_contents()
    prompt = f"You are looking at company called {company_name}\n"
    prompt += "Here are the contents of its landing page and other relevant pages.\n"
    prompt += details
    return prompt[:max_chars]
