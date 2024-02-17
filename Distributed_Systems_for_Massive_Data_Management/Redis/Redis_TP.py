import redis
import hashlib
import regex

def connect_to_redis(host='localhost', port=6379, db=0):
    # To connect to Redis server 
    # (localhost by default is 6379)
    # Redis supports by default 16 different databases (db) enumerated from 0 to 15
    # We connect to database 0, the databases are isolated between each other
    # decode_responses = True converts into string the binary data (makes it readable)
    r = redis.Redis(host=host, port=port, db=db, decode_responses=True)
    return r


def generate_short_url(long_url):
    
    # We use haslib with algorithm SHA-256 to generate a short and unique hash
    #print("\nInput Long_URL:", long_url, "\n")
    #print("Binary Long_URL Version: ", long_url.encode(), "\n")
    #print("Hashed Version:", hashlib.sha256(long_url.encode()), "\n")
    #print("Hexadecimal Hashed Version:", hashlib.sha256(long_url.encode()).hexdigest(), "\n")
    short_hash = hashlib.sha256(long_url.encode()).hexdigest()[:10]
    return f"http://short.url/{short_hash}"

def store_url_mapping(r, long_url, short_url, user_email):
    # We store in Redis the key made up by the concatenation of email:longURL
    # and assign as value shortURL
    r.hset(user_email, long_url, short_url)

def get_short_url(r, long_url, user_email):
    # We check the existence of a shortURL by receiving as input 
    # the user email and the longURL
    existing_short_url = r.hexists(user_email, long_url)
    if existing_short_url:
        print("\nShort URL found:\n")
        return r.hget(user_email, long_url)
    else:
        # Generar una nueva URL corta y almacenarla
        print("Short URL not found, proceeding to its creation.")
        short_url = generate_short_url(long_url)
        store_url_mapping(r, long_url, short_url, user_email)
        return short_url

def main():
    # Conectar a Redis
    r = connect_to_redis()
    
    # Datos de prueba
    #user_email = "user@example.com"
    #long_url = "https://www.example.com/very/long/url/that/needs/to/be/shortened"
    
    # Obtener o generar una URL corta
    print("\n\nWelcome MyRedis Database System by Mollita Corportive Management Systems.\n\nAvailable operations to perform:\n  1. Given an long URL and authentication email, check the existence of the short corresponding URL within MyRedis.\n  2. Given a short URL, access to the long URL version.\n  3. Given a email authentication, display statistics of insertion & requests for the user.\n")
    answer1 = input("What do you want to do? Choose the corresponding number: ")
    if answer1 == "1":
        print("Please introduce the long URL and email:\n")
        long_url = input("URL: ")
        while long_url.strip() == "":
            print("\nPlease provide a not empty URL.")
            long_url = input("URL: ")

        user_email = input("Email: ")
        while user_email.strip() == "":
            print("\nPlease provide a not empty email.")
            short_url = input("Email: ")

        short_url = get_short_url(r, long_url, user_email)
        print("The short URL is:", short_url, "\n")


    elif answer1 == "2":
        print("\nPlease introduce the short URL and email:\n")
        short_url = input("URL: ")
        while short_url.strip() == "":
            print("\nPlease provide a not empty URL.")
            short_url = input("URL: ")
        
        email = input("Email: ")
        while email.strip() == "":
            print("\nPlease provide a not empty email.")
            email = input("Email: ")

        long_url = None
        for long_URL in r.hkeys(email):
            if r.hget(email, long_URL) == short_url:
                long_url = long_URL
                print("\nThe corresponding long URL is:", long_url)
                break
        if long_url == None:
            print("\nError. The introduced short URL does not exist.")

    elif answer1 == "3":
        email = input("\nPlease introduce the email: ")
        while email.strip() == "":
            email = input("\nPlease provide a not empty email.")
        
        urls = r.hgetall(email)
        print(f"\nThe total number of insertions for user {email} is:", len(urls))
        print("The dictionary of (long_URL, short_URL) is:", urls, "\n")
    else:
        print("Operation not valid. Thank you for your attention.")


if __name__ == "__main__":
    main()
