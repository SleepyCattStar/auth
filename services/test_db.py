from auth.db.mongodb import user_collection

users = user_collection.find_one()

print(user_collection)

#  python3 -m auth.services.test_db