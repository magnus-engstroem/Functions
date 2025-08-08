## Some functions for Open Webui

#### `translate_filter.py`

A filter which translates the user message before passing it to the model:
1. Input
2. Translate no -> en
3. Model response
4. Translate en -> no
5. Output

#### `summarization_pipe.py`

A pipe which uses the `flan-t5` as a `transformers.pipeline` to summarize text

(May require a restart of the pipelines container)
