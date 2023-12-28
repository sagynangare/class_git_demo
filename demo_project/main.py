from flask import Flask, render_template, url_for, request, flash, redirect

from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///company.db"
app.app_context().push()
db = SQLAlchemy(app)

class Employee(db.Model):
	id  = db.Column(db.Integer, primary_key=True)
	name= db.Column(db.String(100))
	city= db.Column(db.String(50))
	addr= db.Column(db.String(200))
	pin = db.Column(db.String(10))

	def __init__(self, name, city, addr, pin):
		self.name=name
		self.city=city
		self.addr=addr
		self.pin =pin


@app.route("/")
def index():
	return render_template("index.html", employees=Employee.query.all())

@app.route("/insert", methods=['GET', 'POST'])
def insert():
	if request.method=='POST':
		emp=Employee(request.form['name'], request.form['city'], request.form['addr'], request.form['pin'])
		db.session.add(emp)
		db.session.commit()
		return redirect(url_for("index"))

	return render_template("insert.html")


@app.route("/update/<int:eid>", methods=['GET', 'POST'])
def update(eid):
	emp=Employee.query.get(eid)
	#emp=Employee.query.get_or_404(eid)

	if request.method=="POST":
		if emp:
			emp.name=request.form['name']
			emp.city=request.form['city']
			emp.addr=request.form['addr']
			emp.pin=request.form['pin']
			db.session.commit()
			return redirect(url_for("index"))
		else:
			return f"Employee with id={eid}"

	return render_template("update.html", employee=emp)


@app.route("/delete/<int:eid>", methods=['GET', 'POST'])
def delete(eid):
	emp=Employee.query.get(eid)

	if request.method=="POST":
		db.session.delete(emp)
		db.session.commit()
		return redirect(url_for("index"))

	return render_template("delete.html", employee=emp)

if __name__=="__main__":
	db.create_all()
	app.run(debug=True)