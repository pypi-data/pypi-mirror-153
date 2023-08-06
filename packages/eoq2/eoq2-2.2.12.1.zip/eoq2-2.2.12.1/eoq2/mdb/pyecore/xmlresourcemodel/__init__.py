from pyecore.resources import global_registry
from .xmlresourcemodel import getEClassifier, eClassifiers
from .xmlresourcemodel import name, nsURI, nsPrefix, eClass
from .xmlresourcemodel import Document, Element, Attribute, CommentA, Comment, CData


from . import xmlresourcemodel

__all__ = ['Document', 'Element', 'Attribute', 'CommentA', 'Comment', 'CData']

eSubpackages = []
eSuperPackage = None
xmlresourcemodel.eSubpackages = eSubpackages
xmlresourcemodel.eSuperPackage = eSuperPackage

Document.rootelement.eType = Element
Document.comments.eType = CommentA
Element.attributes.eType = Attribute
Element.subelements.eType = Element

otherClassifiers = []

for classif in otherClassifiers:
    eClassifiers[classif.name] = classif
    classif.ePackage = eClass

for classif in eClassifiers.values():
    eClass.eClassifiers.append(classif.eClass)

for subpack in eSubpackages:
    eClass.eSubpackages.append(subpack.eClass)

register_packages = [xmlresourcemodel] + eSubpackages
for pack in register_packages:
    global_registry[pack.nsURI] = pack
