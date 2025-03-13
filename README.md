# Image Editing Using AI

## Overview
This project is an **AI-powered image editor** that allows users to upload an image, provide a textual prompt, and apply edits using **Stable Diffusion's image-to-image** functionality. The edited image is displayed alongside the original image.

## Features
- Upload an image in PNG, JPG, or JPEG format.
- Enter a text prompt to describe desired edits.
- Adjust the strength of the edit using a slider.
- AI-generated edited image appears next to the original.
- Uses **Stable Diffusion v1.5** for image-to-image transformation.

## Installation
### Prerequisites
Ensure you have Python installed. You also need the required libraries:
```sh
pip install diffusers torch pillow
```

### Clone the Repository
```sh
git clone https://github.com/saradune6/Image-Editing-Using-Ai.git
cd Image-Editing-Using-Ai
```

### Run the Application
```sh
python app.py
```

## Usage
1. Upload an image.
2. Enter a prompt describing the desired changes.
3. Adjust the edit strength (higher values make stronger edits).
4. Run the script to generate the edited image.

## Technologies Used
- **Stable Diffusion v1.5** (AI Image Editing)
- **Diffusers** (Hugging Face Model Integration)
- **PyTorch** (Deep Learning Framework)

## Contributing
Feel free to submit pull requests or report issues!

## License
This project is licensed under the MIT License.
