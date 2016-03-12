def valid_day(day):
	if day.isdigit():
		if int(day) >= 1 and int(day) <= 31:
			print day
		else:
			print None