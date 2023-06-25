from flask import Flask,render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
db=SQLAlchemy()
app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///TODO.db'
db.init_app(app)
class manoj(db.Model):
    sno=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String,nullable=True)
    desc=db.Column(db.String(200),nullable=True)
    date_created=db.Column(db.DateTime,default=datetime.utcnow)\

    def __repr__(self):
        return f'{self.title}-{self.desc}'
with app.app_context():
    db.create_all()

def about1():
    return render_template('about.html')
    

@app.route('/',methods=['GET','POST'])
def hi():
    if request.method=='POST':
        # title=request.form['title']
        # desc=request.form['desc']
        title=request.form['title']
        desc=request.form['desc']
        todo=manoj(title=title,desc=desc)
        db.session.add(todo)
        db.session.commit()
    alltodo=manoj.query.all()
    return render_template('index.html',alltodo=alltodo)
@app.route('/update/<int:sno>',methods=['GET',"POST"])
def update(sno):
    if request.method=='POST':
        title=request.form['title']
        desc=request.form['desc']   
        todo=manoj.query.filter_by(sno=sno).first()
        
        todo.title=title
        todo.desc=desc

        db.session.add(todo)
        db.session.commit()
        return redirect('/')
    todo=manoj.query.filter_by(sno=sno).first()
    return render_template('update.html',todo=todo)
@app.route('/delete/<int:sno>')
def delete(sno):
    todo=manoj.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect('/')

@app.route('/about')
def about():
    return render_template('about.html')

        
        
    
if __name__=='__main__':
    app.run(debug=True,port=8000, host="0.0.0.0")
    