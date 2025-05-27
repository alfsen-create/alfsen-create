# AI Mold/Disease Diagnostic with AR Tray Placement

This prototype demonstrates a **multi-agent** approach to diagnosing mold or plant disease from an input image. A dedicated agent runs the machine-learning model while another agent handles AR tray placement. A simple controller orchestrates these agents.

## Requirements

- Python 3.8+
- TensorFlow and Keras
- OpenCV
- NumPy

Install dependencies (requires internet access):

```bash
pip install tensorflow opencv-python numpy
```

## Usage

```bash
python main.py --image PATH_TO_IMAGE --model PATH_TO_MODEL.h5 [--place-tray]
```

- `--image`: path to the image to diagnose
- `--model`: path to a trained Keras model
- `--place-tray`: if provided, calls the AR tray placement stub

The controller prints the predicted label index and confidence score. Implement your own label mapping and AR logic as needed.

## Multi-Agent Architecture

See [MULTI_AGENT_ARCHITECTURE.md](MULTI_AGENT_ARCHITECTURE.md) for an overview of how the `DiagnosticAgent`, `TrayPlacementAgent`, and `Controller` work together.
