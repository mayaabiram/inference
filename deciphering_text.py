import re 

def get_sentences():
    file_path = 'story.txt'
    with open(file_path, 'r') as f:
        text = f.read()
    # split the text into sentences using punctuation marks as delimiters
    sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', text)
    for i in range(len(sentences)):
        sentences[i] = sentences[i].replace('\n', '')
    return sentences
