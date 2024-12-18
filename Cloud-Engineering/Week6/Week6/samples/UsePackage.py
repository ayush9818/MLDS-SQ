from iris_classifier.IrisClassifier import IrisClassifier
import numpy as np

# create an instance of the classifier
classifier = IrisClassifier()

# load data
X, y = classifier.load_data()

# split data
X_train, X_test, y_train, y_test = classifier.split_data(X, y)

# create model
classifier.model = classifier.create_model(
    input_shape=(X.shape[1],), num_classes=len(np.unique(y)))

# train model
classifier.train_model(X_train, y_train)

# evaluate model
accuracy = classifier.evaluate_model(X_test, y_test)
print(f"Accuracy: {accuracy:.2f}")
