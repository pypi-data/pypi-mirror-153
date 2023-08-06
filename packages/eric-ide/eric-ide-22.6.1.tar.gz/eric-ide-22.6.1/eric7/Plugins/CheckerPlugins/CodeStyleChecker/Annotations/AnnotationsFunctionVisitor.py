# -*- coding: utf-8 -*-

# Copyright (c) 2021 - 2022 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing a node visitor for function type annotations.
"""

#
# The visitor and associated classes are adapted from flake8-annotations v2.7.0
#

import ast
import itertools
import sys

from .AnnotationsEnums import AnnotationType, ClassDecoratorType, FunctionType

# The order of AST_ARG_TYPES must match Python's grammar
AST_ARG_TYPES = ("posonlyargs", "args", "vararg", "kwonlyargs", "kwarg")


class Argument:
    """
    Class representing a function argument.
    """
    def __init__(self, argname, lineno, col_offset, annotationType,
                 hasTypeAnnotation=False, has3107Annotation=False,
                 hasTypeComment=False):
        """
        Constructor
        
        @param argname name of the argument
        @type str
        @param lineno line number
        @type int
        @param col_offset column number
        @type int
        @param annotationType type of annotation
        @type AnnotationType
        @param hasTypeAnnotation flag indicating the presence of a type
            annotation (defaults to False)
        @type bool (optional)
        @param has3107Annotation flag indicating the presence of a PEP 3107
            annotation (defaults to False)
        @type bool (optional)
        @param hasTypeComment flag indicating the presence of a type comment
            (defaults to False)
        @type bool (optional)
        """
        self.argname = argname
        self.lineno = lineno
        self.col_offset = col_offset
        self.annotationType = annotationType
        self.hasTypeAnnotation = hasTypeAnnotation
        self.has3107Annotation = has3107Annotation
        self.hasTypeComment = hasTypeComment
    
    @classmethod
    def fromNode(cls, node, annotationTypeName):
        """
        Class method to create an Argument object based on the given node.
        
        @param node reference to the node to be converted
        @type ast.arguments
        @param annotationTypeName name of the annotation type
        @type str
        @return Argument object
        @rtype Argument
        """
        annotationType = AnnotationType[annotationTypeName]
        newArg = cls(node.arg, node.lineno, node.col_offset, annotationType)

        newArg.hasTypeAnnotation = False
        if node.annotation:
            newArg.hasTypeAnnotation = True
            newArg.has3107Annotation = True

        if node.type_comment:
            newArg.hasTypeAnnotation = True
            newArg.hasTypeComment = True

        return newArg


class Function:
    """
    Class representing a function.
    """
    def __init__(self, name, lineno, col_offset,
                 functionType=FunctionType.PUBLIC, isClassMethod=False,
                 classDecoratorType=None, isReturnAnnotated=False,
                 hasTypeComment=False, hasOnlyNoneReturns=True,
                 isNested=False, decoratorList=None, args=None):
        """
        Constructor
        
        @param name name of the function
        @type str
        @param lineno line number
        @type int
        @param col_offset column number
        @type int
        @param functionType type of the function (defaults to
            FunctionType.PUBLIC)
        @type FunctionType (optional)
        @param isClassMethod flag indicating a class method (defaults to False)
        @type bool (optional)
        @param classDecoratorType type of a function decorator
            (defaults to None)
        @type ClassDecoratorType or None (optional)
        @param isReturnAnnotated flag indicating the presence of a return
            type annotation (defaults to False)
        @type bool (optional)
        @param hasTypeComment flag indicating the presence of a type comment
            (defaults to False)
        @type bool (optional)
        @param hasOnlyNoneReturns flag indicating only None return values
            (defaults to True)
        @type bool (optional)
        @param isNested flag indicating a nested function (defaults to False)
        @type bool (optional)
        @param decoratorList list of decorator nodes (defaults to None)
        @type list of ast.Attribute, ast.Call or ast.Name (optional)
        @param args list of arguments (defaults to None)
        @type list of Argument (optional)
        """
        self.name = name
        self.lineno = lineno
        self.col_offset = col_offset
        self.functionType = functionType
        self.isClassMethod = isClassMethod
        self.classDecoratorType = classDecoratorType
        self.isReturnAnnotated = isReturnAnnotated
        self.hasTypeComment = hasTypeComment
        self.hasOnlyNoneReturns = hasOnlyNoneReturns
        self.isNested = isNested
        self.decoratorList = decoratorList
        self.args = args
    
    def isFullyAnnotated(self):
        """
        Public method to check, if the function definition is fully type
        annotated.

        Note: self.args will always include an Argument object for return.
        
        @return flag indicating a fully annotated function definition
        @rtype bool
        """
        return all(arg.hasTypeAnnotation for arg in self.args)
    
    def isDynamicallyTyped(self):
        """
        Public method to check, if a function definition is dynamically typed
        (i.e. completely lacking hints).
        
        @return flag indicating a dynamically typed function definition
        @rtype bool
        """
        return not any(arg.hasTypeAnnotation for arg in self.args)

    def getMissedAnnotations(self):
        """
        Public method to provide a list of arguments with missing type
        annotations.
        
        @return list of arguments with missing type annotations
        @rtype list of Argument
        """
        return [arg for arg in self.args if not arg.hasTypeAnnotation]

    def getAnnotatedArguments(self):
        """
        Public method to get list of arguments with type annotations.
        
        @return list of arguments with type annotations.
        @rtype list of Argument
        """
        return [arg for arg in self.args if arg.hasTypeAnnotation]
    
    def hasDecorator(self, checkDecorators):
        """
        Public method to check whether the function node is decorated by any of
        the provided decorators.
        
        Decorator matching is done against the provided `checkDecorators` set.
        Decorators are assumed to be either a module attribute (e.g.
        `@typing.overload`) or name (e.g. `@overload`). For the case of a
        module attribute, only the attribute is checked against
        `overload_decorators`.
        
        Note: Deeper decorator imports (e.g. `a.b.overload`) are not explicitly
        supported.
        
        @param checkDecorators set of decorators to check against
        @type set of str
        @return flag indicating the presence of any decorators
        @rtype bool
        """
        for decorator in self.decoratorList:
            # Drop to a helper to allow for simpler handling of callable
            # decorators
            return self.__decoratorChecker(decorator, checkDecorators)
        else:
            return False
    
    def __decoratorChecker(self, decorator, checkDecorators):
        """
        Private method to check the provided decorator for a match against the
        provided set of check names.
        
        Decorators are assumed to be of the following form:
            * `a.name` or `a.name()`
            * `name` or `name()`
        
        Note: Deeper imports (e.g. `a.b.name`) are not explicitly supported.
        
        @param decorator decorator node to check
        @type ast.Attribute, ast.Call or ast.Name
        @param checkDecorators set of decorators to check against
        @type set of str
        @return flag indicating the presence of any decorators
        @rtype bool
        """
        if isinstance(decorator, ast.Name):
            # e.g. `@overload`, where `decorator.id` will be the name
            if decorator.id in checkDecorators:
                return True
        elif isinstance(decorator, ast.Attribute):
            # e.g. `@typing.overload`, where `decorator.attr` will be the name
            if decorator.attr in checkDecorators:
                return True
        elif isinstance(decorator, ast.Call):
            # e.g. `@overload()` or `@typing.overload()`, where
            # `decorator.func` will be `ast.Name` or `ast.Attribute`,
            # which we can check recursively
            return self.__decoratorChecker(decorator.func, checkDecorators)
        
        return None
    
    @classmethod
    def fromNode(cls, node, lines, **kwargs):
        """
        Class method to create a Function object from ast.FunctionDef or
        ast.AsyncFunctionDef nodes.
        
        Accept the source code, as a list of strings, in order to get the
        column where the function definition ends.
        
        With exceptions, input kwargs are passed straight through to Function's
        __init__. The following kwargs will be overridden:
          * function_type
          * class_decorator_type
          * args
        
        @param node reference to the function definition node
        @type ast.AsyncFunctionDef or ast.FunctionDef
        @param lines list of source code lines
        @type list of str
        @keyparam **kwargs keyword arguments
        @type dict
        @return created Function object
        @rtype Function
        """
        # Extract function types from function name
        kwargs["functionType"] = cls.getFunctionType(node.name)
        
        # Identify type of class method, if applicable
        if kwargs.get("isClassMethod", False):
            kwargs["classDecoratorType"] = cls.getClassDecoratorType(node)
        
        # Store raw decorator list for use by property methods
        kwargs["decoratorList"] = node.decorator_list
        
        # Instantiate empty args list here since it has no default
        kwargs["args"] = []

        newFunction = cls(node.name, node.lineno, node.col_offset, **kwargs)
        
        # Iterate over arguments by type & add
        for argType in AST_ARG_TYPES:
            args = node.args.__getattribute__(argType)
            if args:
                if not isinstance(args, list):
                    args = [args]
                
                newFunction.args.extend(
                    [Argument.fromNode(arg, argType.upper())
                     for arg in args]
                )
        
        # Create an Argument object for the return hint
        defEndLineno, defEndColOffset = cls.colonSeeker(node, lines)
        returnArg = Argument("return", defEndLineno, defEndColOffset,
                             AnnotationType.RETURN)
        if node.returns:
            returnArg.hasTypeAnnotation = True
            returnArg.has3107Annotation = True
            newFunction.isReturnAnnotated = True
        
        newFunction.args.append(returnArg)
        
        # Type comments in-line with input arguments are handled by the
        # Argument class. If a function-level type comment is present, attempt
        # to parse for any missed type hints.
        if node.type_comment:
            newFunction.hasTypeComment = True
            newFunction = cls.tryTypeComment(newFunction, node)
        
        # Check for the presence of non-`None` returns using the special-case
        # return node visitor.
        returnVisitor = ReturnVisitor(node)
        returnVisitor.visit(node)
        newFunction.hasOnlyNoneReturns = returnVisitor.hasOnlyNoneReturns
        
        return newFunction
    
    @staticmethod
    def colonSeeker(node, lines):
        """
        Static method to find the line & column indices of the function
        definition's closing colon.
        
        @param node reference to the function definition node
        @type ast.AsyncFunctionDef or ast.FunctionDef
        @param lines list of source code lines
        @type list of str
        @return line and column offset of the colon
        @rtype tuple of (int, int)
        """
        # Special case single line function definitions
        if node.lineno == node.body[0].lineno:
            return Function._singleLineColonSeeker(
                node, lines[node.lineno - 1])
        
        # With Python < 3.8, the function node includes the docstring and the
        # body does not, so we have to rewind through any docstrings, if
        # present, before looking for the def colon. We should end up with
        # lines[defEndLineno - 1] having the colon.
        defEndLineno = node.body[0].lineno
        if sys.version_info < (3, 8, 0):
            # If the docstring is on one line then no rewinding is necessary.
            nTripleQuotes = lines[defEndLineno - 1].count('"""')
            if nTripleQuotes == 1:
                # Docstring closure, rewind until the opening is found and take
                # the line prior.
                while True:
                    defEndLineno -= 1
                    if '"""' in lines[defEndLineno - 1]:
                        # Docstring has closed
                        break
        
        # Once we've gotten here, we've found the line where the docstring
        # begins, so we have to step up one more line to get to the close of
        # the def.
        defEndLineno -= 1
        
        # Use str.rfind() to account for annotations on the same line,
        # definition closure should be the last : on the line
        defEndColOffset = lines[defEndLineno - 1].rfind(":")
        
        return defEndLineno, defEndColOffset
    
    @staticmethod
    def _singleLineColonSeeker(node, line):
        """
        Static method to find the line & column indices of a single line
        function definition.
        
        @param node reference to the function definition node
        @type ast.AsyncFunctionDef or ast.FunctionDef
        @param line source code line
        @type str
        @return line and column offset of the colon
        @rtype tuple of (int, int)
        """
        colStart = node.col_offset
        colEnd = node.body[0].col_offset
        defEndColOffset = line.rfind(":", colStart, colEnd)
        
        return node.lineno, defEndColOffset
    
    @staticmethod
    def tryTypeComment(funcObj, node):
        """
        Static method to infer type hints from a function-level type comment.
        
        If a function is type commented it is assumed to have a return
        annotation, otherwise Python will fail to parse the hint.
        
        @param funcObj reference to the Function object
        @type Function
        @param node reference to the function definition node
        @type ast.AsyncFunctionDef or ast.FunctionDef
        @return reference to the modified Function object
        @rtype Function
        """
        hintTree = ast.parse(node.type_comment, "<func_type>", "func_type")
        hintTree = Function._maybeInjectClassArgument(hintTree, funcObj)
        
        for arg, hintComment in itertools.zip_longest(
            funcObj.args, hintTree.argtypes
        ):
            if isinstance(hintComment, ast.Ellipsis):
                continue
            
            if arg and hintComment:
                arg.hasTypeAnnotation = True
                arg.hasTypeComment = True
        
        # Return arg is always last
        funcObj.args[-1].hasTypeAnnotation = True
        funcObj.args[-1].hasTypeComment = True
        funcObj.isReturnAnnotated = True
        
        return funcObj
    
    @staticmethod
    def _maybeInjectClassArgument(hintTree, funcObj):
        """
        Static method to inject `self` or `cls` args into a type comment to
        align with PEP 3107-style annotations.
        
        Because PEP 484 does not describe a method to provide partial function-
        level type comments, there is a potential for ambiguity in the context
        of both class methods and classmethods when aligning type comments to
        method arguments.
        
        These two class methods, for example, should lint equivalently:
        
            def bar(self, a):
                # type: (int) -> int
                ...
        
            def bar(self, a: int) -> int
                ...
        
        When this example type comment is parsed by `ast` and then matched with
        the method's arguments, it associates the `int` hint to `self` rather
        than `a`, so a dummy hint needs to be provided in situations where
        `self` or `class` are not hinted in the type comment in order to
        achieve equivalent linting results to PEP-3107 style annotations.
        
        A dummy `ast.Ellipses` constant is injected if the following criteria
        are met:
            1. The function node is either a class method or classmethod
            2. The number of hinted args is at least 1 less than the number
               of function args
        
        @param hintTree parsed type hint node
        @type ast.FunctionType
        @param funcObj reference to the Function object
        @type Function
        @return reference to the hint node
        @rtype ast.FunctionType
        """
        if not funcObj.isClassMethod:
            # Short circuit
            return hintTree

        if (
            funcObj.classDecoratorType != ClassDecoratorType.STATICMETHOD and
            len(hintTree.argtypes) < (len(funcObj.args) - 1)
        ):
            # Subtract 1 to skip return arg
            hintTree.argtypes = [ast.Ellipsis()] + hintTree.argtypes
        
        return hintTree
    
    @staticmethod
    def getFunctionType(functionName):
        """
        Static method to determine the function's FunctionType from its name.

        MethodType is determined by the following priority:
          1. Special: function name prefixed & suffixed by "__"
          2. Private: function name prefixed by "__"
          3. Protected: function name prefixed by "_"
          4. Public: everything else
        
        @param functionName function name to be checked
        @type str
        @return type of function
        @rtype FunctionType
        """
        if functionName.startswith("__") and functionName.endswith("__"):
            return FunctionType.SPECIAL
        elif functionName.startswith("__"):
            return FunctionType.PRIVATE
        elif functionName.startswith("_"):
            return FunctionType.PROTECTED
        else:
            return FunctionType.PUBLIC
    
    @staticmethod
    def getClassDecoratorType(functionNode):
        """
        Static method to get the class method's decorator type from its
        function node.
        
        Only @classmethod and @staticmethod decorators are identified; all
        other decorators are ignored
        
        If @classmethod or @staticmethod decorators are not present, this
        function will return None.
        
        @param functionNode reference to the function definition node
        @type ast.AsyncFunctionDef or ast.FunctionDef
        @return class decorator type
        @rtype ClassDecoratorType or None
        """
        # @classmethod and @staticmethod will show up as ast.Name objects,
        # where callable decorators will show up as ast.Call, which we can
        # ignore
        decorators = [
            decorator.id
            for decorator in functionNode.decorator_list
            if isinstance(decorator, ast.Name)
        ]

        if "classmethod" in decorators:
            return ClassDecoratorType.CLASSMETHOD
        elif "staticmethod" in decorators:
            return ClassDecoratorType.STATICMETHOD
        else:
            return None


class FunctionVisitor(ast.NodeVisitor):
    """
    Class implementing a node visitor to check function annotations.
    """
    AstFuncTypes = (ast.FunctionDef, ast.AsyncFunctionDef)
    
    def __init__(self, lines):
        """
        Constructor
        
        @param lines source code lines of the function
        @type list of str
        """
        self.lines = lines
        self.functionDefinitions = []
        self.__context = []
    
    def switchContext(self, node):
        """
        Public method implementing a context switcher as a generic function
        visitor in order to track function context.
        
        Without keeping track of context, it's challenging to reliably
        differentiate class methods from "regular" functions, especially in the
        case of nested classes.
        
        @param node reference to the function definition node to be analyzed
        @type ast.AsyncFunctionDef or ast.FunctionDef
        """
        if isinstance(node, FunctionVisitor.AstFuncTypes):
            # Check for non-empty context first to prevent IndexErrors for
            # non-nested nodes
            if self.__context:
                if isinstance(self.__context[-1], ast.ClassDef):
                    # Check if current context is a ClassDef node & pass the
                    # appropriate flag
                    self.functionDefinitions.append(
                        Function.fromNode(node, self.lines, isClassMethod=True)
                    )
                elif isinstance(
                    self.__context[-1], FunctionVisitor.AstFuncTypes
                ):
                    # Check for nested function & pass the appropriate flag
                    self.functionDefinitions.append(
                        Function.fromNode(node, self.lines, isNested=True)
                    )
            else:
                self.functionDefinitions.append(
                    Function.fromNode(node, self.lines))
        
        self.__context.append(node)
        self.generic_visit(node)
        self.__context.pop()
    
    visit_FunctionDef = switchContext
    visit_AsyncFunctionDef = switchContext
    visit_ClassDef = switchContext


class ReturnVisitor(ast.NodeVisitor):
    """
    Class implementing a node visitor to check the return statements of a
    function node.
    
    If the function node being visited has an explicit return statement of
    anything other than `None`, the `instance.hasOnlyNoneReturns` flag will
    be set to `False`.
    
    If the function node being visited has no return statement, or contains
    only return statement(s) that explicitly return `None`, the
    `instance.hasOnlyNoneReturns` flag will be set to `True`.
    
    Due to the generic visiting being done, we need to keep track of the
    context in which a non-`None` return node is found. These functions are
    added to a set that is checked to see whether nor not the parent node is
    present.
    """
    def __init__(self, parentNode):
        """
        Constructor
        
        @param parentNode reference to the function definition node to be
            analyzed
        @type ast.AsyncFunctionDef or ast.FunctionDef
        """
        self.parentNode = parentNode
        self.__context = []
        self.__nonNoneReturnNodes = set()
    
    @property
    def hasOnlyNoneReturns(self):
        """
        Public method indicating, that the parent node isn't in the visited
        nodes that don't return `None`.
        
        @return flag indicating, that the parent node isn't in the visited
            nodes that don't return `None`
        @rtype bool
        """
        return self.parentNode not in self.__nonNoneReturnNodes
    
    def visit_Return(self, node):
        """
        Public method to check each Return node to see if it returns anything
        other than `None`.
        
        If the node being visited returns anything other than `None`, its
        parent context is added to the set of non-returning child nodes of
        the parent node.
        
        @param node reference to the AST Return node
        @type ast.Return
        """
        if node.value is not None:
            # In the event of an explicit `None` return (`return None`), the
            # node body will be an instance of either `ast.Constant` (3.8+) or
            # `ast.NameConstant`, which we need to check to see if it's
            # actually `None`
            if (
                isinstance(node.value, (ast.Constant, ast.NameConstant)) and
                node.value.value is None
            ):
                return
            
            self.__nonNoneReturnNodes.add(self.__context[-1])

    def switchContext(self, node):
        """
        Public method implementing a context switcher as a generic function
        visitor in order to track function context.
        
        Without keeping track of context, it's challenging to reliably
        differentiate class methods from "regular" functions, especially in the
        case of nested classes.
        
        @param node reference to the function definition node to be analyzed
        @type ast.AsyncFunctionDef or ast.FunctionDef
        """
        self.__context.append(node)
        self.generic_visit(node)
        self.__context.pop()

    visit_FunctionDef = switchContext
    visit_AsyncFunctionDef = switchContext
