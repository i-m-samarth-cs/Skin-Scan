import cv2
import numpy as np
import matplotlib.pyplot as plt
import io
import base64
from PIL import Image

def get_image_features(image_path):
    """Extract features from the skin lesion image using a pre-trained VGG16 model."""
    # Read the image
    img = cv2.imread(image_path)
    
    # Resize the image to 224x224 (VGG16 input size)
    img_resized = cv2.resize(img, (224, 224))
    
    # Convert image to RGB
    img_rgb = cv2.cvtColor(img_resized, cv2.COLOR_BGR2RGB)
    
    # Expand dimensions for model input
    img_expanded = np.expand_dims(img_rgb, axis=0)
    
    # Preprocess the image for VGG16
    img_preprocessed = preprocess_input(img_expanded)
    
    # Load pre-trained VGG16 model (include top layer)
    model = VGG16(weights='imagenet', include_top=False)
    
    # Get features from the model
    features = model.predict(img_preprocessed)
    
    # Flatten the features to a 1D array
    flattened_features = features.flatten()
    
    return flattened_features

def enhance_image(image_path):
    """Enhance the skin lesion image for better visualization"""
    # Read the image
    img = cv2.imread(image_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    # Apply histogram equalization to improve contrast
    img_yuv = cv2.cvtColor(img, cv2.COLOR_RGB2YUV)
    img_yuv[:,:,0] = cv2.equalizeHist(img_yuv[:,:,0])
    enhanced_img = cv2.cvtColor(img_yuv, cv2.COLOR_YUV2RGB)
    
    return enhanced_img

def segment_lesion(image_path):
    """Segment the skin lesion from the background"""
    # Read the image
    img = cv2.imread(image_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    
    # Apply Gaussian blur to reduce noise
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    
    # Thresholding to get binary image
    _, thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    
    # Find the largest contour (assumed to be the lesion)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    if not contours:
        return img, img  # Return original if no contours found
    
    # Find the largest contour
    largest_contour = max(contours, key=cv2.contourArea)
    
    # Create mask and fill the largest contour
    mask = np.zeros(thresh.shape, np.uint8)
    cv2.drawContours(mask, [largest_contour], 0, 255, -1)
    
    # Apply the mask to the original image
    segmented = cv2.bitwise_and(img, img, mask=mask)
    
    # Create a version with highlighted contour
    highlighted = img.copy()
    cv2.drawContours(highlighted, [largest_contour], 0, (0, 255, 0), 2)
    
    return segmented, highlighted

def preprocess_image(image_path):
    """Preprocess the image for model input"""
    # Read the image
    img = cv2.imread(image_path)
    
    # Resize the image to 224x224 (assuming the model requires this input size)
    img_resized = cv2.resize(img, (224, 224))
    
    # Normalize the image by scaling pixel values to [0, 1]
    img_normalized = img_resized.astype('float32') / 255.0
    
    return img_normalized

def augment_image(image_path):
    """Apply random augmentation techniques to the image"""
    img = cv2.imread(image_path)
    
    # Flip the image horizontally
    flipped = cv2.flip(img, 1)
    
    # Rotate the image by a random angle
    angle = np.random.randint(-15, 15)
    M = cv2.getRotationMatrix2D((img.shape[1] // 2, img.shape[0] // 2), angle, 1)
    rotated = cv2.warpAffine(img, M, (img.shape[1], img.shape[0]))
    
    # Randomly adjust brightness (scale by a factor)
    alpha = np.random.uniform(0.7, 1.3)
    augmented_img = cv2.convertScaleAbs(img, alpha=alpha)
    
    return flipped, rotated, augmented_img

def crop_lesion(image_path):
    """Crop the lesion area from the image using segmentation"""
    # Segment the lesion
    segmented, _ = segment_lesion(image_path)
    
    # Convert the segmented image to grayscale
    gray = cv2.cvtColor(segmented, cv2.COLOR_RGB2GRAY)
    
    # Find non-zero pixels to detect the lesion boundary
    non_zero = cv2.findNonZero(gray)
    
    if non_zero is None or len(non_zero) == 0:
        return None  # No lesion found, return None
    
    # Get the bounding rectangle for the lesion
    x, y, w, h = cv2.boundingRect(non_zero)
    
    # Crop the image to the bounding box around the lesion
    cropped_lesion = segmented[y:y+h, x:x+w]
    
    return cropped_lesion

def create_analysis_plots(image_path):
    """Create analysis plots for the image"""
    # Original image
    img = cv2.imread(image_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    # Enhanced image
    enhanced = enhance_image(image_path)
    
    # Segmented image and contour
    segmented, contour = segment_lesion(image_path)
    
    # Create figure with subplots
    fig, axes = plt.subplots(2, 2, figsize=(10, 8))
    
    # Original
    axes[0, 0].imshow(img)
    axes[0, 0].set_title('Original Image')
    axes[0, 0].axis('off')
    
    # Enhanced
    axes[0, 1].imshow(enhanced)
    axes[0, 1].set_title('Enhanced Image')
    axes[0, 1].axis('off')
    
    # Segmented
    axes[1, 0].imshow(segmented)
    axes[1, 0].set_title('Segmented Lesion')
    axes[1, 0].axis('off')
    
    # Contour
    axes[1, 1].imshow(contour)
    axes[1, 1].set_title('Lesion Boundary')
    axes[1, 1].axis('off')
    
    # Tight layout
    plt.tight_layout()
    
    # Convert plot to image
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close(fig)
    buf.seek(0)
    
    # Encode to base64 for Streamlit
    data = base64.b64encode(buf.read()).decode('utf-8')
    return f"data:image/png;base64,{data}"
