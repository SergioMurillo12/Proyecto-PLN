"""
Script simple hecho por un alumno:
Calcula unigramas y bigramas (con y sin fronteras), genera tablas CSV y las imprime.
Lee el corpus desde un archivo corpus.txt (una oración por línea).
Uso: python n_grams_analysis.py
"""

from collections import Counter
import csv
import os

# Leer corpus desde corpus.txt en la misma carpeta
corpus_file = os.path.join(os.path.dirname(__file__), 'corpus.txt')
with open(corpus_file, 'r', encoding='utf-8') as f:
    corpus = [line.strip() for line in f if line.strip()]

def tokenize(corpus):
    return [sent.lower().split() for sent in corpus]

def build_ngrams(tokenized, use_bounds=False):
    unigrams = Counter()
    bigrams = Counter()
    for sent in tokenized:
        if use_bounds:
            sent_b = ['<s>'] + sent + ['</s>']
        else:
            sent_b = sent
        for w in sent_b:
            unigrams[w] += 1
        for i in range(len(sent_b)-1):
            bigrams[(sent_b[i], sent_b[i+1])] += 1
    return unigrams, bigrams

def save_bigram_table(unigrams, bigrams, out_csv):
    with open(out_csv, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['w_{i-1}','w_i','C(w_{i-1},w_i)','C(w_{i-1})','P(w_i|w_{i-1})'])
        for (w1, w2), c in sorted(bigrams.items()):
            c_w1 = unigrams[w1]
            prob = c / c_w1 if c_w1 > 0 else 0.0
            writer.writerow([w1, w2, c, c_w1, "{:.6f}".format(prob)])

def main():
    tokenized = tokenize(corpus)
    # Sin fronteras
    unigrams, bigrams = build_ngrams(tokenized, use_bounds=False)
    out_dir = os.path.dirname(__file__)
    save_bigram_table(unigrams, bigrams, os.path.join(out_dir, 'bigrams_no_bounds.csv'))
    # Con fronteras
    unigrams_b, bigrams_b = build_ngrams(tokenized, use_bounds=True)
    save_bigram_table(unigrams_b, bigrams_b, os.path.join(out_dir, 'bigrams_with_bounds.csv'))

    print("Tablas generadas en:", out_dir)
    print("- bigrams_no_bounds.csv")
    print("- bigrams_with_bounds.csv")
    print("\nResumen (impreso):\n")
    for (w1, w2), c in sorted(bigrams_b.items()):
        prob = c / unigrams_b[w1]
        print(f"P({w2}|{w1}) = {c}/{unigrams_b[w1]} = {prob:.6f}")

if __name__ == '__main__':
    main()
