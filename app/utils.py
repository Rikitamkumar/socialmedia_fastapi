from passlib.context import CryptContext

pdw_context = CryptContext(schemes=["bcrypt"], deprecated = "auto")

def hash(password:str):

    return pdw_context.hash(password)


def verify_password(regular_password, hashed_password):

    return pdw_context.verify(regular_password,hashed_password)
    # return pdw_context.hash(regular_password) == hashed_password





"""


|           Part       |                                              Meaning                                                                                   |
| -------------------- | ---------------------------------------------------------------------------------------------------------------------------------------|
| `CryptContext(...)`  |        Creates a reusable password hashing manager                                                                                     |
| `schemes=["bcrypt"]` |        Specifies which hashing algorithm(s) to use (bcrypt is a strong, industry-standard choice)                                      |
| `deprecated="auto"`  |        If we use multiple schemes, this marks older ones as deprecated automatically (helps rotate hashing methods safely over time)   |



"""