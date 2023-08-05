## ddcompiler

ddcompiler is the parser used by AutomationEdge AI Studio dialog designer. In dialog designer, conditions can be used either in an action dialog element or a branch dialog element. A condition is an expression which evaluates either to True or False. ddcompiler has a lexer and a parser which respectively tokenizes and parses the given expression.

### Installation

**pip install ddcompiler** will install the library. It has been tested with Python 3.9.6, but should work with any Python 3.\* version.

### Basic Usage

```python
import ddcompiler as ddc
var_dict = {
    'conv.lang': 'fr',
}

# Variables used in the expression of the form ${var_name} should be present in the var_dict.
expression = '${conv.lang} == "fr" or ${conv.lang} == "de" and contains("aistudio", "studio")'

# Instantiate parser and lexer, pass expression to the lexer.
ddparser = ddc.DDParser(ddc.DDLexer(expression))
tree = ddparser.parse()
# Prints parse tree
tree.traverse()
# Get list of variables used in the expression in form of a set
print(f"VARIABLES in the expression: {ddparser.get_variables()}")

print(f"INPUT: {expression}")
print(f"EVALUATION: {tree.evaluate(var_dict)}")
```

### Expression Language

Visit [AI Studio](https://docs.automationedge.ai/docs/getting-started/manual-configuration/conditions/) documentation to get list of supported constructs.

### More Examples

Go through [parser test file](https://bitbucket.org/yovyom/ddcompiler/src/master/tests/test_parser.py) to see different examples of expressions.
