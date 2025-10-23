# 📄 Dodanie Node "Generate HTML Report" w N8N

**Cel:** Wygenerowanie interaktywnego raportu HTML na podstawie JSONa z porównania dokumentów

---

## 🎯 Rozwiązanie - 2 Opcje

### **Opcja A: HTML z wstrzykniętymi danymi (ZALECANE)**

Node wygeneruje kompletny HTML z danymi już załadowanymi - nie trzeba uploadować JSONa.

### **Opcja B: HTML + osobny plik JSON**

Node wygeneruje HTML viewer + osobny plik JSON do pobrania.

---

## 📋 Opcja A: Node "Generate HTML Report" - Krok po Kroku

### 1. Otwórz workflow w N8N

### 2. Dodaj nowy node PO "Final Summary"

**Kliknij `+`** po node "Final Summary" i wybierz **"Code"**

### 3. Nazwa node: "Generate HTML Report"

### 4. Wklej ten kod JavaScript:

```javascript
// Pobierz complete_json z poprzedniego node
const jsonData = $json.complete_json;

// Template HTML - cały result_viewer.html z wstrzykniętymi danymi
const htmlContent = `<!DOCTYPE html>
<html lang="pl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Raport Porównania Dokumentów</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: #F2F2F2;
            color: #595959;
            padding: 20px;
            line-height: 1.6;
        }
        .container {
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
            padding: 30px;
        }
        h1 {
            color: #009597;
            border-bottom: 3px solid #009597;
            padding-bottom: 10px;
            margin-bottom: 30px;
        }
        h2 {
            color: #70A300;
            margin-top: 30px;
            margin-bottom: 15px;
            padding-bottom: 5px;
            border-bottom: 2px solid #70A300;
        }
        h3 { color: #009597; margin-top: 20px; margin-bottom: 10px; }
        .summary-box {
            background: linear-gradient(135deg, #009597 0%, #70A300 100%);
            color: white;
            padding: 30px;
            border-radius: 8px;
            margin: 30px 0;
            text-align: center;
        }
        .summary-box h3 { color: white; border: none; margin: 0 0 20px 0; }
        .summary-stats {
            display: flex;
            justify-content: space-around;
            flex-wrap: wrap;
        }
        .summary-stat { padding: 10px 20px; }
        .summary-stat-value { font-size: 48px; font-weight: bold; }
        .summary-stat-label {
            font-size: 14px;
            opacity: 0.9;
            text-transform: uppercase;
        }
        .statistics {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin: 30px 0;
        }
        .stat-card {
            background: #f9f9f9;
            border-left: 4px solid #009597;
            padding: 20px;
            border-radius: 4px;
        }
        .stat-card.modified { border-left-color: #ED1B2F; }
        .stat-card.added { border-left-color: #70A300; }
        .stat-card.deleted { border-left-color: #ED1B2F; }
        .stat-label {
            font-size: 14px;
            color: #999;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        .stat-value {
            font-size: 36px;
            font-weight: bold;
            color: #595959;
            margin-top: 5px;
        }
        .paragraph {
            margin: 20px 0;
            padding: 20px;
            border-radius: 4px;
            border-left: 5px solid #A6A6A6;
        }
        .paragraph.unchanged { background: #f9f9f9; border-left-color: #A6A6A6; }
        .paragraph.modified { background: #fff3f3; border-left-color: #ED1B2F; }
        .paragraph.added { background: #f0f8e8; border-left-color: #70A300; }
        .paragraph.deleted {
            background: #fff3f3;
            border-left-color: #ED1B2F;
            opacity: 0.7;
        }
        .paragraph-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 10px;
        }
        .paragraph-index { font-weight: bold; color: #595959; }
        .paragraph-type {
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: bold;
            text-transform: uppercase;
        }
        .paragraph-type.unchanged { background: #A6A6A6; color: white; }
        .paragraph-type.modified { background: #ED1B2F; color: white; }
        .paragraph-type.added { background: #70A300; color: white; }
        .paragraph-type.deleted { background: #ED1B2F; color: white; }
        .changes {
            margin-top: 15px;
            padding: 15px;
            background: white;
            border-radius: 4px;
            border: 1px solid #A6A6A6;
        }
        .change-label { font-weight: bold; margin-bottom: 10px; color: #009597; }
        .change-text { line-height: 1.8; }
        .change-equal { color: #595959; }
        .change-delete {
            background: #ffebee;
            color: #c62828;
            text-decoration: line-through;
            padding: 2px 4px;
            border-radius: 2px;
        }
        .change-insert {
            background: #e8f5e9;
            color: #2e7d32;
            font-weight: bold;
            padding: 2px 4px;
            border-radius: 2px;
        }
        .metadata {
            background: #f9f9f9;
            padding: 20px;
            border-radius: 4px;
            margin: 20px 0;
        }
        .metadata-row {
            display: flex;
            padding: 8px 0;
            border-bottom: 1px solid #e0e0e0;
        }
        .metadata-row:last-child { border-bottom: none; }
        .metadata-label {
            font-weight: bold;
            width: 200px;
            color: #009597;
        }
        .metadata-value { color: #595959; }
        .filters {
            margin: 20px 0;
            padding: 20px;
            background: #f9f9f9;
            border-radius: 4px;
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            align-items: center;
        }
        .filter-label { font-weight: bold; color: #595959; }
        .filter-btn {
            padding: 8px 16px;
            border: 2px solid #009597;
            background: white;
            color: #009597;
            border-radius: 4px;
            cursor: pointer;
            transition: all 0.3s;
        }
        .filter-btn.active { background: #009597; color: white; }
        .filter-btn:hover { background: #e8f5f5; }
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 15px 0;
        }
        th, td {
            padding: 12px;
            text-align: left;
            border: 1px solid #A6A6A6;
        }
        th {
            background: #009597;
            color: white;
            font-weight: bold;
        }
        td { background: white; }
        td.modified-cell { background: #fff3f3; }
    </style>
</head>
<body>
    <div class="container">
        <h1>📊 Raport Porównania Dokumentów</h1>

        <!-- Summary -->
        <div class="summary-box">
            <h3>Podsumowanie Porównania</h3>
            <div class="summary-stats">
                <div class="summary-stat">
                    <div class="summary-stat-value" id="totalChanges">0</div>
                    <div class="summary-stat-label">Łącznie Zmian</div>
                </div>
                <div class="summary-stat">
                    <div class="summary-stat-value" id="modifiedCount">0</div>
                    <div class="summary-stat-label">Zmodyfikowane</div>
                </div>
                <div class="summary-stat">
                    <div class="summary-stat-value" id="addedCount">0</div>
                    <div class="summary-stat-label">Dodane</div>
                </div>
                <div class="summary-stat">
                    <div class="summary-stat-value" id="deletedCount">0</div>
                    <div class="summary-stat-label">Usunięte</div>
                </div>
            </div>
        </div>

        <!-- Metadata -->
        <h2>ℹ️ Informacje</h2>
        <div class="metadata" id="metadata"></div>

        <!-- Statistics -->
        <h2>📈 Statystyki</h2>
        <div class="statistics" id="statistics"></div>

        <!-- Filters -->
        <h2>📝 Paragrafy</h2>
        <div class="filters">
            <span class="filter-label">Pokaż:</span>
            <button class="filter-btn active" onclick="filterParagraphs('all')">Wszystkie</button>
            <button class="filter-btn" onclick="filterParagraphs('modified')">Zmodyfikowane</button>
            <button class="filter-btn" onclick="filterParagraphs('added')">Dodane</button>
            <button class="filter-btn" onclick="filterParagraphs('deleted')">Usunięte</button>
            <button class="filter-btn" onclick="filterParagraphs('unchanged')">Niezmienione</button>
        </div>

        <!-- Paragraphs -->
        <div id="paragraphs"></div>

        <!-- Tables -->
        <h2>📋 Tabele</h2>
        <div id="tables"></div>
    </div>

    <script>
        // DANE WSTRZYKNIĘTE AUTOMATYCZNIE
        const fullData = ${JSON.stringify(jsonData)};
        let currentFilter = 'all';

        // Automatyczne wyświetlenie po załadowaniu strony
        window.addEventListener('DOMContentLoaded', () => {
            displayResults();
        });

        function displayResults() {
            displayMetadata();
            displaySummary();
            displayStatistics();
            displayParagraphs();
            displayTables();
        }

        function displayMetadata() {
            const metadata = document.getElementById('metadata');
            const stats = fullData.statistics;

            metadata.innerHTML = \`
                <div class="metadata-row">
                    <div class="metadata-label">Process ID:</div>
                    <div class="metadata-value">\${fullData.process_id}</div>
                </div>
                <div class="metadata-row">
                    <div class="metadata-label">Document Pair ID:</div>
                    <div class="metadata-value">\${fullData.document_pair_id}</div>
                </div>
                <div class="metadata-row">
                    <div class="metadata-label">Wygenerowano:</div>
                    <div class="metadata-value">\${new Date(fullData.generated_at).toLocaleString('pl-PL')}</div>
                </div>
                <div class="metadata-row">
                    <div class="metadata-label">Wszystkich paragrafów:</div>
                    <div class="metadata-value">\${stats.total_paragraphs}</div>
                </div>
                <div class="metadata-row">
                    <div class="metadata-label">Tabel:</div>
                    <div class="metadata-value">\${stats.tables_count || 0}</div>
                </div>
            \`;
        }

        function displaySummary() {
            const stats = fullData.statistics;
            document.getElementById('totalChanges').textContent = stats.total_changes || 0;
            document.getElementById('modifiedCount').textContent = stats.modified_paragraphs || 0;
            document.getElementById('addedCount').textContent = stats.added_paragraphs || 0;
            document.getElementById('deletedCount').textContent = stats.deleted_paragraphs || 0;
        }

        function displayStatistics() {
            const stats = fullData.statistics;
            const container = document.getElementById('statistics');

            container.innerHTML = \`
                <div class="stat-card">
                    <div class="stat-label">Wszystkie</div>
                    <div class="stat-value">\${stats.total_paragraphs || 0}</div>
                </div>
                <div class="stat-card">
                    <div class="stat-label">Niezmienione</div>
                    <div class="stat-value">\${stats.unchanged_paragraphs || 0}</div>
                </div>
                <div class="stat-card modified">
                    <div class="stat-label">Zmodyfikowane</div>
                    <div class="stat-value">\${stats.modified_paragraphs || 0}</div>
                </div>
                <div class="stat-card added">
                    <div class="stat-label">Dodane</div>
                    <div class="stat-value">\${stats.added_paragraphs || 0}</div>
                </div>
                <div class="stat-card deleted">
                    <div class="stat-label">Usunięte</div>
                    <div class="stat-value">\${stats.deleted_paragraphs || 0}</div>
                </div>
                <div class="stat-card">
                    <div class="stat-label">Zmodyfikowane Komórki</div>
                    <div class="stat-value">\${stats.modified_cells || 0}</div>
                </div>
            \`;
        }

        function displayParagraphs() {
            const container = document.getElementById('paragraphs');
            const paragraphs = fullData.paragraphs || [];

            let html = '';

            paragraphs.forEach(para => {
                if (currentFilter !== 'all' && para.type !== currentFilter) {
                    return;
                }

                html += \`
                    <div class="paragraph \${para.type}" data-type="\${para.type}">
                        <div class="paragraph-header">
                            <span class="paragraph-index">Paragraf #\${para.index}</span>
                            <span class="paragraph-type \${para.type}">\${getTypeName(para.type)}</span>
                        </div>
                        <div class="paragraph-content">
                            <strong>Treść:</strong><br>
                            \${escapeHtml(para.text)}
                        </div>
                \`;

                if (para.type === 'modified' && para.changes) {
                    html += \`
                        <div class="changes">
                            <div class="change-label">Zmiany:</div>
                            <div class="change-text">
                                \${renderChanges(para.changes)}
                            </div>
                        </div>
                    \`;

                    if (para.old_text) {
                        html += \`
                            <div style="margin-top: 15px;">
                                <strong>Stara treść:</strong><br>
                                <em style="color: #999;">\${escapeHtml(para.old_text)}</em>
                            </div>
                        \`;
                    }
                }

                if (para.type === 'deleted' && para.old_text) {
                    html += \`
                        <div style="margin-top: 15px;">
                            <strong>Usunięta treść:</strong><br>
                            <em style="color: #999;">\${escapeHtml(para.old_text)}</em>
                        </div>
                    \`;
                }

                html += \`</div>\`;
            });

            if (html === '') {
                html = '<p style="text-align: center; color: #999; padding: 40px;">Brak paragrafów do wyświetlenia</p>';
            }

            container.innerHTML = html;
        }

        function displayTables() {
            const container = document.getElementById('tables');
            const tables = fullData.tables || [];

            if (tables.length === 0) {
                container.innerHTML = '<p style="text-align: center; color: #999; padding: 20px;">Brak tabel w dokumencie</p>';
                return;
            }

            let html = '';

            tables.forEach((table, idx) => {
                html += \`
                    <h3>Tabela #\${table.index}</h3>
                    <div class="table-container">
                        <table>
                \`;

                if (table.rows && table.rows.length > 0) {
                    html += '<thead><tr>';
                    table.rows[0].forEach(cell => {
                        html += \`<th>\${escapeHtml(cell)}</th>\`;
                    });
                    html += '</tr></thead>';

                    html += '<tbody>';
                    for (let i = 1; i < table.rows.length; i++) {
                        html += '<tr>';
                        table.rows[i].forEach((cell, colIdx) => {
                            const isModified = isTableCellModified(table, i, colIdx);
                            html += \`<td class="\${isModified ? 'modified-cell' : ''}">\${escapeHtml(cell)}</td>\`;
                        });
                        html += '</tr>';
                    }
                    html += '</tbody></table>';

                    if (table.changes && table.changes.length > 0) {
                        html += '<div class="changes" style="margin-top: 10px;">';
                        html += '<div class="change-label">Zmiany w tabeli:</div>';
                        html += '<ul>';
                        table.changes.forEach(change => {
                            html += \`<li>Wiersz \${change.row_index}, Kolumna \${change.col_index}:
                                     <span class="change-delete">\${escapeHtml(change.old_value)}</span> �?                                     <span class="change-insert">\${escapeHtml(change.new_value)}</span>
                                     </li>\`;
                        });
                        html += '</ul></div>';
                    }
                }

                html += '</div>';
            });

            container.innerHTML = html;
        }

        function isTableCellModified(table, rowIdx, colIdx) {
            if (!table.changes) return false;
            return table.changes.some(change =>
                change.row_index === rowIdx && change.col_index === colIdx
            );
        }

        function renderChanges(changes) {
            let html = '';
            changes.forEach(change => {
                const text = escapeHtml(change.text);
                if (change.operation === 'delete') {
                    html += \`<span class="change-delete">\${text}</span>\`;
                } else if (change.operation === 'insert') {
                    html += \`<span class="change-insert">\${text}</span>\`;
                } else {
                    html += \`<span class="change-equal">\${text}</span>\`;
                }
            });
            return html;
        }

        function filterParagraphs(type) {
            currentFilter = type;

            document.querySelectorAll('.filter-btn').forEach(btn => {
                btn.classList.remove('active');
            });
            event.target.classList.add('active');

            displayParagraphs();
        }

        function getTypeName(type) {
            const names = {
                'unchanged': 'Niezmieniony',
                'modified': 'Zmodyfikowany',
                'added': 'Dodany',
                'deleted': 'Usunięty'
            };
            return names[type] || type;
        }

        function escapeHtml(text) {
            if (!text) return '';
            const div = document.createElement('div');
            div.textContent = text;
            return div.innerHTML;
        }
    </script>
</body>
</html>`;

// Zwróć HTML jako binary file
return {
  json: {
    success: true,
    message: "HTML report generated successfully",
    filename: `report_${$json.process_id}.html`
  },
  binary: {
    data: Buffer.from(htmlContent, 'utf-8'),
    fileName: `comparison_report_${$json.process_id}.html`,
    mimeType: 'text/html',
    fileExtension: 'html'
  }
};
```

---

## 📊 Jak to działa:

1. **Pobiera JSON** z poprzedniego node (`$json.complete_json`)
2. **Generuje HTML** z całym szablonem result_viewer.html
3. **Wstrzykuje dane** bezpośrednio do JavaScript: `const fullData = ${JSON.stringify(jsonData)};`
4. **Zwraca binary file** - gotowy plik HTML do pobrania

---

## 🔗 Jak podłączyć w workflow:

```
[Final Summary]
       �?[Generate HTML Report] �?NOWY NODE
       �?[Opcjonalnie: Save to Dropbox/Disk]
```

---

## 💾 Co dalej z plikiem HTML?

### Opcja 1: Zapisz do Dropbox

Dodaj node **"Dropbox"** po "Generate HTML Report":

```yaml
Operation: Upload
Path: /BAW_Reports/report_{{ $json.json.filename }}
Binary Data: true
Binary Property: data
```

### Opcja 2: Wyświetl w przeglądarce (tylko development)

Plik HTML będzie dostępny w binary output node - możesz go pobrać ręcznie z N8N UI.

### Opcja 3: Wyślij emailem

Dodaj node **"Send Email"** z attachmentem:

```yaml
Attachments: Binary Property "data"
```

---

## 🧪 Test

Po uruchomieniu workflow:
1. Otwórz node "Generate HTML Report"
2. Zobacz output - będzie:
   - **JSON:** `{ success: true, message: "...", filename: "..." }`
   - **Binary:** Plik HTML gotowy do pobrania
3. Kliknij **"Download Binary"** w N8N UI
4. Otwórz pobrany plik HTML w przeglądarce
5. Raport powinien się wyświetlić automatycznie z wszystkimi danymi! 🎉

---

**Autor:** BAW Project
**Data:** 2025-10-23
