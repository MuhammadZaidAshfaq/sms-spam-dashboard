"""
charts.py — All chart / visualization functions
SMS Spam Collection Dashboard
Course: Exploratory Data Analysis | Instructor: Ali Hassan Sherazi
"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

# ── Consistent colour palette ─────────────────────────────────────────────────
PALETTE    = {'ham': '#27AE60', 'spam': '#E74C3C'}
sns.set_theme(style='whitegrid', font_scale=1.05)
plt.rcParams.update({
    'axes.titlesize'  : 13,
    'axes.titleweight': 'bold',
    'axes.labelsize'  : 10,
})


def _fig_close(fig):
    plt.close(fig)


# ─────────────────────────────────────────────────────────────────────────────
# Chart 1 — Pie Chart
# ─────────────────────────────────────────────────────────────────────────────
def chart_pie(df):
    fig, ax = plt.subplots(figsize=(6, 6))
    counts  = df['label'].value_counts()
    wedges, texts, autotexts = ax.pie(
        counts,
        labels=[l.capitalize() for l in counts.index],
        autopct='%1.1f%%',
        colors=[PALETTE.get(l, '#999') for l in counts.index],
        explode=[0.04] * len(counts),
        startangle=140, shadow=True,
        wedgeprops={'edgecolor': 'white', 'linewidth': 2.5}
    )
    for at in autotexts:
        at.set_fontsize(12); at.set_fontweight('bold')
    ax.set_title('Spam vs Ham Distribution')
    ax.legend(wedges, [f'{l.capitalize()} ({c})' for l, c in zip(counts.index, counts)],
              title='Label', loc='lower right', fontsize=9)
    plt.tight_layout()
    return fig


# ─────────────────────────────────────────────────────────────────────────────
# Chart 2 — Histogram
# ─────────────────────────────────────────────────────────────────────────────
def chart_histogram(df):
    fig, axes = plt.subplots(1, 2, figsize=(12, 4))
    for ax, (col, xlabel) in zip(axes, [
        ('msg_length', 'Message Length (chars)'),
        ('word_count', 'Word Count')
    ]):
        for lbl, grp in df.groupby('label'):
            ax.hist(grp[col], bins=45, alpha=0.65,
                    color=PALETTE.get(lbl, '#999'),
                    label=lbl.capitalize(), edgecolor='white')
        ax.set_title(f'{xlabel} Frequency')
        ax.set_xlabel(xlabel)
        ax.set_ylabel('Frequency')
        ax.legend(title='Label')
    fig.suptitle('Histogram — Message Length & Word Count', fontweight='bold')
    plt.tight_layout()
    return fig


# ─────────────────────────────────────────────────────────────────────────────
# Chart 3 — Line Chart
# ─────────────────────────────────────────────────────────────────────────────
def chart_line(df):
    df2 = df.copy()
    df2['word_bin'] = pd.cut(df2['word_count'], bins=range(0, 65, 5), right=False)
    line_data = (
        df2.groupby(['word_bin', 'label'], observed=True)['msg_length']
        .mean().reset_index()
    )
    fig, ax = plt.subplots(figsize=(12, 4))
    for lbl, grp in line_data.groupby('label'):
        ax.plot(grp['word_bin'].astype(str), grp['msg_length'],
                marker='o', markersize=5,
                color=PALETTE.get(lbl, '#999'),
                label=lbl.capitalize(), linewidth=2.2)
        ax.fill_between(grp['word_bin'].astype(str), grp['msg_length'],
                        alpha=0.1, color=PALETTE.get(lbl, '#999'))
    ax.set_title('Line Chart — Avg Message Length vs Word-Count Range')
    ax.set_xlabel('Word Count Bin')
    ax.set_ylabel('Avg Char Length')
    ax.legend(title='Label')
    plt.xticks(rotation=40, ha='right')
    plt.tight_layout()
    return fig


# ─────────────────────────────────────────────────────────────────────────────
# Chart 4 — Bar Chart
# ─────────────────────────────────────────────────────────────────────────────
def chart_bar(df):
    features = ['msg_length', 'word_count', 'digit_count',
                'upper_count', 'punct_count', 'exclaim_count']
    flabels  = ['Msg Length', 'Word Count', 'Digits',
                'Uppercase', 'Punctuation', 'Exclamations']
    avg_vals = df.groupby('label')[features].mean()
    x, w = np.arange(len(features)), 0.35
    fig, ax = plt.subplots(figsize=(11, 4))
    for i, (lbl, offset) in enumerate(zip(['ham', 'spam'], [-w/2, w/2])):
        if lbl in avg_vals.index:
            bars = ax.bar(x + offset, avg_vals.loc[lbl], w,
                          label=lbl.capitalize(),
                          color=PALETTE[lbl], edgecolor='white')
            for b in bars:
                ax.text(b.get_x() + b.get_width()/2, b.get_height() + 0.3,
                        f'{b.get_height():.1f}', ha='center', va='bottom', fontsize=8)
    ax.set_title('Bar Chart — Avg Feature Values: Ham vs Spam')
    ax.set_xlabel('Feature')
    ax.set_ylabel('Average Value')
    ax.set_xticks(x)
    ax.set_xticklabels(flabels)
    ax.legend(title='Label')
    plt.tight_layout()
    return fig


# ─────────────────────────────────────────────────────────────────────────────
# Chart 5 — Scatter Plot
# ─────────────────────────────────────────────────────────────────────────────
def chart_scatter(df):
    fig, ax = plt.subplots(figsize=(8, 5))
    for lbl, grp in df.groupby('label'):
        ax.scatter(grp['word_count'], grp['msg_length'],
                   alpha=0.3, s=16,
                   color=PALETTE.get(lbl, '#999'),
                   label=lbl.capitalize())
        m, b = np.polyfit(grp['word_count'], grp['msg_length'], 1)
        x_l = np.linspace(grp['word_count'].min(), grp['word_count'].max(), 200)
        ax.plot(x_l, m*x_l + b, color=PALETTE.get(lbl, '#999'),
                linewidth=2, linestyle='--', alpha=0.85)
    ax.set_title('Scatter Plot — Message Length vs Word Count\n(dashed = linear trend)')
    ax.set_xlabel('Word Count')
    ax.set_ylabel('Message Length (chars)')
    ax.legend(title='Label')
    plt.tight_layout()
    return fig


# ─────────────────────────────────────────────────────────────────────────────
# Chart 6 — Box Plot
# ─────────────────────────────────────────────────────────────────────────────
def chart_box(df):
    fig, axes = plt.subplots(1, 3, figsize=(13, 5))
    for ax, (col, ylabel) in zip(axes, [
        ('msg_length',  'Message Length (chars)'),
        ('word_count',  'Word Count'),
        ('upper_count', 'Uppercase Count'),
    ]):
        sns.boxplot(data=df, x='label', y=col, hue='label', palette=PALETTE,
                    order=['ham', 'spam'], legend=False, width=0.45, linewidth=1.4,
                    flierprops={'marker':'o','markersize':3,'alpha':0.4}, ax=ax)
        ax.set_title(ylabel)
        ax.set_xlabel('Label')
        ax.set_ylabel(ylabel)
        ax.set_xticks([0, 1]); ax.set_xticklabels(['Ham', 'Spam'])
    fig.suptitle('Box Plot — Spread, Median & Outliers by Label', fontweight='bold')
    plt.tight_layout()
    return fig


# ─────────────────────────────────────────────────────────────────────────────
# Chart 7 — Heatmap
# ─────────────────────────────────────────────────────────────────────────────
def chart_heatmap(df):
    cols = ['label_binary','msg_length','word_count','digit_count',
            'upper_count','punct_count','exclaim_count','url_flag','avg_word_length']
    names = ['Is Spam','Msg Length','Word Count','Digits',
             'Uppercase','Punctuation','Exclamations','URL Flag','Avg Word Len']
    corr = df[cols].corr()
    corr.index = corr.columns = names
    mask = np.triu(np.ones_like(corr, dtype=bool))
    fig, ax = plt.subplots(figsize=(10, 7))
    sns.heatmap(corr, mask=mask, annot=True, fmt='.2f', annot_kws={'size':8.5},
                cmap='RdYlGn', center=0, vmin=-1, vmax=1,
                linewidths=0.4, square=True,
                cbar_kws={'shrink':0.75, 'label':'Correlation'}, ax=ax)
    ax.set_title('Heatmap — Feature Correlation Matrix')
    plt.tight_layout()
    return fig


# ─────────────────────────────────────────────────────────────────────────────
# Chart 8 — Area Chart
# ─────────────────────────────────────────────────────────────────────────────
def chart_area(df):
    fig, axes = plt.subplots(1, 2, figsize=(13, 4))
    # CDF
    ax = axes[0]
    for lbl, grp in df.groupby('label'):
        sv  = np.sort(grp['msg_length'].values)
        cdf = np.arange(1, len(sv)+1) / len(sv) * 100
        ax.fill_between(sv, cdf, alpha=0.3, color=PALETTE.get(lbl,'#999'))
        ax.plot(sv, cdf, color=PALETTE.get(lbl,'#999'),
                label=lbl.capitalize(), linewidth=2)
    ax.set_title('Area — CDF of Message Length')
    ax.set_xlabel('Message Length (chars)')
    ax.set_ylabel('Cumulative %')
    ax.legend(title='Label')
    # Stacked area
    ax2 = axes[1]
    n   = min(400, len(df))
    idx = np.linspace(0, len(df)-1, n, dtype=int)
    r_ham  = (df['label'].iloc[idx]=='ham').astype(int).rolling(30, min_periods=1).mean()*100
    r_spam = (df['label'].iloc[idx]=='spam').astype(int).rolling(30, min_periods=1).mean()*100
    ax2.stackplot(np.arange(n), r_ham, r_spam, labels=['Ham %','Spam %'],
                  colors=[PALETTE['ham'], PALETTE['spam']], alpha=0.72)
    ax2.set_title('Area — Rolling Ham/Spam % Over Sequence')
    ax2.set_xlabel('Message Index (sampled)')
    ax2.set_ylabel('Rolling Proportion (%)')
    ax2.legend(title='Label', loc='upper right')
    fig.suptitle('Area Charts — Cumulative Trends', fontweight='bold')
    plt.tight_layout()
    return fig


# ─────────────────────────────────────────────────────────────────────────────
# Chart 9 — Count Plot
# ─────────────────────────────────────────────────────────────────────────────
def chart_count(df):
    fig, axes = plt.subplots(1, 2, figsize=(12, 4))
    ax = axes[0]
    sns.countplot(data=df, x='url_label', hue='label', palette=PALETTE,
                  order=['No URL','Has URL'], edgecolor='white', ax=ax)
    for p in ax.patches:
        if p.get_height() > 0:
            ax.annotate(f'{int(p.get_height())}',
                        (p.get_x()+p.get_width()/2, p.get_height()),
                        ha='center', va='bottom', fontsize=8.5)
    ax.set_title('URL Presence by Label')
    ax.set_xlabel('URL Presence'); ax.set_ylabel('Count')
    ax.legend(title='Label', labels=['Ham','Spam'])

    ax2 = axes[1]
    sns.countplot(data=df, x='label', hue='label', palette=PALETTE,
                  order=['ham','spam'], legend=False, edgecolor='white', ax=ax2)
    for p in ax2.patches:
        ax2.annotate(f'{int(p.get_height())}',
                     (p.get_x()+p.get_width()/2, p.get_height()),
                     ha='center', va='bottom', fontsize=9)
    ax2.set_title('Total Ham vs Spam Count')
    ax2.set_xlabel('Label'); ax2.set_ylabel('Count')
    ax2.set_xticks([0, 1]); ax2.set_xticklabels(['Ham','Spam'])

    fig.suptitle('Count Plots — Categorical Frequency', fontweight='bold')
    plt.tight_layout()
    return fig


# ─────────────────────────────────────────────────────────────────────────────
# Chart 10 — Violin Plot
# ─────────────────────────────────────────────────────────────────────────────
def chart_violin(df):
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    for ax, (col, ylabel) in zip(axes, [
        ('word_count', 'Word Count'),
        ('msg_length', 'Message Length (chars)'),
    ]):
        sns.violinplot(data=df, x='label', y=col, hue='label', palette=PALETTE,
                       order=['ham','spam'], legend=False, inner='quartile',
                       linewidth=1.4, ax=ax)
        ax.set_title(f'{ylabel} Distribution')
        ax.set_xlabel('Label'); ax.set_ylabel(ylabel)
        ax.set_xticks([0, 1]); ax.set_xticklabels(['Ham','Spam'])
    fig.suptitle('Violin Plot — Distribution & Probability Density by Label',
                 fontweight='bold')
    plt.tight_layout()
    return fig
