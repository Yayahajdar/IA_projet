
# CLI Azure
Installation : https://learn.microsoft.com/fr-fr/cli/azure/install-azure-cli  
Documentation az CLI : https://learn.microsoft.com/fr-fr/cli/azure/group?view=azure-cli-latest

Connection à Azure:
```bash
 az login
```

Création de groupe de ressources:
```bash
 RESOURCE_GROUP=ocr-goudot
 LOCATION=francecentral

 az group create --name $RESOURCE_GROUP --location $LOCATION
```

Lister les groupes de ressources (sous forme de table):
```bash
 az group list -o table
```

Création venv:
```bash
 python3 -m venv venv
 source env/bin/activate
 pip install -r requirements.txt
```

# Azure Vision API
Documentation : https://learn.microsoft.com/en-us/azure/ai-services/computer-vision/quickstarts-sdk/image-analysis-client-library-40?tabs=visual-studio%2Clinux&pivots=programming-language-python  
OCR avec curl:
```bash
 IMAGE="https://invoiceocrp3.azurewebsites.net/invoices/FAC_2024_0002-2338479"
 curl -s -H "Ocp-Apim-Subscription-Key: $VISION_KEY" -H "Content-Type: application/json" "$VISION_ENDPOINT/computervision/imageanalysis:analyze?features=caption,read&model-version=latest&language=en&api-version=2024-02-01" -d "{'url':'$IMAGE'}" | jq
```
