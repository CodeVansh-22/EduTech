import os

class Config:
    SECRET_KEY = 'super-secret-edutech-key'
    # Use your COPIED Atlas URI here. 
    # REMOVE the < > brackets and put your real password.
    MONGO_URI = 'mongodb+srv://vanshchauhand_db_user:3AVqDae56QjeOA7u@edutech.r7dodng.mongodb.net/?appName=EduTech'
    # --- RAZORPAY SETTINGS ---
    RAZORPAY_KEY_ID = 'rzp_test_RnqzlJgS6MFe2M'
    RAZORPAY_KEY_SECRET = '12nYyjrzt1QQ4nYtXUUPE8UY'