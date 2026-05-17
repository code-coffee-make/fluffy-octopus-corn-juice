# 导入框架中的工具
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker

# 链接music库
engine = create_engine("mysql+pymysql://root:lyq123123@localhost:3306/music?charset=utf8mb4", echo=True)

#base 存建表的模板，在数据库中建表必须继承父类base元素才会被存入表
Base = declarative_base()

#定义一个类，这个类是以一个表格形式存在数据库中
class Singer(Base):
    __tablename__ = "Singers"
    id = Column(Integer, primary_key=True, autoincrement=True)#Column:列的意思
    name = Column(String(20), nullable=False)
    gender = Column(String(2))  # 男/女/保密
    age = Column(Integer)
    phone = Column(String(11), unique=True)  # 手机号唯一
    debut_year = Column(Integer)
    representative_song = Column(String(50))
    
#自动建表
Base.metadata.create_all(engine) #会建立base中所有类的表

#创建会话，绑定数据库
Session = sessionmaker(bind=engine)
session = Session()#创建一个工作台先在session上完成修改，再commit

#q清空
session.query(Singer).delete()
session.commit()#把删除操作同步数据库

#插入五个人
singers = [
    Singer(name="周杰伦", gender="男", age=45, phone="13800000001", debut_year=2000, representative_song="七里香"),
    Singer(name="林俊杰", gender="男", age=43, phone="13800000002", debut_year=2003, representative_song="江南"),
    Singer(name="邓紫棋", gender="女", age=32, phone="13800000003", debut_year=2008, representative_song="光年之外"),
    Singer(name="刘若英", gender="女", age=53, phone="13800000004", debut_year=1995, representative_song="后来"),
    Singer(name="李荣浩", gender="男", age=38, phone="13800000005", debut_year=2010, representative_song="年少有为"),
]
session.add_all(singers)#放在桌子上
session.commit()#提交到数据库中

#查询并输出
print("======年龄>30======")
result = session.query(Singer).filter(Singer.age > 30).all()
for s in result:
    print(s.name, s.age)

print("======女歌手======")
girls = session.query(Singer).filter(Singer.gender == "女").all()
for g in girls:
    print(g.name, g.representative_song)

print("======按出道年份升序======")
sorted_singers = session.query(Singer).order_by(Singer.debut_year.asc()).all()
for s in sorted_singers:
    print(s.name, s.debut_year)
zhou = session.query(Singer).filter(Singer.name == "周杰伦").first()
zhou.age = 46
session.commit()

deng = session.query(Singer).filter(Singer.name == "邓紫棋").first()
deng.representative_song = "泡沫"
session.commit()

print("======插入刘德华======")
def add_singer(name, gender, age, phone, debut_year, song):
    exists = session.query(Singer).filter(Singer.phone == phone).first()
    if exists:
        print(f"插入失败:手机号 {phone} 已存在")
        return
    
    new_singer = Singer(name=name, gender=gender, age=age, phone=phone, debut_year=debut_year, representative_song=song)
    session.add(new_singer)
    session.commit()
    print(f"{name} 插入成功")
add_singer("刘德华", "男", 55, "13800000001", 1985, "忘情水")

print("======插入陈奕迅======")
add_singer("陈奕迅", "男", 50, "13800000006", 1996, "十年")

print("======删除邓紫棋======")

#query():找singer表    filter():筛选条件 只招名字为邓紫棋的      first只找第一个
deng = session.query(Singer).filter(Singer.name == "邓紫棋").first()
session.delete(deng)
session.commit()

print("======查询最终表中所有歌手信息======")
all_singer = session.query(Singer).all()
for i in all_singer:
    print(i.name,i.gender,i.age,i.phone,i.debut_year,i.representative_song)

print("======事务回滚======")
try:
    with session.begin():
        exit = session.query(Singer).filter(Singer.phone == "13800000006").first()
        if not exit:
            add_singer(name="王菲", gender="女", age=55, phone="13800000006", debut_year=1989, representative_song="传奇")
        raise Exception("模拟出错")
except:
    print("事务已回滚")
print("回滚后结果:")
for i in session.query(Singer).all():
    print(i.name)