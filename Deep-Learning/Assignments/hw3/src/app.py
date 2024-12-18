import warnings
warnings.filterwarnings("ignore")

import streamlit as st
import torch 
from PIL import Image
import numpy as np
from torchvision.models import resnet50, efficientnet_v2_m
import timm 
from torchvision.transforms import v2
import json

LABEL2ID = json.load(open('config/LABEL2ID.json'))
MODEL_PATHS = json.load(open('config/model_config.json'))
IMAGE_SIZE=(224,224)

class Classifier:
    """Model Classifier Class"""
    def __init__(self, model_name, model_path, label2id, image_size=(224,224)):
        """
        Args:
            model_name : name of the model to load. eg resnet50, efficientnet_v2
            model_path : local path for model weights
            label2id   : mapping of label to model ids
            image_size : Size of the image to use for inference
        """
        self.label2id = label2id 
        self.id2label = {v:k for k,v in self.label2id.items()}
        num_classes = len(self.id2label)
        self.model_path = model_path
        # Load the Model Classifier
        self.classifier = self.load_model(model_name, num_classes)

        # Prepare Test Transforms
        self.transform = self.get_transform(image_size)  

    def get_transform(self, image_size):
        """Method creates test transforms"""
        test_transforms = v2.Compose([
            v2.PILToTensor(),
            v2.Resize(image_size),
            v2.ToDtype(torch.float32, scale=True),
            v2.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ])
        return test_transforms

    def load_model(self, model_name, num_classes):
        """Method loads model into the memory using model_name and num_classes"""
        if model_name == 'resnet50':
            classifier = resnet50(pretrained=True)
            in_ftrs = classifier.fc.in_features
            classifier.fc = torch.nn.Linear(in_ftrs, num_classes)

            state_dict = torch.load(self.model_path, map_location=torch.device('cpu'))
            classifier.load_state_dict(state_dict)
            return classifier 
        
        elif model_name == "efficientnet":
            classifier = efficientnet_v2_m(pretrained=False)
            in_ftrs = classifier.classifier[1].in_features
            classifier.classifier[1] = torch.nn.Linear(in_ftrs, num_classes)

            state_dict = torch.load(self.model_path, map_location=torch.device('cpu'))
            classifier.load_state_dict(state_dict)
            return classifier 

        elif model_name == "vit":
            classifier = timm.create_model('vit_base_patch16_224',pretrained=False,num_classes=num_classes)
            state_dict = torch.load(self.model_path, map_location=torch.device('cpu'))
            classifier.load_state_dict(state_dict)
            return classifier 

        else:
            raise NotImplementedError(f"{model_name} not available")
        
    def predict(self, image_path):
        """Given a image path, model run prediction on the image"""
        image = Image.open(image_path).convert('RGB')
        image = self.transform(image).unsqueeze(0)
        self.classifier.eval()
        with torch.no_grad():
            outputs = self.classifier(image)
            _, predicted = torch.max(outputs, 1)
            return self.id2label[predicted.item()]


def app():
    # Sidebar for user inputs
    st.sidebar.header('User Input Features')
    uploaded_file = st.sidebar.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])
    if uploaded_file is not None:
        image = Image.open(uploaded_file).convert('RGB')
        model_name = st.sidebar.selectbox("Select Model", options=list(MODEL_PATHS.keys()))

        model = Classifier(model_name, MODEL_PATHS[model_name], LABEL2ID, IMAGE_SIZE)
        if st.sidebar.button('Run Model'):
            predicted_label = model.predict(uploaded_file)
            # You might need to map `predicted_label` to the actual class name if necessary
            st.write(f'Predicted label: {predicted_label}')
            st.image(image, use_column_width=True)


if __name__ == '__main__':
    app()