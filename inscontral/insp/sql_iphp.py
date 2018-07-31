import pymysql
import json


class sqlcont:
    def __init__(self, contuser, contpwd, database):
        self.contuser = contuser
        self.contpwd = contpwd
        self.database = database
        #self.shopid = 0
        self.conn = pymysql.connect('127.0.0.1', user=self.contuser, password=self.contpwd, database=self.database,
                                    charset='utf8mb4')
        self.cursor = self.conn.cursor(cursor=pymysql.cursors.DictCursor)

    def sqlinsert(self, data, shopname):
        print(shopname)
        shopdata = self.shopget('', shopname)
        print(shopdata)
        if shopdata['count'] == 0:
            self.conn.close()
            print('Cannot find this shop!')
            return 'Cannot find this shop!'
        # SQL 插入语句
        #self.data['data']['user']['edge_followed_by']['page_info']['end_cursor']


        for i in data['data']['user']['edge_followed_by']['edges']:

            counttmp = 1;
            sql = "SELECT * FROM follower \
                   WHERE userid = '%s'" % (i['node']['id'])
            try:
                # 执行SQL语句
                self.cursor.execute(sql)
                # 获取所有记录列表
                counttmp = self.cursor.rowcount
                #print(counttmp)
            except:
                print("Error: unable to fetch data")

            if counttmp > 0:
                print('Have User!')
            else:
                print(i)
                username = i['node']['username']
                userid = i['node']['id']
                is_verified = i['node']['is_verified']
                followed_by_viewer = i['node']['followed_by_viewer']
                requested_by_viewer = i['node']['requested_by_viewer']
                sql = "INSERT INTO follower(username, userid, is_verified, followed_by_viewer, requested_by_viewer, shopname) VALUES ('%s', '%s', '%s', '%s', '%s', '%s')" % (username, userid, is_verified, followed_by_viewer, requested_by_viewer, shopname)
                print(sql)
                try:
                    # 执行sql语句
                    self.cursor.execute(sql)
                    # 提交到数据库执行
                    test2 = self.conn.commit()
                    print(test2)
                except:
                    # 如果发生错误则回滚
                    self.conn.rollback()

        if data['data']['user']['edge_followed_by']['page_info']['has_next_page']:
            self.pagecursor(data['data']['user']['edge_followed_by']['page_info']['end_cursor'], shopname)


        #print(values)
        #cursor.close()
        #self.conn.close()

    def pagecursor(self, cursor, shopname):
        sql = "UPDATE shoplist SET end_cursor='%s' WHERE shopname='%s'" % (cursor, shopname)
        print(sql)
        try:
            # 执行sql语句
            self.cursor.execute(sql)
            # 提交到数据库执行
            test2 = self.conn.commit()
            print(test2)
        except:
            # 如果发生错误则回滚
            self.conn.rollback()



    def shopget(self, methode, shopname):
        #conn = pymysql.connect('localhost', user=self.contuser, password=self.contpwd, database=self.database)
        #cursor = conn.cursor()
        shopcountre = {}
        sql = "SELECT * FROM shoplist WHERE shopname = '%s'" % (shopname)
        print(sql)
        try:
            # 执行SQL语句
            self.cursor.execute(sql)

            if methode == 'getdata':
                shopcountre['count'] = 1
                shopcountre['data'] = self.cursor.fetchone()
                #print(shopcountre['data'])
            else:
                shopcountre['count'] = self.cursor.rowcount
                shopcountre['data'] = self.cursor.fetchone()
                #print(shopcountre)
            # 获取所有记录列表
        except:
            print("Error: unable to fetch data")


        #conn.close()

        return shopcountre

    def shopinsert(self, data):
        #conn = pymysql.connect('localhost', user=self.contuser, password=self.contpwd, database=self.database)
        #cursor = conn.cursor()
        shopdetil = ''

        sql = "INSERT INTO shoplist(shopid, shopname, flonum, end_cursor) VALUES ('%s', '%s', '%s', '%s')" % (
        data['shopid'], data['shopname'], data['flonum'], data['cursor'])
        try:
            # 执行SQL语句
            self.cursor.execute(sql)
            # 获取所有记录列表
            self.conn.commit()
        except:
            self.conn.rollback()

        #conn.close()

    #def save_cookies_sql(self,  cookies):

    def getemail(self):
        gr = {}
        gr['is_ok'] = 0
        sql = "SELECT * FROM email WHERE username = ''"
        try:
            # 执行SQL语句

            self.cursor.execute(sql)
            gr['content'] = self.cursor.fetchone()
            gr['is_ok'] = 1
        except:
            #gr['is_ok'] = 0
            print("Error: unable to fetch data")
        return gr

    def newusername(self):
        gr = {}
        gr['is_ok'] = 0
        sql = "SELECT id FROM user WHERE username LIKE 'urhkpost10%' ORDER BY id DESC"
        try:
            # 执行SQL语句
            self.cursor.execute(sql)
            grtmp = int(self.cursor.fetchone()['id']) + 10001
            gr['content'] =  "urhkpost"+str(grtmp)
            gr['is_ok'] = 1

        except:
            # gr['is_ok'] = 0
            print("Error: unable to fetch data")
        return gr

    def insertuser(self, username, pwd):

        sql = "INSERT INTO user(username, pwd) VALUES ('%s', '%s')" % (username, pwd)
        try:
            # 执行SQL语句
            self.cursor.execute(sql)
            # 获取所有记录列表
            self.conn.commit()
        except:
            print("Error!insertuser1!")
            self.conn.rollback()

    def updatauser(self, username, dataname, data):
        sql = "UPDATE user SET %s='%s' WHERE username='%s'" % (dataname, data, username)
        print(sql)
        try:
            # 执行SQL语句
            self.cursor.execute(sql)
            # 获取所有记录列表
            self.conn.commit()
        except:
            print("Error!updatauser!")
            self.conn.rollback()

    def updatauser_byid(self, userid, dataname, data):
        sql = "UPDATE user SET %s='%s' WHERE id='%s'" % (dataname, data, userid)
        print(sql)
        retmp = False
        try:
            # 执行SQL语句
            self.cursor.execute(sql)
            # 获取所有记录列表
            self.conn.commit()
            retmp = True
        except:
            print("Error!updatauser_byid!")
            self.conn.rollback()
            retmp = False
        return retmp

    def getdatauser(self):
        gr = {}
        gr.state = False
        sql = "SELECT * FROM user WHERE creatstep>0 AND creatstep<10 "
        try:
            # 执行SQL语句
            self.cursor.execute(sql)
            grtmp = self.cursor.fetchone()
            if grtmp == None:
                gr['state'] = False
            else:
                gr['content'] = grtmp
                gr['state'] = True
        except:
            # gr['is_ok'] = 0
            print("Error: unable to fetch data")
        return gr

    def getdatauser_byname(self, username):
        gr = {}
        gr['state'] = False
        sql = "SELECT * FROM user WHERE username='%s' " % username
        try:
            # 执行SQL语句
            self.cursor.execute(sql)
            grtmp = self.cursor.fetchone()
            if grtmp == None:
                gr['state'] = False
            else:
                gr['content'] = grtmp
                gr['state'] = True
        except:
            # gr['is_ok'] = 0
            print("Error: unable to fetch data")
        return gr

    def getdatauser_name(self):
        gr = {}
        sql = "SELECT username FROM user WHERE creatstep>=10"

        self.cursor.execute(sql)
        grtmp = self.cursor.fetchall()

        return grtmp

    def searchdata(self, dataname, data):
        sql = "SELECT username FROM user WHERE %s=%s" % (dataname, data)

        self.cursor.execute(sql)
        grtmp = self.cursor.fetchall()

        return grtmp

    def getdatauser_all(self, search, sort, order, offset, limit):
        if search:
            search = "AND username LIKE '%s%s'" % (search,'%')
        else:
            search = ''

        if sort:
            sort = sort
        else:
            sort = 'id'

        sql = "SELECT id,username,lastsrc,pwd,phonenum,profile,uploadset,followset FROM user WHERE creatstep>=10 %s ORDER BY %s %s LIMIT %s,%s  " % (search, sort, order, offset, limit)
        self.cursor.execute(sql)
        grtmp = self.cursor.fetchall()

        return grtmp

    def getdatauser_all_count(self, search, sort, order, offset, limit):
        if search:
            search = "AND username LIKE '%s%s'" % (search,'%')
        else:
            search = ''

        if sort:
            sort = sort
        else:
            sort = 'id'

        sql = "SELECT COUNT(*) AS total FROM user WHERE creatstep>=10 %s ORDER BY %s %s LIMIT %s,%s  " % (search, sort, order, offset, limit)
        self.cursor.execute(sql)
        grtmp = self.cursor.fetchone()

        return grtmp


    def get_user_eamil(self):
        gr = {}
        gr['is_ok'] = 0
        sql = "SELECT user.username,email.email,user.pwd,email.password  FROM user LEFT JOIN email  ON user.username=email.username WHERE user.emailverify='0' ORDER BY user.id ASC"
        try:
            # 执行SQL语句
            self.cursor.execute(sql)
            grtmp = self.cursor.fetchone()
            gr['content'] = grtmp
            gr['is_ok'] = 1

        except:
            # gr['is_ok'] = 0
            print("Error: unable to fetch data")
        return gr

    def get_cookie(self,username):
        gr = {}
        gr['is_ok'] = 0
        sql = "SELECT cookielogin  FROM user  WHERE username='%s'" % (username)
        print(sql)
        try:
            # 执行SQL语句
            self.cursor.execute(sql)
            grtmp = self.cursor.fetchone()['cookielogin']
            #print(grtmp)
            gr['content'] = grtmp
            gr['is_ok'] = 1

        except:
            # gr['is_ok'] = 0
            print("Error: unable to fetch data")
        return gr

    def save_cookie(self, username, cookie):
        gr = False
        sql = "UPDATE user SET cookielogin='%s' WHERE username='%s'" % (cookie,username)
        print(sql)
        try:
            # 执行SQL语句
            self.cursor.execute(sql)
            # 获取所有记录列表
            self.conn.commit()
            gr = True
        except:
            print("Error!insertuser2!")
            self.conn.rollback()
        return gr

    def close(self):
        self.conn.close()

