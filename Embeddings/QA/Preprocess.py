import pandas as pd
import tiktoken
import openai

openai.api_key='Dsk-b6DuOcQzGYepLf3cpzawT3BlbkFJXm6M8TC6yDfkS93NlUoo'

def remove_newlines(serie):
    serie = serie.str.replace('\n', ' ')
    serie = serie.str.replace('  ', ' ')
    return serie

texts=[]

with open("../Data/data.txt", "r",encoding="UTF-8") as f:
            text = f.read()
            texts.append(text.replace('-',' ').replace('_', ' '))

df = pd.DataFrame(texts, columns = ['text'])
df['text'] = remove_newlines(df.text)
df.to_csv('../Data/scraped.csv')



tokenizer = tiktoken.get_encoding("cl100k_base")

df = pd.read_csv('../Data/scraped.csv', index_col=0)
df['n_tokens'] = df.text.apply(lambda x: len(tokenizer.encode(x)))



max_tokens = 256

def split_into_many(text, max_tokens = max_tokens):

    sentences = text.split('. ')
    n_tokens = [len(tokenizer.encode(" " + sentence)) for sentence in sentences]
    
    chunks = []
    tokens_so_far = 0
    chunk = []

    for sentence, token in zip(sentences, n_tokens):
        if tokens_so_far + token > max_tokens:
            chunks.append(". ".join(chunk) + ".")
            chunk = []
            tokens_so_far = 0

        if token > max_tokens:
            continue
        
        chunk.append(sentence)
        tokens_so_far += token + 1

    return chunks
    

shortened = []

for row in df.iterrows():
    if row[1]['text'] is None:
        continue

    if row[1]['n_tokens'] > max_tokens:
        shortened += split_into_many(row[1]['text'])
    else:
        shortened.append( row[1]['text'] )



df = pd.DataFrame(shortened, columns = ['text'])
df['n_tokens'] = df.text.apply(lambda x: len(tokenizer.encode(x)))



df['embeddings'] = df.text.apply(lambda x: openai.Embedding.create(input=x, engine='text-embedding-ada-002')['data'][0]['embedding'])
df.to_csv('../Data/embeddings.csv')

