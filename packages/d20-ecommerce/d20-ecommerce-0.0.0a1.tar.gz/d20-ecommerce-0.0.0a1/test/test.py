import stripe

stripe.api_key = "sk_test_4eC39HqLyjWDarjtT1zdp7dc"

pi = stripe.PaymentIntent.create(
  amount=1000,
  currency='usd',
  payment_method_types=['card'],
  receipt_email='jenny.rosen@example.com',
)


print(pi)