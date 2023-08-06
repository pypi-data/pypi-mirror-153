from typing import overload
import QuantConnectStubsGenerator.Model
import QuantConnectStubsGenerator.Utility
import System
import System.Collections.Generic
import System.Xml


class DependencyGraph(System.Object):
    """
    The DependencyGraph is used by the NamespaceRenderer as a sort of queue
    to render classes in such order to limit the amount of forward references.
    """

    def AddClass(self, cls: QuantConnectStubsGenerator.Model.Class) -> None:
        ...

    def AddDependency(self, cls: QuantConnectStubsGenerator.Model.Class, type: QuantConnectStubsGenerator.Model.PythonType) -> None:
        ...

    def GetClassesInOrder(self) -> System.Collections.Generic.IEnumerable[QuantConnectStubsGenerator.Model.Class]:
        ...


class StringExtensions(System.Object):
    """This class has no documentation."""

    @staticmethod
    def Indent(str: str, level: int = 1) -> str:
        ...


class XmlExtensions(System.Object):
    """This class has no documentation."""

    @staticmethod
    def GetText(element: System.Xml.XmlElement) -> str:
        ...


