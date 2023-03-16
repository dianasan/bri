import os
from nltk.corpus import stopwords
from numpy import nonzero
from tabulate import tabulate

dataset_encoding = 'latin1'
stopwords = set(stopwords.words('portuguese'))

if __name__ == '__main__':
    #aqui foi preciso fazer a leitura de cada subpasta
    dataset_path = r"C:\obras_machado_assis\miscelanea"
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

# esse faz a busca vetorial pelo cosseno
def vectorial_search(query, td_matrix, vocab, filenames):
    query_vector = []
    for term in query.split():
        if term in vocab:
            query_vector.append(1)
        else:
            query_vector.append(0)

    similarities = []
    for j in range(len(filenames)):
        file_vector = []
        for i in range(len(vocab)):
            row = td_matrix[i]
            file_vector.append(row[j])
        dot_product = sum(a * b for a, b in zip(query_vector, file_vector))
        file_length = sum([i ** 2 for i in file_vector]) ** 0.5
        if file_length != 0:
            cosine_similarity = dot_product / file_length
        else:
            cosine_similarity = 0
        similarities.append((filenames[j], cosine_similarity))

    similarities.sort(reverse=True, key=lambda x: x[1])
    return similarities

# A partir daqui faremos as queries e imprimiremos os resultados

# chamando a função e imprimindo o documento e a similaridade
results1 = vectorial_search("olhos de ressaca", td_matrix, vocab, files_to_read)
print("Resultados para a query olhos de ressaca")
print(tabulate(results1, headers=["Documento", "Similaridade"]))
print("-" * 180)

results2 = vectorial_search("o dinheiro não traz felicidade", td_matrix, vocab, files_to_read)
print("Resultados para a query o dinheiro não traz felicidade")
print(tabulate(results2, headers=["Documento", "Similaridade"]))
print("-" * 180)

results3 = vectorial_search("creia em si", td_matrix, vocab, files_to_read)
print("Resultados para a query creia em si")
print(tabulate(results3, headers=["Documento", "Similaridade"]))
print("-" * 180)

results4 = vectorial_search("quem é bentinho?", td_matrix, vocab, files_to_read)
print("Resultados para a query quem é bentinho?")
print(tabulate(results4, headers=["Documento", "Similaridade"]))
print("-" * 180)