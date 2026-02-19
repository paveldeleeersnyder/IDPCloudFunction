import os
from dotenv import load_dotenv
from supabase import create_client
import json
from dateutil.parser import parse

load_dotenv()

supabase_url = os.getenv('SUPABASE_URL')
supabase_key = os.getenv('SUPABASE_KEY')

supabase: Client = create_client(supabase_url, supabase_key)

def insert_quote(quote_details):
    print(quote_details)
    print(quote_details.keys())
    mandatory_properties = ["supplier", "date", "terms_and_conditions", "phone_number", "products"]
    for mandatory_property in mandatory_properties:
        if (mandatory_property not in quote_details.keys()):
            return f"your argument is missing {mandatory_property}, keep trying to insert the quote until you get a success."
    
    id = ""
    try:
        date = parse(quote_details["date"])
        response = (
            supabase.table("quotes")
            .insert({"date": date.isoformat(), "terms_and_conditions": quote_details["terms_and_conditions"], "supplier": quote_details["supplier"], "phone_number": quote_details["phone_number"]})
            .execute()
        )
        id = response.data[0]["id"]
    except Exception as e:
        print(repr(e))
        return str(repr(e))

    try:
        for product in quote_details["products"]:
            response = (
                supabase.table("products")
                .insert({"quote_id": id, **product})
                .execute()
            )
    except TypeError:
        return "You did not follow the tools schema, keep trying to insert the data until you reacht the full product details"
    except Exception as e:
        print(repr(e))
        return str(repr(e))

    return "success"