import xml.etree.ElementTree as ET

def read_csproject_file(filepath):
    xml = ET.parse(filepath)
    root = xml.getroot()
    namespaces = {'pns': 'http://schemas.microsoft.com/developer/msbuild/2003'}

    for item in root.findall("*/pns:Content", namespaces=namespaces):
        print item.get('Include')
