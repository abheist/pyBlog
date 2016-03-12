months = ["january", "fabruary", "march", "april", "may", "june", "july", "august", "september", "octuber", "november", "december"]

def valid_month(month):
	for i in months:
		if month.lower() == i.lower():
			return month.capitalize()
	return None

print valid_month("january")