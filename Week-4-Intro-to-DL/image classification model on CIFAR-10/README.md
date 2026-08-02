# CIFAR-10 Image Classification using ANN and CNN

## 📌 Project Overview

This project implements and compares **Artificial Neural Networks (ANN)** and **Convolutional Neural Networks (CNN)** for image classification on the **CIFAR-10** dataset using TensorFlow and Keras.

The objective is to understand how different network architectures and training strategies affect image classification performance.

---

## 🎯 Objectives

* Build an image classification model using ANN.
* Build an image classification model using CNN.
* Compare ANN and CNN performance.
* Analyze the effect of different architectures and training strategies.
* Understand how CNN extracts spatial features from images.

---

## 📂 Dataset

The project uses the **CIFAR-10** dataset provided by TensorFlow.

* **Training Images:** 50,000
* **Testing Images:** 10,000
* **Image Size:** 32 × 32 × 3 (RGB)
* **Classes:** 10

Classes:

* Airplane
* Automobile
* Bird
* Cat
* Deer
* Dog
* Frog
* Horse
* Ship
* Truck

---

## 🛠️ Technologies Used

* Python
* TensorFlow
* Keras
* NumPy
* Pandas
* Matplotlib
* Google Colab

---

## 📁 Project Structure

```
image-classification-cifar10/
│
├── README.md
├── requirements.txt
├── .gitignore
│
├── notebooks/
│   └── cifar10_ann_cnn.ipynb
│
├── images/
│   ├── accuracy_comparison.png
│   ├── loss_curves.png
│   └── generalization_plot.png
│
└── results/
    └── final_comparison.csv
```

---

## 🔬 Experiments Performed

### Artificial Neural Network (ANN)

* Original ANN
* ANN with More Layers
* ANN trained for 20 Epochs

### Convolutional Neural Network (CNN)

* Original CNN
* CNN with More Filters
* CNN trained for 20 Epochs
* CNN with Early Stopping
* CNN with Data Augmentation

---

## ⚙️ Data Preprocessing

* Loaded CIFAR-10 dataset
* Normalized pixel values from 0–255 to 0–1
* Flattened images for ANN
* Used original image shape for CNN

---

## 📈 Evaluation Metrics

The following metrics were used for comparison:

* Test Accuracy
* Validation Loss
* Training Loss
* Learning Curves
* Generalization Performance

---

## 📊 Results Summary

The experiments showed that:

* ANN can classify images but performs relatively poorly because it cannot capture spatial information.
* Increasing ANN depth and training epochs slightly improves performance.
* CNN significantly outperforms ANN by learning image features through convolution operations.
* Increasing filters improves feature extraction but increases training time.
* Training for more epochs can improve performance but may also lead to overfitting.
* Early Stopping helps reduce unnecessary training and prevents overfitting.
* Data Augmentation improves the model's ability to generalize by exposing it to transformed images.

---

## 📉 Model Comparison

The models were compared using:

* Test Accuracy
* Validation Loss Curves
* Training vs Validation Accuracy
* Generalization Ability
* Training Strategies

---

## 🚀 Key Learning Outcomes

Through this project, I learned:

* Difference between ANN and CNN
* Image preprocessing techniques
* CNN architecture design
* Effect of network depth
* Importance of convolution and pooling layers
* Batch Normalization
* Dropout Regularization
* Early Stopping
* Data Augmentation
* Model evaluation and comparison

---

## ▶️ How to Run

1. Clone the repository.

```bash
git clone https://github.com/your-username/image-classification-cifar10.git
```

2. Install dependencies.

```bash
pip install -r requirements.txt
```

3. Open the notebook.

```
notebooks/cifar10_ann_cnn.ipynb
```

4. Run all cells.

---

## 📌 Conclusion

This project demonstrates that **Convolutional Neural Networks (CNNs)** are much more effective than **Artificial Neural Networks (ANNs)** for image classification tasks. CNNs preserve spatial information and automatically learn meaningful image features, leading to significantly higher accuracy and better generalization. Training strategies such as Batch Normalization, Dropout, Early Stopping, and Data Augmentation further improve model robustness and performance.

---

## 👨‍💻 Author

**Siddharth Gupta**

B.Tech CSE (AI, ML & Robotics)

DIT University
