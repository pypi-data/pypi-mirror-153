# Generated from DurakParser.g4 by ANTLR 4.10.1
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .DurakParser import DurakParser
else:
    from DurakParser import DurakParser

# This class defines a complete generic visitor for a parse tree produced by DurakParser.

class DurakParserVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by DurakParser#document.
    def visitDocument(self, ctx:DurakParser.DocumentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DurakParser#entity.
    def visitEntity(self, ctx:DurakParser.EntityContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DurakParser#element.
    def visitElement(self, ctx:DurakParser.ElementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DurakParser#tag_attribute.
    def visitTag_attribute(self, ctx:DurakParser.Tag_attributeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DurakParser#tag_attribute_last.
    def visitTag_attribute_last(self, ctx:DurakParser.Tag_attribute_lastContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DurakParser#directive.
    def visitDirective(self, ctx:DurakParser.DirectiveContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DurakParser#if_directive.
    def visitIf_directive(self, ctx:DurakParser.If_directiveContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DurakParser#if_directive_elif.
    def visitIf_directive_elif(self, ctx:DurakParser.If_directive_elifContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DurakParser#foreach_directive.
    def visitForeach_directive(self, ctx:DurakParser.Foreach_directiveContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DurakParser#include_directive.
    def visitInclude_directive(self, ctx:DurakParser.Include_directiveContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DurakParser#insert_directive.
    def visitInsert_directive(self, ctx:DurakParser.Insert_directiveContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DurakParser#injection.
    def visitInjection(self, ctx:DurakParser.InjectionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DurakParser#expr.
    def visitExpr(self, ctx:DurakParser.ExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DurakParser#expr_or.
    def visitExpr_or(self, ctx:DurakParser.Expr_orContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DurakParser#expr_and.
    def visitExpr_and(self, ctx:DurakParser.Expr_andContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DurakParser#expr_not.
    def visitExpr_not(self, ctx:DurakParser.Expr_notContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DurakParser#expr_comp.
    def visitExpr_comp(self, ctx:DurakParser.Expr_compContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DurakParser#expr_addsub.
    def visitExpr_addsub(self, ctx:DurakParser.Expr_addsubContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DurakParser#expr_multdiv.
    def visitExpr_multdiv(self, ctx:DurakParser.Expr_multdivContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DurakParser#expr_dot.
    def visitExpr_dot(self, ctx:DurakParser.Expr_dotContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DurakParser#expr_atom.
    def visitExpr_atom(self, ctx:DurakParser.Expr_atomContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DurakParser#expr_literal.
    def visitExpr_literal(self, ctx:DurakParser.Expr_literalContext):
        return self.visitChildren(ctx)



del DurakParser