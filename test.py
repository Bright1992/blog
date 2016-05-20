#!/opt/Apps/local/Python/anaconda/bin/python2.7
import os,unittest
from flaskr.models import User,Post,Comment,Like
from config import basedir
from flaskr import app,db
from flaskr.appviews import uniqueMail
from datetime import datetime,timedelta
class TestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING']=True
        app.config['WTF-CSRF_DATABASE_URI']=False
        app.config['SQLALCHEMY_DATABASE_RUI']='sqlite:///'+os.path.join(basedir,'test.db')
        self.app=app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
    #
    # def test_avater(self):
    #     u=User(nickname='john',email='john@example.com')
    #     avatar=u.avatar(128)
    #
    def test_make_unique_email(self):
        u=User(nickname='john',email='john@exampled.com')
        db.session.add(u)
        db.session.commit()
        boolemail=uniqueMail('john@exampled.com')
        assert not boolemail
        u1=User(nickname='susan',email='john@example.com')
        db.session.add(u1)
        db.session.commit()
        boolemail2=uniqueMail('john@exampled.com')
        assert not boolemail2
        assert boolemail ==boolemail2

    def test_follow(self):
        u1 = User(nickname = 'john', email = 'john@example.com')
        u2 = User(nickname = 'susan', email = 'susan@example.com')
        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()
        assert u1.unfollow(u2) == None
        u = u1.follow(u2)
        db.session.add(u)
        db.session.commit()
        assert u1.follow(u2) == None
        assert u1.is_following(u2)
        assert u1.followed.count() == 1
        assert u1.followed.first().nickname == 'susan'
        assert u2.followers.count() == 1
        assert u2.followers.first().nickname == 'john'
        u = u1.unfollow(u2)
        assert u != None
        db.session.add(u)
        db.session.commit()
        assert u1.is_following(u2) == False
        assert u1.followed.count() == 0
        assert u2.followers.count() == 0

    # def test_follow_posts(self):
    #     u1 = User(nickname = 'john', email = 'john@example.com',password='wei')
    #     u2 = User(nickname = 'susan', email = 'susan@example.com',password='wei')
    #     u3 = User(nickname = 'mary', email = 'mary@example.com',password='wei')
    #     u4 = User(nickname = 'david', email = 'david@example.com',password='wei')
    #     db.session.add(u1)
    #     db.session.add(u2)
    #     db.session.add(u3)
    #     db.session.add(u4)
    #     # make four posts
    #     utcnow = datetime.utcnow()
    #     p1 = Post(body = "post from john", author = u1, timestamp = utcnow + timedelta(seconds = 1))
    #     p2 = Post(body = "post from susan", author = u2, timestamp = utcnow + timedelta(seconds = 2))
    #     p3 = Post(body = "post from mary", author = u3, timestamp = utcnow + timedelta(seconds = 3))
    #     p4 = Post(body = "post from david", author = u4, timestamp = utcnow + timedelta(seconds = 4))
    #     db.session.add(p1)
    #     db.session.add(p2)
    #     db.session.add(p3)
    #     db.session.add(p4)
    #     db.session.commit()
    #     # setup the followers
    #     u1.follow(u1) # john follows himself
    #     u1.follow(u2) # john follows susan
    #     u1.follow(u4) # john follows david
    #     u2.follow(u2) # susan follows herself
    #     u2.follow(u3) # susan follows mary
    #     u3.follow(u3) # mary follows herself
    #     u3.follow(u4) # mary follows david
    #     u4.follow(u4) # david follows himself
    #     db.session.add(u1)
    #     db.session.add(u2)
    #     db.session.add(u3)
    #     db.session.add(u4)
    #     db.session.commit()
    #     # check the followed posts of each user
    #     f1 = u1.followed_posts().all()
    #     f2 = u2.followed_posts().all()
    #     f3 = u3.followed_posts().all()
    #     f4 = u4.followed_posts().all()
    #     assert len(f1) == 3
    #     assert len(f2) == 2
    #     assert len(f3) == 2
    #     assert len(f4) == 1
    #     assert f1 == [p4, p2, p1]
    #     assert f2 == [p3, p2]
    #     assert f3 == [p4, p3]
    #     assert f4 == [p4]
    def test_reject_posts(self):
        u1 = User(nickname = 'john', email = 'john@example.com',password='wei')
        u2 = User(nickname = 'susan', email = 'susan@example.com',password='wei')
        u3 = User(nickname = 'mary', email = 'mary@example.com',password='wei')
        u4 = User(nickname = 'david', email = 'david@example.com',password='wei')
        db.session.add(u1)
        db.session.add(u2)
        db.session.add(u3)
        db.session.add(u4)
        # make four posts
        utcnow = datetime.utcnow()
        p1 = Post(body = "post from john", author = u1, timestamp = utcnow + timedelta(seconds = 1),title='heheda')
        p2 = Post(body = "post from susan", author = u2, timestamp = utcnow + timedelta(seconds = 2))
        p3 = Post(body = "post from mary", author = u3, timestamp = utcnow + timedelta(seconds = 3))
        p4 = Post(body = "post from david", author = u4, timestamp =utcnow + timedelta(seconds = 4))
        c1=Comment(body="it's amazing!!!",byuser=u2,topost=p1,timestamp=utcnow + timedelta(seconds = 5))
        pc=p1.comments.all()
        L1 = Like(is_like=True, topost=p1, byuser=u2)
        L2 = Like(is_like=True, topost=p1, byuser=u1)
        db.session.add(L1)
        db.session.add(L2)
        db.session.commit()
        print p1.likes.count()
        lp1=p1.likes.all()
        print lp1[0].byuser.nickname
        print lp1[1].byuser.nickname
        print pc
        print pc[0].body
        u2c=u2.comments.all()
        print u2c
        print u2c[0].body
        print c1.byuser.nickname
        print c1.topost.title
        db.session.add(p1)
        db.session.add(p2)
        db.session.add(p3)
        db.session.add(p4)
        db.session.add(c1)
        db.session.commit()
        # setup the followers
        u1.follow(u1) # john follows himself
        u1.follow(u2) # john follows susan
        u1.follow(u4) # john follows david
        u2.follow(u2) # susan follows herself
        u2.follow(u3) # susan follows mary
        u3.follow(u3) # mary follows herself
        u3.follow(u4) # mary follows david
        u4.follow(u4) # david follows himself
        db.session.add(u1)
        db.session.add(u2)
        db.session.add(u3)
        db.session.add(u4)
        db.session.commit()
        u1.reject(u2)
        u1.reject(u4)
        db.session.add(u1)
        db.session.commit()
        # check the followed posts of each user
        f1 = u1.followed_posts()
        f2 = u2.followed_posts()
        f3 = u3.followed_posts()
        f4 = u4.followed_posts()
        assert len(f1) == 1
        assert len(f2) == 2
        assert len(f3) == 2
        assert len(f4) == 1
        assert f1 == [p1]
        assert f2 == [p3, p2]
        assert f3 == [p4, p3]
        assert f4 == [p4]



if __name__=='__main__':
    unittest.main()