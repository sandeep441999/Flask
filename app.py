from flask import Flask,request,render_template,url_for,redirect,flash
from flask_sqlalchemy import SQLAlchemy

app=Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI']='postgres://skqhxjbvovcuth:80a59a4db046be90beb378f00ecdcb504c6a7c1b13d8c135a91d9657e58046e2@ec2-54-167-152-185.compute-1.amazonaws.com:5432/d3mquckdv85u3i'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

db=SQLAlchemy(app)

class todos(db.Model):
    id=db.Column("todo_id",db.Integer,primary_key=True)
    title=db.Column(db.String(100))
    complete=db.Column(db.Boolean)
    
    def __init__(self,title,complete=False):
        self.title=title
        self.complete=complete
    
@app.route('/')
def index():
    tasks=todos.query.all()
    return render_template('todohome1.html',tasks=tasks)
    
@app.route('/add',methods=["POST"])
def addtask():
    if len(request.form['title'])==0:
        msg="Please fill the Title"
        return render_template('todohome1.html',msg=msg)
    todo=todos(title=request.form['title'],complete=False)
    db.session.add(todo)
    db.session.commit()
    
    return redirect(url_for('index'))

@app.route('/update/<int:id>')
def update(id):
    todo=todos.query.filter_by(id=id).first()
    todo.complete= not todo.complete
    db.session.commit()
    
    return redirect(url_for('index'))
    
@app.route('/delete/<int:id>')
def delete(id):
    todo=todos.query.filter_by(id=id).first()
    db.session.delete(todo)
    db.session.commit()
    
    return redirect(url_for('index'))
    
if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
    
