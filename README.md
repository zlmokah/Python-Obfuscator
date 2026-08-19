# HotKit

A lightweight Python tool that packages a Python script into a small extractor that reconstructs and runs the original code at runtime.

## What does it do?

1. You select a Python `.py` file
2. It compresses and encodes the source code
3. It generates an extractor containing the encoded code
4. The extractor splits the code into multiple temporary files at runtime
5. It reconstructs and executes the original Python code
6. Temporary files are removed after execution

## Features

- Simple PyQt5 interface
- Python file browser
- Code compression and Base64 encoding
- XOR-based transformation
- Runtime code reconstruction
- SHA-256 hash check
- Automatic cleanup of temporary files
- Minimal dark-themed UI

## How to use

Select your `.py` file using **Browse**, choose an output directory, then click **Build**.

The tool generates a `main.py` extractor containing the processed source code.

## Example

Select:

`payload.py`

Choose an output folder.

Click **Build**.

HotKit creates:

`main.py`

Running the generated file reconstructs and executes the original Python source.
