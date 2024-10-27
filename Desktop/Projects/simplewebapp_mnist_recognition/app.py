# app.py
from flask import Flask, request, render_template, jsonify
import torch
import torch.nn as nn
import torch.nn.functional as F
from torchvision import transforms
from PIL import Image
import io

app = Flask(__name__)


# Définition de la classe CNN
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


# Chargement du modèle
model = CNN()
model.load_state_dict(torch.load('mnist_cnn.pth', map_location=torch.device('cpu')))
model.eval()

# Prétraitement de l'image
transform = transforms.Compose([
    transforms.Resize((28, 28)),
    transforms.ToTensor(),
    transforms.Normalize((0.1307,), (0.3081,))
])


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Gérer le téléchargement de l'image et la prédiction
        file = request.files['file']
        img = Image.open(io.BytesIO(file.read())).convert('L')
        img_tensor = transform(img).unsqueeze(0)

        with torch.no_grad():
            output = model(img_tensor)

        prob = torch.exp(output)
        _, predicted = torch.max(output.data, 1)
        digit = predicted.item()
        confidence = prob[0][digit].item()

        return jsonify({'digit': int(digit), 'confidence': float(confidence)})
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)