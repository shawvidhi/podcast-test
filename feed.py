import yaml  # Import the YAML module to parse the feed.yaml file
import xml.etree.ElementTree as xml_tree  # Import the XML module to create and write XML data

# Open the YAML file and load its content into a Python dictionary
with open('feed.yaml', 'r') as file:
    yaml_data = yaml.safe_load(file)  # Parse the YAML file and store its data in 'yaml_data'

# Create the root <rss> element with attributes for version and namespaces
rss_element = xml_tree.Element('rss', {
    'version': '2.0',  # Specify the RSS version
    'xmlns:itunes': 'http://www.itunes.com/dtds/podcast-1.0.dtd',  # Add the iTunes namespace
    'xmlns:content': 'http://purl.org/rss/1.0/modules/content/'  # Add the content namespace
})

# Create a <channel> element as a child of the <rss> element
channel_element = xml_tree.SubElement(rss_element, 'channel')

link_prefix = yaml_data['link']

# Add a <title> element inside the <channel> and set its text to the title from the YAML data
xml_tree.SubElement(channel_element, 'title').text = yaml_data['title']
xml_tree.SubElement(channel_element, 'format').text = yaml_data['format']
xml_tree.SubElement(channel_element, 'subtitle').text = yaml_data['subtitle']
xml_tree.SubElement(channel_element, 'itunes:author').text = yaml_data['author']
xml_tree.SubElement(channel_element, 'description').text = yaml_data['description']
xml_tree.SubElement(channel_element, 'itunes:image', {'href': link_prefix + yaml_data['image']})
xml_tree.SubElement(channel_element, 'language').text = yaml_data['language']
xml_tree.SubElement(channel_element, 'link').text = link_prefix

xml_tree.SubElement(channel_element, 'category').text = yaml_data['category']


for item in yaml_data['item']:
    item_element = xml_tree.SubElement(channel_element, 'item') 
    xml_tree.SubElement(item_element, 'title').text = item['title']
    xml_tree.SubElement(item_element, 'itunes:author').text = yaml_data['author']
    xml_tree.SubElement(item_element, 'description').text = item['description']
    xml_tree.SubElement(item_element, 'itunes:duration').text = item['duration']
    xml_tree.SubElement(item_element, 'pubDate').text = item['published']
    xml_tree.SubElement(item_element, 'title').text = item['title']

    enclosure = xml_tree.SubElement(item_element, 'enclosure', {
        'url' : link_prefix + item['file'], 
        'type' : 'audio/mpeg',
        'length' : item['length']  
    })

# Create an ElementTree object with the root <rss> element
output_tree = xml_tree.ElementTree(rss_element)

# Write the XML tree to a file named 'podcast.xml'
# Use UTF-8 encoding and include an XML declaration at the top
output_tree.write('podcast.xml', encoding='UTF-8', xml_declaration=True)
