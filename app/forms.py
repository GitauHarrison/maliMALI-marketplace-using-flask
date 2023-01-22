from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, \
    SelectField, IntegerField
from wtforms.validators import DataRequired, Length, EqualTo, Email, \
    Regexp, ValidationError
import phonenumbers


class LoginForm(FlaskForm):
    """Login Form"""
    username = StringField('Username', validators=[DataRequired(), Length(1, 64)])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log In')


# Using form inheritance

class User(FlaskForm):
    """General User Data"""
    username = StringField('Username', validators=[DataRequired(), Length(1, 64)])
    email = StringField(
        'Email',
        validators=[DataRequired(), Email()],
        render_kw={'placeholder': 'johndoe@email.com'})
    phone = StringField(
        'Phone Number',
        validators=[DataRequired(), Length(min=2, max=30)])
    password = PasswordField(
        'Password:',
        validators=[DataRequired(), Length(min=8, max=20),
        Regexp(r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$',
               message='Password must be at least 8 characters long and '
               'contain at least one letter and one number.')],
        render_kw={'placeholder': 'Use: fullstack2023'})
    confirm_password = PasswordField(
        'Confirm Password',
        validators=[DataRequired(), EqualTo('password')],
        render_kw={'placeholder': 'Confirm Your Password Above'})

    def validate_username(self, username):
        """Check if username already exists"""
        parent = User.query.filter_by(username=username.data).first()
        if parent is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        """Check if email already exists"""
        parent = User.query.filter_by(email=email.data).first()
        if parent is not None:
            raise ValidationError('Please use a different email address.')

    def validate_phone(self, phone):
        p = phonenumbers.parse(phone.data)
        try:
            if not phonenumbers.is_valid_number(p):
                raise ValueError()
        except (phonenumbers.phonenumberutil.NumberParseException, ValueError) as exc:
            raise ValidationError('Invalid phone number.\n\n', exc ) from exc


class VendorRegistrationForm(User):
    """Vendor Registration Form"""
    shop_name = StringField('Shop Name', validators=[DataRequired(), Length(1, 64)])
    submit = SubmitField('Register')


class CustomerRegistrationForm(User):
    """Customer Registration Form"""
    residence = StringField('Residence', validators=[DataRequired(), Length(1, 64)])
    submit = SubmitField('Register')


class AdminRegistrationForm(User):
    """Admin Registration Form"""
    department = SelectField(
        'Department',
        choices=[
            ('Support', 'Support'),
            ('Finance', 'Finance'),
            ('HR', 'HR')
        ])
    submit = SubmitField('Register')


class AddToCart(FlaskForm):
    """Add items to the cart"""
    quantity = IntegerField('Quantity', validators=[DataRequired()])
    add = SubmitField('Add To Cart')
