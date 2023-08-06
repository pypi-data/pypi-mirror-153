from typing import overload
import abc
import typing

import QuantConnectStubsGenerator.Model
import QuantConnectStubsGenerator.Renderer
import System
import System.IO

QuantConnectStubsGenerator_Renderer_ObjectRenderer_T = typing.TypeVar("QuantConnectStubsGenerator_Renderer_ObjectRenderer_T")
QuantConnectStubsGenerator_Renderer_ObjectRenderer_CreateRenderer_TRenderer = typing.TypeVar("QuantConnectStubsGenerator_Renderer_ObjectRenderer_CreateRenderer_TRenderer")


class BaseRenderer(System.Object, metaclass=abc.ABCMeta):
    """This class has no documentation."""

    @property
    def Writer(self) -> System.IO.StreamWriter:
        """This field is protected."""
        ...

    def __init__(self, writer: System.IO.StreamWriter) -> None:
        """This method is protected."""
        ...

    def Write(self, value: str) -> None:
        """This method is protected."""
        ...

    def WriteLine(self, value: str = ...) -> None:
        """This method is protected."""
        ...


class AlgorithmImportsRenderer(QuantConnectStubsGenerator.Renderer.BaseRenderer):
    """This class has no documentation."""

    def __init__(self, writer: System.IO.StreamWriter, leanPath: str) -> None:
        ...

    def Render(self) -> None:
        ...


class ObjectRenderer(typing.Generic[QuantConnectStubsGenerator_Renderer_ObjectRenderer_T], QuantConnectStubsGenerator.Renderer.BaseRenderer, metaclass=abc.ABCMeta):
    """This class has no documentation."""

    def __init__(self, writer: System.IO.StreamWriter, indentationLevel: int) -> None:
        """This method is protected."""
        ...

    def CreateRenderer(self, indented: bool = True) -> QuantConnectStubsGenerator_Renderer_ObjectRenderer_CreateRenderer_TRenderer:
        """This method is protected."""
        ...

    def Render(self, item: QuantConnectStubsGenerator_Renderer_ObjectRenderer_T) -> None:
        ...

    def Write(self, value: str) -> None:
        """This method is protected."""
        ...

    def WriteLine(self, value: str = ...) -> None:
        """This method is protected."""
        ...

    def WriteSummary(self, summary: str, indented: bool = False) -> None:
        """This method is protected."""
        ...


class ClassRenderer(QuantConnectStubsGenerator.Renderer.ObjectRenderer[QuantConnectStubsGenerator.Model.Class]):
    """This class has no documentation."""

    def __init__(self, writer: System.IO.StreamWriter, indentationLevel: int) -> None:
        ...

    def Render(self, cls: QuantConnectStubsGenerator.Model.Class) -> None:
        ...


class ClrStubsRenderer(QuantConnectStubsGenerator.Renderer.BaseRenderer):
    """This class has no documentation."""

    def __init__(self, writer: System.IO.StreamWriter) -> None:
        ...

    def Render(self) -> None:
        ...


class MethodRenderer(QuantConnectStubsGenerator.Renderer.ObjectRenderer[QuantConnectStubsGenerator.Model.Method]):
    """This class has no documentation."""

    def __init__(self, writer: System.IO.StreamWriter, indentationLevel: int) -> None:
        ...

    def Render(self, method: QuantConnectStubsGenerator.Model.Method) -> None:
        ...


class NamespaceRenderer(QuantConnectStubsGenerator.Renderer.ObjectRenderer[QuantConnectStubsGenerator.Model.Namespace]):
    """This class has no documentation."""

    def __init__(self, writer: System.IO.StreamWriter, indentationLevel: int) -> None:
        ...

    def Render(self, ns: QuantConnectStubsGenerator.Model.Namespace) -> None:
        ...


class PropertyRenderer(QuantConnectStubsGenerator.Renderer.ObjectRenderer[QuantConnectStubsGenerator.Model.Property]):
    """This class has no documentation."""

    def __init__(self, writer: System.IO.StreamWriter, indentationLevel: int) -> None:
        ...

    def Render(self, property: QuantConnectStubsGenerator.Model.Property) -> None:
        ...


class PyLoaderRenderer(QuantConnectStubsGenerator.Renderer.BaseRenderer):
    """This class has no documentation."""

    def __init__(self, writer: System.IO.StreamWriter) -> None:
        ...

    def Render(self, ns: str) -> None:
        ...


class SetupRenderer(QuantConnectStubsGenerator.Renderer.BaseRenderer):
    """This class has no documentation."""

    def __init__(self, writer: System.IO.StreamWriter, leanPath: str, outputDirectory: str) -> None:
        ...

    def Render(self) -> None:
        ...


