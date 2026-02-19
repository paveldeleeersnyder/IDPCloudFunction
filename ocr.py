from google.cloud import vision
import requests

mime_type = "application/pdf"

def get_text_for_pdf(url = None):
    if (url == None):
        raise Exception("Must provide url to pdf")

    print("found url")

    content = requests.get(url).content

    client = vision.ImageAnnotatorClient()

    input_config = vision.InputConfig(
        content=content,
        mime_type="application/pdf",
    )

    feature = vision.Feature(type_=vision.Feature.Type.DOCUMENT_TEXT_DETECTION)

    request = vision.AnnotateFileRequest(features=[feature], input_config=input_config)

    print("sending request")
    response = client.batch_annotate_files(requests=[request])
    print("got response")

    result = ""
    for page in response.responses[0].responses:
        result += page.full_text_annotation.text
    return result