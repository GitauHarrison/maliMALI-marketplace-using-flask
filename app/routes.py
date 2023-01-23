from app import app, db
from flask import render_template, url_for, redirect, flash, session,\
    request
import requests
from app.forms import LoginForm, VendorRegistrationForm, \
    CustomerRegistrationForm, AdminRegistrationForm, AddToCart,\
    ProductsForSaleForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import Admin, Vendor, Customer, User, ProductsForSale,\
    PurchasedProducts
from werkzeug.utils import secure_filename
import os
from urllib.parse import urlparse


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

        product_image_path_list = product_image_path.split('/')[2:]
        new_product_image_path = '/'.join(product_image_path_list)
        product.image = new_product_image_path

        db.session.add(product)
        db.session.commit()
        flash('Product saved.')
        return redirect(url_for('dashboard_vendor_all_products'))
    return render_template('vendor/dashboard.html', title='Add Product', form=form)


@app.route('/dashboard/vendor/all-products', methods=['GET', 'POST'])
@login_required
def dashboard_vendor_all_products():
    form = AddToCart()
    products = current_user.products_for_sale.all()
    num_products = len(products)
    return render_template(
        'vendor/products.html',
        title='All Products',
        form=form,
        products=products,
        num_products=num_products)


@app.route('/dashboard/vendor/product/<int:id>/delete', methods=['GET', 'POST'])
@login_required
def dashboard_vendor_delete_product(id):
    product = ProductsForSale.query.filter_by(id=id).first_or_404()
    db.session.delete(product)
    db.session.commit()
    flash('Product deleted successfully.')
    return redirect(url_for('dashboard_vendor_all_products'))


@app.route('/dashboard/vendor/product/<int:id>/allow', methods=['GET', 'POST'])
@login_required
def dashboard_vendor_allow_product(id):
    product = ProductsForSale.query.filter_by(id=id).first_or_404()
    product.allow_status=True
    db.session.commit()
    flash('Product allowed to appear in home page. Head over there to check')
    return redirect(url_for('dashboard_vendor_all_products'))


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
        if current_user.type == 'customer':
            return redirect(url_for('dashboard_customer'))
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


# ===========
# CUSTOMER
# ===========


@app.route('/', methods=['GET', 'POST'])
@app.route('/shop', methods=['GET', 'POST'])
def shop():
    """All products listed here"""
    if current_user.is_authenticated:
        if current_user.type == 'customer':
            return redirect(url_for('dashboard_customer'))
        if current_user.type == 'admin':
            return redirect(url_for('dashboard_admin'))
        if current_user.type == 'vendor':
            return redirect(url_for('dashboard_vendor'))
    products = ProductsForSale.query.filter_by(allow_status=True).all()
    form = AddToCart()
    try:
        if 'product' in session:
            # Get product details
            cart_product = ProductsForSale.query.get(session['product']['product_id'])

            # Add product to db
            product_for_purchase = PurchasedProducts(
                name=cart_product.name,
                cost=session['product']['quantity'] * cart_product.price,
                quantity=session['product']['quantity'],
                currency=cart_product.currency,
                description=cart_product.description,
                image=cart_product.image,
                vendor_id=cart_product.vendor_id
            )
            db.session.add(product_for_purchase)
            db.session.commit()
            flash('Product added to cart. Continue shopping, otherise see cart to checkout.')
            del session['product']
            return redirect(url_for('shop'))
    except:
        session.clear()
    num_products = len(products)
    #print(items_in_cart[0]['product_id'])
    return render_template(
        'index.html',
        title='From The Shop',
        form=form,
        products=products,
        num_products=num_products)


@app.route('/dashboard/customer/purchase-history', methods=['GET', 'POST'])
@login_required
def dashboard_customer():
    return render_template('dashboard_customer.html', title='Purchase History')


@app.route('/shop/product/<int:id>', methods=['GET', 'POST'])
def view_product(id):
    if current_user.is_authenticated:
        if current_user.type == 'customer':
            return redirect(url_for('dashboard_customer'))
        if current_user.type == 'admin':
            return redirect(url_for('dashboard_admin'))
        if current_user.type == 'vendor':
            return redirect(url_for('dashboard_vendor'))
    product = ProductsForSale.query.filter_by(id=id).first_or_404()
    form = AddToCart()
    if form.validate_on_submit():
        add_product = {
            "product_id": product.id,
            "quantity": form.quantity.data
        }
        session['product'] = add_product
        return redirect(url_for('shop'))
    return render_template(
        'product_customer.html',
        title='Product Details',
        product=product,
        form=form)


@app.route('/customer/cart-items')
def dashboard_customer_cart_items():
    if current_user.is_authenticated:
        if current_user.type == 'customer':
            return redirect(url_for('dashboard_customer'))
        if current_user.type == 'admin':
            return redirect(url_for('dashboard_admin'))
        if current_user.type == 'vendor':
            return redirect(url_for('dashboard_vendor'))
    cart_items = PurchasedProducts.query.all()
    num_cart_items = len(cart_items)
    return render_template(
        'cart_items.html',
        title='Cart Items',
        cart_items=cart_items,
        num_cart_items=num_cart_items)


@app.route('/dashboard/customer/cart-item/<int:id>/delete')
@login_required
def dashboard_customer_cart_items_delete(id):
    cart_item = PurchasedProducts.query.filter_by(id=id).first_or_404()
    db.session.delete(cart_item)
    db.session.commit()
    flash(f'{cart_item.name} deleted from your cart.')
    return redirect(url_for('dashboard_customer_cart_items'))


@app.route('/dashboard/customer/cart-items/buy')
@login_required
def dashboard_customer_checkout():
    cart_items = PurchasedProducts.query.all()
    num_cart_items = len(cart_items)
    return render_template(
        'cart_items_checkout.html',
        title='Buy Your Items',
        cart_items=cart_items,
        num_cart_items=num_cart_items)


# ===========
# END OF CUSTOMER
# ===========
