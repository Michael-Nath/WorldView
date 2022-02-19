from nlp import summarize_content, get_sentences

with open("sample_content.txt", "r") as f:
    content = f.read()
    summarize_content(content)

