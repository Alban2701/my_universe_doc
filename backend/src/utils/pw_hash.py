from pwdlib import PasswordHash

pw = "azer"
hasher = PasswordHash.recommended()
print(hasher.hash(pw))
