### User Model

This user model is a custom model from the default one. It manages both clients and admin (in this case the single vendor user). Hence it has the following extra fields:
- Stripe id (in order to process payments)
- Addresses (billing and/or shipping which are both optional)
- On click purchasing if user can purchase without giving extra data
- Phone number
- First and Last Name (always required)

Note that the user's main credential is set to be the email address

The fields related to __uid__ and __token__ are necessary for resetting password and user's account authentication when register. They are generated in the tokens.py file

The __is_active__ prop is only set to __True__ ones the user has been authenticated.

This app does NOT use the default authentication method of DRF neither the allauth's one. Instead, the authentication method is manually configured and uses the email address of the client and the __uid__ and __token__ four properties of the user model.
