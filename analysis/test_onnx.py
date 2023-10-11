
import onnxruntime, torch, random


ort_session = onnxruntime.InferenceSession("trained_network.onnx", providers=['AzureExecutionProvider', 'CPUExecutionProvider'])

inputs = [random.randint(0, 1) for i in range(80)]
tensor = torch.tensor(inputs, dtype=torch.float32)

def to_numpy(tensor):
    return tensor.detach().cpu().numpy() if tensor.requires_grad else tensor.cpu().numpy()

ort_outs = ort_session.run(["out"], {"in": to_numpy(tensor)})

print(ort_outs)