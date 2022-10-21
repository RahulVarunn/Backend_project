
from urllib import response
from flask import Flask
from flask_restful import Resource, Api, reqparse
from flask import jsonify 
import psycopg2 
import psycopg2.extras



app = Flask(__name__)
api = Api(app)


# class media(Resource):
#     def get(self):
#         conn = psycopg2.connect(database="Project_social", host="localhost",user = "postgres", password = "root", port = "5432")

#         cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

#         fetch_all_as_dict = lambda cursor: [dict(row) for row in cursor]
#         cur.execute("""select * from  project_media""")
#         return (fetch_all_as_dict(cur))
#         # response = jsonify({"data":details})
  
# api.add_resource(media,'/details')

class upload(Resource):
    def get(self):
        conn = psycopg2.connect(database="Project_social", host="localhost",user = "postgres", password = "root", port = "5432")

        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        fetch_all_as_dict = lambda cursor: [dict(row) for row in cursor]
        cur.execute("select * from uploads")
        return (fetch_all_as_dict(cur))
        # response = jsonify({"data":details})
  




class insert_upload(Resource):
    def post(self):
        parser=reqparse.RequestParser()
        parser.add_argument('upload_id', required=True)
        parser.add_argument('user_id', required=True)
        parser.add_argument('filename', required=True)
        parser.add_argument('upload_date', required=True)
        parser.add_argument('captions', required=True)
        parser.add_argument('tags', required=True)
        args=parser.parse_args()
        conn = psycopg2.connect(database="Project_social", host="localhost",user = "postgres", password = "root", port = "5432")
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute("insert into uploads (upload_id,user_id, filename,,upload_date,captions,tags) values('{}','{}','{}','{}','{}','{}')".format(args['upload_id'], args['user_id'],args['filename'], args['upload_date'], args['captions'], args['tags']))
        conn.commit()
        return {'message':"inserted"}


class update_file(Resource):
    def post(self):
        parser=reqparse.RequestParser()
        parser.add_argument('upload_id', required=True)
        args=parser.parse_args()
        conn = psycopg2.connect(database="Project_social", host="localhost",user = "postgres", password = "root", port = "5432")
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute("update uploads set where upload_id={}".format(args['upload_id'])
        conn.commit()
        return {'message':"done"}


class delete_file(Resource):
    def post(self):
        parser=reqparse.RequestParser()
        parser.add_argument('upload_id', required=True)
        args=parser.parse_args()
        conn = psycopg2.connect(database="Project_social", host="localhost",user = "postgres", password = "root", port = "5432")
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute("delete from uploads where upload_id={}".format(args['upload_id'])
        conn.commit()
        return {'message':"done"}




api.add_resource(upload,'/upload')
api.add_resource(insert_upload,'/insertfile')
api.add_resource(update_file,'/uploadfile')
api.add_resource(delete_file,'/deletefile')

if __name__=='__main__':
    app.run(debug=True,port=5000,host='localhost')