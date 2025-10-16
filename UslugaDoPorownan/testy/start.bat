UPLOAD_RESPONSE=$(curl -s -X POST http://localhost:8001/api/documents/upload -F "old_document=@stary.docx" -F "new_document=@nowy.docx")

DOCUMENT_PAIR_ID=$(echo $UPLOAD_RESPONSE | jq -r '.document_pair_id')
echo "Document Pair ID: $DOCUMENT_PAIR_ID"

# 2. Rozpocznij przetwarzanie
PROCESS_RESPONSE=$(curl -s -X POST http://localhost:8001/api/process -H "Content-Type: application/json" -d "{\"document_pair_id\": \"$DOCUMENT_PAIR_ID\"}")

PROCESS_ID=$(echo $PROCESS_RESPONSE | jq -r '.process_id')
echo "Process ID: $PROCESS_ID"

# 3. Sprawdzaj status (pętla)
while true; do
  STATUS=$(curl -s http://localhost:8001/api/status/$PROCESS_ID | jq -r '.status')
  echo "Status: $STATUS"

  if [ "$STATUS" = "completed" ]; then
    break
  elif [ "$STATUS" = "error" ]; then
    echo "Błąd podczas przetwarzania!"
    exit 1
  fi

  sleep 2
done

# 4. Pobierz wyniki
curl -s http://localhost:8001/api/result/$PROCESS_ID/full > full_result.json
curl -s http://localhost:8001/api/result/$PROCESS_ID/modified > modified.json
curl -s http://localhost:8001/api/result/$PROCESS_ID/added > added.json
curl -s http://localhost:8001/api/result/$PROCESS_ID/deleted > deleted.json

echo "Wyniki zapisane w plikach JSON"