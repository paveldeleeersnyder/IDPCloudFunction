# IDP in google cloud function

Dit is de Proof-Of-Concept om offertes te verwerken binnen een google cloud function.  
Een google cloud function is zeer gelijkaardig als een container hosten in de google cloud, maar in plaats van een container te voorzien, lever je enkel de code, en staat google in voor de omgeving te voorzien.  
Deze code maakt geen gebruik van docTR of Ollama, deze componenten vereisen namelijk meer infrastructuur dan wat haalbaar is binnen een cloud functio.  
In de plaats spreek ik de google cloud equivalenten aan van deze componenten, de google vision API en de google AI API (Gemini).

## Vision API

De vision API is niet standaard ingeschakeld op de google cloud. Je kan het [hier](https://console.cloud.google.com/marketplace/product/google/vision.googleapis.com?q=search&referrer=search&hl=nl) aanzetten.

## Google AI API

Ook voor de LLM moet je in google's AI studio de API inschakelen en koppelen aan een billing account.  
Vervolgens kan je een API key laten genereren, deze moet je in de .env file plaatsen onder `AI_API_KEY`.
Je kan AI studio [hier]([https://aistudio.google.com/api-keys](https://aistudio.google.com/api-keys)) bereiken.

## Supabase

Om de details in te voeren in supabase zijn ook een supabase url en key nodig.  
De url heeft het volgende formaat: `https://<project-id>.supabase.co`.   
De key kan je op [deze pagina](https://supabase.com/dashboard/project/nfqziitzsforksgauqvv/settings/api-keys) terugvinden.

## Local development

Om de app Lokaal uit te voeren moet je ingelogt zijn in de google cloud met het `gcloud` commando.  
Je kan de volgende commando's hiervoor gebruiken:  
```
gcloud auth application-default login
gcloud auth application-default set-quota-project PROJECT_ID
```

vervolgens kan je de app starten met `functions-framework --target=idp_http`

## App hosten

Om de app te hosten in de google cloud begin je met een nieuwe function service aan te maken. Onder "Write a function" kan je voor de taal python kiezen.  
Je kan deze function een naam geven zoals je zelf wil, kies Python 3.14 als runtime, allow public access, en onder 'Containers, networking, security', heb je 'Variables & Secrets'. Hier kan je dezelfde env variablen meegeven als in de .env file.  
Ondertussen is het best om de request timeout te verhogen zodat grote offertes niet onderbroken worden.  
Wanneer je de function hebt gemaakt kan je dezelfde files aanmaken als degene in deze repo, en de code overkopieren.  
Na op de 'Save and redeploy' knop te drukken is de function live en kan je het bereiken met de URL die zichtbaar is op de pagina.