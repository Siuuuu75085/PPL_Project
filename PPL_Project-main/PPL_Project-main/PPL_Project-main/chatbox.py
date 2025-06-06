import sys, os
import subprocess
import unittest
import json
from antlr4 import *

DIR = os.path.dirname(__file__)
ANTLR_JAR = 'C:/PPL/antlr4-4.9.2-complete.jar'
CPL_Dest = 'CompiledFiles'
SRC = 'chatbox.g4'

def printUsage():
    print('python chatbox.py gen')
    print('python chatbox.py run')

def printBreak():
    print('-------------------------------------------------')

def generateAntlr2Python():
    print('Antlr4 is running...')
    subprocess.run(['java', '-jar', ANTLR_JAR, '-o', CPL_Dest, '-visitor', '-no-listener', '-Dlanguage=Python3', SRC])

    print('Generate successfully.')

def process_user_input(user_input):
    return f"Processed: {user_input}"

   
def run():
    print('Chatbox is now online! Please proceed the command or type \'exit\' to stop the chatbox.')
    
    from CompiledFiles.chatboxLexer import chatboxLexer
    from CompiledFiles.chatboxParser import chatboxParser
    from antlr4.error.ErrorListener import ErrorListener
    
    class CustomErrorListener(ErrorListener):
        def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
            print(f"Input rejected: {msg}")
            exit(1)
    
    from CartVisitor import CartVisitor
    visitor = CartVisitor()

    while True:
        try:
            user_input = input("\n>> ").strip().lower()
            if not user_input:
                continue
            if user_input in ("exit", "quit"):
                print("Exiting chatbox.")
                break

            input_stream = InputStream(user_input)
            lexer = chatboxLexer(input_stream)
            lexer.removeErrorListeners()
            lexer.addErrorListener(CustomErrorListener())

            token_stream = CommonTokenStream(lexer)
            parser = chatboxParser(token_stream)
            parser.removeErrorListeners()
            parser.addErrorListener(CustomErrorListener())

            tree = parser.program()
            result = visitor.visit(tree)

            if visitor.error:
                print(f"Error: {visitor.error}")
                visitor.error = None
            elif result is not None:
                print(result)
                if isinstance(result, dict) and 'total' in result:
                    total = result['total']
                    cart = result['cart']  
                    save_to_database(customer_id=1, total=total)

        except Exception as e:
            print(f"Input rejected: {e}")
  
def main(argv):
    print('Complete jar file ANTLR  :  ' + str(ANTLR_JAR))
    print('Length of arguments      :  ' + str(len(argv)))    
    printBreak()

    if len(argv) < 1:
        printUsage()
    elif argv[0] == 'gen':
        generateAntlr2Python()    
    elif argv[0] == 'run':       
        run()
    else:
        printUsage()

if __name__ == "__main__":
    main(sys.argv[1:])

import mysql.connector
import json

def save_to_database(customer_id: int, total: float, discount_code: str = None):
    try:
        with open("db_config.json") as f:
            config = json.load(f)

        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()
        sql="""
                INSERT INTO orders (customer_id, total, discount_code)
                VALUES (%s, %s, %s)
            """
        values = (customer_id, total, discount_code)

        cursor.execute(sql, values)
        conn.commit()
        print("Receipt saved to database.")
    except mysql.connector.Error as err:
        print(f"Database error: {err}")
    finally:
        cursor.close()
        conn.close()


def handle_input(user_input):
    from CompiledFiles.chatboxLexer import chatboxLexer
    from CompiledFiles.chatboxParser import chatboxParser
    from CartVisitor import CartVisitor
    from antlr4 import InputStream, CommonTokenStream

    class CustomErrorListener:
        def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
            raise Exception(f"Input rejected: {msg}")

    visitor = CartVisitor()

    input_stream = InputStream(user_input)
    lexer = chatboxLexer(input_stream)
    token_stream = CommonTokenStream(lexer)
    parser = chatboxParser(token_stream)

    tree = parser.program()
    result = visitor.visit(tree)

    if visitor.error:
        return f"Error: {visitor.error}"
    elif result is not None:
        if isinstance(result, dict) and 'total' in result:
            # save to DB if needed
            save_to_database(customer_id=1, total=result['total'])
        return str(result)
    return "No output"


# noname4now