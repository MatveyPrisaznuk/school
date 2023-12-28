from flask import Flask, render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app=Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///school.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy (app)

class School (db.Model):
 _id = db.Column(db.Integer, primary_key=True)
 title = db.Column(db.String(200), nullable=False) 
 desc = db.Column(db.String(500), nullable=False)
 created_at = db.Column(db.DateTime, default = datetime.utcnow)



with app.app_context():
    db.create_all()




@app.route('/', methods=['POST', 'GET'])
def home():
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['describtion']
        todo = School(title=title, desc=desc)
        db.session.add(todo)
        db.session.commit()

    all_todos = School.query.all()
    return render_template('index.html', todos=all_todos)

@app.route('/delete/<int:_id>')
def delete(_id): 
    todo = School.query.filter_by(_id=_id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect('/')




if __name__ == "__main__":
    app.run(debug=True)