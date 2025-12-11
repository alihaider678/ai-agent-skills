import os

# 🟢 SAFE: Environment variable
db_url = os.getenv("DB_URL")

# 🟢 SAFE: Placeholder text (The generic regex might catch this, but Agent should ignore it)
aws_key = "YOUR_KEY_HERE"

# 🔴 DANGER: A real-looking hardcoded secret (Longer string now)
stripe_secret_token = "sk_live_EXAMPLE_KEY_123456789"

# 🔴 DANGER: A plain text password
app_password = "super_secret_password_123"