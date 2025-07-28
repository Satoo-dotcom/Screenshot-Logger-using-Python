from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///payroll.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Models
class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    position = db.Column(db.String(100), nullable=False)
    salary = db.Column(db.Float, nullable=False)
    payrolls = db.relationship('Payroll', backref='employee', lazy=True)

class Payroll(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'), nullable=False)
    base_salary = db.Column(db.Float, nullable=False)
    deductions = db.Column(db.Float, nullable=False)
    net_pay = db.Column(db.Float, nullable=False)
    date = db.Column(db.String(20), nullable=False)

@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/')
def index():
    employees = Employee.query.all()
    return render_template('index.html', employees=employees)

@app.route('/add_employee', methods=['GET', 'POST'])
def add_employee():
    if request.method == 'POST':
        name = request.form['name']
        position = request.form['position']
        salary = float(request.form['salary'])
        new_emp = Employee(name=name, position=position, salary=salary)
        db.session.add(new_emp)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add_employee.html')

@app.route('/delete_employee/<int:emp_id>')
def delete_employee(emp_id):
    emp = Employee.query.get_or_404(emp_id)
    db.session.delete(emp)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/payroll/<int:emp_id>', methods=['GET', 'POST'])
def payroll(emp_id):
    emp = Employee.query.get_or_404(emp_id)
    if request.method == 'POST':
        base_salary = emp.salary
        deductions = float(request.form['deductions'])
        net_pay = base_salary - deductions
        from datetime import datetime
        payroll = Payroll(employee_id=emp.id, base_salary=base_salary, deductions=deductions, net_pay=net_pay, date=datetime.now().strftime('%Y-%m-%d'))
        db.session.add(payroll)
        db.session.commit()
    payrolls = Payroll.query.filter_by(employee_id=emp.id).all()
    return render_template('payroll.html', emp=emp, payrolls=payrolls)

if __name__ == '__main__':
    app.run(debug=True)