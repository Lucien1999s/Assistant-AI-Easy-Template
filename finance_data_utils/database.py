import ast
import sqlite3

def create(sectorId, data):
    """初始化-創建新資料庫"""
    conn = sqlite3.connect('stock.db')
    c = conn.cursor()
    c.execute(f'''CREATE TABLE IF NOT EXISTS stock_info (sector{sectorId} info)''')
    c.execute("INSERT INTO stock_info VALUES (?)", (data,))
    conn.commit()
    conn.close()

def insert_data_to_db(sectorId, data):
    """新增新的sector的資料到table當中"""
    conn = sqlite3.connect('stock.db')
    c = conn.cursor()
    c.execute(f'''ALTER TABLE stock_info ADD COLUMN sector{sectorId} info''')
    c.execute(f'''UPDATE stock_info SET sector{sectorId} = ?''', (data,))
    conn.commit()
    conn.close()

def fetch_data_from_db(sectorId):
    """透過查詢sectorId來獲取該sector資料"""
    conn = sqlite3.connect('stock.db')
    c = conn.cursor()
    c.execute(f"SELECT sector{sectorId} FROM stock_info")
    rows = c.fetchall()
    res=ast.literal_eval(rows[0][0])
    conn.close()
    return res

def update_data(sectorId, new_value):
    """更新sector資料為新狀態"""
    conn = sqlite3.connect('stock.db')
    c = conn.cursor()
    c.execute(f"UPDATE stock_info SET sector{sectorId} = ?", (new_value,))
    conn.commit()
    conn.close()

def check_table_columns():
    """檢查資料庫中有哪些sector資料集"""
    conn = sqlite3.connect('stock.db')
    c = conn.cursor()
    c.execute(f"PRAGMA table_info(stock_info)")
    rows = c.fetchall()
    column_names = [row[1] for row in rows]
    conn.close()
    return column_names

if __name__ == "__main__":
    check_table_columns()
    res = fetch_data_from_db("40")
    print(type(res))