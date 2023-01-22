from app import app, db
from flask import render_template, url_for, redirect, flash
from app.forms import LoginForm, VendorRegistrationForm, \
    CustomerRegistrationForm, AdminRegistrationForm, AddToCart,\
    ProductsForSaleForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import Admin, Vendor, Customer, User


@app.route('/dashboard/register/vendor')
@login_required
def dashboard_admin():
    form = VendorRegistrationForm()
    if form.validate_on_submit():
        vendor = Vendor(
            username=form.username.data,
            email=form.email.data,
            phone=form.phone.data,
            shop_name=form.shop_name.data)
        vendor.set_password(form.password.data)
        db.session.add(vendor)
        db.session.commit()
        flash('Registered successfully as vendor. Please log in to continue')
        return redirect(url_for('login'))
    return render_template('dashboard_admin.html', title='Dashboard', form=form)


@app.route('/dashboard/vendor')
@login_required
def dashboard_vendor():
    form = ProductsForSaleForm()
    if form.validate_on_submit():
        vendor = Vendor(
            username=form.username.data,
            email=form.email.data,
            phone=form.phone.data,
            shop_name=form.shop_name.data)
        vendor.set_password(form.password.data)
        db.session.add(vendor)
        db.session.commit()
        flash('Registered successfully as vendor. Please log in to continue')
        return redirect(url_for('login'))
    return render_template('vendor/dashboard.html', title='Dashboard', form=form)


@app.route('/dashboard/customer')
@login_required
def dashboard_customer():    
    return render_template('dashboard_customer.html', title='Dashboard')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        if current_user.type == 'admin':
            return redirect(url_for('dashboard_admin'))
        if current_user.type == 'vendor':
            return redirect(url_for('dashboard_vendor'))
        if current_user.type == 'customer':
            return redirect(url_for('dashboard_customer'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        flash(f'Welcome {user.username}')
        if current_user.type == 'admin':
            return redirect(url_for('dashboard_admin'))
        if current_user.type == 'vendor':
            return redirect(url_for('dashboard_vendor'))
    return render_template('auth/login.html', title='Login', form=form)


@app.route('/register/customer',methods=['GET', 'POST'])
def register_customer():
    if current_user.is_authenticated:
        if current_user.type == 'admin':
            return redirect(url_for('dashboard_admin'))
        if current_user.type == 'vendor':
            return redirect(url_for('dashboard_vendor'))
        if current_user.type == 'customer':
            return redirect(url_for('dashboard_customer'))
    form = CustomerRegistrationForm()
    if form.validate_on_submit():
        user = Customer(
            username=form.username.data,
            email=form.email.data,
            phone=form.phone.data,
            residence=form.residence.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Registered successfully as customer. Please log in to continue')
        return redirect(url_for('login'))
    return render_template('auth/register.html', title='Register', form=form)


# @app.route('/register/vendor',methods=['GET', 'POST'])
# @login_required
# def register_vendor():
#     if current_user.is_authenticated:
#         return redirect(url_for('dashboard'))
#     form = VendorRegistrationForm()
#     if form.validate_on_submit():
#         vendor = Vendor(
#             username=form.username.data,
#             email=form.email.data,
#             phone=form.phone.data,
#             shop_name=form.shop_name.data)
#         vendor.set_password(form.password.data)
#         db.session.add(vendor)
#         db.session.commit()
#         flash('Registered successfully as vendor. Please log in to continue')
#         return redirect(url_for('login'))
#     return render_template('auth/register.html', title='Register', form=form)


@app.route('/register/admin',methods=['GET', 'POST'])
def register_admin():
    if current_user.is_authenticated:
        if current_user.type == 'admin':
            return redirect(url_for('dashboard_admin'))
        if current_user.type == 'vendor':
            return redirect(url_for('dashboard_vendor'))
        if current_user.type == 'customer':
            return redirect(url_for('dashboard_customer'))
    form = AdminRegistrationForm()
    if form.validate_on_submit():
        admin = Admin(
            username=form.username.data,
            email=form.email.data,
            phone=form.phone.data,
            department=form.department.data)
        admin.set_password(form.password.data)
        db.session.add(admin)
        db.session.commit()
        flash('Registered successfully as admin. Please log in to continue')
        return redirect(url_for('login'))
    return render_template('auth/register.html', title='Register', form=form)


@app.route('/logout')
@login_required
def logout():
    """Used to log out a user"""
    logout_user()
    return redirect(url_for('login'))


@app.route('/')
@app.route('/shop')
def shop():
    """All products listed here"""
    form = AddToCart()
    return render_template('index.html', title='From The Shop', form=form)
