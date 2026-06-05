"""
filters.py — Data filtering & preprocessing functions
SMS Spam Collection Dashboard
Course: Exploratory Data Analysis | Instructor: Ali Hassan Sherazi
"""

import pandas as pd
import numpy as np
import os
import re

# Folder where THIS file lives — makes paths work no matter where you run from
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def load_data(filepath=None):
    """Load the SMS Spam Collection dataset. DO NOT rename the file.

    Searches several likely locations so it works locally AND on Streamlit Cloud.
    """
    # Candidate locations to try, in order
    candidates = []
    if filepath:
        candidates.append(filepath)
    candidates += [
        os.path.join(BASE_DIR, 'data', 'SMSSpamCollection'),
        os.path.join(BASE_DIR, 'data', 'SMSSpamCollection.csv'),
        os.path.join(BASE_DIR, 'SMSSpamCollection'),
        'data/SMSSpamCollection',
        'SMSSpamCollection',
    ]

    found = next((p for p in candidates if os.path.exists(p)), None)
    if found is None:
        raise FileNotFoundError(
            "Could not find 'SMSSpamCollection'. Make sure the file is in the "
            "'data/' folder next to app.py. Tried: " + ", ".join(candidates)
        )

    df = pd.read_csv(
        found,
        sep='\t',
        header=None,
        names=['label', 'message'],
        encoding='utf-8'
    )
    return df


def clean_and_engineer(df):
    """Clean data and add engineered features. Returns a processed DataFrame."""
    df = df.copy()

    # Basic cleaning
    df.drop_duplicates(inplace=True)
    df.reset_index(drop=True, inplace=True)
    df['label']   = df['label'].str.strip().str.lower()
    df['message'] = df['message'].str.strip()
    df.dropna(inplace=True)

    # Engineered features
    df['msg_length']      = df['message'].apply(len)
    df['word_count']      = df['message'].apply(lambda x: len(x.split()))
    df['char_count']      = df['message'].apply(len)
    df['digit_count']     = df['message'].apply(lambda x: sum(c.isdigit() for c in x))
    df['upper_count']     = df['message'].apply(lambda x: sum(c.isupper() for c in x))
    df['punct_count']     = df['message'].apply(
        lambda x: sum(not c.isalnum() and not c.isspace() for c in x))
    df['exclaim_count']   = df['message'].str.count(r'!')
    df['url_flag']        = df['message'].str.contains(
        r'http|www|\.com', case=False, regex=True).astype(int)
    df['avg_word_length'] = df['message'].apply(
        lambda x: round(np.mean([len(w) for w in x.split()]), 2) if x.split() else 0)
    df['label_binary']    = (df['label'] == 'spam').astype(int)
    df['url_label']       = df['url_flag'].map({0: 'No URL', 1: 'Has URL'})

    return df


# ─────────────────────────────────────────────────────────────────────────────
# FILTER FUNCTIONS (all connected to charts in app.py)
# ─────────────────────────────────────────────────────────────────────────────

def apply_filters(
    data,
    label_filter=None,
    msg_len_range=(0, 1000),
    word_count_range=(0, 200),
    url_filter=None,
    keyword=''
):
    """
    Apply all dashboard filters simultaneously.

    Parameters
    ----------
    data             : pd.DataFrame — cleaned dataset
    label_filter     : str  — 'ham' | 'spam' | None (all)
    msg_len_range    : tuple(int, int) — min/max character length
    word_count_range : tuple(int, int) — min/max word count
    url_filter       : str  — 'Has URL' | 'No URL' | None (all)
    keyword          : str  — keyword to search in message text

    Returns
    -------
    pd.DataFrame — filtered copy, index reset
    """
    filtered = data.copy()

    # ── Category filter (dropdown) ────────────────────────────────────────────
    if label_filter and label_filter.lower() not in ('all', ''):
        filtered = filtered[filtered['label'] == label_filter.lower()]

    # ── Numerical range sliders ───────────────────────────────────────────────
    filtered = filtered[
        (filtered['msg_length']  >= msg_len_range[0])    &
        (filtered['msg_length']  <= msg_len_range[1])    &
        (filtered['word_count']  >= word_count_range[0]) &
        (filtered['word_count']  <= word_count_range[1])
    ]

    # ── Multi-select: URL filter ──────────────────────────────────────────────
    if url_filter and url_filter not in ('All', ''):
        filtered = filtered[filtered['url_label'] == url_filter]

    # ── Text / keyword search ─────────────────────────────────────────────────
    if keyword.strip():
        filtered = filtered[
            filtered['message'].str.contains(keyword.strip(), case=False, na=False)
        ]

    return filtered.reset_index(drop=True)


def reset_filters(data):
    """Return a clean unfiltered copy of the full dataset."""
    return data.copy()


def get_kpis(data):
    """Return a dict of KPI values for the summary cards."""
    total    = len(data)
    spam_n   = (data['label'] == 'spam').sum()
    ham_n    = (data['label'] == 'ham').sum()
    return {
        'total'      : total,
        'spam_count' : int(spam_n),
        'ham_count'  : int(ham_n),
        'spam_pct'   : round(spam_n / total * 100, 1) if total else 0,
        'avg_length' : round(data['msg_length'].mean(), 1) if total else 0,
        'max_length' : int(data['msg_length'].max()) if total else 0,
        'url_pct'    : round(data['url_flag'].mean() * 100, 1) if total else 0,
        'avg_words'  : round(data['word_count'].mean(), 1) if total else 0,
    }
