from .sql import *

class UI_texts:
	UserNotFind = "Пользователь не найден"
	WrongPass   = "Неверный пароль"

SQL_BIGINT_MAX_VALUE = 9223372036854775806 # константа
HASH_KEY = 7433494284023295923 # случайное число
def hash(password):
	a_bytes = str(password).encode("utf-8")
	a_number = int(a_bytes.hex(), 16)
	return (a_number * HASH_KEY) % SQL_BIGINT_MAX_VALUE

class Account (debug_object):

	def __init__(self, base: Base, login: str, password: int, sql_sync=True):
		global DEBUG
		self.DEBUG = DEBUG
		
		self.login = login
		self.password = password
		self.name = "Untitled"
		
		if not sql_sync: return

		with TableHandler(base, AccountsManager.Head) as handle:
			self.ID = handle.add_row(self.login, self.password, self.name)
			self.name = f"User-{self.ID}"
			handle.update(self.ID, "name", self.name)
	
	def update_on_base(self, base: Base):
		with TableHandler(base, AccountsManager.Head) as handle:
			handle.update(self.ID, "name",   self.name  )
	
	# not a method
	def unpack(base, response: list):
		new = Account(None, None, None, sql_sync=False)
		new.ID, new.login, new.password, new.name = response
		return new

	def __repr__(self):
		return f"{self.name},{self.ID}"




class AccountsManager (debug_object):
	TableName = TABLE + "accaunts"
	Head = TableHead(TableName,
		Column("ID",       int, "int identity(0,1)",        Flag.Default),
		Column("login",    str, "varchar(32)",              Flag.Default),
		Column("password", int, "BIGINT",                   Flag.Default),
		Column("name",     str, "varchar(256)",             Flag.Encode ),
	)

	def __init__(self, base: Base):
		global DEBUG
		self.DEBUG = DEBUG
		
		self.base = base

	def try_to_login(self, login: str, password: str) -> Account | str:
		"""if success - returns Account
		if failed - error string"""
		if len(str(password)) < 4:
			return UI_texts.WrongPass

		with TableHandler(self.base, self.Head) as handle:
			finded = handle.get_by("login", login)

			if len(finded) == 0:
				return UI_texts.UserNotFind
			
			for response in finded:
				user_data = Account.unpack(self.base, response)
				if hash(password) == user_data.password or password == user_data.password: # !!! DEBUG ##################################
					return user_data
			
			return UI_texts.WrongPass

	def check_login(self, login: str) -> bool:
		"""Возвращает существующий ли аккаунт с указанным login"""
		with TableHandler(self.base, self.Head) as handle:
			return len(handle.get_by("login", login)) != 0
	
	def find(self, requester_id: int, request: str) -> list:
		with TableHandler(self.base, self.Head) as handle:
			raw_finded = handle.get_where("name LIKE '%" + encode(request) + "%'")
			
			if request.isdigit():
				raw_finded = handle.get_rows(int(request)) + raw_finded
			
			debug_object.value("raw_finded", raw_finded)

			finded = []
			
			for i in raw_finded:
				if i not in finded:
					finded.append(i)
			
			if len(finded) == 0:
				return []

			result = []
			for item in finded:
				acc = Account.unpack(self.base, item)
				if acc.ID == requester_id:
					continue
				result.append(acc)

			return result

	def add(self, login: str, password: str) -> Account:
		"""Создаёт аккаунт на базе и возвращает его"""
		return Account(self.base, login, hash(password))

	def delete(self, ID: int):
		pass
	
	def _debug_get_all(self):
		with TableHandler(self.base, self.Head) as handle:
			last_ID = handle._get_last_ID()
			result = []
			
			if last_ID != None:
				for i in range(last_ID + 1):
					result.append(Account.unpack(self.base, handle.get_row(i)))
			
			return result




class ClientManager:
	def __init__(self):
		self.clients = dict()
		self.sids = dict()

	def add(self, ip: str, account: Account) -> None:
		"""Добавляет нового клиента"""
		self.clients[ip] = account
	
	def add_sid(self, ID: int, sid: str) -> None:
		self.sids[ID] = sid

	def remove(self, ip: int) -> None:
		"""Удаляет клиента с указанным ip (адресом)"""
		try:
			del self.clients[ip]
		except:
			None

	def get(self, ip: int) -> Account:
		"""Возвращает экземпляр Account по ip"""
		try:
			return self.clients[ip]
		except:
			return None
	
	def get_sid(self, ID: int) -> str:
		try:
			return self.sids[ID]
		except:
			return None

	def __getitem__(self, ip) -> Account:
		return self.get(ip)




class Product:
	Columns = [
		Column("ID",       int, "int identity(0,1)", Flag.Default),
		Column("name",     str, "varchar(1024)",     Flag.Encode),
		Column("price",    float, "float",           Flag.Default),
		Column("category", str, "varchar(1024)",     Flag.Encode),
		Column("picture",  str, "varchar(1024)",     Flag.Encrypt)
	]

	def __init__(self, ID: int, name: str, price: float, category: str, picture: str):
		global DEBUG
		self.DEBUG = DEBUG

		self.ID = ID
		self.name = name
		self.price = price
		self.category = category
		self.picture = picture
  
	def pack(self) -> str:
		return f"{self.ID},{self.name},{self.price},{self.category},{self.picture}"

	# not a method
	def unpack(response: list):
		new = Product(None, None, None, None, None)
		new.ID, new.name, new.price, new.category, new.picture = response
		return new




class ProductManager:
	ProductsTableName = TABLE + "products"
	ProductsHead = TableHead(ProductsTableName, *Product.Columns)

	def __init__ (self, base: Base):
		global DEBUG
		self.DEBUG = DEBUG

		self.base = base
		with BaseHandler(base) as base_handle:
			if self.ProductsTableName not in base.tables:
				base_handle.create_table(self.ProductsHead)
			else:
				with TableHandler(base, self.ProductsHead) as products_handle:
					last_ID = products_handle._get_last_ID()

	def get_all(self):
		with TableHandler(self.base, self.ProductsHead) as products_handle:
			finded = products_handle._READ(f"SELECT * FROM {self.ProductsTableName}")
			finded = [[self.ProductsHead.columns[i].unconvert(value) for i, value in enumerate(row)] for row in finded]
			result = [Product.unpack(i) for i in finded]
			return result
	
	def get_categories(self):
		with TableHandler(self.base, self.ProductsHead) as product_handle:
			finded = product_handle.get_column("category")
			print(finded)
			categories = set(finded)
			print(categories)
			return categories