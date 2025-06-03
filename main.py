from source.preset  import *
from source.pages    import *
from source.requests import*

if not accounts.check_login("admin"):
	admin = Account(base, "admin", 6463131979109318604)
	admin.name = "Админ"
	admin.update_on_base(base)

socket.run(app, debug=True, host="0.0.0.0")
