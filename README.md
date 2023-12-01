# ChatGPT Presentation codebase

## Installation

- Copy .env.dist to .env
- Install requirements either by doing

```sh
    poetry install
```

or by

```sh
    conda create -n chatgpt-presentation
    conda activate -n chatgpt-presentation
    pip install -r requirements.txt
```

## Usage

- Run the bot using

```sh
    poetry run streamlit run src/app.py
```

or by

```sh
    streamlit run src/app.py
```
