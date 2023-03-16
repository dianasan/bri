import os
import whoosh
from whoosh.fields import Schema, TEXT, ID
from whoosh import index
from whoosh.qparser import QueryParser
from whoosh import scoring, index
import chardet

# Diretório contendo os arquivos de texto
docs_path = "C:\obras_machado_assis"

# Diretório onde será criado o índice
index_dir = "C:\obras_machado_assis"

# Define o esquema do índice
schema = Schema(title=TEXT(stored=True), path=ID(stored=True), content=TEXT)

# Cria o diretório de índice se ele não existir
if not os.path.exists(index_dir):
    os.mkdir(index_dir)

# Cria o índice
ix = index.create_in(index_dir, schema)

# Abre um escritor para adicionar documentos ao índice
writer = ix.writer()

# Percorre todos os arquivos de texto no diretório e adiciona-os ao índice
for root, dirs, files in os.walk(docs_path):
    for filename in files:
        filepath = os.path.join(root, filename)
        if filename.endswith(".txt"):
            with open(filepath, "rb") as f:
                # Detecta o encoding do arquivo
                encoding = chardet.detect(f.read())["encoding"]
            with open(filepath, "r", encoding=encoding) as f:
                # Lê o conteúdo do arquivo
                content = f.read()
                print(f"Lendo o arquivo {filepath}")

            # Adiciona o documento ao índice
            writer.add_document(title=filename, path=filepath, content=content)

# Finaliza o escritor e fecha o índice
writer.commit()
ix.close()

# Abre o índice
ix = index.open_dir(index_dir)

# Define o modelo de pontuação (BM25)
searcher = ix.searcher(weighting=scoring.BM25F)

# Cria um parser de consultas
query_parser = QueryParser("content", schema=ix.schema)

# Consulta a ser realizada
query_str = "olhos de ressaca"

# Faz a busca
query = query_parser.parse(query_str)
results = searcher.search(query)

# Imprime os resultados
print(f"Encontrados {len(results)} resultados para a consulta '{query_str}':\n")
for hit in results:
    print(f"Título: {hit['title']}")
    print(f"Caminho: {hit['path']}")
    print(f"Pontuação: {hit.score}")
    print("\n")

# Consulta a ser realizada
query_str = "o dinheiro não traz felicidade"

# Faz a busca
query = query_parser.parse(query_str)
results = searcher.search(query)

# Imprime os resultados
print(f"Encontrados {len(results)} resultados para a consulta '{query_str}':\n")
for hit in results:
    print(f"Título: {hit['title']}")
    print(f"Caminho: {hit['path']}")
    print(f"Pontuação: {hit.score}")
    print("\n")

# Consulta a ser realizada
query_str = "creia em si"

# Faz a busca
query = query_parser.parse(query_str)
results = searcher.search(query)

# Imprime os resultados
print(f"Encontrados {len(results)} resultados para a consulta '{query_str}':\n")
for hit in results:
    print(f"Título: {hit['title']}")
    print(f"Caminho: {hit['path']}")
    print(f"Pontuação: {hit.score}")
    print("\n")

# Consulta a ser realizada
query_str = "quem é bentinho? "

# Faz a busca
query = query_parser.parse(query_str)
results = searcher.search(query)

# Imprime os resultados
print(f"Encontrados {len(results)} resultados para a consulta '{query_str}':\n")
for hit in results:
    print(f"Título: {hit['title']}")
    print(f"Caminho: {hit['path']}")
    print(f"Pontuação: {hit.score}")
    print("\n")