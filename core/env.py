import environ

env = environ.Env(
    DEBUG=(bool, False),
    SECRET_KEY=(str, "no-safe-key"),
    POLYGON_API_KEY=(str, None),
    STRIPE_SECRET_KEY=(str, "no-safe-key"),
    STRIPE_PUBLIC_KEY=(str, None),
    STRIPE_WEBHOOK_SECRET_KEY=(str, None),
)
