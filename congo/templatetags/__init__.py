from django import template

class Library(template.Library):
    def smart_tag(self, func = None, takes_context = None, name = None):
        # based on: http://bl.ocks.org/natevw/f14812604be62c073461

        # imports necessary to match original context
        from django.template.base import TemplateSyntaxError, TagHelperNode, parse_bits
        from inspect import getargspec

        def dec(func):
            params, varargs, varkw, defaults = getargspec(func)

            # added from Django's simple_tag implementation
            class SimpleNode(TagHelperNode):
                def render(self, context):
                    resolved_args, resolved_kwargs = self.get_resolved_arguments(context)
                    return func(*resolved_args, **resolved_kwargs)

            class AssignmentNode(TagHelperNode):
                def __init__(self, takes_context, args, kwargs, target_var):
                    super(AssignmentNode, self).__init__(takes_context, args, kwargs)
                    self.target_var = target_var

                def render(self, context):
                    resolved_args, resolved_kwargs = self.get_resolved_arguments(context)
                    context[self.target_var] = func(*resolved_args, **resolved_kwargs)
                    return ''

            function_name = (name or getattr(func, '_decorated_function', func).__name__)

            def compile_func(parser, token):
                bits = token.split_contents()[1:]
    #            if len(bits) < 2 or bits[-2] != 'as':
    #                raise TemplateSyntaxError(
    #                    "'%s' tag takes at least 2 arguments and the "
    #                    "second last argument must be 'as'" % function_name)

                # replaced above choose between AssignmentNode or SimpleNode
                if len(bits) > 1 and bits[-2] == 'as':
                    target_var = bits[-1]
                    bits = bits[:-2]
                    args, kwargs = parse_bits(parser, bits, params,
                        varargs, varkw, defaults, takes_context, function_name)
                    return AssignmentNode(takes_context, args, kwargs, target_var)
                else:
                    args, kwargs = parse_bits(parser, bits, params,
                        varargs, varkw, defaults, takes_context, function_name)
                    return SimpleNode(takes_context, args, kwargs)

            compile_func.__doc__ = func.__doc__
            self.tag(function_name, compile_func)
            return func

        if func is None:
            # @register.smart_tag(...)
            return dec
        elif callable(func):
            # @register.smart_tag
            return dec(func)
        else:
            raise TemplateSyntaxError("Invalid arguments provided to smart_tag")
