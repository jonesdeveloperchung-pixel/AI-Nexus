
## 🖥️ 1. CLI Tool: `zhconvert.py`

### ✅ Features
- Convert between Simplified and Traditional Chinese
- Supports Taiwan/Hong Kong variants
- Easy to integrate into shell scripts or pipelines

### 📦 Setup
```bash
pip install opencc-python-reimplemented
```

### 🧪 Sample CLI Script
```python
# zhconvert.py
import argparse
from opencc import OpenCC

parser = argparse.ArgumentParser(description='Convert between Simplified and Traditional Chinese.')
parser.add_argument('text', help='Text to convert')
parser.add_argument('--mode', default='s2t', choices=[
    's2t', 't2s', 's2tw', 'tw2s', 's2hk', 'hk2s', 't2tw', 'tw2t'
], help='Conversion mode')
args = parser.parse_args()

cc = OpenCC(args.mode)
converted = cc.convert(args.text)
print(converted)
```

### 🧪 Usage
```bash
python zhconvert.py "汉字转换测试" --mode s2t
```

---

## 🌐 2. Web App Integration (Flask + OpenCC)

### 🧰 Backend (Flask)
```python
from flask import Flask, request, jsonify
from opencc import OpenCC

app = Flask(__name__)

@app.route('/convert', methods=['POST'])
def convert():
    data = request.json
    text = data.get('text', '')
    mode = data.get('mode', 's2t')
    cc = OpenCC(mode)
    return jsonify({'converted': cc.convert(text)})
```

### 🧪 Frontend (HTML + JS)
```html
<select id="mode">
  <option value="s2t">简体 → 繁體</option>
  <option value="t2s">繁體 → 简体</option>
</select>
<textarea id="inputText"></textarea>
<button onclick="convert()">Convert</button>
<div id="outputText"></div>

<script>
function convert() {
  fetch('/convert', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({
      text: document.getElementById('inputText').value,
      mode: document.getElementById('mode').value
    })
  })
  .then(res => res.json())
  .then(data => document.getElementById('outputText').innerText = data.converted);
}
</script>
```

---

## 🌏 3. Multilingual UI Toggle

### 🧩 Strategy
- Use `lang` attribute or i18n libraries (e.g., `i18next`, `vue-i18n`)
- Provide UI labels in Traditional Chinese, Simplified Chinese, and English
- Store user preference in localStorage or cookies

### 🧪 Sample Toggle (HTML)
```html
<select id="language" onchange="setLanguage(this.value)">
  <option value="en">English</option>
  <option value="zh-Hans">简体中文</option>
  <option value="zh-Hant">繁體中文</option>
</select>
```

### 🧪 Sample JS i18n Mapping
```javascript
const translations = {
  'en': { convert: 'Convert', input: 'Input Text' },
  'zh-Hans': { convert: '转换', input: '输入文本' },
  'zh-Hant': { convert: '轉換', input: '輸入文字' }
};

function setLanguage(lang) {
  document.getElementById('convertBtn').innerText = translations[lang].convert;
  document.getElementById('inputLabel').innerText = translations[lang].input;
}
```
