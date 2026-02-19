from google import genai
from google.genai import types
from data import insert_quote
import os
from dotenv import load_dotenv
from typing import TypedDict, List, Optional

load_dotenv()

api_key = os.getenv('AI_API_KEY')

tools = [types.Tool(function_declarations=[types.FunctionDeclaration(
    name="insert_quote",
    description="insert the technical details of a quote to the database",
    parameters={
          "type": "object",
          "required": ["supplier", "date", "terms_and_conditions", "phone_number", "products"],
          "properties": {
            "supplier": {"type": "string", "description": "Supplier name of this quote"},
            "date": {"type": "string", "format": "date", "description": "The date the quote was sent"},
            "terms_and_conditions": {"type": "string", "description": "A short description of the general terms and conditions"},
            "phone_number": {"type": "string", "description": "Phone number of the supplier"},
            "products": {
              "type": "array",
              "items": {
                "type": "object",
                "required": ["amount", "price", "name"],
                "properties": {
                    "amount": {"type": "number", "description": "The amount of times the product was ordered"},
                    "unit": {"type": "string", "description": "A short description of the unit in which the product was ordered (ex. pcs, m, ...) null when it doesn't make sense"},
                    "price": {"type": "number", "description": "Price per unit of product ordered"},
                    "name": {"type": "string", "description": "An identifier of the product which was ordered"},
                }
            }, "description": "A list of the products ordered in the quote"}
          }
        }
    )])]

model = "gemini-2.5-flash"
with open("quote.txt", "r") as file:
    base_prompt = file.read()

def get_quote_details(quote_text):
    prompt = base_prompt + "\n" + quote_text
    history = [types.Content(role="user", parts=[types.Part(text=prompt)])]

    client = genai.Client(api_key=api_key)

    response = generate_response(client, history)

    print(response)

    while response.function_calls != None:
        function_call = response.function_calls[0]
        history.append(response.candidates[0].content)
        call = response.function_calls[0]
        result = insert_quote(function_call.args)
        print(f"Tool called: {result}")
        history.append(types.Content(role="tool", parts=[types.Part.from_function_response(name=function_call.name, response={"result": result})]))
        response = generate_response(client, history)
        
    types.FunctionResponse()

    return response.text

def generate_response(client, history):
    print("sending request to llm")

    return client.models.generate_content(
        model=model,
        contents=history,
        config=types.GenerateContentConfig(
            tools=tools,
        ),
    )