from enum import Enum

class NudeNetDetections(str, Enum):
    FEMALE_PRIVATE_AREA= "female-private-area"
    FEMALE_FACE= "female-face"
    BUTTOCKS_BARE= "buttocks-bare"
    FEMALE_BREAST_BARE= "female-breast-bare"
    FEMALE_VAGINA= "female-vagina"
    MALE_BREAST_BARE= "male-breast-bare"
    ANUS_BARE= "anus-bare"
    FEET_BARE= "feet-bare"
    BELLY= "belly"
    FEET= "feet"
    ARMPITS= "armpits"
    ARMPITS_BARE= "armpits-bare"
    MALE_FACE= "male-face"
    BELLY_BARE= "belly-bare"
    MALE_PENIS= "male-penis"
    ANUS_AREA= "anus-area"
    FEMALE_BREAST= "female-breast"
    BUTTOCKS= "buttocks"

class CensorMethod(str, Enum):
    PIXELATE= "pixelate"
    BLUR= "blur"
    GAUSSIAN_BLUR= "gaussian blur"
    MEDIAN_BLUR= "median blur"
    BLOCK= "block"
    IMAGE= "image"
