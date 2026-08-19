# HotKit

A lightweight Python tool that packages a Python script into a small extractor that reconstructs and runs the original code at runtime.

<img width="400" height="250" alt="image" src="https://github.com/user-attachments/assets/b37d7c99-5283-494c-bfb2-f01f30dc1e3a" />

## What does it do?

1. You select a Python `.py` file
2. It compresses and encodes the source code
3. It generates an extractor containing the encoded code
4. The extractor splits the code into multiple temporary files at runtime
5. It reconstructs and executes the original Python code
6. Temporary files are removed after execution
<img width="807" height="405" alt="image" src="https://github.com/user-attachments/assets/532c81bb-ac10-4ffc-8676-f3bde473eb3f" />

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
