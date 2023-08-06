import json
import requests
import xml.dom.minidom
from xml.dom.minidom import Node

import os
import sys
import inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)


from simple_rss_reader.exceptions import InvalidXML, RequestError


class SimpleRssReader:
    def __init__(self, source: str):
        """
        Constructor for Simple Rss Reader

        :param source: string contain xml string or url
        :return:
        """
        self.rss = self.load_source(source)

        try:
            self.xmlparse = self.get_xmlparse()
        except Exception as e:
            raise InvalidXML("input is not a valid xml file")
        self.parsed = self._get_xml_items()

    def _get_xml_items(self):
        """
        Perse the xml into items

        :return: Dict represent headers data and items
        """
        for elem in self.xmlparse.getElementsByTagName("channel"):
            res = {"headers": {}, "items": []}
            for x in elem.childNodes:
                if x.nodeType == Node.ELEMENT_NODE and x.tagName == "item":
                    item = {}
                    for item_el in x.childNodes:
                        if item_el.nodeType == Node.ELEMENT_NODE and len(
                            item_el.childNodes
                        ):
                            item[item_el.tagName] = item_el.childNodes[0].data
                    res["items"].append(item)
                elif x.nodeType == Node.ELEMENT_NODE:
                    if hasattr(x.childNodes[0], "data"):
                        res["headers"][x.tagName] = x.childNodes[0].data
        return res

    def prettyxml(self):
        """RequestError
        A wrapper for xmlparse.toprettyxml function
        :return: formmated XML
        """
        print(self.xmlparse.toprettyxml())

    def get_xmlparse(self):
        return xml.dom.minidom.parseString(self.rss)

    def request(self, source):
        res = requests.get(source)
        if res.ok:
            return res.content
        else:
            raise RequestError(f"Not A valid url, status: {res.status_code}")

    def load_source(self, source: str):
        try:
            return self.request(source) if source.startswith("http") == True else source
        except Exception as e:
            raise RequestError("input is not a valid xml file")

    def to_dict(self):
        """
        Get xml data as dict

        :return: Dict represent the xml data
        """
        return self.parsed

    def to_json(self):
        """
        Get xml data as json

        :return: data in json format
        """
        return json.dumps(self.parsed)

    def get_items(self):
        return self.parsed["items"]


if __name__ == "__main__":
    """
    Usage Example, pass url as argument
    """

    print(
        r"""
    Cosmo is purring
    |\---/|
    | o_o |
     \_^_/
    
    Ginger say Meow
    |\---/|
    | o_o |
     \_^_/
        """
    )
    import sys

    if (len(sys.argv)) == 1:
        raise Exception("No url given as a command argument")
    print(sys.argv[1])

    a = SimpleRssReader(sys.argv[1])
    print(a.to_dict())
