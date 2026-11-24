# Rubik's Cube Simulator

This is a Python Program that simulates and renders a Rubik's Cube using `pygame` and `PyOpenGL`.

The Rubik's Cube in this program can be rotated, turned, scrambled, and solved using GUI buttons or inputs from the keyboard.

Before running the program, please make sure the dependencies are installed. You can choose to install them directly into your Python, or you can create a virtual environment and install the libraries here. The libraries can be found in `requirements.txt` at the root directory.

From this point, this README will teach you how to use the application.

## How to install dependencies

All depenencies are listed in requirements.txt. Before running the game, you should download them using these commands:

Download to virtual environment (.venv):

```bash
pip install -r requirements.txt
```

Activate the virtual environment:

```bash
.\venv\Scripts\Activate.ps1
```

## How to use the inputs

### Mouse inputs

Click and hold Left Click to rotate the cube around. This will not effect the internal cube's current orientation (e.g. the current U face).

### Keyboard inputs

To turn the faces, you need to use the keyboard. Here is the list of keys and their corresponding moves:

| Keys | Move |
| --- | --- |
| `F` | `F` |
| `B` | `B` |
| `U` or `Up Arrow` | `U` |
| `D` or `Down Arrow` | `D` |
| `R` or `Right Arrow` | `R` |
| `L` or `Left Arrow` | `L` |
| `M` | `M` |
| `E` | `E` |
| `S` | `S` |
| `X` | `x` |
| `Y` | `y` |
| `Z` | `z` |

Hold `Left Shift` or `Right Shift` while pressing a key to perform the inverse move (for example, `Shift + U` performs `U'`).
