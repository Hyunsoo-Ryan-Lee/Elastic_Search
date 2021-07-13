from datetime import datetime
from elasticsearch import Elasticsearch

# es 사용 가능한 python 객체 생성
# 이 소스가 실행중인 시스템에서 실행되는 es에 자동 접속
es = Elasticsearch()

def put():
    # doc 라는 변수에 3개의 field 선언해서 값 설정
    # python 자체적으로는 dict 타입. es 관점에서는 field와 value
    doc = {
        'author': 'YEIN',
        'text': 'Elasticsearch YEAH!!',
        'timestamp': datetime.now(),
    }

    # es.index(index="test-index", id=1, body=doc)
    # 객체.index생성(index명, id값, 저장될 data 설정)
    # *doc : dict 구조의 변수값으로 index에 새로운 data 생성. 이미 존재할 경우 update
    ''' 아래 ES 코드와 동일
            PUT test-index/_doc/1
        {
        "author": "LEE",
        "text": "hahahahaha",
        "time": "2021-07-13"
        } 
    '''
    res = es.index(index="test-index", id=2, body=doc)
    print(res['result']) # 새로 생성된거면 created, 수정된거면 updated 출력


def get():
    res = es.get(index="test-index", id=1)
    print(res['_source']) # source에 대한 값 출력

def match_all():
        #     GET test-index/_search
        # {
        # "query": {
        #     "match_all": {}
        # }
        # }
    res = es.search(index="test-index", body={"query": {"match_all": {}}})

    print("Got %d Hits:" %res['hits']['total']['value'])
    for hit in res['hits']['hits']:
        print("%(timestamp)s %(author)s: %(text)s" % hit["_source"])

if __name__ == '__main__':
    put()
    match_all()