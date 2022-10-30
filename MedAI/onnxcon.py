[1, 3, 1024, 1024]
PATH='ChestXR31.pt'


import torch
from torchvision.models.detection import fasterrcnn_resnet50_fpn
from torchvision.models.detection.faster_rcnn import FastRCNNPredictor

device = 'cuda:0' if torch.cuda.is_available() else 'cpu'

def get_model():
    model = fasterrcnn_resnet50_fpn(pretrained=False)
    in_features = model.roi_heads.box_predictor.cls_score.in_features
    model.roi_heads.box_predictor = FastRCNNPredictor(in_features, 15)
    return model

model = get_model().to(device)
model.load_state_dict(torch.load(PATH, map_location=torch.device(device)))

dummpy_input = torch.randn(1, 3, 1024, 1024)
model.eval()
out = model(dummpy_input)
print(out)
# Export the model
torch.onnx.export(model,            # model being run
                  dummpy_input,     # model input (or a tuple for multiple inputs)
                  "xray.onnx",     # where to save the model (can be a file or file-like object)
                  export_params=True,         # store the trained parameter weights inside the model file
                  opset_version=11,           # the ONNX version to export the model to
                  do_constant_folding=True,   # whether to execute constant folding for optimization
                  input_names = ['input'],    # the model's input names
                  output_names = ['output'],) # the model's output names)