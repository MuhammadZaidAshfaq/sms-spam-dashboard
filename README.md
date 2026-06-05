# 📩 SMS Spam Collection — Data Visualization Dashboard

**Course:** Exploratory Data Analysis  
**Instructor:** Ali Hassan Sherazi  
**Submission Date:** 05-June-2026  

---

## 📁 Project Structure

```
dashboard_project/
├── data/
│   └── SMSSpamCollection          ← EXACT original file name (do NOT rename)
├── notebooks/
│   └── analysis.ipynb             ← Full EDA notebook (run this first)
├── charts/                        ← Auto-generated chart images
├── app.py                         ← Main Streamlit dashboard
├── charts.py                      ← All 10 chart functions
├── filters.py                     ← Filter & preprocessing functions
├── requirements.txt               ← Python dependencies
└── README.md                      ← This file
```

---

## ⚙️ Installation

```bash
# 1. Clone / unzip the project folder
cd dashboard_project

# 2. (Optional) create a virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt
```

---

## ▶️ Running the Dashboard

```bash
streamlit run app.py
```

Open your browser at **http://localhost:8501**

---

## 📓 Running the Jupyter Notebook

```bash
cd notebooks
jupyter notebook analysis.ipynb
```

Run all cells top-to-bottom (Kernel → Restart & Run All).  
Charts are saved to the `charts/` folder automatically.

---

## 📊 Charts Included

| # | Chart Type   | Insight Shown                                |
|---|--------------|----------------------------------------------|
| 1 | Pie Chart    | Spam vs Ham proportional split               |
| 2 | Histogram    | Message length & word count frequency        |
| 3 | Line Chart   | Avg message length across word-count bins    |
| 4 | Bar Chart    | Average feature values: Ham vs Spam          |
| 5 | Scatter Plot | Message length vs word count (with trend)    |
| 6 | Box Plot     | Spread, median, outliers for key features    |
| 7 | Heatmap      | Feature correlation matrix                   |
| 8 | Area Chart   | CDF of message length + rolling proportions  |
| 9 | Count Plot   | URL presence & label frequency counts        |
|10 | Violin Plot  | Distribution density — word count & length   |
| ★ | Pair Plot    | Multi-feature relationships (bonus)          |

---

## 🔍 Dashboard Filters

All filters are connected to **all 10 charts** and update dynamically:

| Filter | Description |
|--------|-------------|
| Category Filter | Dropdown — All / Ham / Spam |
| Message Length Slider | Min–max character length range |
| Word Count Slider | Min–max word count range |
| URL Multi-Select | All / No URL / Has URL |
| Keyword Search | Free-text search in message content |
| Reset Button | Restores all filters to default |

---

## 💡 Key Insights

1. **Class Imbalance** — ~86.6% of messages are Ham, only ~13.4% Spam.
2. **Message Length** — Spam messages are ~2.5× longer than Ham on average.
3. **Uppercase Usage** — Spam contains significantly more uppercase letters, a strong spam signal.
4. **URLs** — A much higher proportion of spam messages contain URLs compared to Ham.
5. **Digits** — Spam contains more digits (phone numbers, prize amounts, promo codes).
6. **Best Features** for classification: `msg_length`, `upper_count`, `digit_count`, `url_flag`.

---

## 🛠️ Tech Stack

| Tool | Role |
|------|------|
| Python 3.x | Core language |
| Pandas | Data loading, cleaning, filtering |
| NumPy | Numerical operations |
| Matplotlib | Core chart creation |
| Seaborn | Statistical visualizations |
| Streamlit | Interactive dashboard frontend |
| Jupyter | EDA notebook environment |
