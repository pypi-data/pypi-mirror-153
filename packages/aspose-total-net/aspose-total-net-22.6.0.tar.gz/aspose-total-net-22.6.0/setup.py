# coding: utf-8
from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

NAME = "aspose-total-net"
VERSION = "22.6.0"

REQUIRES = ['aspose-words',
            'Aspose.Slides',
            'Aspose.Email-for-Python-via-NET',
            'aspose-3d']
setup(
    name=NAME,
    version=VERSION,
    description='Aspose.Total for Python via .NET is a Document Processing python class library that allows developers to work with Microsoft Word®, Microsoft PowerPoint®, Microsoft Outlook®, OpenOffice®, & 3D file formats without needing Office Automation.',
    keywords=["DOC", "DOCX", "RTF", "DOT", "DOTX", "DOTM", "DOCM FlatOPC", "FlatOpcMacroEnabled", "FlatOpcTemplate", "FlatOpcTemplateMacroEnabled", "ODT", "OTT", "WordML", "HTML", "MHTML", "PDF", "MOBI", "TXT", "PDF/A", "XPS", "OpenXPS", "PostScript (PS)", "TIFF", "JPEG", "PNG", "BMP", "SVG", "EMF", "GIF", "HtmlFixed", "PCL", "EPUB", "XamlFixed", "XamlFlow", "XamlFlowPack", "MSG", "PST", "OST", "OFT", "EML", "EMLX", "MBOX", "ICS", "VCF", "OLM", "PPT", "PPTX", "PPS", "POT", "PPSX", "PPTM", "PPSM", "POTX", "POTM", "ODP", "FBX", "STL", "OBJ", "3DS", "U3D",
              "DAE", "glTF", "ASCII", "Binary", "DRC", "RVM", "AMF", "PLY", "A3DW", "X", "DirectX", "JT", "DXF", "3MF", "ASE", "VRML", "Create", "Clone", "Render", "Compare", "Join", "Split", "Encrypt", "Digital Signature", "Mail Merge", "Reporting", "Watermark", "LINQ", "Reporting Engine", "Editor", "Merger", "Viewer", "Conversion", "Splitter", "OCR", "Translator", "Compress", "SSL", "TLS", "TNEF", "Email Attachment", "Email", "POP3", "IMAP", "iCalendar", "OleObject", "Chart", "3D", "Scene", "Triangulate", "Vulkan", "Geometry", "Camera", "Mesh", "Shape"],
    url='https://products.aspose.com/total/python-net',
    author='Aspose',
    author_email='total@aspose.com',
    license='UNKNOWN',
    packages=['aspose-total-net'],
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
