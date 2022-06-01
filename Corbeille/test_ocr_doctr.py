"""
from doctr.io import DocumentFile
# pip install python-doctr
# for TensorFlow -> pip install "python-doctr[tf]"
# for PyTorch -> pip install "python-doctr[torch]"
# Image
single_img_doc = DocumentFile.from_images("data/sample.jpg")
"""

from doctr.models import ocr_predictor
from doctr.io import DocumentFile


model = ocr_predictor(pretrained=True)
# Image
single_img_doc = DocumentFile.from_images("../data/sample.jpg")

# Analyze
result = model(single_img_doc)
result.show(result)





