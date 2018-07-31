import pymysql


class sqlcont():
    def __init__(self, contuser, contpwd, database):
        self.contuser = contuser
        self.contpwd = contpwd
        self.database = database
        self.shopid = 0
        self.conn = pymysql.connect('localhost', user=self.contuser, password=self.contpwd, database=self.database)
        self.cursor = self.conn.cursor(cursor=pymysql.cursors.DictCursor)

    def sqlinsert(self, data):

        shopdata = self.shopget('')
        print(shopdata['data']['shopid'])
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
                sql = "INSERT INTO follower(username, userid, is_verified, followed_by_viewer, requested_by_viewer, shopid) VALUES ('%s', '%s', '%s', '%s', '%s', '%s')" % (username, userid, is_verified, followed_by_viewer, requested_by_viewer, shopdata['data']['shopid'])
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



        #print(values)
        #cursor.close()
        self.conn.close()



    def shopget(self, methode):
        #conn = pymysql.connect('localhost', user=self.contuser, password=self.contpwd, database=self.database)
        #cursor = conn.cursor()
        shopcountre = {}
        sql = "SELECT * FROM shoplist WHERE shopid = '%d'" % (self.shopid)
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

        sql = "INSERT INTO shoplist(shopid, shopname, flonum, cursor) VALUES ('%s', '%s', '%s', '%s')" % (
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


    def close(self):
        self.conn.close()
