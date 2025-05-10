import pikepdf
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

pdf_path = "abcde.pdf"
wordlist_path = "rockyou.txt"
NUM_THREADS = 10
BATCH_SIZE = 1000
found = False
tentativas = 0

def try_password(password):
    global found
    if found:
        return None
    try:
        with pikepdf.open(pdf_path, password=password):
            found = True
            return password
    except pikepdf.PasswordError:
        return None
    except Exception as e:
        return None

def password_batches(passwords, batch_size):
    for i in range(0, len(passwords), batch_size):
        yield passwords[i:i + batch_size]

start_time = time.time()

with open(wordlist_path, "r", encoding="latin-1") as f:
    all_passwords = [line.strip() for line in f]

for batch in password_batches(all_passwords, BATCH_SIZE):
    if found:
        break
    with ThreadPoolExecutor(max_workers=NUM_THREADS) as executor:
        futures = {executor.submit(try_password, pwd): pwd for pwd in batch}
        for future in as_completed(futures):
            result = future.result()
            tentativas += 1
            if result:
                print(f"[+] Senha encontrada: {result}")
                found = True
                break

end_time = time.time()
print(f"🔢 Tentativas: {tentativas}")
print(f"⏱️ Tempo total: {end_time - start_time:.2f} segundos")
