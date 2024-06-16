import io
from typing import List

from fastapi import FastAPI, UploadFile
from fastapi.exceptions import RequestValidationError
from fastapi.responses import Response as fastapi_response

from PIL import Image, PngImagePlugin

from structures import *
import helper

description= """
NudeNet FastAPI helps you censor your images.
## Features
### 1- Detect gender and any body part  
  #### e.g. *female face, belly, feet*
### 2- Exposed or unexposed:  
  #### e.g. *breast or breast-bare*
### 3- Add information to image metadata
  #### e.g. *"NudeNet: female-face:0.86; belly:0.54"*  
### 4- Censor as desired (or not):
  #### a- Blur. *(adjust block size for effect)*
  #### b- Pixelate. *(adjust block size for effect)*
  #### c- Cover with image *(overlay image, you can use RGBA images)*.
  #### d- Black box.
### 5- Adjustable sensitivity for the detection.
"""

censor_api_endpoint_description = """
Return a censored image based on censorship criteria and censor method provided.\n
Along with the image response, two headers are added:\n
1- used_censor_method.\n
2- censored_parts: It may be different from the provided criteria, since it is based on what the NudeNet model detected.\n
\n
If 'image' censorship method is used and no overlay image is provided, the default overlay image is used (censored.png).\n
*NSFW metadata will be true if there were any part censored based on the provided censorship criteria.*
"""

app = FastAPI(
    title= "NudeNet FastAPI",
    description= description,
    summary= "FastAPI implementation of NudeNet",
    version= "1.0",
    license_info= {"name": "MIT License", "identifier": "MIT"},
    docs_url=None,
    redoc_url="/docs"
)


@app.post("/censor", 
          description=censor_api_endpoint_description,
          response_description="Successfully Censored Image",
          responses={
                200: {
                    "content": {"image/png": {}},
                }
            },
            response_class=fastapi_response)
async def censor_image(image: UploadFile,
                       censor_method: CensorMethod= CensorMethod.PIXELATE, 
                       censorship_criteria: List[NudeNetDetections]= [NudeNetDetections.FEMALE_VAGINA], 
                       detection_threshold: float= 0.2,
                       blocks: int= 3,
                       include_metadata: bool= True,
                       overlay_image: UploadFile | None = None):
    
    #Limit blocks range from 3 to 100. Since gaussian blur relies on primes?
    if(censor_method == CensorMethod.GAUSSIAN_BLUR):
        if blocks > 100:
            raise RequestValidationError(errors=[{
                "loc": ["query","censor_method"],
                "msg": "Blocks value need to be less than 100 for gaussian blur.",
                "type": "less_than"
            },
        ])
        elif blocks < 3:
            raise RequestValidationError(errors=[{
                "loc": ["query","censor_method"],
                "msg": "Blocks value need to be greater than 2 for gaussian blur.",
                "type": "greater_than"
            },
        ])
    
    image_content = await image.read()
    image_pil: Image.Image = Image.open(io.BytesIO(image_content))

    overlay_as_bytes = None
    
    if censor_method == CensorMethod.IMAGE:
        if overlay_image is None:
            # Use default overlay image.
            overlay_as_bytes = None
        else:
            overlay_as_bytes = await overlay_image.read()
    
    censored_image_bytes_array, censored_parts = helper.censor_image(censorship_criteria=censorship_criteria,
                                                         censor_method=censor_method,
                                                         detection_threshold=detection_threshold,
                                                         blocks=blocks,
                                                         include_metadata=include_metadata,
                                                         image=image_pil,
                                                         overlay_as_bytes=overlay_as_bytes)
    

    return fastapi_response(content=censored_image_bytes_array,
                        media_type="image/png",
                        headers={"used_censor_method": "pixelate",
                                 "censored_parts": ','.join(censored_parts)})

@app.post("/isNSFW",
          description="Return if the image is not safe for work (NSFW) based on the criteria provided.",
          response_description="NSFW Boolean",)
async def is_nsfw(image: UploadFile, 
                  nsfw_criteria: List[NudeNetDetections]= [
                      NudeNetDetections.FEMALE_PRIVATE_AREA,
                      NudeNetDetections.ANUS_AREA,
                      NudeNetDetections.ANUS_BARE,
                      NudeNetDetections.BUTTOCKS_BARE,
                      NudeNetDetections.FEMALE_VAGINA,
                      NudeNetDetections.FEMALE_BREAST_BARE,
                      NudeNetDetections.MALE_PENIS
                  ], detection_threshold: float= 0.2) -> bool:
    
    image_content = await image.read()
    image_pil: Image.Image = Image.open(io.BytesIO(image_content))
    
    return helper.is_NSFW(image_pil, nsfw_criteria, detection_threshold)