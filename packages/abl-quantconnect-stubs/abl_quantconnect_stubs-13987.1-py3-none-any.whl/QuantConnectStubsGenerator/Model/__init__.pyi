from typing import overload
import typing

import QuantConnectStubsGenerator.Model
import System
import System.Collections.Generic

QuantConnectStubsGenerator_Model_PythonType = typing.Any


class PythonType(System.Object, System.IEquatable[QuantConnectStubsGenerator_Model_PythonType]):
    """This class has no documentation."""

    @property
    def Name(self) -> str:
        ...

    @Name.setter
    def Name(self, value: str):
        ...

    @property
    def Namespace(self) -> str:
        ...

    @Namespace.setter
    def Namespace(self, value: str):
        ...

    @property
    def Alias(self) -> str:
        ...

    @Alias.setter
    def Alias(self, value: str):
        ...

    @property
    def IsNamedTypeParameter(self) -> bool:
        ...

    @IsNamedTypeParameter.setter
    def IsNamedTypeParameter(self, value: bool):
        ...

    @property
    def TypeParameters(self) -> System.Collections.Generic.IList[QuantConnectStubsGenerator.Model.PythonType]:
        ...

    @TypeParameters.setter
    def TypeParameters(self, value: System.Collections.Generic.IList[QuantConnectStubsGenerator.Model.PythonType]):
        ...

    def __init__(self, name: str, ns: str = None) -> None:
        ...

    @overload
    def Equals(self, other: QuantConnectStubsGenerator.Model.PythonType) -> bool:
        ...

    @overload
    def Equals(self, obj: typing.Any) -> bool:
        ...

    def GetBaseName(self) -> str:
        ...

    def GetHashCode(self) -> int:
        ...

    def ToPythonString(self, ignoreAlias: bool = False) -> str:
        ...


class Property(System.Object):
    """This class has no documentation."""

    @property
    def Name(self) -> str:
        ...

    @property
    def Type(self) -> QuantConnectStubsGenerator.Model.PythonType:
        ...

    @Type.setter
    def Type(self, value: QuantConnectStubsGenerator.Model.PythonType):
        ...

    @property
    def ReadOnly(self) -> bool:
        ...

    @ReadOnly.setter
    def ReadOnly(self, value: bool):
        ...

    @property
    def Static(self) -> bool:
        ...

    @Static.setter
    def Static(self, value: bool):
        ...

    @property
    def Abstract(self) -> bool:
        ...

    @Abstract.setter
    def Abstract(self, value: bool):
        ...

    @property
    def Value(self) -> str:
        ...

    @Value.setter
    def Value(self, value: str):
        ...

    @property
    def Summary(self) -> str:
        ...

    @Summary.setter
    def Summary(self, value: str):
        ...

    @property
    def DeprecationReason(self) -> str:
        ...

    @DeprecationReason.setter
    def DeprecationReason(self, value: str):
        ...

    def __init__(self, name: str) -> None:
        ...


class Parameter(System.Object):
    """This class has no documentation."""

    @property
    def Name(self) -> str:
        ...

    @property
    def Type(self) -> QuantConnectStubsGenerator.Model.PythonType:
        ...

    @Type.setter
    def Type(self, value: QuantConnectStubsGenerator.Model.PythonType):
        ...

    @property
    def VarArgs(self) -> bool:
        ...

    @VarArgs.setter
    def VarArgs(self, value: bool):
        ...

    @property
    def Value(self) -> str:
        ...

    @Value.setter
    def Value(self, value: str):
        ...

    def __init__(self, name: str, type: QuantConnectStubsGenerator.Model.PythonType) -> None:
        ...


class Method(System.Object):
    """This class has no documentation."""

    @property
    def Name(self) -> str:
        ...

    @property
    def ReturnType(self) -> QuantConnectStubsGenerator.Model.PythonType:
        ...

    @ReturnType.setter
    def ReturnType(self, value: QuantConnectStubsGenerator.Model.PythonType):
        ...

    @property
    def Static(self) -> bool:
        ...

    @Static.setter
    def Static(self, value: bool):
        ...

    @property
    def Overload(self) -> bool:
        ...

    @Overload.setter
    def Overload(self, value: bool):
        ...

    @property
    def Summary(self) -> str:
        ...

    @Summary.setter
    def Summary(self, value: str):
        ...

    @property
    def File(self) -> str:
        ...

    @File.setter
    def File(self, value: str):
        ...

    @property
    def DeprecationReason(self) -> str:
        ...

    @DeprecationReason.setter
    def DeprecationReason(self, value: str):
        ...

    @property
    def Parameters(self) -> System.Collections.Generic.IList[QuantConnectStubsGenerator.Model.Parameter]:
        ...

    def __init__(self, name: str, returnType: QuantConnectStubsGenerator.Model.PythonType) -> None:
        ...


class Class(System.Object):
    """This class has no documentation."""

    @property
    def Type(self) -> QuantConnectStubsGenerator.Model.PythonType:
        ...

    @property
    def Summary(self) -> str:
        ...

    @Summary.setter
    def Summary(self, value: str):
        ...

    @property
    def Static(self) -> bool:
        ...

    @Static.setter
    def Static(self, value: bool):
        ...

    @property
    def Interface(self) -> bool:
        ...

    @Interface.setter
    def Interface(self, value: bool):
        ...

    @property
    def InheritsFrom(self) -> System.Collections.Generic.IList[QuantConnectStubsGenerator.Model.PythonType]:
        ...

    @InheritsFrom.setter
    def InheritsFrom(self, value: System.Collections.Generic.IList[QuantConnectStubsGenerator.Model.PythonType]):
        ...

    @property
    def MetaClass(self) -> QuantConnectStubsGenerator.Model.PythonType:
        ...

    @MetaClass.setter
    def MetaClass(self, value: QuantConnectStubsGenerator.Model.PythonType):
        ...

    @property
    def ParentClass(self) -> QuantConnectStubsGenerator.Model.Class:
        ...

    @ParentClass.setter
    def ParentClass(self, value: QuantConnectStubsGenerator.Model.Class):
        ...

    @property
    def InnerClasses(self) -> System.Collections.Generic.IList[QuantConnectStubsGenerator.Model.Class]:
        ...

    @property
    def Properties(self) -> System.Collections.Generic.IList[QuantConnectStubsGenerator.Model.Property]:
        ...

    @property
    def Methods(self) -> System.Collections.Generic.IList[QuantConnectStubsGenerator.Model.Method]:
        ...

    def __init__(self, type: QuantConnectStubsGenerator.Model.PythonType) -> None:
        ...

    def GetUsedTypes(self) -> System.Collections.Generic.IEnumerable[QuantConnectStubsGenerator.Model.PythonType]:
        ...

    def IsEnum(self) -> bool:
        ...


class Namespace(System.Object):
    """This class has no documentation."""

    @property
    def Name(self) -> str:
        ...

    def __init__(self, name: str) -> None:
        ...

    def GetClassByType(self, type: QuantConnectStubsGenerator.Model.PythonType) -> QuantConnectStubsGenerator.Model.Class:
        ...

    def GetClasses(self) -> System.Collections.Generic.IEnumerable[QuantConnectStubsGenerator.Model.Class]:
        ...

    def GetParentClasses(self) -> System.Collections.Generic.IEnumerable[QuantConnectStubsGenerator.Model.Class]:
        ...

    def HasClass(self, type: QuantConnectStubsGenerator.Model.PythonType) -> bool:
        ...

    def RegisterClass(self, cls: QuantConnectStubsGenerator.Model.Class) -> None:
        ...


class ParseContext(System.Object):
    """
    The ParseContext is the root container which is filled with information gathered from the C# files.
    
    At the start of the program one instance of this class is created and passed to all parsers.
    The parsers are responsible for filling the ParseContext with all relevant information.
    Afterwards, this information is used by the renderers to create the necessary Python stubs.
    """

    def GetNamespaceByName(self, name: str) -> QuantConnectStubsGenerator.Model.Namespace:
        ...

    def GetNamespaces(self) -> System.Collections.Generic.IEnumerable[QuantConnectStubsGenerator.Model.Namespace]:
        ...

    def HasNamespace(self, name: str) -> bool:
        ...

    def RegisterNamespace(self, ns: QuantConnectStubsGenerator.Model.Namespace) -> None:
        ...


