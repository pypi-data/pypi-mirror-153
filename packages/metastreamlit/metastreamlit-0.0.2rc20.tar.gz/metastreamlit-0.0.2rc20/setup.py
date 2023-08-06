import setuptools
import os

METASTREAMLIT_VERSION = os.environ.get("METASTREAMLIT_VERSION", "0.0.0")

setuptools.setup(
    name="metastreamlit",
    version=METASTREAMLIT_VERSION,
    author="Daniel Haziza",
    author_email="",
    description="Helper library for creating ML demos in streamlit",
    long_description="",
    long_description_content_type="text/plain",
    url="",
    packages=setuptools.find_packages(),
    include_package_data=True,
    classifiers=[],
    python_requires=">=3.6",
    install_requires=[
        # By definition, a Custom Component depends on Streamlit.
        # If your component has other Python dependencies, list
        # them here.
        "streamlit >= 1.9",
    ],
)
