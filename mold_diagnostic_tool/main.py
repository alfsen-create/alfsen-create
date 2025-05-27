import argparse
import cv2
import numpy as np
from tensorflow.keras.models import load_model


class DiagnosticAgent:
    """Agent responsible for running the ML model for diagnosis."""

    def __init__(self, model_path: str):
        self.model = load_model(model_path)

    def diagnose(self, image_path: str):
        image = cv2.imread(image_path)
        image_resized = cv2.resize(image, (224, 224))
        image_normalized = image_resized / 255.0
        image_batch = np.expand_dims(image_normalized, axis=0)
        prediction = self.model.predict(image_batch)
        label_index = int(np.argmax(prediction))
        confidence = float(prediction[0][label_index])
        return label_index, confidence


class TrayPlacementAgent:
    """Agent responsible for handling AR tray placement."""

    def place_tray(self, image_path: str):
        # Placeholder for AR tray placement logic
        print("[INFO] AR tray placement not implemented; stub call made.")


class Controller:
    """Orchestrates agents to complete the diagnostic workflow."""

    def __init__(self, diagnostic_agent: DiagnosticAgent, tray_agent: TrayPlacementAgent, place_tray: bool):
        self.diagnostic_agent = diagnostic_agent
        self.tray_agent = tray_agent
        self.place_tray = place_tray

    def run(self, image_path: str):
        label_index, confidence = self.diagnostic_agent.diagnose(image_path)
        print(f"Diagnosis label index: {label_index}, confidence: {confidence:.2f}")
        if self.place_tray:
            self.tray_agent.place_tray(image_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="AI Mold/Disease Diagnostic with AR Tray Placement")
    parser.add_argument("--image", required=True, help="Path to input image")
    parser.add_argument("--model", required=True, help="Path to trained Keras model (.h5)")
    parser.add_argument("--place-tray", action="store_true", help="Trigger AR tray placement after diagnosis")

    args = parser.parse_args()

    diagnostic_agent = DiagnosticAgent(args.model)
    tray_agent = TrayPlacementAgent()
    controller = Controller(diagnostic_agent, tray_agent, args.place_tray)
    controller.run(args.image)
