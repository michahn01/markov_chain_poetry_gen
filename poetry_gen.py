import re
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
import random


def read_poems(file_path):
    txt = []
    with open(file_path) as file:
        for line in file:
            line = line.strip()
            if line != '': txt.append(line)
    return txt


# cleans text and classifies words by their parts of speech
def parse_txt(txt):
    cleaned_txt = []
    nouns = set()
    verbs = set()
    adj = set()
    for line in txt:
        line = line.lower()
        line = re.sub(r"[,.\"\'!@#$%^&*(){}?/;`~:<>+=-\\]", "", line)
        tokens = word_tokenize(line)
        words = [word for word in tokens if word.isalpha()]
        tagged_words = pos_tag(words)
        for word in tagged_words:
            if word[1] == "NN":
                nouns.add(word[0])
            elif word[1] == "VB" or word[1] == "VBP":
                verbs.add(word[0])
            elif word[1] == "JJ":
                adj.add(word[0])
        cleaned_txt += words
    return cleaned_txt, nouns, verbs, adj

# creates a Markov model
def make_markov_model(cleaned_stories):
    markov_model = {}
    for i in range(len(cleaned_stories) - 1):
        current_state = cleaned_stories[i]
        next_state = cleaned_stories[i+1]
        if current_state in markov_model:
            if next_state in markov_model[current_state]:
                markov_model[current_state][next_state] += 1
            else:
                markov_model[current_state][next_state] = 1
        else:
            markov_model[current_state] = { next_state : 1 }
        
        
    for current_state, next_states in markov_model.items():
        total_sum = sum(next_states.values())
        for next_state, count in next_states.items():
            markov_model[current_state][next_state] = count / total_sum

    return markov_model

def generate_line(nouns, verbs, adj, markov_model, is_last_line=False):
    curr = random.choice(list(nouns))
    print(curr[0].upper() + curr[1:], end=" ")
    max_value = max(markov_model[curr].values())
    curr = random.choice([key for key, value in markov_model[curr].items() if value == max_value])
    for j in range(6):
        print(curr, end=" ")
        max_value = max(markov_model[curr].values())
        curr = random.choice([key for key, value in markov_model[curr].items() if value == max_value])
    print(curr, end="")
    if curr not in nouns:
        print("", random.choice(list(nouns)), end="")

    if (is_last_line):
        print(".")
    else:
        print(random.choice(["...", ","]))

def generate_poem(num_lines, nouns, verbs, adj, markov_model):
    for i in range(num_lines - 1):
        generate_line(nouns, verbs, adj, markov_model)
    generate_line(nouns, verbs, adj, markov_model, True)


data, nouns, verbs, adj = parse_txt(read_poems("training_data/poems.txt"))
markov_model = make_markov_model(data)

generate_poem(5, nouns, verbs, adj, markov_model)


