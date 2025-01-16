def is_palindrome(num):
    num = str(num)
    return num == num[::-1]
user_input = input("please enter a number:")
if user_input.isdigit():
    if is_palindrome(user_input):
        print("it's a palindrome")
    else:
        print("ooops,it's not a palindrome")
