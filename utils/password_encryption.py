import bcrypt

#Note: bcrypt only accepts b-strings as inputs

def hash_password(input_password):
    encoded_password = input_password.encode("utf-8") #First convert the string into a byte array (b-string)
    hashed_password = bcrypt.hashpw(encoded_password, bcrypt.gensalt())
    decoded_hashed_password = hashed_password.decode("utf-8") #Remove the b'[some_pwd]' for storage in the database

    return decoded_hashed_password

def compare_passwords(new_input_password, stored_hashed_password):
	if not new_input_password or not stored_hashed_password:
		return False #Prevent checkpw() call on non-hash password, which would otherwise result in invalid hash
		
	encoded_input = new_input_password.encode("utf-8") #Convert the plain password into a b-string
	encoded_hashed_password = stored_hashed_password.encode("utf-8")
	
	return bcrypt.checkpw(encoded_input, encoded_hashed_password)
