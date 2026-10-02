# Quote Search Engine

A simple Flask-based search engine that retrieves quotes from an Excel dataset using TF-IDF-based text matching.

The dataset was collected from [What Should I Read Next](https://www.whatshouldireadnext.com/). Searches are performed only against the local dataset, not the live website.

## Features

- Search quotes using a text query.
- Retrieve up to 10 matching results.
- Display each quote alongside its author and source link.
- Access the search interface through a local web application.

## Project Structure

```text
project/
├── app.py               # Flask application and routes
├── project_tfidf2.py     # Text vectorization and search logic
├── data.xlsx            # Quote dataset
├── templates/
│   ├── index.html       # Search page
│   └── result.html      # Results page
└── README.md
```

If your HTML templates reference CSS, JavaScript, or images, place those files in a `static/` directory.

## Requirements

- Python 3
- Flask
- pandas
- scikit-learn
- NumPy
- openpyxl , for reading `.xlsx` files

The `os` module is included in Python's standard library and does not require installation.

## Installation

From the project directory, create a virtual environment:

```bash
python -m venv .venv
```

Activate it:

**Windows:**

```powershell
.venv\Scripts\activate
```

**macOS / Linux:**

```bash
source .venv/bin/activate
```

Install the required libraries:

```bash
python -m pip install Flask pandas scikit-learn numpy openpyxl
```

## Dataset Format

Place `data.xlsx` in the same directory as `project_tfidf2.py`.

The Excel file must contain these columns:

| Column | Description |
|--------|-------------|
| `quote text` | The quote text used for searching |
| `quote author` | The quote's author |
| `quote link` | A link associated with the quote |

The `quote text` column should contain non-empty text values.

## Running the Application

Start the Flask application:

```bash
python app.py
```

Then open the following address in your browser:

```text
http://127.0.0.1:5000
```

Enter a query in the search interface to view results.

The application accepts searches through the `/result` route using the `search` query parameter. For example:

```text
http://127.0.0.1:5000/result?search=friendship
```

## How It Works

### 1. Load the Dataset

The `tfidf2(text)` function reads quotes, authors, and links from `data.xlsx`.

### 2. Build Text Representations

`CountVectorizer` converts quotes into word-count vectors. `TfidfTransformer` calculates inverse document frequency (IDF) weights.

The code then manually multiplies word counts by IDF weights to build document and query vectors.

### 3. Score Quotes

Each quote receives a score based on the dot product of its weighted vector and the query vector.

> **Note:** Although the scoring function is named `cosine_dist`, it currently computes a dot product—not cosine similarity or cosine distance. The vectors are not normalized.

### 4. Return Results

The function selects up to 10 of the highest scores and returns three lists:

```python
quote_2, author_2, link_2
```

Flask passes these lists to `result.html` for display.

## Improving the Search

The core retrieval logic is implemented in `project_tfidf2.py`. Changes to vectorization, scoring, and result selection can generally be made in this file without changing the Flask routes, provided the function's return format stays the same.

Potential improvements include:

- Use normalized TF-IDF vectors and cosine similarity.
- Load the dataset and fit the vectorizer once instead of repeating these steps for every query.
- Keep vectors sparse to reduce memory usage.
- Sort results by score in descending order.
- Select results by row index rather than using `distances.index()`, which can return duplicate rows when scores are equal.
- Handle empty queries, missing values, and queries containing no recognized words.
- Exclude zero-score results when there are no meaningful matches.

### Current Limitations

- The selected scores are returned in ascending order, so the strongest result appears last.
- Equal scores may cause the same quote to appear more than once.
- Queries with no recognized words can still return unrelated results.
- The dataset and text-processing pipeline are rebuilt for every search request.

## Development Notes
 
The application currently enables Flask debug mode. Use this only for local development; disable it and use a production-ready deployment setup before publishing the application.

## Dataset Attribution

Dataset source: [What Should I Read Next](https://www.whatshouldireadnext.com/).

This project searches a local copy of the dataset. Before redistributing the dataset or using it publicly, check the source website's applicable terms and permissions.
