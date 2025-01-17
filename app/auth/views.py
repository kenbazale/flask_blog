from flask import render_template,redirect,request,url_for,flash
from flask_login import login_user.logout_user,login_required,current_user
from . import auth
from . . import User
from . forms import LoginForm,RegistrationForm
from flask_mail import send_email



@auth.route('/')
def login():
    form =LoginForm()
    if form.validated_on_submit():
        user = user.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user,form.remember_me.data)
            return redirect(request.args.get('next')or url_for('mai.index'))
        flash('Invalid username or password')
    return render_template('auth/login.html', form=form)    


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.index'))



@auth.route('/register',methods = ['POST','GET'])
def register():
    form = RegistrationForm()
    if form.validate_on_sudmit():
        user = User(email = form.email.data,username = form.username.data,password = form.password.data)
        db.session.add(user)
        db.commit()
        token = user.generate_confirmation_oken()
        send_email(user.email,'Confirm Your Account','auth/email/confirm',user=user,token=token)
        flash('A confirmationemail has been sent to youby email')
        return redirect(url_for('main.index'))

    return render_template('auth/register.html',form = form )


@auth.route('/confirm/<token>')
@login_required
def confrim(token):
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        flash('you have confirm your account,Thanks!')
    else:
        flash('the confirmation link is invalid or has expired')
    return redirect(url_for('main.index'))  

@auth.before_app_request
def before_request():
    if current_user.is_authenticated() and not current_user.confirmed and request.endpoint[:5] != 'auht.':
        return redirect(url_for('auth.unconfirmed'))

@auth.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous()  or current_user.confirmed:
        return redirect(url_for('main.index'))  
    return render_template('auth/unconfirmed.html')