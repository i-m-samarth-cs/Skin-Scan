import cv2
import numpy as np
import matplotlib.pyplot as plt
import io
import base64
from PIL import Image

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

def get_image_features(image_path):
    """Extract basic features from the lesion image"""
    # Get the segmented image and contour
    segmented, _ = segment_lesion(image_path)
    
    # Convert to grayscale
    gray = cv2.cvtColor(segmented, cv2.COLOR_RGB2GRAY)
    
    # Find non-zero pixels (the lesion)
    non_zero = cv2.findNonZero(gray)
    
    if non_zero is None or len(non_zero) == 0:
        return {
            'area': 0,
            'perimeter': 0,
            'circularity': 0,
            'asymmetry': 0
        }
    
    # Calculate basic features
    x, y, w, h = cv2.boundingRect(non_zero)
    area = cv2.countNonZero(gray)
    
    # Find contours for perimeter calculation
    contours, _ = cv2.findContours(gray, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contours:
        perimeter = 0
        circularity = 0
    else:
        largest_contour = max(contours, key=cv2.contourArea)
        perimeter = cv2.arcLength(largest_contour, True)
        circularity = 4 * np.pi * area / (perimeter * perimeter) if perimeter > 0 else 0
    
    # Calculate asymmetry (using moments)
    moments = cv2.moments(gray)
    if moments['m00'] != 0:
        cx = int(moments['m10'] / moments['m00'])
        cy = int(moments['m01'] / moments['m00'])
        # Create a flipped version and compare
        flipped = cv2.flip(gray, 1)
        diff = cv2.absdiff(gray, flipped)
        asymmetry = np.sum(diff) / (area * 255) if area > 0 else 0
    else:
        asymmetry = 0
    
    return {
        'area': area,
        'perimeter': perimeter,
        'circularity': circularity,
        'asymmetry': asymmetry
    }

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
