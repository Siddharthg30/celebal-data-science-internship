# MNIST Denoising Autoencoder

## Overview

This project implements a Convolutional Denoising Autoencoder using TensorFlow and Keras to remove Gaussian noise from handwritten digit images. The model is trained on the MNIST PNG dataset and learns to reconstruct clean images from noisy inputs.

## Objectives

- Load and preprocess the MNIST dataset
- Add Gaussian noise to input images
- Build a convolutional autoencoder
- Train the model to reconstruct clean images
- Evaluate the denoising performance
- Visualize the reconstructed outputs

## Dataset

- Dataset: MNIST PNG Dataset
- Training Images: 60,000
- Testing Images: 10,000
- Image Size: 28 × 28 pixels
- Color Format: Grayscale

## Model Architecture

### Encoder

- Conv2D (32 filters)
- MaxPooling2D
- Conv2D (64 filters)
- MaxPooling2D

### Decoder

- Conv2D (64 filters)
- UpSampling2D
- Conv2D (32 filters)
- UpSampling2D
- Conv2D (1 filter, Sigmoid)

## Training Configuration

| Parameter | Value |
|-----------|-------|
| Optimizer | Adam |
| Loss Function | Binary Crossentropy |
| Batch Size | 128 |
| Epochs | 15 |
| Noise Type | Gaussian Noise |
| Noise Factor | 0.5 |

## Results

Final Training Loss

```
0.0942
```

Final Validation/Test Loss

```
0.0938
```

The autoencoder successfully removed most of the Gaussian noise while preserving the handwritten digit structure.

## Project Structure

```text
MNIST-Denoising-Autoencoder/
│
├── dataset/
├── images/
├── models/
├── outputs/
├── denoising_autoencoder.ipynb
├── README.md
└── requirements.txt
```

## Output

### Training Loss

`images/loss_curve.png`

### Noisy Samples

`images/noisy_samples.png`

### Reconstructed Images

`images/reconstruction.png`

## How to Run

Clone the repository.

```bash
git clone <repository-url>
```

Install dependencies.

```bash
pip install -r requirements.txt
```

Open the notebook.

```bash
jupyter notebook denoising_autoencoder.ipynb
```

Run all cells sequentially.

## Technologies Used

- Python
- TensorFlow
- Keras
- NumPy
- OpenCV
- Matplotlib

## Conclusion

A convolutional denoising autoencoder was developed to reconstruct clean handwritten digit images from noisy inputs. The trained model effectively reduced Gaussian noise while preserving the essential digit features, demonstrating the capability of autoencoders for image denoising tasks.