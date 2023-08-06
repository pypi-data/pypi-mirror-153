# Generating PDF file using a DSL

## Team

- Nikola Zejak E2 140/2021
- Milan Lukić E2 77/2021
- Milana Tucakov E2 138/2021

## General Idea

Developing a DSL for generating PDF files. It could be used in other apps as a tool for generating dynamic reports, contracts, invoices etc.

## Features

### Must have

- PDF text elements (Heading, text block...)
- Font customization
- Including DSL features into Python module
- Images
- Tabels

### Nice to have

- PDF Templates (for contracts, reports...)
- Text customization (Size, Bolded, Underline, Italic, Alignment)

### Could have

- VSCode plugin

### Create virtual environment

```
python3 -m venv /path/to/new/virtual/environment
```

### Start virtual environment

Mac:

```
source NAME_OF_MY_VIRTUAL_ENVIRONMENT/bin/activate
```

Windows:

```
NAME_OF_MY_VIRTUAL_ENVIRONMENT\Scripts\activate
```

### Install requirements from requirements.txt

```
pip install requirements.txt
```

### Generate pdf and html file

#### Mac users:

```
cd src && python3 main.py
```

#### Windows users:

```
cd src && python main.py
```

### Installing from a local src tree

```
python3 -m pip install -e .
```

### Installing from local archives

```
python3 -m pip install <path>
```

### Installing from PyPI

```
python3 -m pip install "PDF-Generator-with-TextX==version_of_project"
```

### VS Code language support extension

There is language support extension for our new DSL .tff files in VS Code Marketplace. You can search for TFF FTNTeam3 extension.

![extension](./extension.png)
