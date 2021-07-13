from datetime import datetime
from elasticsearch import Elasticsearch
from bs4 import BeautifulSoup 
import urllib.request as req
from selenium import webdriver
from flask import Flask, json, request, render_template, jsonify
import time
from elasticsearch import helpers


es = Elasticsearch()

def get1():
      b = input("은행명 : ")
      for i in range(1,11):
            res = es.get(index="bank", id=i)
            if res['_source']['bank'] == b:
                  print('지점 : '+res['_source']['branch']+ '\n고객수 : '+str(res['_source']['customers']))

# 은행별 branch 종류 출력
def get2():
      ans = []
      b = input("은행명 : ")
      for i in range(1,11):
            res = es.get(index="bank", id=i)
            if res['_source']['bank'] == b:
                  ans.append(res['_source']['branch'])
      print(len(set(ans)))
                  
def get3():
      res = es.search(index="bank", size=0, body={"aggs": {"b_2": {"cardinality": {"field":"bank.keyword"}}}})
      print(res["aggregations"]["b_2"]["value"])
      

def get4():
      res = es.search(index="bank", size=0, body={"query": {"match": {"bank": "NH농협은행"}},"size": 0, "aggs": {"b_4": {"histogram": {"field": "customers","interval": 1000}}}})
      for i in res['aggregations']['b_4']['buckets']:
            print(i)

def delete():
      d = input('삭제 : ')
      es.indices.delete(index=d, ignore=[400, 404])

def es_stock():
      driver = webdriver.Chrome("C:/driver/chromedriver")
      driver.get('https://kr.investing.com/equities/south-korea')
      time.sleep(3) 
      soup = BeautifulSoup(driver.page_source, "lxml" )
      stocks = soup.select('table#cross_rate_markets_stocks_1>tbody > tr>td')
      # driver.close()
      ss = []
      for i in stocks:
          ss.append(i.text)
      
      companies = []
      for j in range(50):
          companies.append(ss[10*j:10*(j+1)][1])
      
      result = []
      for j in range(50):
          datas = ss[10*j:10*(j+1)][1:-1]
          company = datas[0]
          current = datas[1]
          high = datas[2]
          low = datas[3]
          move = datas[4]
          move_per = datas[5]
          amount = datas[6]
          date = datas[7]
          result.append({"index": {"_id": str(j)}})
          result.append({'company':company, 'current':current,'high':high,'low':low,\
          'move':move,'move_per':move_per,'amount':amount,'date':date})

      res = es.index(index="stocks_50", body=result)
      print(res['result'])

    # print('*'*100)
    # for st in result:
    #     if request.form.get('stock_name') == st['comapny']:
    #         return jsonify(st)

if __name__ == '__main__':
      es_stock()





'''
#국민은행 지점별 customers 출력
GET bank/_search
{
  "query": {
    "match": {
      "bank": "국민은행"
    }
  },
  "size": 10, 
  "aggs": {
    "b_1": {
      "terms": {
        "field": "customers"
      }
    }
  }
}

# branch별 유니크한 자료들 출력
GET bank/_search
{
  "size": 0, 
  "aggs": {
    "b_2": {
      "cardinality": {
        "field": "branch.keyword"
      }
    }
  }
}

# 국민은행 고객들에 대한 집계 자료 출력
GET bank/_search
{
  "query": {
    "match": {
      "bank": "국민은행"
    }
  },
  "size": 0, 
  "aggs": {
    "b_3": {
      "stats": {
        "field": "customers"
      }
    }
  }
}

# 농협은행 고객 수 구간별(1000단위) 검색
GET bank/_search
{
  "query": {
    "match": {
      "bank": "NH농협은행"
    }
  },
  "size": 0, 
  "aggs": {
    "b_4": {
      "histogram": {
        "field": "customers",
        "interval": 1000
      }
    }
  }
}
'''