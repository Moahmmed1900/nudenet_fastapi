import io
import nudenet
from structures import *
from PIL import Image, PngImagePlugin
from typing import Tuple, List, ByteString
import sympy
import cv2
import numpy as np


if nudenet.detector is None:
    nudenet.detector = nudenet.NudeDetector(providers=['CPUExecutionProvider']) # loads and initializes model once

def censor_image(censorship_criteria: List[NudeNetDetections],
                 censor_method: CensorMethod,
                 detection_threshold: float,
                 blocks: int,
                 include_metadata: bool,
                 image: Image.Image, 
                 overlay_as_bytes: ByteString | None) -> Tuple[ByteString, List[NudeNetDetections]]:
    
    #For gaussian blur, the blocks need be a prime number? from tests I made is yes, but who knows?...
    if not sympy.isprime(blocks):
        #Find next prime
        blocks = sympy.nextprime(blocks) # type: ignore
    

    nudes = nudenet.detector.censor(image=image, # type: ignore
                                    method=censor_method, 
                                    min_score=detection_threshold, 
                                    censor=censorship_criteria, 
                                    blocks=blocks, 
                                    overlay=overlay_as_bytes)

    censored_parts: List[NudeNetDetections] = [d["label"] for d in nudes.detections if d["label"] in censorship_criteria]

    censored_image_bytes_array = io.BytesIO()

    if(include_metadata):
        meta = '; '.join([f'{d["label"]}:{d["score"]}' for d in nudes.detections])
        nsfw = any([d["label"] in censorship_criteria for d in nudes.detections])

        nudes.output.info["NudeNet"] = meta
        nudes.output.info["NSFW"] = nsfw

        pngMetaData: PngImagePlugin.PngInfo = PngImagePlugin.PngInfo()
        pngMetaData.add_text("NudeNet", meta)
        pngMetaData.add_text("NSFW", str(nsfw))

        nudes.output.save(censored_image_bytes_array, format="PNG", pnginfo=pngMetaData)

    else:
        nudes.output.save(censored_image_bytes_array, format="PNG")

    return (censored_image_bytes_array.getvalue(), censored_parts)

def is_NSFW(image: Image.Image, nsfw_criteria: List[NudeNetDetections], detection_threshold: float):
    image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR) # type: ignore
    all_detected_nudes = nudenet.detector.detect(image, detection_threshold) # type: ignore

    all_detected_nudes = [nude_detected['label'] for nude_detected in all_detected_nudes]

    return len(set(all_detected_nudes) & set(nsfw_criteria)) > 0 #Checking array intersection
    
