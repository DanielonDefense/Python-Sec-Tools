import passlib
from passlib.hash import sha256_crypt

def get_password():
    password = input("Enter the password you want to hash: ")
    return password
def avaliable_hashing_algorithms():
    avaliable_hashing_algorithms = ["sha256", "sha512", "md5"]
    print("Available hashing algorithms:" + ", ".join(avaliable_hashing_algorithms))
    
def sha256_hash(password):
    hashed_password = sha256_crypt.hash(password)
    return hashed_password

def sha512_hash(password):
    hashed_password = passlib.hash.sha512_crypt.hash(password)
    return hashed_password

def main():
    password = get_password()
    choosen_hash = (input("Choose a hashing algorithm, type list to see options: ")).lower()
    if choosen_hash == 'list':
        avaliable_hashing_algorithms()
    elif choosen_hash == "sha256":
        hashed_password = sha256_hash(password)
    elif choosen_hash == "sha512":
        hashed_password = sha512_hash(password)
    elif choosen_hash == "md5":
        hashed_password = passlib.hash.md5_crypt.hash(password)
    else:
        print("Invalid choice.")
        return
    print("Password hashing completed.")
    print('---------------------------------------------------------------------------------')
    print(f"Your hashed password is: {hashed_password}")
    print('---------------------------------------------------------------------------------')
    
if __name__ == "__main__":
    main()