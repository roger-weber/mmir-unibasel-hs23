# Chapter 4: Advanced Text Retrieval

Examining natural language processing using NLTK as an example, this chapter also explores modern methods for creating embeddings and leveraging generative AI to enhance retrieval results.

## Prerequisites

- We use text documents from [project Gutenberg](https://www.gutenberg.org/)
  - `./utils/gutenberg.py` provides a convenience function `get_book(book_id: int)` that returns a dictionary with metadata and a `text` property with header/footer stripped from the original document.
  - The folder `./books/` contains locally cached text bodies downloaded from the Gutenberg site. These files are excluded from the git repository; download your own set of documents for the purpose of studying the methods.
- Install python dependencies

  ```pip
    pip install -r requirements.txt
  ```
  
  - `tokenizers` is an Apache 2.0 open-source library led by Hugging Face. It offers an implementation of widely-used tokenizers with an emphasis on performance and versatility. It is also utilized in transformers. 
  [PyPi page](https://pypi.org/project/tokenizers/) - [documentation](https://huggingface.co/docs/tokenizers/index) - [tutorial](https://huggingface.co/docs/tokenizers/python/latest/quicktour.html)
  - `transformers` is an Apache 2.0 open-source library led by Hugging Face. Transformers provides thousands of pretrained models to perform tasks on different modalities such as text, vision, and audio.
  [PyPi page](https://pypi.org/project/transformers/) - [documentation](https://huggingface.co/docs/transformers/index) - [tutorial](https://huggingface.co/docs/transformers/quicktour)
  - `langchain` started in 2022 as an open source project (MIT License) and quickly gained popularity with improvements form hundreds of contributors for the most common AI use cases and with integration with systems from Amazon, Google, and Microsoft.
    [PyPi page](https://pypi.org/project/langchain/) - [documentation](https://python.langchain.com/docs/get_started/introduction.html) - [tutorial](https://python.langchain.com/docs/additional_resources/tutorials)
  - `nltk` is a popular library for natural language processing with many integrations for text processing, classification, tokenization, stemming, tagging, parsing, and semantic reasoning.
    [PyPi page](https://pypi.org/project/nltk/) - [documentation](https://www.nltk.org/) - [tutorial](https://www.nltk.org/howto.html)


## Slides

- [Advanced Text Retrieval (2023)](https://dmi.unibas.ch/fileadmin/user_upload/dmi/Studium/Computer_Science/Vorlesungen_HS23/Multimedia_Retrieval/04_AdvancedTextRetrieval.pdf)

## Demos

- [Embeddings Projector](https://projector.tensorflow.org)

## Links

- tbd
