import pymysql
import json
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import os

app = FastAPI()

import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# 挂载 js 目录
app.mount(
    "/js",
    StaticFiles(
        directory=os.path.join(os.path.dirname(os.path.abspath(__file__)), "js")
    ),
    name="js",
)

app.mount(
    "/css",
    StaticFiles(
        directory=os.path.join(os.path.dirname(os.path.abspath(__file__)), "css")
    ),
    name="css",
)


@app.get("/index")
def read_root():
    file_path = os.path.join(os.path.dirname(__file__), "index.html")
    with open(file_path, "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read())


@app.get("/category")
async def get_category_list():
    try:
        # 连接数据库
        _dbConn = pymysql.connect(
            host="127.0.0.1",
            user="root",
            password="123123",
            database="northwind",
            charset="utf8mb4",
            cursorclass=pymysql.cursors.DictCursor,  # 让 fetchall() 返回字典
        )

        with _dbConn.cursor() as _cursor:
            _sql = "SELECT CategoryId, CategoryName FROM Category;"
            _cursor.execute(_sql)

            # 获取查询结果
            results = _cursor.fetchall()  # 由于 DictCursor，results 已是字典列表

        return results  # 直接返回结果，不需要再转为 JSON 字符串

    except pymysql.MySQLError as err:
        print(f"数据库错误: {err.args[0]}, {err.args[1]}")
        return {"error": "数据库查询失败"}

    finally:
        if _dbConn:
            _dbConn.close()


@app.get("/category/{category_id}")
async def get_products(category_id: int):
    try:
        # 连接数据库
        _dbConn = pymysql.connect(
            host="127.0.0.1",
            user="root",
            password="123123",
            database="northwind",
            charset="utf8mb4",
            cursorclass=pymysql.cursors.DictCursor,  # 让 fetchall() 返回字典
        )

        with _dbConn.cursor() as _cursor:
            _sql = "SELECT product.ProductId, product.ProductName FROM product WHERE CategoryId = %s"
            _cursor.execute(_sql, (category_id,))  # 参数化查询，防止 SQL 注入

            # 获取查询结果
            results = _cursor.fetchall()  # 由于 DictCursor，results 已是字典列表

        return results  # 直接返回结果，不需要再转为 JSON 字符串

    except pymysql.MySQLError as err:
        print(f"数据库错误: {err.args[0]}, {err.args[1]}")
        return {"error": "数据库查询失败"}

    finally:
        if _dbConn:
            _dbConn.close()


@app.get("/query/1")
async def get_products():
    try:
        # 连接数据库
        _dbConn = pymysql.connect(
            host="127.0.0.1",
            user="root",
            password="123123",
            database="northwind",
            charset="utf8mb4",
            cursorclass=pymysql.cursors.DictCursor,  # 让 fetchall() 返回字典
        )

        with _dbConn.cursor() as _cursor:

            _sql = "SELECT p.ProductName,SUM(od.Quantity) AS TotalSales FROM OrderDetail od JOIN SalesOrder so ON od.OrderId = so.OrderId JOIN Product p ON od.ProductId = p.ProductId GROUP BY p.ProductId ORDER BY TotalSales DESC LIMIT 10"
            _cursor.execute(_sql)  # 参数化查询，防止 SQL 注入

            # 获取查询结果
            results = _cursor.fetchall()  # 由于 DictCursor，results 已是字典列表
        return results  # 直接返回结果，不需要再转为 JSON 字符串

    except pymysql.MySQLError as err:
        print(f"数据库错误: {err.args[0]}, {err.args[1]}")
        return {"error": "数据库查询失败"}

    finally:
        if _dbConn:
            _dbConn.close()


@app.get("/product/{product_id}")
async def get_products(product_id: int):
    try:
        # 连接数据库
        _dbConn = pymysql.connect(
            host="127.0.0.1",
            user="root",
            password="123123",
            database="northwind",
            charset="utf8mb4",
            cursorclass=pymysql.cursors.DictCursor,  # 让 fetchall() 返回字典
        )

        with _dbConn.cursor() as _cursor:

            _sql = "SELECT so.ShipCountry, SUM(od.quantity) as sales_quantity FROM salesorder so INNER JOIN orderdetail od ON so.OrderId = od.OrderId WHERE od.ProductId = %s GROUP BY so.shipcountry ORDER BY so.shipcountry"
            _cursor.execute(_sql, (product_id))  # 参数化查询，防止 SQL 注入

            # 获取查询结果
            results = _cursor.fetchall()  # 由于 DictCursor，results 已是字典列表
        return results  # 直接返回结果，不需要再转为 JSON 字符串

    except pymysql.MySQLError as err:
        print(f"数据库错误: {err.args[0]}, {err.args[1]}")
        return {"error": "数据库查询失败"}

    finally:
        if _dbConn:
            _dbConn.close()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app="app:app", host="localhost", port=8000, reload=True)
