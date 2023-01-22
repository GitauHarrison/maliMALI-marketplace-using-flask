from app import app, db
from flask import render_template, url_for, redirect, flash
from app.forms import LoginForm, VendorRegistrationForm, \
    CustomerRegistrationForm, AdminRegistrationForm, AddToCart,\
    ProductsForSaleForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import Admin, Vendor, Customer, User, ProductsForSale,\
    PurchasedProducts
from werkzeug.utils import secure_filename
import os


@app.route('/dashboard/register/vendor', methods=['GET', 'POST'])
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
        flash('Registered a vendor.They can log in to continue')
        return redirect(url_for('dashboard_admin'))
    vendors = Vendor.query.all()
    return render_template(
        'dashboard_admin.html',
        title='Dashboard',
        form=form,
        vendors=vendors)


@app.route('/dashboard/vendor/add-product', methods=['GET', 'POST'])
@login_required
def dashboard_vendor():
    form = ProductsForSaleForm()
    if form.validate_on_submit():
        product = ProductsForSale(
            name=form.name.data,
            price=form.price.data,
            currency=form.currency.data,
            description=form.description.data,
            quantity=form.quantity.data,
            vendor=current_user)

        # Handling file upload
        uploaded_file = form.image.data
        filename = secure_filename(uploaded_file.filename)
        if not os.path.exists(app.config['VENDOR_UPLOAD_PATH']):
            os.makedirs(app.config['VENDOR_UPLOAD_PATH'])
        product_image_path = os.path.join(
            app.config['VENDOR_UPLOAD_PATH'], filename)
        uploaded_file.save(product_image_path)
        print('Product image path: ', product_image_path)
        # product.image = product_image_path

        product_image_path_list = product_image_path.split('/')[2:]
        new_product_image_path = '/'.join(product_image_path_list)
        print('new_product_image_path: ', new_product_image_path)
        product.image = new_product_image_path

        db.session.add(product)
        db.session.commit()
        flash('Product saved.')
        return redirect(url_for('dashboard_vendor_all_products'))
    return render_template('vendor/dashboard.html', title='Add Product', form=form)


@app.route('/dashboard/vendor/all-products', methods=['GET', 'POST'])
@login_required
def dashboard_vendor_all_products():
    products = current_user.products_for_sale.all()
    print(products)
    return render_template(
        'vendor/products.html',
        title='All Products',
        products=products)


@app.route('/dashboard/customer', methods=['GET', 'POST'])
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


@app.route('/register/customer', methods=['GET', 'POST'])
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


@app.route('/register/admin', methods=['GET', 'POST'])
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


@app.route('/', methods=['GET', 'POST'])
@app.route('/shop', methods=['GET', 'POST'])
def shop():
    """All products listed here"""
    form = AddToCart()
    return render_template('index.html', title='From The Shop', form=form)
