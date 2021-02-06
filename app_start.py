from sqlalchemy import create_engine

# 거의 핵심 기능들을 import 하는데 밑에서 쓰는 것을 보면 알겠지만 주로 db에 연결하거나 주소 경로 설정할때 많이 쓰인다
from flask import Flask, url_for, render_template, request, redirect, session, jsonify, make_response, abort, g, flash
from flask_sqlalchemy import SQLAlchemy
from pip._vendor.appdirs import user_data_dir
from sqlalchemy import desc

# 우리는 타이머 기능을 사용하기 때문에 필요하기도 하지만 날짜를 계산하기 위해서 필요하다.
from datetime import datetime 
import time

from sqlalchemy.sql.expression import null
from _hashlib import new 
from sqlite3 import dbapi2 as sqlite3
from _dummy_thread import error
from contextlib import closing

from pytz import timezone
import atexit
from Cython.Shadow import address


DATABASE = 'DB.db'  # 내가 설정한 DB 이름

app = Flask(__name__) # app 초기화, 밑에 SQLAlchemy에 들어감
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///DB.db'

#파일 업로드 용량 제한
app.config['MAX_CONTENT_LENGTH'] = 16*1024*1024

db2 = SQLAlchemy(app)
app.config.from_object(__name__)
#
def connect_db():
    """DB 연결 후 Connection객체 반환, DB 없으면 내부적으로 새로 생성됨."""
    return sqlite3.connect(app.config['DATABASE'])

###################################### Class start ###############################################
# User테이블 정의하기 위한 클래스\
# 가장 기본이 되는 table 입니다. 이 table과 밑에 나오는 product table이 주가되는 table입니당
class Unit_factory(db2.Model):
    __tablename__ = 'Unit_factory' # 테이블 이름
    # id(primary_key)가 없으면 오류나던데 왜 그런지 모르겠음.. 시간없어서 조사는 못했다 ㅜ
    # 자료형도 설정해 줘야하고 밑에 __repr__함수와 일치시켜야 함
    Unit_no = db2.Column(db2.Integer) 
    Unit_Date = db2.Column(db2.String, primary_key = True) 
    Model = db2.Column(db2.String)
    Unit_horizon = db2.Column(db2.String)
    Unit_vertical = db2.Column(db2.String)
    Unit_hpass = db2.Column(db2.Integer)
    Unit_vpass = db2.Column(db2.Integer)
    Unit_temp = db2.Column(db2.String)

    def __init__(self, Unit_no, Unit_date, Model, Unit_horizon, Unit_vertical, Unit_hpass, Unit_vpass, Unit_temp):
        self.Unit_no = Unit_no
        self.Unit_date = Unit_date
        self.Model = Model
        self.Unit_horizon = Unit_horizon
        self.Unit_vertical = Unit_vertical
        self.Unit_hpass = Unit_hpass
        self.Unit_vpass = Unit_vpass
        self.Unit_temp = Unit_temp
   
    # 앞으로 User테이블을 사용할때 각 column의 자료형을 정의해 준다. 위에 정의한 것과 일치시키면 됨
    def __repr__(self):
        return"<User('%d', '%s', '%s', '%s', '%d', '%d')>" % (self.Unit_no, self.Unit_date, self.Model,
                                                              self.Unit_horizon, self.Unit_vertical, 
                                                              self.Unit_hpass, self.Unit_vpass, self.Unit_temp)

class Result(db2.Model):
    __tablename__ = 'Result'
    
    ResultDate = db2.Column(db2.String, primary_key = True) # 글쓴 사람의 id index로 회원가입한  user table의 name이 아니라 user table의 id임. 절때 헷갈리지 말것!! 이렇게 해야 db끼리 연결이 됩니다 ㅜㅜ
    Result_dateGap = db2.Column(db2.String)
    Model = db2.Column(db2.String)
    Result_LOT = db2.Column(db2.String)
    hStandard = db2.Column(db2.String) 
    vStandard = db2.Column(db2.String) 
    AQL_hpass = db2.Column(db2.String) 
    AQL_vpass = db2.Column(db2.String) 
    hMean = db2.Column(db2.String) 
    vMean = db2.Column(db2.String)
    hSigma = db2.Column(db2.String)
    vSigma = db2.Column(db2.String)
    hCp = db2.Column(db2.String) 
    vCp = db2.Column(db2.String) 
    hunpassCount = db2.Column(db2.String)
    vunpassCount = db2.Column(db2.String)
    TotalunpassCount = db2.Column(db2.String)
    hDefectrate = db2.Column(db2.String)
    vDefectrate = db2.Column(db2.String)
    TotalDefectrate = db2.Column(db2.String)
    Hadjust = db2.Column(db2.String)
    Vadjust = db2.Column(db2.String)
 
    def __init__(self, ResultDate, Result_dateGap, Model, Result_LOT, 
                 hStandard, vStandard, AQL_hpass, AQL_vpass, 
                 hMean, vMean, hSigma, vSigma, hCp, vCp,
                 hunpassCount, vunpassCount, TotalunpassCount, HDefectrate, vDefectrate, 
                 TotalDefectrate, Hadjust, Vadjust):
        self.ResultDate = ResultDate
        self.Result_dateGap = Result_dateGap
        self.Model = Model
        self.Result_LOT = Result_LOT
        self.hStandard = hStandard
        self.vStandard = vStandard
        self.AQL_hpass = AQL_hpass
        self.AQL_vpass = AQL_vpass
        self.hMean = hMean
        self.vMean = vMean
        self.hSigma = hSigma
        self.vSigma = vSigma
        self.hCp = hCp
        self.vCp = vCp
        self.hunpassCount = hunpassCount
        self.vunpassCount = vunpassCount
        self.TotalunpassCount = TotalunpassCount
        self.hDefectrate = hDefectrate
        self.vDefectrate = vDefectrate
        self.TotalDefectrate = TotalDefectrate
        self.Hadjust = Hadjust
        self.Vadjust = Vadjust
        
   
    def __repr__(self):
        return"<Product('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')>" % (self.ResultDate, self.Result_dateGap,
                                                                                            self.Model, self.Result_LOT, self.hStandard,
                                                                                            self.vStandard, self.AQL_hpass,self.AQL_vpass,self.hCp, self.vCp,
                                                                                            self.hunpassCount,self.vunpassCount, self.TotalunpassCount, 
                                                                                            self.hDefectrate, self.vDefectrate, self.TotalDefectrate,
                                                                                            self.Hadjust, self.Vadjust)


###################################### Class end ###############################################

###################################### Method Tool Start ###############################################
""" 쿼리문을 직접 쓸수 있게 해주는 함수 (minitwit에서 쓰던 방식임) """
def query_db(query, args=(), one=False):
    """Queries the database and returns a list of dictionaries."""
    """ g는 전역객체, fetchall():조회할때 쓰는 메소드"""
    cur = g.db.execute(query, args)
    rv = [dict((cur.description[idx][0], value)
               for idx, value in enumerate(row)) for row in cur.fetchall()]
    return (rv[0] if rv else None) if one else rv

""" g.db 전역객체로 DB에 접근하여 query문 적용하기 위한 Method"""
@app.before_request
def before_request():
    """http 요청이 올 때마다 실행 : db연결하고 전역 객체 g에 저장하고 세션에 userid가 저장되어 있는지 체크해서 user 테이블로부터 user 정보 조회 한 후에 전역 객체 g에 저장 """
    g.db=connect_db()
    
# 여기서 말해두지만 g.db와 db2는 엄연히 다른 방식입니다.. 
# g.db는 minitwit에서 끌어다가 쓴 방식이고
# db2 는 박혜정쌤이 게시판 만들때 쓰던 방식입니다 개인적으로 db2 방식이 더 쉬워서 많이썼어요 ㅎㅎ 이 위에있는 두 query_db, before_request 함수는 minitwit에서 쓰는 방식을 가져온 것입니다.

###################################### Method Tool End ###############################################



###################################### Route Method ###############################################
"""
밑에 뷰 함수들을 설명하기 전에 앞서 GET 방식과 POST 방식의 차이에 대해서 알아야 합니다.
GET : HTML 에서 정보를  "받아옴". 정보를 보낼수는 있으나 정보들이 도메인에 노출되고(정보의노출) 보내는 정보량에도 제한이 있어서 좋지 않다.
POST " HTML 에서 정보를 받아오고(이는 GET방식이 default기 때문) 다시 HTML에 정보를 보내고 싶을 때 써줍니다. 정보들이 숨겨져서 보내지고 정보량 제한도 없어서 정보를 보낼때 쓰임!
"""



'''메인페이지 '''
# @app.route()는 무엇이냐? 아하! 예얍~ 사이트의 경로랑 연결지어주는 역할을 합니다. "/" 라고 되어있으므로 "http://(사이트도메인)/" 의 경로에 접속하게 되면 실행되게 경로설정을 해주는 것이지요.
# 저의경우는 http://192.168.25.50:5000/ 에 접속하면 실행되네요 이때 get, post 두가지 방식으로 정보를 받아오는데 아무것도 쓰지 않으면 default(기본값)으로 get 방식을 쓰게 됩니다.
# 아무것도 쓰지 않았기 때문에 지금은 get 방식이겠지요?
# 정리를 하면, http://(사이트도메인)/"의 경로에 사용자가 접속하면 뷰 함수를 호출하는데 method를 표시하지 않았으므로 get 방식으로 이 함수를 호출합니다.
@app.route("/",methods=['GET', 'POST'])
def Dashboard():
    '''factory_data = Unit_factory.query.filter_by(Unit_date='20201113').order_by(Unit_no.desc()).limit(1)'''
    '''result_data = Result.query.filter_by(Model='삼성sdi').first()
    hCp_data = float(result_data.hCp)
    vCp_data = float(result_data.vCp)
    return render_template('Dashboard.html',result_data = result_data,hCp_data = hCp_data, vCp_data = vCp_data)
    '''
    all_data = Result.query.filter().all()
    bnf_list=[]
    for data in all_data:
        bnf_list.append(data.ResultDate)
        bnf_list = list(map(int, bnf_list))
        
    max_val = max(bnf_list)
    resent_data = Result.query.filter_by(ResultDate=max_val).first()   
    hCp_data = float(resent_data.hCp)
    vCp_data = float(resent_data.vCp) 
    
    return render_template('Dashboard.html',resent_data = resent_data,hCp_data = hCp_data, vCp_data = vCp_data)

#################################################################################################################################   
@app.route('/Monitoring')
def Monitoring():
   return render_template('Monitoring.html')
@app.route('/Statistics')
def Statistics():
   return render_template('Statistics.html')
@app.route('/UserInputData')
def UserInputData():
   return render_template('UserInputData.html')

# 메인함수
if __name__ == '__main__':
    app.debug=True # Debug 활성화
#     db2.create_all() #테이블이 생성되고 나서는 주석처리해줌
    app.secret_key = '1234567890'
    app.run(host='192.168.0.134') #본인의 ip로 접속할 수 있게 해줍니다.
