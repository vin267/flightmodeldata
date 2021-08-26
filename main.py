'''from flask import Flask,request
from flask_sqlalchemy import SQLAlchemy # new
from flask_marshmallow import Marshmallow # new
from flask_restful import Api, Resource # new

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db' # new
db = SQLAlchemy(app) # new
ma = Marshmallow(app) # new
api = Api(app) # new

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    content = db.Column(db.String(255))

    def __repr__(self):
        return '<Post %s>' % self.title

class PostSchema(ma.Schema):
    class Meta:
        fields = ("id", "title", "content")
        model = Post

class PostListResource(Resource):
    def get(self):
        posts = Post.query.all()
        return posts_schema.dump(posts)

    def post(self):
        new_post = Post(
            title=request.json['title'],
            content=request.json['content']
        )
        db.session.add(new_post)
        db.session.commit()
        return post_schema.dump(new_post)

api.add_resource(PostListResource, '/posts')

post_schema = PostSchema()
posts_schema = PostSchema(many=True)

class PostResource(Resource):
    def get(self, post_id):
        post = Post.query.get_or_404(post_id)
        return post_schema.dump(post)

    def patch(self, post_id):
        post = Post.query.get_or_404(post_id)

        if 'title' in request.json:
            post.title = request.json['title']
        if 'content' in request.json:
            post.content = request.json['content']

        db.session.commit()
        return post_schema.dump(post)

    def delete(self, post_id):
        post = Post.query.get_or_404(post_id)
        db.session.delete(post)
        db.session.commit()
        return '', 204

api.add_resource(PostResource, '/posts/<int:post_id>')

if __name__ == '__main__':
    app.run(debug=True)'''

'''import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker, relationship, backref

engine = sa.create_engine("sqlite:///:memory:")
session = scoped_session(sessionmaker(bind=engine))
Base = declarative_base()


class Author(Base):
    __tablename__ = "authors"
    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String, nullable=False)

    def __repr__(self):
        return "<Author(name={self.name!r})>".format(self=self)


class Book(Base):
    __tablename__ = "books"
    id = sa.Column(sa.Integer, primary_key=True)
    title = sa.Column(sa.String)
    author_id = sa.Column(sa.Integer, sa.ForeignKey("authors.id"))
    author = relationship("Author", backref=backref("books"))


Base.metadata.create_all(engine)'''


'''final_ls = [('a01', 100, '1-1-1', 'f01'), ('a02', 200, '2-2-2', 'f02')]
name = ['seatnumber','cost','date','flightnumber']
x= []
for i in final_ls:
    x.append(list(zip(name,i)))
print(x)
z = []
for i in x:
    y=(dict(i))
    z.append(y)
print(z)'''

'''final_ls = [('F01', 'a01'), ('F02', 'a01')]
name_ls = ['flightNumber','occupiedSeats']
x= []
for i in final_ls:
    x.append(list(zip(name_ls,i)))
print(x)
z = []
for i in x:
    y=(dict(i))
    z.append(y)
print(z)'''

'''d = {}

flightticket
pk, flight, ticket
1, 1, 1
2, 1, 2

a = [1,2,3,1,1,2]
for x in range(len(a)):
    if a[x] in d:
        print(i, d[a[x]])
    else:
        d[a[x]] = a[x]
print(d)'''

'''d = {}
f01 -> a02(100)   d["f01"] = 100
f01 -> a01(200)   if x.flight.flhtnumber in dic: dic[]
f02 -> a09(900)

{1: 3, 2:4, 3:1}
d = {}
d["f01"] = 100, ["seatnumber"]
d["f02"] = 10

d["f01"] = value that exist in dictionary for f01 (100) + x.ticket.cost'''


#print (dict([('Sachin', 10), ('MSD', 7), ('Kohli', 18), ('Rohit', 45)]))
#xx = [('Sachin', 10), ('MSD', 7), ('Kohli', 18), ('Rohit', 45)]
#yy = [('seatnumber', 'a01'), ('cost', 100), ('date', '1-1-1'), ('flightnumber', 'f01')]
#print(dict(yy))

'''dic = {'F01': [561], 'F02': [111]}
ls1 = ['a1','a2']
ls2 = ['b1','b2']
for i in dic:
    dic[i].append(ls1)
print(dic)'''

'''d = {'F01': 'a03a02a01', 'F02': 'a01'}
for key,value in d.items():
    print(value)'''

#dic["F01"].append(ls1)
#dic['F02'].append(ls2)


'''from iteration_utilities import deepflatten
ls1 = ['a1','a2']
ls2 = ['b1','b2']
d1 = {'F01': [250, [200, [111]]], 'F02': [111]}
for i in d1:
    values = (d1[i])
    flatten_list = list(deepflatten(values))
    d1[i]=sum(flatten_list)
print(d1)'''

'''flight = ['F01', 'F02', 'F01', 'F01']
seat = ['a01', 'a01', 'a02', 'a03']
print(dict(zip(flight,seat)))'''

'''x = ['F01', 'a01', 'F02', 'a01', 'F01', 'a02', 'F01', 'a03']
key = (x[0::2])
value = (x[1::2])
print(key)
print(value)'''

dic = {'F01': 'a03a02a01c05', 'F02': 'a01d02'}
n = 3
for i,j in dic.items():
    print([j[i:i+n] for i in range(0, len(j), n)])

'''x = 'a01a02a03b01'
print(type(x))
n = 3
print([x[i:i+n] for i in range(0, len(x), n)])
print((x.split()))'''








