from xml.etree.ElementTree import Element

from lxml import etree


class XmlProcessor:
    def __init__(self, text: str) -> None:
        self.parser = etree.iterwalk(
            etree.HTML(text),
            events=("end",),
        )

    def __iter__(self):
        for event in self.parser:
            _, element = event
            element: etree._Element

            if element.tag == "p":
                if element.text is None:
                    yield Element("empty-line")
                else:
                    e = Element(element.tag)
                    e.text = element.text
                    yield e
