from google import genai
from google.genai.types import GenerateContentConfig, HttpOptions
import data

class Quote:
    def __init__(self):
        self.a = 5

insert_quote_input = {
    "supplier": str,
    "date": str,
    "terms_and_conditions": str,
    "phone_number": str,
    "products": list[
        {
            "amount": int,
            "unit": str,
            "price": float,
            "name": str
        }
    ]
}

model = "gemini-2.5-flash"
with open("quote.txt", "r") as file:
    base_prompt = file.read()

def get_quote_details(quote_text):
    prompt = base_prompt + "\n" + text_from_quote

    client = genai.Client(http_options=HttpOptions(api_version="v1"))

    response = client.models.generate_content(
    model=model,
    contents=prompt,
    config=GenerateContentConfig(
        tools=[insert_quote_tool],
        temperature=0,
    ),
)

def insert_quote_tool(quote: {"some": insert_quote_input}) -> str:
    """Method for inserting details of a quote into database.

    Args:
        object with supplier and product info:
        {"supplier": str,
        "date": str,
        "terms_and_conditions": str,
        "phone_number": str,
        "products": list[
            {
                "amount": int,
                "unit": str,
                "price": float,
                "name": str
            }
        ]}
    """

    return data.insert_quote(insert_quote_input)