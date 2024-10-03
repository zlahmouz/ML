import torch
import torch.nn as nn
import torch.nn.functional as F
from flask import Flask, render_template, request, redirect, url_for
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
model.load_state_dict(torch.load("mnist_cnn.pth", map_location=torch.device('cpu')))
#model.load_state_dict(torch.load("mnist_cnn.pth"))

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

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        if file:
            img = Image.open(io.BytesIO(file.read()))
            img = transform(img).unsqueeze(0)  # Ajouter une dimension batch
            
            # Faire la prédiction
            with torch.no_grad():
                output = model(img)
                pred = output.argmax(dim=1, keepdim=True)
                return render_template('result.html', prediction=pred.item())
    return render_template('index.html')
