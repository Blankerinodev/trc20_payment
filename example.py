from main import TRCToken

MY_TRC20_ADDRESS = ''

if __name__ == "__main__":
	# Создать объект для работы с TRC20
	trc_token = TRCToken()

	# 1. Создать два новых адреса TRC20
	private_key1, address1 = trc_token.create_trc20_address()
	private_key2, address2 = trc_token.create_trc20_address()

	print(f"Создан адрес 1: {address1} с приватным ключом: {private_key1}")
	print(f"Создан адрес 2: {address2} с приватным ключом: {private_key2}")

	# 2. Проверить балансы обоих адресов
	balance_usdt_address1 = trc_token.get_trc20_balance(address1)
	balance_trx_address1 = trc_token.get_trx_balance(address1)

	balance_usdt_address2 = trc_token.get_trc20_balance(address2)
	balance_trx_address2 = trc_token.get_trx_balance(address2)

	print(f"Баланс USDT адреса 1: {balance_usdt_address1}")
	print(f"Баланс TRX адреса 1: {balance_trx_address1}")
	print(f"Баланс USDT адреса 2: {balance_usdt_address2}")
	print(f"Баланс TRX адреса 2: {balance_trx_address2}")

	# 3. Отправить определенное количество TRX с первого адреса на второй для оплаты комиссии
	# Предположим, что у адреса 1 есть 20 TRX
	amount_trx_to_send = 20_000_000

	try:
		txn_result = trc_token.send_trx(private_key_str=private_key1, to_address=address2, from_address=address1, amount=amount_trx_to_send)
		if txn_result['result']:
			print(f"{amount_trx_to_send} TRX успешно отправлены с адреса 1 на адрес 2")
		else:
			print(f"Ошибка при отправке {amount_trx_to_send} TRX с адреса 1 на адрес 2")
	except Exception as e:
		print(f"Ошибка при отправке TRX: {e}")

	# 4. Отправить весь баланс TRC20 со второго адреса на ваш адрес
	# Предположим, что у адреса 1 есть некоторое количество USDT
	result, tx_id = trc_token.transfer_all_trc20(from_address=address2, private_key=private_key2, to_address=MY_TRC20_ADDRESS)
	if result:
		print(f"USDT успешно отправлен с адреса 1 на ваш адрес. ID транзакции: {tx_id}")
	else:
		print(f"Ошибка при отправке USDT с адреса 1 на ваш адрес")