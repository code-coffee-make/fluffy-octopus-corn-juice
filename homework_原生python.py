""" cursor.execute(sql,  参数必须是元组！)
    cursor.execute(sql)  SQL 里没有任何变量
    修改操作："UPDATE singers SET debut_year = 2026 WHERE name = 'lyq';#多条sql才需要加分号
    查询操作："SELECT name,age FROM singers WHERE gender = '女';
    插入操作："INSERT INTO singers (name,gender)
              VALUES
              ('abc',1),
              ('bcd',2)"
    排序操作："SELECT name FROM singers ORDER BY debut_year ASC/DESC"
    删除操作："DELETE FEOM singers WHERE name = '邓紫棋'
"""
import pymysql
#pymsql.connect()将python代码与Mysql连接上
conn = pymysql.connect(
    host = "localhost",
    user = "root",
    password = "lyq123123",
    database = "music",
    charset = "utf8mb4",
)
cursor = conn.cursor()#创建一个游标

#这行完全可以删掉，在navicat上建表
create_table_sql = """
CREATE TABLE IF NOT EXISTS singers (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(50) NOT NULL,
    gender VARCHAR(2) NOT NULL,
    age INT NOT NULL,
    phone VARCHAR(11) NOT NULL UNIQUE,
    debut_year INT NOT NULL,
    representative_song VARCHAR(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
"""
cursor.execute(create_table_sql)
conn.commit()


#q清空表中内容
cursor.execute("TRUNCATE TABLE singers;")
conn.commit()#注意是提交是连接的功能

print("-----插入五个歌手信息-----")
insert_table = """INSERT INTO singers(name,gender,age,phone,debut_year,representative_song)
VALUES
('周杰伦','男',45,'13800000001',2000,'七里香'),
('林俊杰','男',43,'13800000002',2003,'江南'),
('邓紫棋','女',32,'13800000003',2008,'光年之外'),
('刘若英','女',53,'13800000004',1995,'后来'),
('李荣浩','男',38,'13800000005',2010,'年少有为')"""
cursor.execute(insert_table)
conn.commit()

print("-----查询>30的歌手-----")
insqure = "SELECT name,age FROM singers WHERE age>30"
cursor.execute(insqure)

for element in cursor.fetchall():#拿上一句SELECT的数据，返回列表（每个列表元素是一个元组）
    print(f"{element[0]},{element[1]}")

print("----查询所有女歌手-----")
insqure2 = "SELECT name FROM singers WHERE gender = '女'"
cursor.execute(insqure2)
for element in cursor.fetchall():
    print(f"{element[0]}")
    
print("----按出道年龄升序排列----")
#ASC = 升序 = 从小到大（1995、2000、2008）
#DESC = 降序 = 从大到小（2008、2000、1995）
operate = "SELECT name, debut_year FROM singers ORDER BY debut_year ASC"
cursor.execute(operate)
conn.commit()
result = cursor.fetchall()
for element in result:
    
    """if在一开始开启from pymysql.cursors import DictCursor字典游标,则可以element['name']==element[0]"""
    print(f"{element[0]} {element[1]}")#只查询了俩个内容只能有0，1

print("----更新周杰伦的年龄为46----")
cursor.execute("UPDATE singers SET age = 46 WHERE name = '周杰伦'")
conn.commit()

print("----更新邓紫棋代表作----")
cursor.execute("UPDATE singers SET representative_song = '泡沫' WHERE name = '邓紫棋'")
conn.commit()

print("----查重插入刘德华----")
phone = "13800000001"
cursor.execute("SELECT * FROM singers WHERE phone == %s",(phone,))
exit = cursor.fetchone()
if exit :
    print("插入失败，号码已存在")
else:
    
    #值不固定phone是变量 VALUE后要用（%s,%s）这样的占位符
    cursor.execute("INSERT INTO singers (name,gender,age,phone,debut_year,representative_song) VALUES (%s,%s,%s,%s,%s,%s)",
                   ("陈奕迅", "男", 50, phone, 1996, "十年"))
    conn.commit()

print("----删除邓紫棋----")
cursor.execute("DELETE FROM singers WHERE name = '邓紫棋'")
conn.commit()

print("----查询所有歌手----")
cursor.execute("SELET * FROM singers ORDER BY id")
all_singers = cursor.fetchall()
for element in all_singers:
    print(f"{element[0]} {element[1]} {element[2]}")

print("-------------题目二插入王菲+抛异常---------------")
"""用with自动创建游标会自动关闭 不然
    cursor = conn.cursor()  # 自己创建
    cursor.execute(sql)
    cursor.close() # 自己关闭
    """
try:
    with conn.cursor() as trans_cursor:
        phone = '13800000006'
        trans_cursor.execute("SELECT FROM singers WHERE phone = %s",(phone,))
        exit = cursor.fetchone()
        if not exit:
            trans_cursor.execute("INSERT INTO singers(name,gender,age,phone,debut_year,representative_song) VALUES (%s,%s,%s,%s,%s,%s)",
             ("王菲", "女", 55, "13800000006", 1989, "红豆")
            )
            raise Exception("模拟出错")#raise手动报错
        conn.commit()#提交要在错误之后，提交后再回滚就没用了
except Exception as e:
        conn.rollback()
        print("事务已回滚，王菲未插入")

cursor.close()
conn.close()