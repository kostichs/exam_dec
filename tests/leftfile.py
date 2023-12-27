import requests
import json
valid_sample_add = {
  "id": 92854776000,
  "category": {
    "id": 0,
    "name": "string"
  },
  "name": "doggie",
  "photoUrls": [
    "string"
  ],
  "tags": [
    {
      "id": 0,
      "name": "string"
    }
  ],
  "status": "available"
}

obj = requests.post('https://petstore.swagger.io/v2/pet', json={"id": 999, "name": "sergey", "photoUrls": []})
print(obj.status_code)
