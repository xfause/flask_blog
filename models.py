from blogDB import get_db
from flask import Flask
from functools import reduce

#password类
class password:
    def __init__(self,pwd):
        self.pwd = pwd
    def check(self):
        if self.pwd=='1234':
            return True
        else :
            return False

#Article
class Article:
    def __init__(self,id):
        self.id = id
        self.title = ''
        self.content = ''
        self.tag = ''
        self.file = 1

    def getExit(self):
        # 必加 相当于和数据库连接
        blogdb = get_db()
        cur = blogdb.cursor()
        #
        cur.execute('SELECT id, title, abstract, tag, date, file FROM blog where id = ?',(self.id,))
        exit = cur.fetchall()[0]
        self.id = exit[0]
        self.title = exit[1]
        self.abstract = exit[2]
        self.tag = exit[3]
        date = exit[4]
        if hasattr(date,'strftime'):
            self.date = date.strftime('%x')
        else:
            self.date = date[5:7] + '/' + date[8:10] + '/' + date[:4]
        file = exit[5]
        fileDict = {1:'分类1', 3:'分类2', 4:'分类3', 5:'分类4'}
        self.file = fileDict[file]
        return self

    def getArti(self):
        blogdb = get_db()
        cur = blogdb.cursor()
        cur.execute('SELECT title, date, content, tag, abstract from blog where id = ?',(self.id,))
        arti = cur.fetchall()[0]
        self.title = arti[0]
        self.date = arti[1]
        self.content = arti[2]
        self.tag = arti[3]
        self.abstract = arti[4][:-17]
        com = comment(self.id)
        self.comList = com.commList()
        
    def delArti(self):
        blogdb = get_db()
        cur = blogdb.cursor()
        cur.execute('DELETE FROM blog where id = ?',(self.id,))
        cur.execute('DELETE from tag where id = ?',(self.id,))
        cur.execute("DELETE from comm where id = ?",(self.id,))

    def getEdit(self):
        blogdb = get_db()
        cur = blogdb.cursor()
        cur.execute('SELECT title,content,tag from blog where id = ?',(self.id,))
        content = cur.fetchall()[0]
        self.title = content[0]
        self.content = content[1]
        self.tag = content[2]

    def update(self, title, tag, img, file, content):
        abstract = abstr(content,img)
        tags = (tag or '').replace('，',',')
        blogdb = get_db()
        cur = blogdb.cursor()
        if self.id:
            cur.execute('UPDATE blog SET title = ? ,content = ?,abstract = ?,tag = ? ,file = ? WHERE ID = ?;', (title, content,abstract,tags,file, self.id))
        else:
            cur.execute('insert into blog (title,tag,file,abstract,content) values (?, ?, ?, ?, ?)', (title,tags,file,abstract,content))
            cur.execute('select id from blog order by id desc limit 1')
            blog = cur.fetchall()
            self.id = blog[0][0]
        blogdb.commit()
        cur.execute('delete from tag where blog = ?',(self.id,))
        if tags:
            tags = tags.split(',')
        else:
            tags = []
        for tag in tags:
            cur.execute('insert into tag (tag, blog) values (?, ?)', (tag, self.id))
        blogdb.commit()

#评论类
class comment:
    def __init__(self, id=0):
        self.id = id

    def commList(self):
        try:
            blogdb = get_db()
            cur = blogdb.cursor()
            #按照id降序排列DESC 升序排列ASC order by
            cur.execute('SELECT content,date,author,id,reply from comm where id=? order by id DESC',(self.id,))
            tmp = cur.fetchall() or []
            tmp = list(tmp) #列表化
            tmp = map(lambda x:list(x),tmp) #lambda
            #???
            def coSort(x,y):
                xid = x[4] or x[3]
                yid = y[4] or y[3]
                if xid<yid :
                    return 1
                else:
                    return -1
            tmp = sorted(tmp,coSort)
            def coVeri(x):
                x[4] = x[4] or x[3]
                diff = x[4]-x[3]
                diff = diff or ''
                x[4] = diff and u're'
                return x
            self.cList = map(coVeri,tmp)
            ###
        except:
            self.cList = []
        finally:
            return self.cList

    def getNew(self):
        blogdb = get_db()
        cur = blogdb.cursor()
        cur.execute('SELECT content,date,author,id,blog FROM comm order by id DESC LIMIT 12')
        tmp = cur.fetchall() or []
        self.cList = tmp;
        return self.cList

    def insert(self,content,author,reply):
        author = author or u'访客'
        reply = reply or None
        blogdb = get_db()
        cur = blogdb.cursor()
        cur.execute('INSERT into comm (content,author,blog,reply) values(?,?,?,?)',(content,author,self.id,reply))
        blogdb.commit()

    def delete(self):
        blogdb = get_db()
        cur = blogdb.cursor()
        cur.execute('DELETE from comm where id=?',(self.id,))
        blogdb.commit()

#目录类
class artiList:
    def __init__(self,method='',key='',page=1):
        self.method = method
        self.key = key
        self.page = (page-1)*8

    def getAl(self):
        results = []
        for arti in self.al:
            tmp = Article(arti)
            tmp = tmp.getExit()
            results.append(tmp)
        self.results = results
        return self.results

    def getLen(self):
        blogdb = get_db()
        cur = blogdb.cursor()
        if self.method =='file':
            cur.execute('SELECT count(*) from blog where file=?;',(self.key,))
        elif  self.method =='tag':
            cur.execute('SELECT count(*) FROM tag WHERE tag=?;',(self.key,))
        else :
            cur.execute('SELECT count(*) FROM blog;')
        rawlen = cur.fetchall()
        rawlen = int(rawlen[0][0])
        self.len = round((rawlen+7)/8) or 1
        return self.len

    def alUpdate(self):
        blogdb = get_db()
        cur = blogdb.cursor()
        if self.method == 'file':
            cur.execute(' SELECT id FROM blog WHERE file = ? ORDER BY id DESC LIMIT 8 OFFSET ?',(self.key,self.page,))
        elif self.method == 'tag':
            cur.execute('SELECT blog from tag where tag = ? LIMIT 8 OFFSET ?',(self.key,self.page,))
        else:
            cur.execute(' SELECT id FROM blog ORDER BY id DESC LIMIT 8 OFFSET ?',(self.page,))
        altemp = cur.fetchall()
        altemp = list(map(lambda x: int(x[0]),altemp))
        altemp.sort(reverse = True)
        self.al = altemp
        return self.al

#插入图片
def abstr(text,img=""):
    text = text[:1200]
    text = text.replace(u'&nbsp;',u' ')
    text = text.replace(u'</p',u'\n<')
    text = text.replace(u'</b',u'\n<')
    text = text.replace(u'</h',u'\n<')
    text = text.replace(u'<br>',u'\n')
    def fn(x, y):
        if x[-1] == "<" and y != ">":
            return x
        else:
            return x+y
    text = reduce(fn,text)
    text = text.replace(u'<>',u'')
    text = text.replace(u'\n\n\n',u'\n')
    text = text.replace(u'\n\n',u'\n')
    text = text[:120]+'...'+img
    return text

def exper1():
    cur=get_db().cursor()
    cur.execute('''SELECT TAG, COUNT(*) FROM TAG GROUP BY TAG ORDER BY ID DESC;''')
    print(cur.fetchall())

def inita():
    #`date`        timestamp DEFAULT CURRENT_TIMESTAMP(0), 
    cur=get_db().cursor()
    cur.execute("""CREATE TABLE `blog`
        (
        ID          INTEGER    PRIMARY KEY AUTOINCREMENT,
        title       TEXT,
        content     TEXT      NOT NULL,
        abstract    TEXT      NOT NULL,
        date        TIMESTAMP DEFAULT 'CURRENT_TIMESTAMP(0)',
        tag         TEXT,
        file        INT
        )""")
    cur.execute("""CREATE TABLE `tag`
        (
        ID         INTEGER    PRIMARY KEY AUTOINCREMENT,
        tag        TEXT,
        blog       INT
        )""")
    cur.execute("""CREATE TABLE `comm`
        (
        ID          INTEGER   PRIMARY KEY AUTOINCREMENT,
        author      TEXT,
        content     TEXT      NOT NULL,
        blog        INT       NOT NULL,
        date        TIMESTAMP DEFAULT 'CURRENT_TIMESTAMP(0)',
        reply       smallint
        )""")
    get_db().commit()

