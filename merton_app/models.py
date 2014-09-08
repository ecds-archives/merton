from eulexistdb.manager import Manager
from eulexistdb.models import XmlModel
from eulxml.xmlmap.teimap import Tei, TeiDiv, TEI_NAMESPACE

class Search(XmlModel, TeiDiv):
    ROOT_NAMESPACES = {'tei' : TEI_NAMESPACE}
    objects = Manager('//tei:div')