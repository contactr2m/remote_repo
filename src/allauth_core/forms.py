from django import forms
from allauth.account.forms import (LoginForm, ChangePasswordForm, AddEmailForm,
                                   ResetPasswordForm, SetPasswordForm, ResetPasswordKeyForm)
from django.contrib.auth import get_user_model
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Submit, HTML, Button, Row, Field
from crispy_forms.bootstrap import AppendedText, PrependedText, FormActions
from django.core.urlresolvers import reverse


class MyLoginForm(LoginForm):
    remember_me = forms.BooleanField(required=False, initial=False)

    def __init__(self, *args, **kwargs):
        super(MyLoginForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.fields["login"].widget.input_type = "email"  # ugly hack
        self.helper.form_method = "POST"
        self.helper.form_action = "account_login"
        self.helper.form_class = "login"
        self.helper.layout = Layout(
            Field('login', placeholder="Enter Email", autofocus=""),
            Field('password', placeholder="Enter Password"),
            HTML('<a href="{}">Forgot Password?</a>'.format(
                reverse("account_reset_password"))),
            Field('remember'),
            Submit('sign_in', 'Log in',
                   css_class="btn btn-lg btn-primary btn-block"),
        )


class MyPasswordChangeForm(ChangePasswordForm):

    def __init__(self, *args, **kwargs):
        super(MyPasswordChangeForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_action = "account_change_password"
        self.helper.form_class = "password_change"
        self.helper.form_method = "POST"
        self.helper.layout = Layout(
            Field('oldpassword', placeholder="Enter old password",
                  autofocus=""),
            Field('password1', placeholder="Enter new password"),
            Field('password2', placeholder="Enter new password (again)"),
            Submit('pass_change', 'Change Password', css_class="btn-warning"),
        )


class MyPasswordResetForm(ResetPasswordForm):

    def __init__(self, *args, **kwargs):
        super(MyPasswordResetForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_action = "account_reset_password"
        self.helper.form_class = "password_reset"
        self.helper.form_method = "POST"
        self.helper.layout = Layout(
            Field('email', placeholder="Enter email",
                  autofocus=""),
            Submit('pass_reset', 'Reset Password', css_class="btn-warning"),
        )


class MySetPasswordForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super(MySetPasswordForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_action = "account_set_password"
        self.helper.form_class = "password_set"
        self.helper.form_method = "POST"
        self.helper.layout = Layout(
            Field('password1', placeholder="Enter password",
                  autofocus=""),
            Field('password2', placeholder="Enter password (again)"),
            Submit('pass_change', 'Change Password', css_class="btn-warning"),
        )


class MyResetPasswordKeyForm(ResetPasswordKeyForm):
    def __init__(self, *args, **kwargs):
        super(MyResetPasswordKeyForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_action = "."
        #self.helper.form_class = "password_set"
        self.helper.form_method = "POST"
        self.helper.layout = Layout(
            Field('password1', placeholder="Enter new password",
                  autofocus=""),
            Field('password2', placeholder="Enter new password (again)"),
            Submit('pass_change', 'Change Password', css_class="btn-warning"),
        )


class MyEmail(AddEmailForm):
    def __init__(self, *args, **kwargs):
        super(MyEmail, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_action = "account_email"
        self.helper.form_class = "add_email"
        self.helper.form_method = "POST"
        self.helper.field_class = 'col-md-4'
        #   self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-md-2'
        self.helper.layout = Layout(
            Field('email', placeholder="Enter email address",
                  autofocus=""),
            Submit('action_add', 'Add E-mail', css_class="btn-warning"),

        )

