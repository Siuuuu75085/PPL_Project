# Tutorial for using chatbox


**Requirement**
- You can download ANTLR4 at here: [ANTLR4 4.9.2](https://repo1.maven.org/maven2/org/antlr/antlr4/4.9.2/antlr4-4.9.2-complete.jar)
- There's must be antlr4 4.9.2-complete.jar in your path: ```C:/antlr/antlr4-4.9.2-complete.jar```
- Python 3 is installed


**Set up**
After downloaded and extracted the zip file:
- open VSC, open the directory of project
- use the terminal, type:
    - ```python chatbox.py gen``` to generate the ANTLR
    - ```python chatbox.py run``` to run the project

**Tutorial in command**
- Add/Delete: add/delete [number] [name], 'to cart' is optional for add, 'from cart' is optional for ddelete
    - ```add 3 iPhone to cart```
    - ```delete 5 Laptop from cart```
- Increase/Decrease: increase/decrease [name] by [number], 'by' is optional
    - ```increase iPhone by 3```
    - ```decrease iPhone by 2```
- Set: set [name] to [number]
    - ```set iPhone to 4```
- List: list all products or list [name]
    -```list all products```
    -```list laptop```
- View cart: ```view cart```
- Check out: ```check out```. when enter check out, a receipt.txt is generate with all items in cart with the total money
- Conditional Command: if [condition] then [command]: money and quantity only now
    - ```if money is larger than 100.00 then delete 3 laptop```

*noname4now*