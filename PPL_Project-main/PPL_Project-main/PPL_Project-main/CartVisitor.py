import sys
import json
from CompiledFiles.chatboxVisitor import chatboxVisitor

PRODUCTS_FILE = 'products.json'

class CartVisitor(chatboxVisitor):
    def __init__(self):
        self.cart = {}
        try:
            with open(PRODUCTS_FILE, 'r') as f:
                products_data = json.load(f)
            self.products = {item['id']: item['price'] for item in products_data}
            self.products.update({item['name'].lower(): item['price'] for item in products_data})
        except FileNotFoundError:
            print(f"Error: {PRODUCTS_FILE} not found")
            sys.exit(1)

        self.discounts = {
            "welcome": 0.1,
            "goodbye": 20.0,
            "see you soon": 0.15
        }
        self.current_discount = None
        self.error = None

    def validate_product(self, product):
        return product in self.products

    def calculate_total(self):
        total = sum(qty * self.products[prod] for prod, qty in self.cart.items())
        if self.current_discount:
            discount = self.discounts[self.current_discount]
            if discount < 1:
                total *= (1 - discount)
            else:
                total = max(0, total - discount)
        return round(total, 2)

    def visitProgram(self, ctx):
        if ctx.conditionalCommand():
            return self.visitConditionalCommand(ctx.conditionalCommand())
        elif ctx.command():
            return self.visitCommand(ctx.command())
        else:
            raise Exception("Unknown command structure.")
        
    def visitConditionalCommand(self, ctx):
        return self.visitCondition(ctx.condition())

    def visitCondition(self, ctx):
        if ctx.totalValue():
            return self.visitTotalValue(ctx.totalValue())
        elif ctx.itemAmount():
            return self.visitItemAmount(ctx.itemAmount())
        else:
            raise Exception("Unknown condition type")
    
    def visitTotalValue(self, ctx):
        compare = ctx.compareWords().getText()
        money = float(ctx.MONEY().getText())
        total = self.calculate_total()

        if compare == "equal to":
            return abs(total - money) < 0.01
        elif compare == "more than":
            return total > money
        elif compare == "less than":
            return total < money
        elif compare == "not equal to":
            return abs(total - money) >= 0.01
        elif compare == "greater than or equal to":
            return total >= money
        elif compare == "less than or equal to":
            return total <= money
        return False

    def visitItemAmount(self, ctx):
        product = ctx.NAME().getText()
        if not self.validate_product(product):
            self.error = f"Product '{product}' does not exist."
            return False
        qty = int(ctx.QUANTITY().getText())
        compare = ctx.compareWords().getText()
        current_qty = self.cart.get(product, 0)

        if compare == "equal to":
            return current_qty == qty
        elif compare == "more than":
            return current_qty > qty
        elif compare == "less than":
            return current_qty < qty
        elif compare == "not equal to":
            return current_qty != qty
        elif compare == "greater than or equal to":
            return current_qty >= qty
        elif compare == "less than or equal to":
            return current_qty <= qty
        return False

    def visitCommand(self, ctx):
        if ctx.addProduct():
            return self.visitAddProduct(ctx.addProduct())
        elif ctx.deleteProduct():
            return self.visitDeleteProduct(ctx.deleteProduct())
        elif ctx.increaseAmount():
            return self.visitIncreaseAmount(ctx.increaseAmount())
        elif ctx.decreaseAmount():
            return self.visitDecreaseAmount(ctx.decreaseAmount())
        elif ctx.setAmount():
            return self.visitSetAmount(ctx.setAmount())
        elif ctx.applyDiscount():
            return self.visitApplyDiscount(ctx.applyDiscount())
        elif ctx.listProducts():
            return self.visitListProducts(ctx.listProducts())
        elif ctx.viewCart():
            return self.visitViewCart(ctx.viewCart())
        elif ctx.checkOut():
            return self.visitCheckOut(ctx.checkOut())

    def visitAddProduct(self, ctx):
        items = []
        quantities = [int(q.getText()) for q in ctx.QUANTITY()]
        products = [p.getText() for p in ctx.NAME()]
        for product, qty in zip(products, quantities):
            if not self.validate_product(product):
                self.error = f"Product '{product}' does not exist"
                return
            if qty <= 0:
                self.error = f"Invalid quantity '{qty}' for {product}"
                return
            items.append((product, qty))
        for product, qty in items:
            self.cart[product] = self.cart.get(product, 0) + qty
        return f"Added {', '.join(f'{qty} {prod}' for prod, qty in items)} to cart"

    def visitDeleteProduct(self, ctx):
        products = [p.getText() for p in ctx.NAME()]
        for product in products:
            if not self.validate_product(product):
                self.error = f"Product '{product}' does not exist"
                return
            if product in self.cart:
                del self.cart[product]
        return f"Deleted {', '.join(products)} from cart"

    def visitIncreaseAmount(self, ctx):
        product = ctx.NAME().getText()
        qty = int(ctx.QUANTITY().getText())
        if not self.validate_product(product):
            self.error = f"Product '{product}' does not exist"
            return
        if qty <= 0:
            self.error = f"Invalid quantity '{qty}' for {product}"
            return
        self.cart[product] = self.cart.get(product, 0) + qty
        return f"Increased {product} by {qty}"

    def visitDecreaseAmount(self, ctx):
        product = ctx.NAME().getText()
        qty = int(ctx.QUANTITY().getText())
        if not self.validate_product(product):
            self.error = f"Product '{product}' does not exist"
            return
        if qty <= 0:
            self.error = f"Invalid quantity '{qty}' for {product}"
            return
        if product in self.cart:
            self.cart[product] = max(0, self.cart[product] - qty)
            if self.cart[product] == 0:
                del self.cart[product]
        return f"Decreased {product} by {qty}"

    def visitSetAmount(self, ctx):
        product = ctx.NAME().getText()
        qty = int(ctx.QUANTITY().getText())
        if not self.validate_product(product):
            self.error = f"Product '{product}' does not exist"
            return
        if qty < 0:
            self.error = f"Invalid quantity '{qty}' for {product}"
            return
        self.cart[product] = qty
        return f"Set {product} to {qty}"

    def visitApplyDiscount(self, ctx):
        discount = ctx.DISCOUNT().getText()
        if discount not in self.discounts:
            self.error = f"Invalid discount code: {discount}"
            return
        self.current_discount = discount
        return f"Applied discount '{discount}'"

    def visitListProducts(self, ctx):
        if ctx.getText() == "list all products":
            return "Available products: " + ", ".join(f"{p} (${self.products[p]})" for p in sorted(set(self.products.keys())))
        elif ctx.NAME():
            product = ctx.NAME().getText()
            if not self.validate_product(product):
                self.error = f"Product '{product}' does not exist"
                return
            qty = self.cart.get(product, 0)
            return f"{product}: {qty} in cart"
        return "Available products: " + ", ".join(f"{p} (${self.products[p]})" for p in sorted(set(self.products.keys())))

    def visitViewCart(self, ctx):
        if not self.cart:
            return "Cart is empty"
        result = ["Cart contents:"]
        for prod, qty in sorted(self.cart.items()):
            result.append(f"{prod}: {qty} (Subtotal: ${qty * self.products[prod]:.2f})")
        result.append(f"Total: ${self.calculate_total():.2f}")
        return "\n".join(result)

    def visitCheckOut(self, ctx):
        if not self.cart:
            return "Cart is empty, nothing to check out"
        total = self.calculate_total()
        result = f"Checked out. Total: ${total:.2f}"
        
        lines = ["Receipt:"]
        for prod, qty in sorted(self.cart.items()):
            lines.append(f"{prod}: {qty} (Subtotal: ${qty * self.products[prod]:.2f})")
            
        lines.append(f"Total: ${total:.2f}")    
        lines.append("Thank you for your purchase!")

        with open("receipt.txt", "w") as f:
            f.write("\n".join(lines))
            
        self.cart.clear()
        self.current_discount = None
        return result
    
    
def save_to_database(self, total):
    import mysql.connector, json
    with open("db_config.json") as f:
        config = json.load(f)

    try:
        conn = mysql.connector.connect(**config)
        cur = conn.cursor()

        cur.execute(
            "INSERT INTO orders (total, discount_code) VALUES (%s, %s)",
            (total, self.current_discount)
        )
        order_id = cur.lastrowid

        for prod, qty in self.cart.items():
            cur.execute(
                "INSERT INTO order_items (order_id, product_name, quantity, price_per_unit) VALUES (%s, %s, %s, %s)",
                (order_id, prod, qty, self.products[prod])
            )

        conn.commit()
        cur.close()
        conn.close()
    except mysql.connector.Error as err:
        print("MySQL Error:", err)
# noname4now