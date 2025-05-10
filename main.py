import pikepdf
import time

pdf_path = "abcde.pdf"
wordlist_path = "rockyou.txt"
tentativas = 0

start_time = time.time()

with open(wordlist_path, "r", encoding="latin-1") as wordlist:
    for line in wordlist:
        password = line.strip()
        tentativas += 1
        try:
            with pikepdf.open(pdf_path, password=password):
                print(f"[+] Senha encontrada: {password}")
                break
        except pikepdf.PasswordError:
            continue
        except Exception as e:
            print(f"[!] Erro com '{password}': {e}")

end_time = time.time()
print(f"🔢 Tentativas: {tentativas}")
print(f"⏱️ Tempo total: {end_time - start_time:.2f} segundos")
