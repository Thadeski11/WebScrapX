import argparse
from requests_html import HTMLSession
import re

parser = argparse.ArgumentParser(prog="WebScrapX", description="Script de Scraping.")
parser.add_argument("-u", "--url", help="Passar a url alvo (Recomenda-se o uso de ' ').")
parser.add_argument("-ul", "--ulist", help="Passar a wordlist com as urls.")
args = parser.parse_args()


def Scrap(html):
	email_all = r"[a-z0-9_\.-]+@[a-z0-9_-]+\.[a-z\.]+"
	telef_SA = r"\+?\d{0,3}?\s?\(\d{1,2}\)\s?\d{4,5}\s?-?\.?_?\d{4,5}"
	telef_NA = r"\+?\d{0,3}?\s?\(\d{3}\)\s?\d{3}\s?\.?-?_?\d{4}"
	telef_EU = r"\+?\d{0,3}?\s\d{1,3}\s\d{2,3}\s\d{2,3}\s\d{2,3}\s\d{2,3}" 
	open_Num = r"\d{3,4}\s-?\d{3}\s-?\d{3,4}"

	emails = re.findall(email_all, html)
	telefones_SouthAmerica = re.findall(telef_SA, html)
	telefones_NorthAmerica = re.findall(telef_NA, html)
	telefones_Europe = re.findall(telef_EU, html)
	open_numbers = re.findall(open_Num, html)
	
	#EVITAR DUPLICAÇÃO DE ITENS
	verificar_emails = []
	verificar_telefones = []

	if len(emails) >= 1:
		for email in emails:
			if email.split(".")[-1] not in ["png", "jpg", "jpeg", "gif", "bmp", "tiff", "webp", "svg", "ico", "heif", "heic", "mp4", "mkv", "mov", "avi", "wmv", "flv", "webm", "mpeg", "mpg", "3gp", "ts", "mp3", "wav", "flac", "aac", "ogg", "m4a", "opus", "wma", "amr", "mid", "pdf", "doc", "docx", "xls", "xlsx", "ppt", "pptx", "txt", "rtf", "odt", "ods", "odp", "zip", "rar", "7z", "tar", "gz", "bz2", "xz", "iso", "dmg", "py", "js", "html", "css", "php", "java", "c", "cpp", "cs", "rb", "sh", "bat", "ps1", "go", "ts", "sql", "db", "sqlite", "mdb", "accdb", "ini", "cfg", "conf", "log", "json", "xml", "yaml", "toml", "csv", "md", "epub", "ttf", "otf", "exe", "dll", "apk", "ipa", "bin", "dat"]:
				if email not in verificar_emails:
					verificar_emails.append(email)

	if len(telefones_SouthAmerica) >= 1:
		for telefones in telefones_SouthAmerica:
			if telefones not in verificar_telefones:
				verificar_telefones.append(telefones)

	if len(telefones_NorthAmerica) >= 1:
		for telefones in telefones_NorthAmerica:
			if telefones not in verificar_telefones:
				verificar_telefones.append(telefones)

	if len(telefones_Europe) >= 1:
		for telefones in telefones_Europe:
			if telefones not in verificar_telefones:
				verificar_telefones.append(telefones)

	if len(open_numbers) >= 1:
		for telefones in open_numbers:
			if telefones not in verificar_telefones:
				verificar_telefones.append(telefones)

	return verificar_emails, verificar_telefones

def Check_Url_Only(wordlist):
	session = HTMLSession()
	req = session.get(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0"})

	html = req.text
	emails, telefones = Scrap(html)
	
	if len(emails) >= 1:
		print("EMAILS")
		print(emails)
	if len(telefones) >= 1:
		print("TELEFONES")
		print(telefones)
	

def Check_Urls_Wordlist(urls_wordlist):
	session = HTMLSession()
	with open(urls_wordlist, "r") as w:
		for linhas in w:
			linhas = linhas.strip()
			req = session.get(linhas, headers={"User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0"})

			html = req.text
			emails, telefones = Scrap(html)
			
			if len(emails) == 0 and len(telefones) == 0:
				print(f"{linhas} ❌❌❌")
			else:
				print(f"{linhas} ⬇️ ⬇️ ⬇️")
				if len(emails) >= 1:
					print("			EMAILS:")
					print(f"				{emails}")
				if len(telefones) >= 1:
					print("			TELEFONES:")
					print(f"				{telefones}")

if args.url:
	Check_Url_Only(args.url)
elif args.ulist:
	Check_Urls_Wordlist(args.ulist)
