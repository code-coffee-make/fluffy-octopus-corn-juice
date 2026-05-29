import pymysql
from pymysql.cursors import DictCursor #列表里面装字典
conn = pymysql.connect(
    host = "localhost",
    user = "root",
    password = "lyq123123",
    database = "music",
    charset = "utf8mb4",
    cursorclass = DictCursor,
)

cursor = conn.cursor()

print("\n")
print("====插入测试歌手====")
#pymysql规定占位符%s
insert_operate = """INSERT INTO singers (name,gender,age,phone,debut_year,representative_song)
VALUES(%s, %s, %s, %s, %s, %s)
"""
test_singer = ("测试歌手","保密",20,"13800000099",2020,"测试歌曲")
try:
    cursor.execute(insert_operate,test_singer)
    conn.commit()
    print("插入成功")
except pymysql.err.IntegrityError:
    print("数据已存在不插入跳过插入环节")
    
print("\n")
print("====定义恶意输入====")
malicious_input = '"测试歌手" or "1"="1"'

print("\n")
print("====f_string拼接sql语句(有注入风险)====")
cursor.execute(f"SELECT * FROM singers WHERE name = {malicious_input}")
bad_result = cursor.fetchall()
print("错误方法查到了以下数据：")
for element in bad_result:
    print(f"{element['name']}")

print("\n")
print("用占位符安全输入====")
cursor.execute("SELECT * FROM singers WHERE name = %s",(malicious_input,))
good_result = cursor.fetchall()
print(f"正确方法查到了{len(good_result)}条数据，安全")

"""
为什么参数化能防恶意输入？
1.f-string拼接会直接把输入内容拼接到sql语句中,所以恶意输入会被当作sql语句
2.参数化（%s)会把输入转成一整个纯字符串:'"测试歌手" or '1'='1''不会被当成sql语句
"""

print("\n")
cursor.close()
conn.close()
print("数据库连接已关闭")