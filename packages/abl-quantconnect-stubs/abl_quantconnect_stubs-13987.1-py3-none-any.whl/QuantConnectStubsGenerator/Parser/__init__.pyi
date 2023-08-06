from typing import overload
import abc
import typing

import Microsoft.CodeAnalysis
import Microsoft.CodeAnalysis.CSharp
import Microsoft.CodeAnalysis.CSharp.Syntax
import QuantConnectStubsGenerator.Model
import QuantConnectStubsGenerator.Parser
import System
import System.Xml


class TypeConverter(System.Object):
    """The TypeConverter is responsible for converting AST nodes into PythonType instances."""

    def __init__(self, model: Microsoft.CodeAnalysis.SemanticModel) -> None:
        ...

    def GetSymbol(self, node: Microsoft.CodeAnalysis.SyntaxNode) -> Microsoft.CodeAnalysis.ISymbol:
        """
        Returns the symbol of the given node.
        Returns null if the semantic model does not contain a symbol for the node.
        """
        ...

    @overload
    def GetType(self, node: Microsoft.CodeAnalysis.SyntaxNode, skipPythonTypeCheck: bool = False) -> QuantConnectStubsGenerator.Model.PythonType:
        """
        Returns the Python type of the given node.
        Returns an aliased typing.Any if there is no Python type for the given symbol.
        """
        ...

    @overload
    def GetType(self, symbol: Microsoft.CodeAnalysis.ISymbol, skipPythonTypeCheck: bool = False) -> QuantConnectStubsGenerator.Model.PythonType:
        """
        Returns the Python type of the given symbol.
        Returns an aliased typing.Any if there is no Python type for the given symbol.
        """
        ...


class BaseParser(Microsoft.CodeAnalysis.CSharp.CSharpSyntaxWalker, metaclass=abc.ABCMeta):
    """This class has no documentation."""

    @property
    def _context(self) -> QuantConnectStubsGenerator.Model.ParseContext:
        """This field is protected."""
        ...

    @property
    def _model(self) -> Microsoft.CodeAnalysis.SemanticModel:
        """This field is protected."""
        ...

    @property
    def _typeConverter(self) -> QuantConnectStubsGenerator.Parser.TypeConverter:
        """This field is protected."""
        ...

    @property
    def _currentNamespace(self) -> QuantConnectStubsGenerator.Model.Namespace:
        """This field is protected."""
        ...

    @_currentNamespace.setter
    def _currentNamespace(self, value: QuantConnectStubsGenerator.Model.Namespace):
        """This field is protected."""
        ...

    @property
    def _currentClass(self) -> QuantConnectStubsGenerator.Model.Class:
        """This field is protected."""
        ...

    @_currentClass.setter
    def _currentClass(self, value: QuantConnectStubsGenerator.Model.Class):
        """This field is protected."""
        ...

    def __init__(self, context: QuantConnectStubsGenerator.Model.ParseContext, model: Microsoft.CodeAnalysis.SemanticModel) -> None:
        """This method is protected."""
        ...

    def AppendSummary(self, currentSummary: str, text: str) -> str:
        """
        Appends the given text to the given summary.
        An empty line is placed between the current summary and the given text.
        
        This method is protected.
        """
        ...

    def EnterClass(self, node: Microsoft.CodeAnalysis.CSharp.Syntax.BaseTypeDeclarationSyntax) -> None:
        """
        EnterClass is the method that is called whenever a class/struct/enum/interface is entered.
        In the BaseParser it is assumed that the class that is entered is already registered in the namespace.
        In the ClassParser, which runs before any other parsers, this method is overridden to register classes.
        
        This method is protected.
        """
        ...

    def FormatValue(self, value: str) -> str:
        """
        Format a default C# value into a default Python value.
        
        This method is protected.
        """
        ...

    def GetDeprecationReason(self, node: Microsoft.CodeAnalysis.CSharp.Syntax.MemberDeclarationSyntax) -> str:
        """
        Returns the deprecation message if the node is marked obsolete, or null if it is not.
        
        This method is protected.
        """
        ...

    def HasModifier(self, node: Microsoft.CodeAnalysis.CSharp.Syntax.MemberDeclarationSyntax, modifier: str) -> bool:
        """
        Check if a node has a modifier like private or static.
        
        This method is protected.
        """
        ...

    def ParseDocumentation(self, node: Microsoft.CodeAnalysis.SyntaxNode) -> System.Xml.XmlElement:
        """
        Parses the documentation above a node to an XML element.
        If the documentation contains a summary, this is then accessible with element["summary"].
        
        This method is protected.
        """
        ...

    def VisitClassDeclaration(self, node: Microsoft.CodeAnalysis.CSharp.Syntax.ClassDeclarationSyntax) -> None:
        ...

    def VisitEnumDeclaration(self, node: Microsoft.CodeAnalysis.CSharp.Syntax.EnumDeclarationSyntax) -> None:
        ...

    def VisitInterfaceDeclaration(self, node: Microsoft.CodeAnalysis.CSharp.Syntax.InterfaceDeclarationSyntax) -> None:
        ...

    def VisitNamespaceDeclaration(self, node: Microsoft.CodeAnalysis.CSharp.Syntax.NamespaceDeclarationSyntax) -> None:
        ...

    def VisitStructDeclaration(self, node: Microsoft.CodeAnalysis.CSharp.Syntax.StructDeclarationSyntax) -> None:
        ...


class ClassParser(QuantConnectStubsGenerator.Parser.BaseParser):
    """This class has no documentation."""

    def __init__(self, context: QuantConnectStubsGenerator.Model.ParseContext, model: Microsoft.CodeAnalysis.SemanticModel) -> None:
        ...

    def EnterClass(self, node: Microsoft.CodeAnalysis.CSharp.Syntax.BaseTypeDeclarationSyntax) -> None:
        """This method is protected."""
        ...


class MethodParser(QuantConnectStubsGenerator.Parser.BaseParser):
    """This class has no documentation."""

    def __init__(self, context: QuantConnectStubsGenerator.Model.ParseContext, model: Microsoft.CodeAnalysis.SemanticModel) -> None:
        ...

    def VisitConstructorDeclaration(self, node: Microsoft.CodeAnalysis.CSharp.Syntax.ConstructorDeclarationSyntax) -> None:
        ...

    def VisitDelegateDeclaration(self, node: Microsoft.CodeAnalysis.CSharp.Syntax.DelegateDeclarationSyntax) -> None:
        ...

    def VisitIndexerDeclaration(self, node: Microsoft.CodeAnalysis.CSharp.Syntax.IndexerDeclarationSyntax) -> None:
        ...

    def VisitMethodDeclaration(self, node: Microsoft.CodeAnalysis.CSharp.Syntax.MethodDeclarationSyntax) -> None:
        ...


class PropertyParser(QuantConnectStubsGenerator.Parser.BaseParser):
    """This class has no documentation."""

    def __init__(self, context: QuantConnectStubsGenerator.Model.ParseContext, model: Microsoft.CodeAnalysis.SemanticModel) -> None:
        ...

    def VisitEnumMemberDeclaration(self, node: Microsoft.CodeAnalysis.CSharp.Syntax.EnumMemberDeclarationSyntax) -> None:
        ...

    def VisitEventDeclaration(self, node: Microsoft.CodeAnalysis.CSharp.Syntax.EventDeclarationSyntax) -> None:
        ...

    def VisitEventFieldDeclaration(self, node: Microsoft.CodeAnalysis.CSharp.Syntax.EventFieldDeclarationSyntax) -> None:
        ...

    def VisitFieldDeclaration(self, node: Microsoft.CodeAnalysis.CSharp.Syntax.FieldDeclarationSyntax) -> None:
        ...

    def VisitPropertyDeclaration(self, node: Microsoft.CodeAnalysis.CSharp.Syntax.PropertyDeclarationSyntax) -> None:
        ...


