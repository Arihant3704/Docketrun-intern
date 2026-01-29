
export const courseContent = {
    // --- NumPy Modules ---
    'numpy/intro': {
        title: 'Introduction to NumPy',
        sections: [
            {
                type: 'text',
                content: `NumPy (Numerical Python) is the fundamental package for scientific computing in Python. It provides a high-performance multidimensional array object, and tools for working with these arrays.`
            },
            {
                type: 'callout',
                variant: 'info',
                title: 'Why NumPy?',
                content: 'NumPy arrays are faster and more compact than Python lists. An array consumes less memory and is convenient to use.'
            },
            {
                type: 'text',
                content: `To get started, you need to install it and import it. The convention is to import it as 'np'.`
            },
            {
                type: 'code',
                title: 'Installation & Import',
                code: `
# Installation
# pip install numpy

import numpy as np

print(np.__version__)
        `
            },
            {
                type: 'text',
                content: 'The core of NumPy is the **ndarray** (n-dimensional array) object. Try running this code yourself directly in the browser!'
            },
            {
                type: 'interactive-code',
                title: 'Your First Array (Interactive)',
                code: `import numpy as np

# Create a 1D array
arr = np.array([1, 2, 3, 4, 5])

print("Array:", arr)
print("Type:", type(arr))
print("Sum:", arr.sum())`
            }
        ],
        quiz: [
            {
                question: 'Which of the following creates an array of zeros?',
                options: ['np.empty(5)', 'np.zeros(5)', 'np.array(0, 5)', 'np.0(5)'],
                answer: 1 // correct index
            },
            {
                question: 'What is the main advantage of NumPy arrays over Python lists?',
                options: ['They are slower', 'They consume more memory', 'They are faster and more compact', 'They can only hold integers'],
                answer: 2
            }
        ]
    },
    'numpy/creating-arrays': {
        title: 'Creating Arrays',
        sections: [
            {
                type: 'text',
                content: 'NumPy offers several ways to create arrays beyond just converting lists.'
            },
            {
                type: 'code',
                title: 'Common Creation Methods',
                code: `
import numpy as np

# Array of zeros
zeros = np.zeros(5)
print(zeros) # [0. 0. 0. 0. 0.]

# Array of ones
ones = np.ones((2, 3)) # 2 rows, 3 cols
print(ones)

# Range of numbers (like range())
seq = np.arange(0, 10, 2)
print(seq) # [0 2 4 6 8]

# Linearly spaced numbers
lin = np.linspace(0, 1, 5)
print(lin) # [0.   0.25 0.5  0.75 1.  ]

# Random arrays
rand = np.random.rand(3, 3) # Uniform distribution [0, 1)
print(rand)
        `
            }
        ]
    },
    'numpy/operations': {
        title: 'Array Operations',
        sections: [
            {
                type: 'text',
                content: 'One of the main advantages of NumPy is the ability to perform element-wise operations efficiently.'
            },
            {
                type: 'code',
                title: 'Arithmetic Operations',
                code: `
a = np.array([1, 2, 3, 4])
b = np.array([10, 20, 30, 40])

# Element-wise addition
print(a + b)  # [11 22 33 44]

# Scalar multiplication
print(a * 2)  # [2 4 6 8]

# Powers
print(a ** 2) # [ 1  4  9 16]
        `
            },
            {
                type: 'text',
                content: 'NumPy also provides many universal functions (ufuncs) like `sin`, `cos`, `exp`, `sqrt`.'
            },
            {
                type: 'code',
                title: 'Universal Functions',
                code: `
x = np.array([0, np.pi/2, np.pi])
print(np.sin(x))
# [0.0000000e+00 1.0000000e+00 1.2246468e-16]
        `
            }
        ]
    },
    'numpy/indexing': {
        title: 'Indexing & Slicing',
        sections: [
            {
                type: 'text',
                content: 'Indexing in NumPy is similar to Python lists but much more powerful.'
            },
            {
                type: 'code',
                title: 'Basic Slicing',
                code: `
arr = np.array([0, 1, 2, 3, 4, 5])

print(arr[1:4])  # [1 2 3]
print(arr[:3])   # [0 1 2]
print(arr[::2])  # [0 2 4] (step 2)
        `
            },
            {
                type: 'text',
                content: 'You can also use **Boolean Indexing** to filter data.'
            },
            {
                type: 'code',
                title: 'Boolean Indexing',
                code: `
arr = np.array([1, 10, 3, 25, 4])

# Create a boolean mask
mask = arr > 5
print(mask) # [False  True False  True False]

# Use mask to index
print(arr[mask]) # [10 25]

# One-liner
print(arr[arr > 5]) # [10 25]
        `
            }
        ]
    },
    'numpy/broadcasting': {
        title: 'Broadcasting',
        sections: [
            {
                type: 'text',
                content: 'Broadcasting is a powerful mechanism that allows NumPy to work with arrays of different shapes during arithmetic operations.'
            },
            {
                type: 'callout',
                variant: 'info',
                title: 'Rule of Broadcasting',
                content: 'Two dimensions are compatible when: 1. they are equal, or 2. one of them is 1.'
            },
            {
                type: 'code',
                title: 'Broadcasting Example',
                code: `
A = np.array([[1, 2, 3],
              [4, 5, 6]]) # Shape (2, 3)

b = np.array([10, 20, 30]) # Shape (3,)

# b is 'broadcast' across the rows of A
C = A + b
print(C)
# [[11 22 33]
#  [14 25 36]]
        `
            }
        ]
    },

    // --- Pandas Modules ---
    'pandas/intro': {
        title: 'Series & DataFrames',
        sections: [
            { type: 'text', content: 'Pandas is built on top of NumPy and provides two main data structures: **Series** (1D) and **DataFrame** (2D).' },
            {
                type: 'code', title: 'Creating a DataFrame', code: `
import pandas as pd

data = {
    'Name': ['Alice', 'Bob', 'Charlie'], 
    'Age': [25, 30, 35],
    'City': ['New York', 'Paris', 'London']
}

df = pd.DataFrame(data)
print(df)
            ` },
            { type: 'text', content: 'A DataFrame represents tabular data, similar to a spreadsheet or SQL table.' }
        ]
    },
    'pandas/io': {
        title: 'Reading & Writing Data',
        sections: [
            { type: 'text', content: 'Pandas makes it incredibly easy to read data from various file formats like CSV, Excel, JSON, and SQL.' },
            {
                type: 'code', title: 'Reading CSV', code: `
# Read a CSV file into a DataFrame
df = pd.read_csv('data.csv')

# Inspect the first 5 rows
print(df.head())

# Write to a customized CSV
df.to_csv('output.csv', index=False)
            ` },
            { type: 'callout', variant: 'info', title: 'Pro Tip', content: 'You can also read directly from URLs! e.g. pd.read_csv("https://bit.ly/...")' }
        ]
    },
    'pandas/cleaning': {
        title: 'Data Cleaning',
        sections: [
            { type: 'text', content: 'Real-world data is messy. Pandas provides tools to handle missing values and duplicates.' },
            {
                type: 'code', title: 'Handling Missing Data', code: `
import numpy as np

# DataFrame with missing values
df = pd.DataFrame({'A': [1, 2, np.nan], 'B': [5, np.nan, np.nan]})

# Check for nulls
print(df.isnull().sum())

# Drop rows with any missing values
cleaned = df.dropna()

# Fill missing values with a specific value (e.g. 0)
filled = df.fillna(0)
            ` },
            { type: 'text', content: 'Removing duplicates is also straightforward with `drop_duplicates()`.' }
        ]
    },
    'pandas/manipulation': {
        title: 'Data Manipulation',
        sections: [
            { type: 'text', content: 'Filtering, sorting, and adding new columns are daily tasks in data science.' },
            {
                type: 'code', title: 'Filtering & Adding Columns', code: `
data = {'Product': ['A', 'B', 'C', 'A'], 'Sales': [100, 200, 150, 300]}
df = pd.DataFrame(data)

# Filter rows where Sales > 150
high_sales = df[df['Sales'] > 150]

# Add a new 'Tax' column
df['Tax'] = df['Sales'] * 0.1
print(df)
            ` }
        ]
    },
    'pandas/aggregation': {
        title: 'Aggregation & Grouping',
        sections: [
            { type: 'text', content: 'The `groupby` method allows you to group data and apply aggregate functions (sum, mean, count).' },
            {
                type: 'code', title: 'Group By Example', code: `
df = pd.DataFrame({
    'Category': ['Tech', 'Tech', 'Health', 'Health'],
    'Revenue': [1000, 1500, 500, 600]
})

# Total revenue by category
grouped = df.groupby('Category')['Revenue'].sum()
print(grouped)
# Output:
# Health    1100
# Tech      2500
# Name: Revenue, dtype: int64
            ` }
        ]
    },

    // --- Matplotlib Modules ---
    'matplotlib/intro': {
        title: 'Basic Plotting',
        sections: [
            { type: 'text', content: 'Matplotlib is the "grandfather" of Python visualization libraries. It mimics MATLAB\'s plotting interface.' },
            {
                type: 'code', title: 'Simple Line Plot', code: `
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(0, 10, 100)
y = np.sin(x)

plt.figure(figsize=(8, 4))
plt.plot(x, y, label='Sin(x)')
plt.title('My First Plot')
plt.xlabel('X Axis')
plt.ylabel('Y Axis')
plt.legend()
plt.show() # In a notebook/script this displays the plot
            ` }
        ]
    },
    'matplotlib/customization': {
        title: 'Customizing Plots',
        sections: [
            { type: 'text', content: 'You have full control over every element: colors, markers, line styles, and fonts.' },
            {
                type: 'code', title: 'Styling Example', code: `
x = np.linspace(0, 5, 20)
y = x ** 2

plt.plot(x, y, 
         color='purple', 
         linestyle='--', 
         marker='o', 
         linewidth=2,
         markersize=6)
plt.grid(True, alpha=0.3)
            ` }
        ]
    },
    'matplotlib/subplots': {
        title: 'Subplots & Layouts',
        sections: [
            { type: 'text', content: 'Often you want to display multiple plots side-by-side using `plt.subplots`.' },
            {
                type: 'code', title: 'Creating Subplots', code: `
# Create a figure with 1 row and 2 columns
fig, axes = plt.subplots(1, 2, figsize=(10, 4))

# First plot
axes[0].plot(x, np.sin(x), 'r')
axes[0].set_title('Sine')

# Second plot
axes[1].plot(x, np.cos(x), 'b')
axes[1].set_title('Cosine')

plt.tight_layout() # Adjusts spacing automatically
            ` }
        ]
    },
    'matplotlib/types': {
        title: 'Advanced Plot Types',
        sections: [
            { type: 'text', content: 'Beyond line plots, Matplotlib supports bars, scatter plots, histograms, and heatmaps.' },
            {
                type: 'code', title: 'Scatter & Bar', code: `
# Scatter Plot
plt.scatter(x, y, alpha=0.5)

# Bar Chart
categories = ['A', 'B', 'C']
values = [10, 20, 15]
plt.bar(categories, values, color=['red', 'green', 'blue'])
            ` }
        ]
    },

    // --- OpenCV Modules ---
    'opencv/intro': {
        title: 'Images & Video',
        sections: [
            { type: 'text', content: 'OpenCV (Open Source Computer Vision Library) is the industry standard for computer vision tasks.' },
            {
                type: 'code', title: 'Reading & Displaying', code: `
import cv2

# Read an image (returns a NumPy array)
# 0 = grayscale, 1 = color
img = cv2.imread('image.jpg', 1)

# Check dimensions (Height, Width, Channels)
print(img.shape) 

# Display the image
cv2.imshow('My Image', img)
cv2.waitKey(0) # Wait for any key press
cv2.destroyAllWindows()
            ` }
        ]
    },
    'opencv/drawing': {
        title: 'Drawing Shapes',
        sections: [
            { type: 'text', content: 'You can draw directly on images (NumPy arrays).' },
            {
                type: 'code', title: 'Drawing Functions', code: `
# Create a blank black image
img = np.zeros((512, 512, 3), np.uint8)

# Draw a blue diagonal line (BGR format)
cv2.line(img, (0, 0), (511, 511), (255, 0, 0), 5)

# Draw a green rectangle
cv2.rectangle(img, (384, 0), (510, 128), (0, 255, 0), 3)

# Draw a red circle
cv2.circle(img, (447, 63), 63, (0, 0, 255), -1) # -1 fills it
            ` }
        ]
    },
    'opencv/processing': {
        title: 'Image Processing',
        sections: [
            { type: 'text', content: 'Transform images using standard kernels and filters.' },
            {
                type: 'code', title: 'Convert & Blur', code: `
# Convert BGR to Grayscale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Gaussian Blur (removes noise)
blur = cv2.GaussianBlur(gray, (5, 5), 0)

# Canny Edge Detection
edges = cv2.Canny(img, 100, 200)
            ` }
        ]
    },
    'opencv/detection': {
        title: 'Object Detection',
        sections: [
            { type: 'text', content: 'Face detection using Haar Cascades is a classic computer vision "Hello World".' },
            {
                type: 'code', title: 'Haar Cascade Face Detect', code: `
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
faces = face_cascade.detectMultiScale(gray, 1.1, 4)

for (x, y, w, h) in faces:
    cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
            ` }
        ]
    },

    // --- Scikit-Learn Modules ---
    'sklearn/intro': {
        title: 'The Machine Learning Workflow',
        sections: [
            { type: 'text', content: 'Scikit-learn (sklearn) is the most popular library for traditional machine learning in Python.' },
            {
                type: 'code', title: 'Data Split', code: `
from sklearn.model_selection import train_test_split
import numpy as np

X, y = np.arange(10).reshape((5, 2)), range(5)

# Split arrays or matrices into random train and test subsets
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.33, random_state=42)

print("Train shape:", X_train.shape)
print("Test shape:", X_test.shape)
            ` }
        ]
    },
    'sklearn/preprocessing': {
        title: 'Preprocessing',
        sections: [
            { type: 'text', content: 'Most ML models require data to be scaled or standardized before training.' },
            {
                type: 'code', title: 'StandardScaler', code: `
from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()

# Fit on training set only
scaler.fit(X_train)

# Apply transform to both
X_train_scaled = scaler.transform(X_train)
X_test_scaled = scaler.transform(X_test)
            ` }
        ]
    },
    'sklearn/supervised': {
        title: 'Supervised Learning',
        sections: [
            { type: 'text', content: 'Classification models predict categories. Regression models predict continuous values.' },
            {
                type: 'code', title: 'Logicistic Regression', code: `
from sklearn.linear_model import LogisticRegression

# Initialize
clf = LogisticRegression()

# Train
clf.fit(X_train_scaled, y_train)

# Predict
predictions = clf.predict(X_test_scaled)
print(predictions)
            ` }
        ]
    },
    'sklearn/unsupervised': {
        title: 'Unsupervised Learning',
        sections: [
            { type: 'text', content: 'Clustering algorithms like K-Means group similar data points together without labels.' },
            {
                type: 'code', title: 'K-Means Clustering', code: `
from sklearn.cluster import KMeans

# 3 clusters
kmeans = KMeans(n_clusters=3, random_state=0)

kmeans.fit(X)

print(kmeans.labels_)
print(kmeans.cluster_centers_)
            ` }
        ]
    },
    'sklearn/evaluation': {
        title: 'Model Evaluation',
        sections: [
            { type: 'text', content: 'Metrics tell you how good your model is.' },
            {
                type: 'code', title: 'Accuracy & Confusion Matrix', code: `
from sklearn.metrics import accuracy_score, confusion_matrix

acc = accuracy_score(y_test, predictions)
print(f"Accuracy: {acc}")

cm = confusion_matrix(y_test, predictions)
print("Confusion Matrix:")
print(cm)
            ` }
        ]
    }, // Added missing comma

    // --- Projects ---
    'projects/crypto-analyzer': {
        title: 'Project 1: Crypto Market Analyzer',
        sections: [
            { type: 'text', content: 'In this project, we will use **Pandas** and **Matplotlib** to analyze historical cryptocurrency data, calculate moving averages, and visualize trends.' },
            { type: 'callout', variant: 'info', title: 'Goal', content: 'visualize the "Golden Cross" (when 50-day SMA crosses above 200-day SMA) for Bitcoin.' },
            {
                type: 'code', title: '1. Load & Inspect Data', code: `
import pandas as pd
import matplotlib.pyplot as plt

# Simulate loading data (in reality, read from CSV or API)
data = {
    'Date': pd.date_range(start='2023-01-01', periods=100),
    'Close': np.random.normal(30000, 1000, 100).cumsum() # Random walk
}
df = pd.DataFrame(data)
df.set_index('Date', inplace=True)

print(df.head())
            ` },
            {
                type: 'code', title: '2. Calculate Moving Averages', code: `
# Calculate Simple Moving Averages (SMA)
df['SMA_20'] = df['Close'].rolling(window=20).mean()
df['SMA_50'] = df['Close'].rolling(window=50).mean()

# Check for NaNs created by rolling window
df.dropna(inplace=True)
            ` },
            {
                type: 'code', title: '3. Visualize', code: `
plt.figure(figsize=(12, 6))
plt.plot(df.index, df['Close'], label='Price', alpha=0.5)
plt.plot(df.index, df['SMA_20'], label='SMA 20', color='orange')
plt.plot(df.index, df['SMA_50'], label='SMA 50', color='purple')

plt.title('Bitcoin Price Strategy')
plt.legend()
plt.show()
            ` }
        ]
    },
    'projects/smart-attendance': {
        title: 'Project 2: Smart Attendance System',
        sections: [
            { type: 'text', content: 'This project uses **OpenCV** to detect faces in real-time and log attendance to a CSV file.' },
            {
                type: 'code', title: 'Face Detection Loop', code: `
import cv2
import pandas as pd
from datetime import datetime

# Load pre-trained face detector
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

# Start video capture
cap = cv2.VideoCapture(0)

attendance_log = []

while True:
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)
    
    for (x, y, w, h) in faces:
        # Draw rectangle
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        
        # Log attendance (simplification: log every detection)
        attendance_log.append({
            'Time': datetime.now(), 
            'Status': 'Present'
        })
        
    cv2.imshow('Smart Attendance', frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

# Save to CSV
pd.DataFrame(attendance_log).to_csv('attendance.csv', index=False)
            ` }
        ]
    },
    'projects/movie-recommender': {
        title: 'Project 3: Movie Recommendation Engine',
        sections: [
            { type: 'text', content: 'We will build a content-based recommendation system using **Scikit-Learn** and **Pandas** that suggests movies based on similarity using Cosine Similarity.' },
            {
                type: 'code', title: 'The Recommendation Logic', code: `
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd

# Sample Dataset
movies = pd.DataFrame({
    'Title': ['The Matrix', 'Inception', 'Toy Story', 'Shrek'],
    'Keywords': ['action sci-fi', 'action sci-fi dream', 'animation kids', 'animation comedy']
})

# 1. Convert text to vectors
cv = CountVectorizer()
count_matrix = cv.fit_transform(movies['Keywords'])

# 2. Compute Cosine Similarity
cosine_sim = cosine_similarity(count_matrix)

# 3. Function to recommend
def recommend(movie_title):
    idx = movies[movies['Title'] == movie_title].index[0]
    scores = list(enumerate(cosine_sim[idx]))
    sorted_scores = sorted(scores, key=lambda x: x[1], reverse=True)
    
    # Return top 2 similar movies (excluding itself)
    return [movies.iloc[i[0]]['Title'] for i in sorted_scores[1:3]]

print(recommend('The Matrix')) 
# Output: ['Inception', 'Toy Story'] (Example)
            ` }
        ]
    }
};
