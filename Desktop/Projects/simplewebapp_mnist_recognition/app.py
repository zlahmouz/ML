import torch
import torch.nn as nn
import torch.nn.functional as F
from flask import Flask, request, jsonify
from torchvision import transforms
from PIL import Image
import io

# Définir le modèle CNN (comme dans l'entraînement)
class CNN(nn.Module):
    def __init__(self):
        super(CNN, self).__init__()
        self.conv1 = nn.Conv2d(1, 32, kernel_size=3)
        self.conv2 = nn.Conv2d(32, 64, kernel_size=3)
        self.fc1 = nn.Linear(64 * 12 * 12, 128)
        self.fc2 = nn.Linear(128, 10)

    def forward(self, x):
        x = F.relu(self.conv1(x))
        x = F.max_pool2d(F.relu(self.conv2(x)), 2)
        x = x.view(-1, 64 * 12 * 12)
        x = F.relu(self.fc1(x))
        x = self.fc2(x)
        return F.log_softmax(x, dim=1)

# Charger le modèle sauvegardé
model = CNN()
model.load_state_dict(torch.load('C:\\Users\\33665\\Desktop\\Projects\\simplewebapp_mnist_recognition\\mnist_cnn.pth'))
model.eval()

# Définir l'application Flask
app = Flask(__name__)

# Transformation de l'image (identique à l'entraînement)
transform = transforms.Compose([
    transforms.Grayscale(num_output_channels=1),
    transforms.Resize((28, 28)),
    transforms.ToTensor(),
    transforms.Normalize((0.5,), (0.5,))
])

# Route pour l'API de prédiction
@app.route('/predict', methods=['POST'])
def predict():
    # Récupérer l'image à partir de la requête
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400

    file = request.files['file']
    img = Image.open(io.BytesIO(file.read()))

    # Prétraitement de l'image
    img = transform(img).unsqueeze(0)  # Ajouter une dimension de batch

    # Faire la prédiction avec le modèle
    with torch.no_grad():
        output = model(img)
        predicted_digit = output.argmax(dim=1, keepdim=True).item()

    # Retourner la prédiction sous forme de JSON
    return jsonify({'prediction': predicted_digit})

# Lancer le serveur Flask
if __name__ == '__main__':
    app.run(debug=True)