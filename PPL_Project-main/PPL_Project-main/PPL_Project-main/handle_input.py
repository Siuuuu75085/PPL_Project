from antlr4 import InputStream, CommonTokenStream
from CompiledFiles.chatboxLexer import chatboxLexer
from CompiledFiles.chatboxParser import chatboxParser
from CartVisitor import CartVisitor
from chatbox import save_to_database

class CustomErrorListener:
    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        raise Exception(f"Input rejected: {msg}")

def handle_input(user_input):
    visitor = CartVisitor()

    try:
        input_stream = InputStream(user_input.lower())
        lexer = chatboxLexer(input_stream)
        token_stream = CommonTokenStream(lexer)
        parser = chatboxParser(token_stream)

        tree = parser.program()
        result = visitor.visit(tree)

        if visitor.error:
            return f"Error: {visitor.error}"
        elif result is not None:
            if isinstance(result, dict) and 'total' in result:
                save_to_database(customer_id=1, total=result['total'], discount_code=visitor.current_discount)
            return str(result)

        return "No output"

    except Exception as e:
        return f"Error: {e}"
