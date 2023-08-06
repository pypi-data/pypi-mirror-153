"""Definition of meta model 'constraintmodel'."""
from functools import partial
import pyecore.ecore as Ecore
from pyecore.ecore import *


name = 'constraintmodel'
nsURI = 'http://www.example.org/constraintmodel'
nsPrefix = 'constraintmodel'

eClass = EPackage(name=name, nsURI=nsURI, nsPrefix=nsPrefix)

eClassifiers = {}
getEClassifier = partial(Ecore.getEClassifier, searchspace=eClassifiers)
ConstraintTypeEnum = EEnum('ConstraintTypeEnum', literals=['SOFT', 'HARD'])


class Constraint(EObject, metaclass=MetaEClass):

    constraintType = EAttribute(eType=ConstraintTypeEnum, derived=False, changeable=True)
    target = EAttribute(eType=EString, derived=False, changeable=True)
    feature = EAttribute(eType=EString, derived=False, changeable=True)
    law = EAttribute(eType=EString, derived=False, changeable=True)
    name = EAttribute(eType=EString, derived=False, changeable=True)
    annotation = EAttribute(eType=EString, derived=False, changeable=True)

    def __init__(self, *, constraintType=None, target=None, feature=None, law=None, name=None, annotation=None, **kwargs):
        if kwargs:
            raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()

        if constraintType is not None:
            self.constraintType = constraintType

        if target is not None:
            self.target = target

        if feature is not None:
            self.feature = feature

        if law is not None:
            self.law = law

        if name is not None:
            self.name = name

        if annotation is not None:
            self.annotation = annotation
