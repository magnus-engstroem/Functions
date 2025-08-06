from typing import List, Union, Generator, Iterator
import torch
from transformers import pipeline
from transformers import T5Tokenizer, T5ForConditionalGeneration
from nltk.tokenize import sent_tokenize
import nltk
import importlib
import subprocess
import sys
nltk.download('punkt', quiet=True)
nltk.download('punkt_tab', quiet=True)

def ensure_package(package):
    """
    Installs package

    For packages not already in the Open WebUI python environment
    """
    try:
        importlib.import_module(package)
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])



#Got error doe to packages not found in environment. A restart of the container might be requiered
ensure_package('sentencepiece')
ensure_package('accelerate')


class Pipeline:
    def __init__(self):
        self.name = "Summarizer"
    
    def chunk_text(self, text, max_words=400):
        """
        Breaks down text into chunks

        Divides between sentences, such that no chunk is more than max_words long
        400 words usually fits within the summarizers context

        Parameters
        ---
        text: str
            text to be broken down into chunks
        max_words: int
            max number of words in each chunk
        
        Returns
        ---
        chunks: list of str
            A list of chunks
        
        """
        sentences = sent_tokenize(text)
        chunks = []
        current_chunk = []
        word_count = 0

        for sentence in sentences:
            sentence_words = sentence.split()
            if word_count + len(sentence_words) > max_words:
                chunks.append(" ".join(current_chunk))
                current_chunk = [sentence]
                word_count = len(sentence_words)
            else:
                current_chunk.append(sentence)
                word_count += len(sentence_words)

        if current_chunk:
            chunks.append(" ".join(current_chunk))
        return chunks

    def init_summarizer(self):
        """
        Loads the flan-t5-base model using the transformers.pipeline interface

        Returns
        ---
        summmarizer: pipeline-object
            pipeline of flan-t5-base tokenizer and model, ready to be used on text        
        """


        tokenizer = T5Tokenizer.from_pretrained("google/flan-t5-base")
        model = T5ForConditionalGeneration.from_pretrained("google/flan-t5-base", device_map="auto", torch_dtype=torch.float16)
        summarizer = pipeline("summarization", model=model, tokenizer=tokenizer)

        return summarizer



    def summarize_long_text(self, text, prefix="summarize: ", max_new_tokens=512, min_length=40):
        """
        Preaks down a long text and summarizes each chunk

        Parameters
        ---
        text: str
            to be summarized
        prefix: str
            instruction to flan-t5-base model
        max_new_tokens: int
            specify summary length per chunk
        min_length: int
            specify summary length per chunk
        
        Returns
        ---

        str
            summary       
        """
        summarizer = self.init_summarizer()

        chunks = self.chunk_text(text)
        summaries = []

        for chunk in chunks:
            try:
                prompt = prefix + chunk  # FLAN prefers instruction-style
                summary = summarizer(prompt, max_new_tokens=max_new_tokens, min_length=min_length, do_sample=False)
                summaries.append(summary[0]['summary_text'])
            except Exception as e:
                print("Failed chunk:", e)

        return "\n\n".join(summaries)

    def pipe(self, user_message: str, body: dict) -> str:
        """
        The method called for each user input

        Parameters
        ---
        user_message: str
            string from user
        body: dict
            All information about the user input. (unused)

        Returns
        ---
        self.summarize_long_text(user_message): str
            summary

        """

        return self.summarize_long_text(user_message)




