from elasticsearch import Elasticsearch
import datetime


class elasticSearch():
    #  index_type 储存的是什么类型：server & mqtt   index_name 储存那个空间
    def __init__(self, index_type: str, index_name: str, ip="127.0.0.1"):

        # self.es = Elasticsearch([ip], http_auth=('elastic', 'password'), port=9200)
        self.es = Elasticsearch("121.40.111.33:39011")  # todo 后续改到配置中心或者当作参数传入
        self.index_type = index_type
        self.index_name = index_name
        if not self.es.indices.exists(index=index_name):
            self.create_index()

    # 创建 index_name 为某某的储存空间
    def create_index(self):
        if self.es.indices.exists(index=self.index_name) is True:
            self.es.indices.delete(index=self.index_name)
        self.es.indices.create(index=self.index_name, ignore=400)

    # 删除 index_name 为某某的储存空间
    def delete_index(self):
        try:
            self.es.indices.delete(index=self.index_name)
        except:
            pass

    def get_doc(self, uid):
        return self.es.get(index=self.index_name, id=uid)

    # 插入一条
    def insert_one(self, doc: dict):
        return self.es.index(index=self.index_name, doc_type=self.index_type, body=doc)

    # 插入多条
    def insert_array(self, docs: list):
        for doc in docs:
            self.es.index(index=self.index_name, doc_type=self.index_type, body=doc)

    # query 查询value为url  page_size一页多少条 page_no为从多少条数据开始
    def search(self, query: str = '', page_size: int = 10, page_no: int = 0):
        dsl = {
            "query": {
                "multi_match": {
                    "query": query,
                    "fields": ["url"]
                }
            },
            "highlight": {
                "fields": {
                    "url": {}
                }
            }
        }
        if query:
            match_data = self.es.search(index=self.index_name, body=dsl, size=page_size, from_=page_no)
        else:
            match_data = self.es.search(index=self.index_name, body='', size=page_size, from_=page_no)
        return match_data

# es = elasticSearch(index_type="server_log", index_name="iot-server")
# es.create_index()
# for i in range(10):
#     vv = 'ceshi' + str(i)
#     data = {
#         'url': vv,
#         'content': "select %s from user_info" % vv,
#         'create_time': datetime.datetime.now()
#     }
#
#     es.insert_one(doc=data)

#  查询
# es = elasticSearch(index_type="server_log", index_name="iot-server")
# es.search('iot-server')
# print('')
