import argparse
from requests_html import HTMLSession
import re
import aiohttp
import asyncio

parser = argparse.ArgumentParser(prog="WebScrapX", description="Script de Scraping.")
parser.add_argument("-u", "--url", help="Passar a url alvo (Recomenda-se o uso de ' ').")
parser.add_argument("-ul", "--ulist", help="Passar a wordlist com as urls.")
parser.add_argument("-t", "--time", help="Máximo de Requisições por segundo")
args = parser.parse_args()


def Scrap(html):
	email_all = r"[a-z0-9_\.-]+@[a-z0-9_-]+\.[a-z\.]+"
	telef_SA = r"\+?\d{0,3}?\s?\(\d{1,2}\)\s?\d{4,5}\s?-?\.?_?\d{4,5}"
	telef_NA = r"\+?\d{0,3}?\s?\(\d{3}\)\s?\d{3}\s?\.?-?_?\d{4}"
	telef_EU = r"\+?\d{0,3}?\s\d{1,3}\s\d{2,3}\s\d{2,3}\s\d{2,3}\s\d{2,3}" 
	open_Num = r"\d{3,4}\s\d{3}\s\d{3,4}"

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

def Check_Url_Only(url):
	session = HTMLSession()
	req = session.get(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0"})

	html = req.text
	emails, telefones = Scrap(html)

	if len(emails) == 0 and len(telefones) == 0:
		print(f"{url} ❌❌❌")
	else:
		print(f"{url} ⬇️ ⬇️ ⬇️")
		if len(emails) >= 1:
			print("			EMAILS:")
			print(f"				{emails}")
		if len(telefones) >= 1:
			print("			TELEFONES:")
			print(f"				{telefones}")


max_req_per_second = args.time
semaphore = asyncio.Semaphore(int(max_req_per_second))

async def Busca_Asy(session, url):
	async with semaphore:
		try:
			async with session.get(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0"}) as req:
				html = await req.text()
				return url, html
		except Exception:
			print(f"Erro ao buscar {url}")
			return url, None

async def Check_Urls_Wordlist(urls_wordlist):
	urls = []
	with open(urls_wordlist, "r") as w:
		for url in w.readlines():
			url = url.strip()
			urls.append(url)

	async with aiohttp.ClientSession() as session:
		tarefas = [Busca_Asy(session, url) for url in urls]
		resultados = await asyncio.gather(*tarefas)
	
	for url, html in resultados:
		if html:
			emails, telefones = Scrap(html)

			if len(emails) == 0 and len(telefones) == 0:
				print(f"{url} ❌❌❌")
			else:
				print(f"{url} ⬇️ ⬇️ ⬇️")
				if len(emails) >= 1:
					print("			EMAILS:")
					for item in emails:
						print(f"				{item}")
				if len(telefones) >= 1:
					print("			TELEFONES:")
					for item in telefones:
						print(f"				{item}")


if args.url:
	Check_Url_Only(args.url)
elif args.ulist:
	asyncio.run(Check_Urls_Wordlist(args.ulist))
