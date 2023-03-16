import os
from nltk.corpus import stopwords
from numpy import nonzero
from tabulate import tabulate
import re

dataset_encoding = 'latin1'
stopwords = set(stopwords.words('portuguese'))

if __name__ == '__main__':
    # aqui foi preciso fazer a leitura de cada subpasta
    dataset_path = r"C:\obras_machado_assiss\"
    vocab = {}
    # matrix termo-documento binaria
    binary_td_matrix = []
    # matrix termo-documento com pesos tf
    td_matrix = []
    idf = []

    j = 0

    files_to_read = os.listdir(dataset_path)
    for filename in files_to_read:
        filepath = os.path.join(dataset_path, filename)
        with open(filepath, 'r', encoding=dataset_encoding) as f:
            contentfile = f.read()
            tokens_file = contentfile.split()

            # remover stopwords
            tokens_file = [token for token in tokens_file if token.lower() not in stopwords]

            for token in tokens_file:
                if not (token in vocab.keys()):
                    vocab[token] = len(vocab)
                    binary_td_matrix.append([0] * len(tokens_file))
                    td_matrix.append([0] * len(tokens_file))
                    idf.append(0)

                if td_matrix[vocab[token]][j] == 0:
                    idf[vocab[token]] += 1

                binary_td_matrix[vocab[token]][j] = 1
                td_matrix[vocab[token]][j] += 1

            print("-" * 180)
            print("Numero de termos no vocabulario: ", len(vocab))
            print("Numero de colunas nas matrizes termo-documento: ", len(binary_td_matrix[0]))

        j += 1


# busca booleana com o coeficiente de dice
def boolean_search_dice(query, td_matrix, vocab, filenames):
    # criar um conjunto com os índices dos documentos que contêm pelo menos um termo da query
    file_indices = set()
    terms = query.split()

    for term in terms:
        if term in vocab:
            file_indices |= set([i for i, x in enumerate(td_matrix[vocab.get(term)]) if x > 0])

    # calcular a similaridade Dice para cada documento em relação à query
    similarities = {}
    for i in file_indices:
        file_terms = set([j for j, x in enumerate(td_matrix) if x[i] > 0])
        intersection = len(set(terms)) & (len(file_terms))
        denominator = len(terms) + len(file_terms)
        if denominator != 0:
            similarity = 2 * intersection / denominator
            similarities[filenames[i]] = similarity

    # retornar os documentos em ordem decrescente de similaridade
    return sorted(similarities.items(), key=lambda x: x[1], reverse=True)

# A partir daqui faremos as queries e imprimiremos os resultados

results1 = boolean_search_dice("olhos de ressaca", td_matrix, vocab,files_to_read)
print("Resultados para a query olhos de ressaca")
print(tabulate(results1, headers=["Documento", "Similaridade"]))
print("-" * 180)

results2 = boolean_search_dice("o dinheiro não traz felicidade", td_matrix, vocab,files_to_read)
print("Resultados para a query o dinheiro não traz felicidade")
print(tabulate(results2, headers=["Documento", "Similaridade"]))
print("-" * 180)

results3 = boolean_search_dice("creia em si", td_matrix, vocab,files_to_read)
print("Resultados para a query creia em si")
print(tabulate(results3, headers=["Documento", "Similaridade"]))
print("-" * 180)

consulta4 = "quem é bentinho?"
consulta_tratada = re.sub(r'\?', '', consulta4)

results4 = boolean_search_dice(consulta_tratada, td_matrix, vocab, files_to_read)
print("Resultados para a query quem é bentinho?")
print(tabulate(results4, headers=["Documento", "Similaridade"]))
print("-" * 180)


