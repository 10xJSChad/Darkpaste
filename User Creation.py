from AnaDB import AnaDatabase
darkpaste = AnaDatabase("Darkpaste")
darkpaste.load()
print("Enter username")
username = input()
print("Enter password")
password = input()
darkpaste.enter("users", [username, password, "x", "x"])
darkpaste.save()