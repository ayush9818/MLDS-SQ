# Image-Based Search App

This is a simple image-based search app built with Streamlit and Qdrant. The app allows users to search for similar images in the CIFAR dataset using a provided query image.

### Features

- Upload an image as a query for similarity search.
- Display similar images from the CIFAR dataset based on the query image.
- View detailed information about the selected image.

### Installation

docker pull qdrant/qdrant
docker run -p 6333:6333 qdrant/qdrant

cd image-search
pip install -r requirements.txt

### Command
streamlit run image-search.py