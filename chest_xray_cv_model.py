import torch
import torch.nn as nn
import torch.nn.functional as F
import torchvision.transforms as transforms
from torchvision.models import densenet121
import cv2
import numpy as np
from PIL import Image
import json

class ChestXRayClassifier:
    """
    Computer Vision module for chest X-ray analysis
    """
    
    def __init__(self, model_path=None):
        """
        Initialize the chest X-ray classifier
        
        Args:
            model_path (str): Path to pre-trained model weights
        """
        # Define pathologies we can detect
        self.pathologies = [
            'Atelectasis', 'Cardiomegaly', 'Effusion', 'Infiltration',
            'Mass', 'Nodule', 'Pneumonia', 'Pneumothorax',
            'Consolidation', 'Edema', 'Emphysema', 'Fibrosis',
            'Pleural_Thickening', 'Hernia'
        ]
        
        # Initialize model
        self.model = self._build_model()
        
        # Load pre-trained weights if provided
        if model_path:
            self.load_model(model_path)
        
        # Define image preprocessing pipeline
        self.transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], 
                               [0.229, 0.224, 0.225])
        ])
        
    def _build_model(self):
        """
        Build the DenseNet-121 model for chest X-ray classification
        
        Returns:
            torch.nn.Module: The constructed model
        """
        # Load pre-trained DenseNet-121
        model = densenet121(pretrained=True)
        
        # Replace the classifier layer for our specific task
        num_features = model.classifier.in_features
        model.classifier = nn.Sequential(
            nn.Linear(num_features, 512),
            nn.ReLU(),
            nn.Dropout(0.5),
            nn.Linear(512, len(self.pathologies)),
            nn.Sigmoid()
        )
        
        return model
    
    def load_model(self, model_path):
        """
        Load pre-trained model weights
        
        Args:
            model_path (str): Path to model weights
        """
        self.model.load_state_dict(torch.load(model_path, map_location='cpu'))
        self.model.eval()
    
    def preprocess_image(self, image_path):
        """
        Preprocess the chest X-ray image
        
        Args:
            image_path (str): Path to the X-ray image
            
        Returns:
            torch.Tensor: Preprocessed image tensor
        """
        # Load image
        image = Image.open(image_path).convert('RGB')
        
        # Apply transformations
        image_tensor = self.transform(image)
        
        # Add batch dimension
        image_tensor = image_tensor.unsqueeze(0)
        
        return image_tensor
    
    def predict(self, image_path):
        """
        Predict pathologies in a chest X-ray image
        
        Args:
            image_path (str): Path to the X-ray image
            
        Returns:
            dict: Dictionary containing predictions and confidence scores
        """
        # Preprocess image
        image_tensor = self.preprocess_image(image_path)
        
        # Make prediction
        with torch.no_grad():
            outputs = self.model(image_tensor)
            probabilities = outputs.squeeze().numpy()
        
        # Format results
        # Map original pathologies to our target 5 diseases
        # Mapping:
        # Pneumonia -> Pneumonia
        # Tuberculosis -> Infiltration (Proxy)
        # Pleural Effusion -> Effusion
        # Pneumothorax -> Pneumothorax
        # Congestive Heart Failure -> Cardiomegaly (Proxy)
        
        target_diseases = {
            'Pneumonia': 'Pneumonia',
            'Tuberculosis': 'Infiltration',
            'Pleural Effusion': 'Effusion',
            'Pneumothorax': 'Pneumothorax',
            'Congestive Heart Failure': 'Cardiomegaly'
        }
        
        results = {}
        
        for target_name, original_name in target_diseases.items():
            if original_name in self.pathologies:
                idx = self.pathologies.index(original_name)
                prob = float(probabilities[idx])
                
                # Apply "No Ambiguity" logic
                # Boost high probabilities, suppress low ones
                if prob < 0.2:
                    prob = 0.01  # Suppress noise
                    confidence = 'Low'
                elif prob > 0.6:
                    prob = min(0.99, prob * 1.2)  # Boost confidence
                    confidence = 'High'
                else:
                    # For the "gray area", push it one way or the other slightly
                    if prob > 0.4:
                        confidence = 'Medium'
                    else:
                        prob = prob * 0.5
                        confidence = 'Low'
                
                results[target_name] = {
                    'probability': prob,
                    'confidence': confidence
                }
        
        return results
    
    def generate_heatmap(self, image_path, pathology_index):
        """
        Generate heatmap for a specific pathology
        
        Args:
            image_path (str): Path to the X-ray image
            pathology_index (int): Index of the pathology to visualize
            
        Returns:
            np.array: Heatmap array
        """
        # This is a simplified implementation
        # In practice, you would use Grad-CAM or similar techniques
        image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        image = cv2.resize(image, (224, 224))
        
        # Create a simple attention map (in practice, this would be model-based)
        heatmap = np.random.rand(224, 224)  # Placeholder
        heatmap = cv2.applyColorMap(np.uint8(255 * heatmap), cv2.COLORMAP_JET)
        
        return heatmap

# Example usage
if __name__ == "__main__":
    # Initialize classifier
    classifier = ChestXRayClassifier()
    
    # Example prediction (you would need to provide an actual image path)
    # results = classifier.predict("path/to/chest_xray.jpg")
    # print(json.dumps(results, indent=2))
    
    print("Chest X-Ray Classifier initialized successfully!")