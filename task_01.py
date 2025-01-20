import matplotlib.pyplot as plt
import requests
import string
from concurrent.futures import ThreadPoolExecutor
from collections import defaultdict

def get_text(url):
    try:
        response = requests.get(url)
        response.raise_for_status() 
        return response.text
    except requests.RequestException as e:
        print(f"Failed to retrieve data: {e}")
        return None

def remove_punctuation(text):
    return text.translate(str.maketrans("", "", string.punctuation))

def map_function(word):
    return word.lower(), 1

def shuffle_function(mapped_values):
    shuffled = defaultdict(list)
    for key, value in mapped_values:
        shuffled[key].append(value)
    return shuffled.items()

def reduce_function(key_values):
    key, values = key_values
    return key, sum(values)

def map_reduce(text):
    text = remove_punctuation(text)
    words = text.split()

    with ThreadPoolExecutor() as executor:
        mapped_values = list(executor.map(map_function, words))

    shuffled_values = shuffle_function(mapped_values)

    with ThreadPoolExecutor() as executor:
        reduced_values = list(executor.map(reduce_function, shuffled_values))

    return dict(reduced_values)

def visualize_top_words(word_counts, top_n=10):
    top_words = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)[:top_n]
    words, frequencies = zip(*top_words)
    
    plt.figure(figsize=(10, 5))
    plt.bar(words, frequencies, color='blue')
    plt.xlabel('Words')
    plt.ylabel('Frequency')
    plt.title('Top 10 Most Frequent Words')
    plt.xticks(rotation=45)
    plt.show()

if __name__ == "__main__":
    url = "https://www.gutenberg.org/files/2600/2600-0.txt"
    text = get_text(url)
    if text:
        word_counts = map_reduce(text)
        visualize_top_words(word_counts)
    else:
        print("Error: Could not retrieve the text.")
