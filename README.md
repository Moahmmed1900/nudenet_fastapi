 ### NudeNet FastAPI helps you censor your images and detect NSFW images.

## Features
1- Detect gender and any body part. e.g. *female face, belly, feet*
2- Exposed or unexposed: e.g. *breast or breast-bare*
3- Add information to image metadata. e.g. *"NudeNet: female-face:0.86; belly:0.54"*, *NSFW: false*  
4- Censor as desired: 
- Blur. *(adjust block size for effect)*
- Pixelate. *(adjust block size for effect)*
- Cover with image *(overlay image, you can use RGBA images)*.
- Black box.
5- Adjustable sensitivity for the detection.
6- Customizable detection criteria for NSFW images. e.g. feet-bare, armpits-bare

## Usage
```
pip install -r requirements. txt

python3 main.py
```

## Documentation
### After the server is up and running, navigate to <http://127.0.0.1:8000/docs>
