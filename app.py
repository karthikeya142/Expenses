import os.path

from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy



project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "mydatabase.db"))

app =Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = database_file

db = SQLAlchemy (app)

class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(50), nullable=False)
    expensename = db.Column(db.String(50), nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    category = db.Column(db.String(50), nullable=False)



@app.route('/')
def add():
    return render_template('add.html')

@app.route('/addexpense', methods=['POST'])
def addexpense():
    date =request.form['date']
    expensename=request.form['expensename']
    amount=request.form['amount']
    category=request.form['category']
    print(date +' '+ expensename +' ' + amount +' ' + category)
    expense= Expense(date=date, expensename=expensename, amount=amount, category=category)
    db.session.add(expense)
    db.session.commit()
    return redirect('/expenses')

@app.route('/expenses')
def expenses():
    expenses  =Expense.query.all()
    total=0
    t_business=0
    t_food =0
    t_entertainment=0
    t_others=0


    for expense in expenses:
        total+=expense.amount

        if expense.category=='business':
            t_business+=expense.amount
        elif expense.category=='food':
            t_food+= expense.amount
        elif expense.category=='Entertainment':
            t_entertainment+=expense.amount
        elif expense.category =='others' :
            t_others+= expense.amount

    return render_template('expenses.html', expenses=expenses,total=total, t_others=t_others,t_food=t_food,t_entertainment=t_entertainment,t_business=t_business)

@app.route('/edit',methods=['POST'])
def edit():
    id=request.form['id']
    date=request.form['date']
    expensename=request.form['expensename']
    category=request.form['category']

    expense = Expense.query.filter_by(id=id).first()
    expense.date= date
    expense.expensename=expensename
    expense.amount= amount
    expense.category=category
    db.session.commit()
    return redirect('/expenses')


@app.route('/delete/<int:id>')
def delete(id):
    expense = Expense.query.filter_by(id=id).first()
    db.session.delete(expense)
    db.session.commit()
    return redirect('/expenses')

@app.route('/updateexpense/<int:id>')
def updateexpense(id):
    expense=Expense.query.filter_by(id=id)
    return render_template('updateexpense.html', expense=expense)

@app.route('/addview', methods=['GET','POST'])
def addview():
    if request.method=="GET":
        expenses = Expense.query.all()
        total = 0
        t_business = 0
        t_food = 0
        t_entertainment = 0
        t_others = 0

        for expense in expenses:
            total += expense.amount

            if expense.category == 'business':
                t_business += expense.amount
            elif expense.category == 'food':
                t_food += expense.amount
            elif expense.category == 'Entertainment':
                t_entertainment += expense.amount
            elif expense.category == 'others':
                t_others += expense.amount
            elif request.method=="POST":
                date = request.form['date']
                expensename = request.form['expensename']
                amount = request.form['amount']
                category = request.form['category']
                print(date + ' ' + expensename + ' ' + amount + ' ' + category)
                expense = Expense(date=date, expensename=expensename, amount=amount, category=category)
                db.session.add(expense)
                db.session.commit()
                return redirect('/addview')

        return render_template('addview.html', expenses=expenses, total=total, t_others=t_others, t_food=t_food,
                               t_entertainment=t_entertainment, t_business=t_business)


if __name__ == '__main__':
    app.run(debug=True)

