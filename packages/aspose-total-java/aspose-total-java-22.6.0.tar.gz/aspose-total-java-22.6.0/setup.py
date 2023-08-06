# coding: utf-8
from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

NAME = "aspose-total-java"
VERSION = "22.6.0"

REQUIRES = ["aspose-cells",
            "aspose-barcode-for-python-via-java",
            "aspose-diagram"]

setup(
    name=NAME,
    version=VERSION,
    description='Aspose.Total for Python via Java is a file format Processing python class library that allows developers to work with Microsoft Excel®, Microsoft Visio®, and barcode file formats without needing Office Automation.',
    keywords=["XLS","XLSX","XLSB","XLTX","XLTM","XLSM","XML","ODS","CSV","TSV","TXT","HTML","MHTML","PDF","PDF/A","XPS","JPEG","PNG","BMP","SVG","EMF","GIF","VSDX","VDX","VSX","VTX","VSSX","VSTX","VSDM","VSSM","VSTM","XAML","On Premise API","High Code API","API","Spreadsheets","Excel","Barcode","1D Barcode","2D Barcode","Python Java","Diagram","Visio","Barcode Generation","Barcode Recognition","Read","Write","Export","Worksheet","Render","Text","Image","Scan","High Fidelity","Shapes","File Format","Symbologies","Codabar","Code Text","QR Code","Pivot Table","Pivot Charts","DataMatrix","Aztec","Pdf417","MacroPdf417"],
    url='https://products.aspose.com/total/python-java',
    author='Aspose',
    author_email='total@aspose.com',
    license='UNKNOWN',
    packages=['aspose-total-java'],
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=REQUIRES,
    zip_safe=False,
    classifiers=[
        'Programming Language :: Python :: 3.5',
        'License :: Other/Proprietary License'
    ],
    platforms=[
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows :: Windows 7',
        'Operating System :: Microsoft :: Windows :: Windows Vista',
        'Operating System :: POSIX :: Linux',
    ],
    python_requires='>=3.5',
)
