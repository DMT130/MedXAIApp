# MedAI Project
Machine learning webapp for xray inference. It uses Faster RCNN models trained in +6000 imanges and 15 classes.
The model was then converted from pytorch to onnx for inference. The webApp itself was built using FastAPI a modern
fast and async python webframework.

The does not store the images uploaded for inference and it returns the results in bytes, needing to convert back to
or jpeg. A frontend built in react is also hosted in this github account is used for easy visualization of the inference.
