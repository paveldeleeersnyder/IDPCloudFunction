import functions_framework
from ocr import get_text_for_pdf
from llm import get_quote_details
import logging

@functions_framework.http
def idp_http(request):
    json = request.get_json(silent=True)
    url = json["url"]
    quote_id = json["quoteId"]

    text = get_text_for_pdf(url)
    logging.debug(text)
    result = get_quote_details(text)

    return result