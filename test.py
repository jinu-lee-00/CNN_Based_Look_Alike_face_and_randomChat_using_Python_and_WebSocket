from train import *
import torch


model = models.resnet34()
model.fc = nn.Linear(model.fc.in_features, 9)
model.load_state_dict(torch.load('model_weights.pth'))
model = model.to(device)

with torch.no_grad():


    for inputs, labels in test_dataloader:
        inputs = inputs.to(device)

        outputs = model(inputs)
        print('이것이 outputs', outputs)
        _, preds = torch.max(outputs, 1)

        print(f'[예측 결과: {class_names[preds[0]]}] (실제 정답: {class_names[labels.data[0]]})')
        imshow(inputs.cpu().data[0], title='예측 결과: ' + class_names[preds[0]])