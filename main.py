import re
import tkinter as tk
from tkinter import ttk
import gensim
import self as self
from gensim import corpora
from nltk.corpus import stopwords
from collections import defaultdict
 

# Preprocess text by removing special characters and lowercasing
def preprocess_text(text):
    text = re.sub('[^a-zA-Z]', ' ', text)
    text = text.lower()
    text = text.split()
    return text


# Remove stop words -the,in,with,etc. from text
def remove_stopwords(text):
    stop_words = set(stopwords.words('english')) 
    return [word for word in text if word not in stop_words]


# Get important words from text
def get_important_words(text, num_topics=5, num_words=10):
    # Tokenize text and create dictionary
    processed_text = preprocess_text(text)
    processed_text = remove_stopwords(processed_text)
    dictionary = corpora.Dictionary([processed_text])

    # Create bag-of-words representation of text 
    bow_text = dictionary.doc2bow(processed_text)

    # Train LDA model
    lda_model = gensim.models.LdaModel(corpus=[bow_text], id2word=dictionary, num_topics=num_topics)

    # Get most important words for each topic
    important_words = []
    for topic_id, topic in lda_model.print_topics(num_topics=num_topics, num_words=num_words):
        topic_words = [word for word, _ in lda_model.show_topic(topic_id, num_words)]
        important_words.extend(topic_words)

    # Count frequency of each important word in text
    word_counts = defaultdict(int)
    for word in processed_text:
        if word in important_words:
            word_counts[word] += 1

    return sorted(word_counts.items(), key=lambda x: x[1], reverse=True)


def clear_default_text():
    if self.text_input.get("1.0", "end-1c") == "Write your text here":
        self.text_input.delete("1.0", "end")


class MainWindow:

    def __init__(self, master):
        self.master = master
        self.master.title("Important Word Extractor")
        self.master.geometry("500x500")
        self.master.resizable(False, False)
        self.master.configure(background="#38c788")

        # Create widgets
        self.label = ttk.Label(self.master, text="Enter Your Text:", background="#C73877", borderwidth=8,  relief="groove", font=("Lucida Sans Unicode", 18))
        self.label.pack(pady=10)
 
        self.text_input = tk.Text(self.master, height=30, width=70, borderwidth=10, relief="raised")
        self.text_input.insert("1.0", "Write your text here")
        self.text_input.bind("<FocusIn>", self.clear_default_text)
        self.text_input.pack(pady=10, padx=20)

        self.button = ttk.Button(self.master, text="Submit", command=self.get_important_words, width=20, style='submit.TButton')
        self.button.pack(pady=100,padx=50)

        style = ttk.Style()
        style.configure('Submit.TButton', background="#38c788", relief="raised", padding=10)

        self.result_label = ttk.Label(self.master, text="")
        self.loading_label = ttk.Label(self.master, text="")


    def clear_default_text(self, event):
        if self.text_input.get("1.0", "end-1c") == "Write your text here":
            self.text_input.delete("1.0", "end")

    def get_important_words(self):
        text = self.text_input.get("1.0", "end-1c")
        self.loading_label.configure(text="Loading...")
        self.master.update()
        word_counts = get_important_words(text)
        result_string = ""
        for word, count in word_counts:
            result_string += f"{word}: {count}\n"
            result_string = result_string.upper()

        self.loading_label.configure(text="")
        self.result_label.configure(text=result_string)
        self.master.update()
        result_window = tk.Toplevel(self.master)
        result_window.geometry("500x500")
        result_window.resizable(False, False)
        result_label = ttk.Label(result_window, text=result_string, font=("Arial", 14))
        self.result_label.configure(text=result_window)
        result_window.configure(background="#498fb6")
        result_label.pack(pady=10)
    # Create window


root = tk.Tk()
root.state('zoomed')
app = MainWindow(root)
root.mainloop()
