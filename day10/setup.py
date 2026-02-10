from setuptools import setup, find_packages

setup(
    name="video_labeler_pro",
    version="1.0.0",
    description="Professional Video Labeling Tool with SAM 2",
    author="Arihant",
    packages=find_packages(),
    install_requires=[
        "torch",
        "opencv-python",
        "numpy",
        "Pillow",
        "pyyaml",
    ],
    entry_points={
        "console_scripts": [
            "video-labeler=labeler_app.main:main",
        ],
    },
)
