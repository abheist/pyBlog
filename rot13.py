def rot(s):
	s = s.lower()
	arr = list(s)
	newStr = ""
	for each in arr:
		each = ord(each)
		if each >= ord('a') and each <= ord('z'):
			each = each + 13
			if each >= ord('z'):
				each = each - 26
			each = chr(each)
			newStr = newStr + each
		else:
			newStr = newStr + chr(each)
	return newStr
print rot("uryyb ?");