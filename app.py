from flask import Flask, render_template, request, jsonify
import mysql.connector

app = Flask(__name__)


# =========================================================
# DATABASE CONNECTION
# =========================================================
def get_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="tiger",
        database="ai_business_db"
    )


# =========================================================
# HOME
# =========================================================
@app.route("/")
def home():
    return render_template("index.html")


# =========================================================
# LOGIN
# =========================================================
@app.route("/api/login", methods=["POST"])
def login():

    db = None
    cursor = None

    try:
        data = request.get_json() or {}

        email = str(data.get("email", "")).strip().lower()
        password = str(data.get("password", ""))

        if not email or not password:
            return jsonify({
                "success": False,
                "message": "Email and password are required."
            }), 400

        db = get_db()
        cursor = db.cursor(dictionary=True)

        cursor.execute("""
            SELECT id, name, email, password
            FROM users
            WHERE LOWER(email) = %s
            LIMIT 1
        """, (email,))

        user = cursor.fetchone()

        if not user:
            return jsonify({
                "success": False,
                "message": "Invalid email or password"
            }), 401

        if str(user["password"]) != password:
            return jsonify({
                "success": False,
                "message": "Invalid email or password"
            }), 401

        return jsonify({
            "success": True,
            "message": "Login Successful",
            "user": {
                "id": user["id"],
                "name": user["name"],
                "email": user["email"]
            }
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)
        }), 500

    finally:
        if cursor:
            cursor.close()

        if db:
            db.close()


# =========================================================
# CUSTOMERS - GET
# =========================================================
@app.route("/api/customers", methods=["GET"])
def get_customers():

    db = None
    cursor = None

    try:
        db = get_db()
        cursor = db.cursor(dictionary=True)

        cursor.execute("""
            SELECT *
            FROM customers
            ORDER BY id DESC
        """)

        customers = cursor.fetchall()

        return jsonify(customers)

    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)
        }), 500

    finally:
        if cursor:
            cursor.close()

        if db:
            db.close()


# =========================================================
# CUSTOMERS - ADD
# =========================================================
@app.route("/api/customers", methods=["POST"])
def add_customer():

    db = None
    cursor = None

    try:
        data = request.get_json() or {}

        name = data.get("name")
        phone = data.get("phone")
        email = data.get("email")
        city = data.get("city")

        if not name:
            return jsonify({
                "success": False,
                "message": "Customer name is required."
            }), 400

        db = get_db()
        cursor = db.cursor()

        cursor.execute("""
            INSERT INTO customers
            (
                name,
                phone,
                email,
                city
            )
            VALUES (%s, %s, %s, %s)
        """, (
            name,
            phone,
            email,
            city
        ))

        db.commit()

        return jsonify({
            "success": True,
            "message": "Customer added successfully."
        })

    except Exception as e:

        if db:
            db.rollback()

        return jsonify({
            "success": False,
            "message": str(e)
        }), 500

    finally:
        if cursor:
            cursor.close()

        if db:
            db.close()


# =========================================================
# PRODUCTS - GET
# =========================================================
@app.route("/api/products", methods=["GET"])
def get_products():

    db = None
    cursor = None

    try:
        db = get_db()
        cursor = db.cursor(dictionary=True)

        cursor.execute("""
            SELECT
                id,
                brand,
                model,
                imei1,
                imei2,
                ram,
                storage,
                color,
                name,
                sku,
                category,
                purchase_price,
                selling_price,
                stock,
                min_stock,
                supplier,
                warranty,
                created_at
            FROM products
            ORDER BY id DESC
        """)

        products = cursor.fetchall()

        return jsonify(products)

    except Exception as e:

        return jsonify({
            "success": False,
            "message": str(e)
        }), 500

    finally:
        if cursor:
            cursor.close()

        if db:
            db.close()


# =========================================================
# PRODUCTS - ADD
# =========================================================
@app.route("/api/products", methods=["POST"])
def add_product():

    db = None
    cursor = None

    try:
        data = request.get_json() or {}

        # Mobile details
        brand = data.get("brand")
        model = data.get("model")
        imei1 = data.get("imei1")
        imei2 = data.get("imei2")
        ram = data.get("ram")
        storage = data.get("storage")
        color = data.get("color")

        # Product details
        name = data.get("name")
        sku = data.get("sku")
        category = data.get("category")

        # Price / stock
        try:
            purchase_price = float(data.get("purchase_price", 0) or 0)
        except:
            purchase_price = 0

        try:
            selling_price = float(data.get("selling_price", 0) or 0)
        except:
            selling_price = 0

        try:
            stock = int(data.get("stock", 0) or 0)
        except:
            stock = 0

        try:
            min_stock = int(data.get("min_stock", 0) or 0)
        except:
            min_stock = 0

        # Other
        supplier = data.get("supplier")
        warranty = data.get("warranty")

        # Validation
        if not brand:
            return jsonify({
                "success": False,
                "message": "Brand is required."
            }), 400

        if not model:
            return jsonify({
                "success": False,
                "message": "Model is required."
            }), 400

        if purchase_price < 0:
            return jsonify({
                "success": False,
                "message": "Purchase price cannot be negative."
            }), 400

        if selling_price < 0:
            return jsonify({
                "success": False,
                "message": "Selling price cannot be negative."
            }), 400

        if stock < 0:
            return jsonify({
                "success": False,
                "message": "Stock cannot be negative."
            }), 400

        db = get_db()
        cursor = db.cursor()

        cursor.execute("""
            INSERT INTO products
            (
                brand,
                model,
                imei1,
                imei2,
                ram,
                storage,
                color,
                name,
                sku,
                category,
                purchase_price,
                selling_price,
                stock,
                min_stock,
                supplier,
                warranty
            )
            VALUES
            (
                %s, %s, %s, %s,
                %s, %s, %s, %s,
                %s, %s, %s, %s,
                %s, %s, %s, %s
            )
        """, (
            brand,
            model,
            imei1,
            imei2,
            ram,
            storage,
            color,
            name,
            sku,
            category,
            purchase_price,
            selling_price,
            stock,
            min_stock,
            supplier,
            warranty
        ))

        db.commit()

        return jsonify({
            "success": True,
            "message": "Mobile added successfully."
        })

    except Exception as e:

        if db:
            db.rollback()

        return jsonify({
            "success": False,
            "message": str(e)
        }), 500

    finally:
        if cursor:
            cursor.close()

        if db:
            db.close()


# =========================================================
# SALES - GET
# =========================================================
@app.route("/api/sales", methods=["GET"])
def get_sales():

    db = None
    cursor = None

    try:
        db = get_db()
        cursor = db.cursor(dictionary=True)

        cursor.execute("""
            SELECT
                sales.id,
                sales.customer_name,
                sales.product_id,
                products.name AS product_name,
                products.brand,
                products.model,
                sales.quantity,
                sales.amount,
                sales.sale_date
            FROM sales
            LEFT JOIN products
                ON sales.product_id = products.id
            ORDER BY sales.id DESC
        """)

        sales = cursor.fetchall()

        return jsonify(sales)

    except Exception as e:

        return jsonify({
            "success": False,
            "message": str(e)
        }), 500

    finally:
        if cursor:
            cursor.close()

        if db:
            db.close()


# =========================================================
# SALES - ADD
# =========================================================
@app.route("/api/sales", methods=["POST"])
def add_sale():

    db = None
    cursor = None

    try:
        data = request.get_json() or {}

        customer_name = data.get("customer_name")
        product_id = data.get("product_id")

        try:
            product_id = int(product_id)
        except:
            product_id = 0

        try:
            quantity = int(data.get("quantity", 0) or 0)
        except:
            quantity = 0

        if not product_id:
            return jsonify({
                "success": False,
                "message": "Product is required."
            }), 400

        if quantity <= 0:
            return jsonify({
                "success": False,
                "message": "Quantity must be greater than 0."
            }), 400

        db = get_db()

        # Transaction cursor
        cursor = db.cursor(dictionary=True)

        # -------------------------------------------------
        # GET PRODUCT
        # -------------------------------------------------
        cursor.execute("""
            SELECT
                id,
                name,
                brand,
                model,
                selling_price,
                stock
            FROM products
            WHERE id = %s
            FOR UPDATE
        """, (product_id,))

        product = cursor.fetchone()

        if not product:
            return jsonify({
                "success": False,
                "message": "Product not found."
            }), 404

        # -------------------------------------------------
        # STOCK CHECK
        # -------------------------------------------------
        if product["stock"] < quantity:
            return jsonify({
                "success": False,
                "message": "Insufficient stock."
            }), 400

        # -------------------------------------------------
        # CALCULATE AMOUNT
        # -------------------------------------------------
        amount = float(product["selling_price"] or 0) * quantity

        # -------------------------------------------------
        # INSERT SALE
        # -------------------------------------------------
        cursor.execute("""
            INSERT INTO sales
            (
                customer_name,
                product_id,
                quantity,
                amount
            )
            VALUES (%s, %s, %s, %s)
        """, (
            customer_name,
            product_id,
            quantity,
            amount
        ))

        # -------------------------------------------------
        # REDUCE STOCK
        # -------------------------------------------------
        cursor.execute("""
            UPDATE products
            SET stock = stock - %s
            WHERE id = %s
        """, (
            quantity,
            product_id
        ))

        db.commit()

        new_stock = int(product["stock"]) - quantity

        return jsonify({
            "success": True,
            "message": "Sale added successfully.",
            "amount": amount,
            "new_stock": new_stock
        })

    except Exception as e:

        if db:
            db.rollback()

        return jsonify({
            "success": False,
            "message": str(e)
        }), 500

    finally:
        if cursor:
            cursor.close()

        if db:
            db.close()


# =========================================================
# PURCHASES - GET
# =========================================================
@app.route("/api/purchases", methods=["GET"])
def get_purchases():

    db = None
    cursor = None

    try:
        db = get_db()
        cursor = db.cursor(dictionary=True)

        cursor.execute("""
            SELECT
                purchases.id,
                purchases.supplier,
                purchases.product_id,
                products.brand,
                products.model,
                products.name AS product_name,
                purchases.quantity,
                purchases.purchase_price,
                purchases.total_amount,
                purchases.purchase_date,
                purchases.invoice_no,
                purchases.notes,
                purchases.created_at
            FROM purchases
            LEFT JOIN products
                ON purchases.product_id = products.id
            ORDER BY purchases.id DESC
        """)

        purchases = cursor.fetchall()

        return jsonify(purchases)

    except Exception as e:

        return jsonify({
            "success": False,
            "message": str(e)
        }), 500

    finally:
        if cursor:
            cursor.close()

        if db:
            db.close()


# =========================================================
# PURCHASES - ADD
# =========================================================
@app.route("/api/purchases", methods=["POST"])
def add_purchase():

    db = None
    cursor = None

    try:
        data = request.get_json() or {}

        supplier = data.get("supplier")
        product_id = data.get("product_id")
        purchase_date = data.get("purchase_date")
        invoice_no = data.get("invoice_no")
        notes = data.get("notes")

        try:
            product_id = int(product_id)
        except:
            product_id = 0

        try:
            quantity = int(data.get("quantity", 0) or 0)
        except:
            quantity = 0

        try:
            purchase_price = float(
                data.get("purchase_price", 0) or 0
            )
        except:
            purchase_price = 0

        # -------------------------------------------------
        # VALIDATION
        # -------------------------------------------------
        if not supplier:
            return jsonify({
                "success": False,
                "message": "Supplier is required."
            }), 400

        if not product_id:
            return jsonify({
                "success": False,
                "message": "Product is required."
            }), 400

        if quantity <= 0:
            return jsonify({
                "success": False,
                "message": "Quantity must be greater than 0."
            }), 400

        if purchase_price < 0:
            return jsonify({
                "success": False,
                "message": "Purchase price cannot be negative."
            }), 400

        if not purchase_date:
            return jsonify({
                "success": False,
                "message": "Purchase date is required."
            }), 400

        db = get_db()

        cursor = db.cursor(dictionary=True)

        # -------------------------------------------------
        # GET PRODUCT
        # -------------------------------------------------
        cursor.execute("""
            SELECT
                id,
                brand,
                model,
                stock
            FROM products
            WHERE id = %s
            FOR UPDATE
        """, (product_id,))

        product = cursor.fetchone()

        if not product:
            return jsonify({
                "success": False,
                "message": "Product not found."
            }), 404

        # -------------------------------------------------
        # TOTAL
        # -------------------------------------------------
        total_amount = quantity * purchase_price

        # -------------------------------------------------
        # INSERT PURCHASE
        # -------------------------------------------------
        cursor.execute("""
            INSERT INTO purchases
            (
                supplier,
                product_id,
                quantity,
                purchase_price,
                total_amount,
                purchase_date,
                invoice_no,
                notes
            )
            VALUES
            (
                %s, %s, %s, %s,
                %s, %s, %s, %s
            )
        """, (
            supplier,
            product_id,
            quantity,
            purchase_price,
            total_amount,
            purchase_date,
            invoice_no,
            notes
        ))

        # -------------------------------------------------
        # UPDATE STOCK
        # -------------------------------------------------
        cursor.execute("""
            UPDATE products
            SET
                stock = stock + %s,
                purchase_price = %s,
                supplier = %s
            WHERE id = %s
        """, (
            quantity,
            purchase_price,
            supplier,
            product_id
        ))

        db.commit()

        new_stock = int(product["stock"]) + quantity

        return jsonify({
            "success": True,
            "message": "Purchase added successfully.",
            "quantity_added": quantity,
            "total_amount": float(total_amount),
            "new_stock": new_stock
        })

    except Exception as e:

        if db:
            db.rollback()

        return jsonify({
            "success": False,
            "message": str(e)
        }), 500

    finally:
        if cursor:
            cursor.close()

        if db:
            db.close()


# =========================================================
# EXPENSES - GET
# =========================================================
@app.route("/api/expenses", methods=["GET"])
def get_expenses():

    db = None
    cursor = None

    try:
        db = get_db()
        cursor = db.cursor(dictionary=True)

        cursor.execute("""
            SELECT
                id,
                title,
                category,
                amount,
                expense_date,
                notes,
                created_at
            FROM expenses
            ORDER BY id DESC
        """)

        expenses = cursor.fetchall()

        return jsonify(expenses)

    except Exception as e:

        return jsonify({
            "success": False,
            "message": str(e)
        }), 500

    finally:
        if cursor:
            cursor.close()

        if db:
            db.close()


# =========================================================
# EXPENSES - ADD
# =========================================================
@app.route("/api/expenses", methods=["POST"])
def add_expense():

    db = None
    cursor = None

    try:
        data = request.get_json() or {}

        title = data.get("title")
        category = data.get("category")
        amount = data.get("amount")
        expense_date = data.get("expense_date")
        notes = data.get("notes")

        if not title:
            return jsonify({
                "success": False,
                "message": "Title is required."
            }), 400

        if amount is None or amount == "":
            return jsonify({
                "success": False,
                "message": "Amount is required."
            }), 400

        if not expense_date:
            return jsonify({
                "success": False,
                "message": "Expense date is required."
            }), 400

        try:
            amount = float(amount)
        except:
            return jsonify({
                "success": False,
                "message": "Invalid expense amount."
            }), 400

        if amount < 0:
            return jsonify({
                "success": False,
                "message": "Amount cannot be negative."
            }), 400

        db = get_db()
        cursor = db.cursor()

        cursor.execute("""
            INSERT INTO expenses
            (
                title,
                category,
                amount,
                expense_date,
                notes
            )
            VALUES (%s, %s, %s, %s, %s)
        """, (
            title,
            category,
            amount,
            expense_date,
            notes
        ))

        db.commit()

        return jsonify({
            "success": True,
            "message": "Expense added successfully."
        })

    except Exception as e:

        if db:
            db.rollback()

        return jsonify({
            "success": False,
            "message": str(e)
        }), 500

    finally:
        if cursor:
            cursor.close()

        if db:
            db.close()


# =========================================================
# REPORTS API
# =========================================================
@app.route("/api/reports", methods=["GET"])
def get_reports():

    db = None
    cursor = None

    try:
        db = get_db()
        cursor = db.cursor(dictionary=True)

        # 1. Total Sales
        cursor.execute("""
            SELECT COALESCE(SUM(amount), 0) AS total_sales
            FROM sales
        """)
        sales_data = cursor.fetchone()

        # 2. Total Purchases
        cursor.execute("""
            SELECT COALESCE(SUM(total_amount), 0) AS total_purchases
            FROM purchases
        """)
        purchases_data = cursor.fetchone()

        # 3. Total Expenses
        cursor.execute("""
            SELECT COALESCE(SUM(amount), 0) AS total_expenses
            FROM expenses
        """)
        expenses_data = cursor.fetchone()

        # 4. Total Products and Current Stock
        cursor.execute("""
            SELECT
                COUNT(*) AS total_products,
                COALESCE(SUM(stock), 0) AS total_stock
            FROM products
        """)
        products_data = cursor.fetchone()

        # 5. Estimated Profit
        # Uses the current purchase_price for sold products.
        cursor.execute("""
            SELECT COALESCE(
                SUM(s.quantity * COALESCE(p.purchase_price, 0)),
                0
            ) AS estimated_cost_of_goods
            FROM sales s
            LEFT JOIN products p
                ON s.product_id = p.id
        """)
        cost_data = cursor.fetchone()

        total_sales = float(sales_data["total_sales"] or 0)
        total_purchases = float(
            purchases_data["total_purchases"] or 0
        )
        total_expenses = float(
            expenses_data["total_expenses"] or 0
        )
        total_products = int(products_data["total_products"] or 0)
        total_stock = int(products_data["total_stock"] or 0)
        estimated_cost = float(
            cost_data["estimated_cost_of_goods"] or 0
        )

        estimated_profit = (
            total_sales - estimated_cost - total_expenses
        )

        return jsonify({
            "success": True,
            "total_sales": round(total_sales, 2),
            "total_purchases": round(total_purchases, 2),
            "total_expenses": round(total_expenses, 2),
            "total_products": total_products,
            "total_stock": total_stock,
            "estimated_cost_of_goods": round(estimated_cost, 2),
            "estimated_profit": round(estimated_profit, 2)
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)
        }), 500

    finally:
        if cursor:
            cursor.close()

        if db:
            db.close()

# =========================================================
# RUN APPLICATION
# =========================================================
if __name__ == "__main__":
    app.run(
        debug=True,
        host="127.0.0.1",
        port=5000
    )