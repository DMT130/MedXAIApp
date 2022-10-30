from PIL import Image
from io import BytesIO
import numpy as np
import pydicom
from pydicom.pixel_data_handlers.util import apply_voi_lut, apply_modality_lut
import matplotlib.pyplot as plt
from onnxpre import onnxpredic
from nmax import non_max_suppression_fast as nms
PATH='ChestXR31.pt'

label2target = {'Aortic enlargement': 2,'Atelectasis': 8,'Calcification': 12,'Cardiomegaly': 1,'Consolidation': 13,
 'ILD': 4,'Infiltration': 10,'Lung Opacity': 7,'Nodule/Mass': 5,'Other lesion': 9,'Pleural effusion': 11,
 'Pleural thickening': 3,'Pneumothorax': 14,'Pulmonary fibrosis': 6,'background': 0}

target2label = {0: 'background',1: 'Cardiomegaly',2: 'Aortic enlargement',3: 'Pleural thickening',4: 'ILD',
 5: 'Nodule/Mass',6: 'Pulmonary fibrosis',7: 'Lung Opacity',8: 'Atelectasis',9: 'Other lesion',
 10: 'Infiltration',11: 'Pleural effusion',12: 'Calcification',13: 'Consolidation',14: 'Pneumothorax'}

SIZE = (1024, 1024)


def read_normal_image(image_encoded):
    pil_image = Image.open(BytesIO(image_encoded))
    return pil_image


def read_dcm_image(image_encoded, voi_lut = True, fix_monochrome = True):
    image_encoded = BytesIO(image_encoded)
    dicom = pydicom.read_file(image_encoded)
    if voi_lut:
        data = apply_voi_lut(dicom.pixel_array, dicom)
    else:
        data = dicom.pixel_array
    if fix_monochrome and dicom.PhotometricInterpretation == "MONOCHROME1":
        data = np.amax(data) - data
    data = data - np.min(data)
    data = data / np.max(data)
    data = (data * 255).astype(np.uint8)
    return data

def im_show_dcm(array, size=1024, keep_ratio=False, resample=Image.BILINEAR):
    im = Image.fromarray(array)
    if keep_ratio:
        im.thumbnail((size, size), resample)
    else:
        im = im.resize((size, size), resample)
    return im

def im_show_normal(image):
    image = image.resize(SIZE, Image.BILINEAR)
    return image

def preprocess_dcm(image):
    image = im_show_dcm(image)
    image = np.array(image)
    image = image/255.
    image = np.reshape(image, SIZE)
    image = np.stack([image, image, image], axis=0)
    image = image.astype('float32')
    return image

def preprocess_normal(image):
    image = image.resize(SIZE, Image.BILINEAR)
    image = np.asarray(image)
    if image.shape[-1]==3:
        image = np.rollaxis(image,2)
        image = image.astype('float32')
        return image
    elif len(image.shape) ==2:
        image = image / 255.
        image = np.stack([image, image, image], axis=0)
        image = image.astype('float32')
        return image
    else:
        image = image[:,:,0] / 255.
        image = np.stack([image, image, image], axis=0)
        image = image.astype('float32')
        return image

def decode_output(output, proba_limit=0.05):
    'convert tensors to numpy arrays'
    bbs, labels, confs = output
    #bbs = output['boxes'].cpu().detach().numpy().astype(np.uint16)
    labels = np.array([target2label[i] for i in labels])#.cpu().detach().numpy()])
    #confs = output['scores']#.cpu().detach().numpy()
    ixs = nms(bbs.astype(np.float32), 0.05)
    bbs, confs, labels = [tensor[ixs] for tensor in [bbs, confs, labels]]
    indices = []
    for i in range(len(confs)):
      if confs[i]>proba_limit:
        indices.append(i)
    confs = [confs[i] for i in indices]
    bbs = [bbs[i] for i in indices]
    labels = [labels[i] for i in indices]
    return bbs, confs, labels

    #if len(ixs) == 1:
       # bbs, confs, labels = [np.array([tensor]) for tensor in [bbs, confs, labels]]
    return bbs.tolist(), confs.tolist(), labels.tolist()



def predict(image):
    image=np.expand_dims(image, axis=0)
    print('shape:', image.shape)
    #outputs = model(image)
    outputs=onnxpredic(image)
    print(outputs)
    #for ix, output in enumerate(outputs):
    bbs, confs, labels = decode_output(outputs)
    info = [f'{l}:{c:.2f}' for l,c in zip(labels, confs)]
    return info, bbs, labels