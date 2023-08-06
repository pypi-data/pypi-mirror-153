# Django 2FA using Twilio Verify

## Prerequisites

* Python 3.6+
* [Twilio](https://twilio.com) account
* `django` 2.29+
* `twilio` 7.8.2+
* `phonenumbers` 8.12.26+

## Installation

Install using `pip install django-twilio-2fa`.

Add to your `INSTALLED_APPS`:
```python
INSTALLED_APPS = (
    ...
    "django_twilio_2fa",
    "django_widget_tweaks",  # only required if using included templates
    ...
)
```

Add the project `urls.py`:
```python
urlpatterns = [
    ...
    path(
        "2fa/",  # Can be changed to any path
        include("django_twilio_2fa.urls")
    ),
]
```

## Flow

A user should only enter the 2FA flow if:
* They need to register for 2FA
* They have no previous 2FA authentication
* Their previous 2FA authentication has expired and needs to be renewed

Users should enter the flow through the Start view. If they are not registered for 2FA, they will be redirected to the Register view. Otherwise, it is assumed their 2FA authentication has expired.  

How and when to enter into the flow is determined outside the scope of this project. However, there is sample middleware in `test_app/middleware.py` that can be used as a reference.

### Start

This is the primary entrypoint into the 2FA flow.

If `PHONE_NUMBER_CB` returns `None` (indicating the user has not registered for 2FA), the user will be redirected to the Register view.

If only one method is allowed, the verification will be created using that method and user would be redirected to the Verify view. (The user would not see this screen.)

Otherwise, the user is presented with a choice of verification methods.

Template for this view: `start.html`

<img src="docs/assets/view-start.png" width="50%">

### Register

If the user has not registered for 2FA and `ALLOW_REGISTER` is `True`, the user will be shown this screen to add a phone number to their account.

If `ALLOW_REGISTER` is `False` and no phone number is available, the user is redirected to the Failed view.

If `REGISTER_OPTIONAL` is `True`, the user has the ability to skip 2FA registration. See that setting for more details.

Template for this view: `register.html`

| <img src="docs/assets/view-register-required.png" width="50%"> | <img src="docs/assets/view-register-optional.png" width="50%"> |
|----------------------------------------------------------------|----------------------------------------------------------------|
| `REGISTER_OPTIONAL` is `False`                                 | `REGISTER_OPTIONAL` is `True`                                  |

### Change

If the user has already registered and wants to change their phone number, this view is shown. 

It is the exact same view as register except `is_optional` is always `False`.

Template for this view: `change.html`

### Verify

Once the verification has been sent, the user will enter the code on this view. The copy changes based on what method was used.

An incorrect code will show an error message and allow the user to retry up to a total of 5 attempts. 

If the user exhausts all attempts, the user will be redirected to the Failed view.

If the user has not received the verification, they can click on the "Haven't received the <>?" link. If it has been more than the specified time, the verification will be recreated. (See `RETRY_TIME`.)

Template for this view: `verify.html`

<img src="docs/assets/view-verify.png" width="50%">

### Success

If no `VERIFY_SUCCESS_URL` is defined, the user is redirected to this view upon a successful verification.

Template for this view: `success.html`

### Failed

In case of a verification failure, the user is redirected to this view.

Depending on `RETRY, the user will be able to 

Template for this view: `failed.html`

| <img src="docs/assets/view-failed-retry.png" width="50%"> | <img src="docs/assets/view-failed-noretry.png" width="50%"> |
|-----------------------------------------------------------|-------------------------------------------------------------|
| User can retry verification                               | User cannot retry verification                              |

## Settings

All settings are prefixed with `TWILIO_2FA_`.

Any of the settings can be a callback. However, settings ending with `_CB` **must** be a callback. If a callback setting is defined but is not callable, a `ValueError` will be thrown.

### `ACCOUNT_SID`

Your Twilio account SID from the Twilio Console.

_Note: You cannot use test credentials with Verify._

### `AUTH_TOKEN`

Your Twilio auth token from the Twilio Console.

_Note: You cannot use test credentials with Verify._

### `SERVICE_ID`

Verify service ID from the Twilio Console.

### `ALLOWED_METHODS`

A list of allowed methods. The method must be enabled in the Verify service you setup in the Twilio Console.

Available methods: `sms`, `call`, and `whatsapp`. _Note: `email` is currently not supported._

If this setting is `None` or not set, all available methods will be presented to the end user.

### `PHONE_NUMBER_DEFAULT_REGION`

The default region for [`phonenumbers`](https://github.com/daviddrysdale/python-phonenumbers) library. Typically, this is the country code, but the entire list can be found [here](https://github.com/daviddrysdale/python-phonenumbers/tree/dev/python/phonenumbers/data).

Setting this allows users to not need to enter a country code with their phone number. 

You can set this to `None` to not have a default region. 

Defaults to `US` for the United States.

### `PHONE_NUMBER_ALLOWED_COUNTRIES`

A list of country codes from which phone numbers are allowed to originate.

Defaults to `["US"]`.

### `PHONE_NUMBER_DISALLOWED_COUNTRIES`

A list of country codes from which phone numbers *are not* allowed to originate. This can be used in conjunction with `PHONE_NUMBER_ALLOWED_COUNTRIES`.

Defaults to `[]`.

### `PHONE_NUMBER_CARRIER_LOOKUP`

Indicates whether the carrier information lookup should be performed via Twilio. *(Note: carrier lookups may affect billing.)*

Defaults to `True`.

### `PHONE_NUMBER_ALLOWED_CARRIER_TYPES`

A list of allowed carrier types.

Available types: `voip`, `landline`, and `mobile`.

Defaults to `["mobile"]`.

### `OBFUSCATE`

Indicates whether the phone number presented in the views should be obfuscated (`(123) 456-7890` vs `(XXX) XXX-7890`).

Defaults to `True`.

### `ALLOW_REGISTER`

Indicates whether users should be allowed to register their phone number if one does not already exist. 

If this is `False` and the user has no phone number, they will not be able to use 2FA.

Defaults to `True`.

### `REGISTER_OPTIONAL`

Indicates whether user registration can be skipped by a user. 

If `True` and the user clicks the Skip button, the user will be redirected to `REGISTER_OPTIONAL_URL`.

Defaults to `False`.

### `REGISTER_OPTIONAL_URL`

URL to redirect user when skipping registration.

Defaults to `javascript:history.back()`.

### `RETRY_TIME`

Amount of time (in seconds) after the last delivery attempt to allow the user to reattempt delivery of the verification.

Twilio does not have a limit on the amount of time between retries.

Defaults to 180 seconds or 3 minutes.

### `VERIFY_SUCCESS_URL`

The URL to redirect users to after a successful verification. This _should not_ return a `Response` instead (like `HttpResponseRedirect`) and should only return the URL as a string.

Defaults to `reverse_lazy("twilio_2fa:success")`

### `SERVICE_NAME`

Overrides the Verify service's friendly name set in the Twilio Console.

Arguments sent if callable:
* `user`: User instance
* `request`: `Request` instance
* `method`: Method string
* `phone_number`: Phone number string

Defaults to `None` (no override).

### `ALLOW_CHANGE`

Indicates if a user can change the phone number associated with their 2FA.

Defaults to `True`.

### `MAX_ATTEMPTS`

The maximum number of attempts the user has to successfully verify.

Arguments sent if callable:
* `user`: User instance

Defaults to `5`.

### `MAX_ATTEMPTS_TIMEOUT`

Amount of time (in seconds) before the user will be able to attempt another verification after a maximum attempts failure.

A timed out user will be redirected to the Failure view.

If this setting is `None`, `0` or `False`, there will be no timeout and the user will be able to immediately try again.

*Note: This timeout uses the sessions. It would be advisable to put this logic into a middleware and set this value to None.*

Defaults to `600` seconds or 10 minutes.

### `REGISTER_CB`

This callback is triggered when the user registers their phone number and should be used to update the user.

Arguments sent to this callback:
* `user`: User instance
* `phone_number`: Phone number string

No return is expected with this callback. 

### `PHONE_NUMBER_CB`

This callback is triggered on each verification request and should return the user's phone number.

Arguments sent to this callback:
* `user`: User instance

Expected return of this callback:
* String of the user's phone number

### `METHOD_DISPLAY_CB`

This callback is triggered on each request and allows customization of the method icon and label.

Arguments sent to this callback:
* `method`: Method string

Expected return of this callback is a `dict` with one or more of the following values (the default will be used if not included):
* `icon`: Font Awesome 5 icon classes (return `None` to not use an icon)
* `label`: Label string

### `TIMEOUT_CB`

This callback is triggered on each verification request and should return the timeout timestamp for the current user as a `DateTime` instance or `None` if no timeout exists.

Arguments sent to this callback:
* `user`: User instance

## Signals

Signal names are prefixed `twilio_2fa_`.

All signals are sent with at least the following arguments:
* `request`: Current `Request` instance
* `user`: `User` instance
* `twofa`: Instance of `TwoFA`

The `TwoFA` class has the following attributes:
* `method`: 2FA verification method chosen by user
* `phone_number`: Phone number used for verification in E164 format
* `twilio_sid`: The SID for this verification instance
* `attempts`: Number of attempts to verify

### `verification_sent`

This signal is triggered anytime a verification is sent. 

Additional arguments sent with this signal:
* `timestamp`: `DateTime` instance

### `verification_success`

This signal is triggered when a user completes verification successfully.

The `verification_status_changed` signal is also triggered during a successful verification.


### `verification_status_changed`

This signal is triggered when the Twilio verification status is changed. 

Options for `status`: `approved` and `canceled`.

Additional arguments sent with this signal:
* `status`: Status verification was changed to

### `verification_failed`

This signal is triggered when the Twilio verification attempt has failed.

### `verification_retries_exceeded`

This signal is trigger when the number of failed attempts to verify exceeds `MAX_ATTEMPTS`. 

You should handle storing the timeout timestamp for retrieval by `TIMEOUT_CB`. 

Additional arguments sent with this signal:
* `timeout`: The value of `MAX_ATTEMPTS`
* `timeout_until`: `DateTime` instance of timeout

## Customization

The presentation code uses [Bootstrap 5](https://getbootstrap.com/docs/5.1/), [Font Awesome 5](https://fontawesome.com/v5/search), and [django-widget-tweaks](https://github.com/jazzband/django-widget-tweaks). None are an absolute requirement and can be removed using custom templates or, in the case of Font Awesome, defining the `METHOD_DISPLAY_CB` setting.

All templates are in the `twilio_2fa` directory. To override these templates, you can put your version in your own `twilio_2fa` directory anywhere your templates are stored.

<img src="docs/assets/customization-diagram.png" width="50%">

### `_base.html`

This is the primary template that all main templates extends.

It defines a single block for content: `content` (outlined in yellow above). For `django_widget_tweaks`, the `content` block is wrapped by `WIDGET_ERROR_CLASS`.

The header can also be changed using the `header` block (outlined in red). Header icon classes changed using the `header_icon_class` block (outlined in blue) and text changed using the `header_text` block (outlined in green). 

### `_messages.html`

This template shows messages from `django.contrib.messages` and is included in each of the main templates.

### `_form_errors.html`

This template displays a form field's errors. `field` should be passed in the context.

### `failed.html`

This template is shown when the user's verification failed either from a timeout of the verification, maximum tries are exceeded, an API failure with Twilio, or other general error.

It conditionally allows users to retry verification based on the `can_retry` session variable.

### `registration_form.html`

This template shows the registration form to the user and serves as the base template for `register.html` and `change.html`. 

### `register.html`

This template shows the registration form to the user.

If `ALLOW_REGISTRATION` is `False`, the user is not shown this view and will be redirected to the failure page if no phone number is returned by `PHONE_NUMBER_CB`.

It is based on `registration_form.html`.

### `change.html`

This template shows the change form to the user.

It is based on `registration_form.html`.

### `start.html`

This template allows the user to select the verification method.

If only one method exists, the user will not see this page.

### `success.html`

This template is shown on a successful verification if `VERIFY_SUCCESS_URL` is not set.

### `verify.html`

This template shows the token form.

## Development

Perform the following steps in the root directory:

1. Create a virtual environment and activate.
2. Install `django_twilio_2fa`: `pip install -e .`

Perform the following steps in the `test_app` directory:

3. Install requirements: `pip install -r requirements.txt`.
4. Copy `.env-sample` to `.env` and update with your settings.
5. Run migrations: `python manage.py migrate`.
6. Run the server: `python manage.py runserver`.

The test app should now be available at http://localtest.me:8000.

### To-Do

* Internationalization
