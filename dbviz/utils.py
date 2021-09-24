import re
#code to check whether an ISBN13 is valid via the checksum
#then convert it into an isbn 10

def isOdd(n):
  #small utility for isbn13 check sum
  if n%2 == 0 :
    return False
  else:
    return True

def isValidISBN13(code):
  code = str(code)
  result = False
  #isbn13 has 13 chars
  #first 3 digits are 978
  #last digit matches check sum
  if code[0:3] == '978' and re.match('^\d{10}$', code[3:]):
    sum=0
    for i in range(0,12):
      sum += int(code[i]) * (3 if isOdd(i) else 1)
    result = (10 - (sum % 10)) % 10 == int(code[12])
    
  return result

def calcCheckDigitForISBN10(code):
  #take 9 digits from isbn13 and create check digit for an isbn10
  #isbn10 check sum weight goes down from from 10 to 2 from first digit to penultimate
  #check sum modulus is 11 with 10 represented by X
  code = code.replace("-","")
  sum = 0
  weight = 10
  for i in range(len(code)):
    sum += int(code[i]) * (weight - i)
    #print(sum)
  check = 11 - (sum % 11)
  if check == 10:
    check = 'X'
  if check == 11:
    check = 0
  return check

def toISBN10(isbn):
  isbn = str(isbn)
  code = ""
  if isValidISBN13(isbn):
  #converts ISBN13 to ISBN 10
    code = isbn[3:len(isbn)-1]
    code += str(calcCheckDigitForISBN10(code))
  return code