from typing import overload
import QuantConnectStubsGenerator.Tests.Model
import System


class ClassTests(System.Object):
    """This class has no documentation."""

    def GetUsedTypesShouldReturnAllTypesInTheClassAndItsInnerClasses(self) -> None:
        ...

    def GetUsedTypesShouldReturnAllTypesInTheClassAndItsMethods(self) -> None:
        ...

    def GetUsedTypesShouldReturnAllTypesInTheClassAndItsNonStaticProperties(self) -> None:
        ...

    def GetUsedTypesShouldReturnAllTypesInTheClassAndItsStaticProperties(self) -> None:
        ...


class NamespaceTests(System.Object):
    """This class has no documentation."""

    def GetClassByTypeShouldReturnThePreviouslyRegisteredClass(self) -> None:
        ...

    def GetClassByTypeShouldThrowIfNotRegistered(self) -> None:
        ...

    def GetClassesShouldReturnAllRegisteredClasses(self) -> None:
        ...

    def GetParentClassesShouldReturnAllRegisteredParentClasses(self) -> None:
        ...

    def HasClassShouldReturnFalseIfClassHasNotBeenRegistered(self) -> None:
        ...

    def HasClassShouldReturnTrueIfClassHasBeenRegistered(self) -> None:
        ...


class ParseContextTests(System.Object):
    """This class has no documentation."""

    def GetNamespaceByNameShouldReturnNamespaceIfItHasBeenRegistered(self) -> None:
        ...

    def GetNamespaceByNameShouldThrowIfNamespaceHasNotBeenRegistered(self) -> None:
        ...

    def GetNamespacesShouldReturnAllRegisteredNamespaces(self) -> None:
        ...

    def HasNamespaceShouldReturnFalseIfNamespaceHasNotBeenRegistered(self) -> None:
        ...

    def HasNamespaceShouldReturnTrueIfNamespaceHasBeenRegistered(self) -> None:
        ...


class PythonTypeTests(System.Object):
    """This class has no documentation."""

    def ToPythonStringCorrectlyAddsNamespace(self) -> None:
        ...

    def ToPythonStringCorrectlyFormatsAlias(self) -> None:
        ...

    def ToPythonStringCorrectlyFormatsCallable(self) -> None:
        ...

    def ToPythonStringCorrectlyFormatsNamedTypeParameter(self) -> None:
        ...

    def ToPythonStringCorrectlyFormatsTypeParameters(self) -> None:
        ...

    def ToPythonStringCorrectlyIgnoresAlias(self) -> None:
        ...

    def ToPythonStringOmitsNamespaceWhenNamespaceIsNull(self) -> None:
        ...


