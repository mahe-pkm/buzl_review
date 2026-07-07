# Backend API Integration Requirements Guide

This document outlines the technical requirements and JSON payload specifications for backend developers to implement so that the Google Review Assistant frontend (`https://buzl.rclk.in`) can transition from Mock Mode to your live APIs.

---

## 🔒 1. Cross-Origin Resource Sharing (CORS)
Since the frontend is hosted on `https://buzl.rclk.in` and the API is hosted on `https://dev.web.gobuzl.com`, the API server **MUST** return correct CORS headers to prevent browsers from blocking requests:

*   **Allowed Origin**: `Access-Control-Allow-Origin: https://buzl.rclk.in` (or `*`)
*   **Allowed Headers**: `Access-Control-Allow-Headers: Content-Type, Authorization`
*   **Allowed Methods**: `Access-Control-Allow-Methods: GET, POST, OPTIONS`
*   *Note: Ensure preflight `OPTIONS` requests respond with a `204 No Content` or `200 OK` containing these headers.*

---

## 📋 2. API 1: Fetch Questions (`reviewquestions`)

*   **Method**: `GET`
*   **Endpoint**: `https://dev.web.gobuzl.com/api/locations/{locationId}/reviewquestions`
*   **Headers**:
    *   `Authorization: Basic <base64(locationId + ":")>`

### Expected JSON Response Structure
```json
{
    "resp": {
        "locId": "locn-dev-397",
        "placeId": "ChIJbfT9ntf1qjsRCjeaPBrgenM", 
        "scope": "location",
        "count": 1,
        "questions": [
            {
                "_id": "6a43e328e6de60db9817b7b7",
                "qid": "rvq-9b66a6d5-cd45-4598-a351-c0d486124176",
                "scope": "location",
                "locId": "locn-dev-397",
                "question": "How were the faculty?",
                "responseGuidance": {
                    "location": "Santhiya Chandran IAS Academy",
                    "keyword": "",
                    "aspect": "staff"
                },
                "suggestedResponses": [
                    "Excellent",
                    "Knowledgeable",
                    "Average",
                    "Disappointing"
                ]
            }
        ]
    }
}
```

### Critical Keys for Frontend:
1.  **`resp.placeId`** (or `googlePlaceId`, or `reviewUrl`): Must return the Google Place ID of the business. The frontend uses this to generate the Google Review redirect link. If missing, it defaults to Buzl.
2.  **`questions[0].responseGuidance.location`**: Must return the actual business name. The frontend extracts this to update header logos and instruction subtitles dynamically.

---

## 🔄 3. API 2: Review Generation (`reviewsgeneration`)

*   **Method**: `POST`
*   **Endpoint**: `https://dev.web.gobuzl.com/api/locations/{locationId}/reviewsgeneration`
*   **Headers**:
    *   `Content-Type: application/json`
    *   `Authorization: Basic <base64(locationId + ":")>`

### Expected JSON Request Payload
```json
{
    "language": "en", 
    "writingStyle": "Simple",
    "answers": [
        {
            "qid": "rvq-9b66a6d5-cd45-4598-a351-c0d486124176",
            "response": "Excellent"
        }
    ],
    "customDetail": "The teaching method was superb. Very helpful."
}
```
*Note on `language` mapping*:
*   "English" ➡️ `"en"`
*   "Tamil" ➡️ `"ta"`
*   "Tamil-English Mix" ➡️ `"ta-en"`

### Expected JSON Response Structure
```json
{
    "resp": {
        "status": "complete",
        "sessId": "rv_272889dfaa7e4c23",
        "language": "en",
        "variants": [
            {
                "index": 0,
                "text": "First AI-generated review draft based on the dynamic answers."
            },
            {
                "index": 1,
                "text": "Second alternative review draft based on the dynamic answers."
            }
        ]
    }
}
```

---

## 🛠️ 4. Local Testing & Mock Mode Toggle
The frontend contains a configuration toggle:
```javascript
const host = window.location.hostname;
if (host === 'localhost' || host === '127.0.0.1' || urlParams.get('mock') === 'true') {
  API_CONFIG.isLocalMock = true;
}
```
*   When `isLocalMock` is `true`, it bypasses CORS and basic auth entirely by reading local mock JSON files from the `/API sample json/` directory.
*   Once backend Basic Authentication and CORS are fixed, access the site normally (without `?mock=true`) to fetch from the live endpoints.
