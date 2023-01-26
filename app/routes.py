from app import app, db
from flask import render_template, url_for, redirect, flash, session,\
    request, jsonify
from app.forms import LoginForm, VendorRegistrationForm, \
    CustomerRegistrationForm, AdminRegistrationForm, AddToCart,\
    ProductsForSaleForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import Admin, Vendor, Customer, User, ProductsForSale,\
    PurchasedProducts
from werkzeug.utils import secure_filename
import os
import requests
from app import mpesa
from app.ip_address import get_user_location
from app.map import get_shops_data, get_shops
from geoalchemy2 import Geometry
from app.airtime import send_airtime



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
            return redirect(url_for('dashboard_customer_checkout'))
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
            return redirect(url_for('dashboard_customer_checkout'))
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


# @app.route('/register/admin', methods=['GET', 'POST'])
# def register_admin():
#     if current_user.is_authenticated:
#         if current_user.type == 'admin':
#             return redirect(url_for('dashboard_admin'))
#         if current_user.type == 'vendor':
#             return redirect(url_for('dashboard_vendor'))
#         if current_user.type == 'customer':
#             return redirect(url_for('dashboard_customer'))
#     form = AdminRegistrationForm()
#     if form.validate_on_submit():
#         admin = Admin(
#             username=form.username.data,
#             email=form.email.data,
#             phone=form.phone.data,
#             department=form.department.data)
#         admin.set_password(form.password.data)
#         db.session.add(admin)
#         db.session.commit()
#         flash('Registered successfully as admin. Please log in to continue')
#         return redirect(url_for('login'))
#     return render_template('auth/register.html', title='Register', form=form)


@app.route('/logout')
@login_required
def logout():
    """Used to log out a user"""
    logout_user()
    return redirect(url_for('login'))


# ===========
# CUSTOMER
# ===========


@app.route('/')
@app.route('/home')
def home():
    return render_template('landing_page.html', title='Home')


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
    try:
        if 'product' in session:
            # Get product details
            cart_product = ProductsForSale.query.get(session['product']['product_id'])

            # Add product to db
            product_for_purchase = PurchasedProducts(
                name=cart_product.name,
                price=cart_product.price,
                quantity=session['product']['quantity'],
                cost=session['product']['quantity'] * cart_product.price,                
                currency=cart_product.currency,
                description=cart_product.description,
                image=cart_product.image,
                vendor_id=cart_product.vendor_id)
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
        title='Home',
        products=products,
        num_products=num_products)


@app.route('/vendors')
def vendors():
    allvendors = Vendor.query.all()

    # Get current user location
    location = get_user_location()
    lat = location.latitude
    lng = location.longitude

    # Convert into json
    appvendors = jsonify(allvendors)
    print('Status:', appvendors.status_code)

    return appvendors


@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query')

    location = get_user_location()
    lat = location.latitude
    lng = location.longitude

    url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json'
    params = {
        'location': f'{lat},{lng}',
        'radius': 1000,
        'keyword': query,
        'key': app.config['GOOGLE_MAPS_API_KEY']
    }
    response = requests.get(url, params=params)
    data = response.json()
    return data


# @app.route('/vendors/nearby/<customer_id>/<distance>')
# @login_required
# def get_nearby_vendors(customer_id, distance):
#     customer = Customer.query.filter_by(id=customer_id).first()
#     # user_location = get_user_location()
#     if customer is None:
#         flash("No customer with that ID was found")
#         return redirect(url_for('shop'))
#     else:
#         customer_location = customer.location
#         vendors = Vendor.query.filter(
#             func.ST_DWithin(Vendor.location, customer_location, distance)).all()
#         if not vendors:
#             flash ("No vendors found near that customer")
#             return redirect(url_for('shop'))
#         else:
#             vendor_list = []
#             for vendor in vendors:
#                 vendor_list.append({'name': vendor.name, 'location': vendor.location.data})
#             return render_template(
#                 'map.html',
#                 vendors=vendor_list,
#                 customer_location=customer.location.data)


@app.route('/vendors/nearby')
def vendors_nearby():
    radius = 500
    customer_location = Geometry('POINT(x y)', srid=4326)
    nearby_vendors = Vendor.query.filter(
        Vendor.location.ST_Distance_Sphere(customer_location) < radius).all()
    return jsonify([vendor.to_dict() for vendor in nearby_vendors])


@app.route('/dashboard/customer/purchase-history', methods=['GET', 'POST'])
@login_required
def dashboard_customer():
    # Get all purchased products by the current user
    paid_products = current_user.purchased_products.filter_by(payment_status=True).all()

    # User location coordinates
    user_location = get_user_location()
    latitude = user_location.latitude
    longitude = user_location.longitude

    return render_template(
        'dashboard_customer.html',
        title='Purchase History',
        latitude=latitude,
        longitude=longitude,
        paid_products=paid_products)


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
        add_product = {"product_id": product.id,"quantity": form.quantity.data}
        session['product'] = add_product
        return redirect(url_for('shop'))

    # Get user location
    location = get_user_location()
    lat = location.latitude
    lon = location.longitude
    print(lat, ' , ', lon)

    # Display map
    markers = get_shops_data()
    print('Shops:', markers.encode('utf-8'))

    my_shops = get_shops()
    print('My shops: ', my_shops)

    return render_template(
        'product_customer.html',
        title='Product Details',
        product=product,
        form=form,
        markers=markers,
        lat=lat,
        lon=lon)


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

    # Get user location
    location = get_user_location()
    lat = location.latitude
    lon = location.longitude

    # Display map
    markers = get_shops_data()

    return render_template(
        'cart_items.html',
        title='Cart Items',
        cart_items=cart_items,
        num_cart_items=num_cart_items,
        markers=markers,
        lat=lat,
        lon=lon)


@app.route('/dashboard/customer/cart-item/<int:id>/delete')
@login_required
def dashboard_customer_cart_items_delete(id):
    cart_item = PurchasedProducts.query.filter_by(id=id).first_or_404()
    db.session.delete(cart_item)
    db.session.commit()
    flash(f'{cart_item.name} deleted from your cart.')
    return redirect(url_for('dashboard_customer_cart_items'))


@app.route('/dashboard/customer/cart-items/ready-to-buy')
@login_required
def dashboard_customer_checkout():
    cart_items = PurchasedProducts.query.all()
    num_cart_items = len(cart_items)

    # Get user location
    location = get_user_location()
    lat = location.latitude
    lon = location.longitude

    # Display map
    markers = get_shops_data()

    return render_template(
        'cart_items_checkout.html',
        title='Buy Your Items',
        cart_items=cart_items,
        num_cart_items=num_cart_items,
        markers=markers,
        lat=lat,
        lon=lon)


@app.route('/dashboard/customer/cart-item/<int:id>/buy')
@login_required
def dashboard_customer_buy_product(id):
    cart_items = PurchasedProducts.query.all()
    for item in cart_items:
        if item.id is id:
            if item.customer_id is None:
                item.customer_id = current_user.id
                db.session.commit()
    return redirect(url_for('dashboard_customer_checkout'))


@app.route('/product/<int:id>/lipa-na-mpesa')
@login_required
def lipa_na_mpesa(id):    
    access_token = mpesa.MpesaAccessToken.validated_mpesa_access_token
    api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
    headers = {'Authorization': 'Bearer %s' % access_token}
    mpesa_request = {
        'BusinessShortCode': mpesa.LipaNaMpesaPassword.business_short_code,   # org receiving funds
        'Password': mpesa.LipaNaMpesaPassword.decode_online_password,         # used to encrypt the request
        'Timestamp':mpesa.LipaNaMpesaPassword.lipa_time,                      # transaction time
        'TransactionType': 'CustomerPayBillOnline',
        'Amount': 1,                                                          # transaction amount
        'PartyA': int((current_user.phone).replace('+', '')),                 # MSISDN sending the funds
        'PartyB': mpesa.LipaNaMpesaPassword.business_short_code,               # org receiving the funds
        'PhoneNumber': int((current_user.phone).replace('+', '')),            # MSISDN sending the funds
        'CallBackURL': 'https://sandbox.safaricom.co.ke/mpesa/',
        'AccountReference': 'primashop',
        'TransactionDesc': 'testing stk push for ecommerce app'
    }
    try:
        response = requests.post(api_url, json=mpesa_request, headers=headers)
        print(response.text, f'\n\nStatus: {response.status_code}')

        # Update payment status in database
        product = PurchasedProducts.query.filter_by(id=id).first_or_404()
        product.payment_status = True
        db.session.commit()
        flash(f'{product.name} paid for.')

        # Send airtime after purchase
        send_airtime()

    except Exception as e:
        print(f'Error: \n\n {e}')    
    return redirect(url_for('dashboard_customer'))


# ===========
# END OF CUSTOMER
# ===========
