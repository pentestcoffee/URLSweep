import requests
from concurrent.futures import ThreadPoolExecutor
from urllib3 import disable_warnings
from colorama import init, Fore, Style

# 初始化 colorama
init(autoreset=True)

disable_warnings()

# 检测URL是否有效
def check_url(url):
    try:
        response = requests.get(url, timeout=5, verify=False)
        # 如果状态码是200，则认为是有效的URL
        if response.status_code == 200:
            print(f"{Fore.GREEN}[+] valid url: {url}{Style.RESET_ALL}")
            with open("valid.txt", "a") as f:
                f.write(url + "\n")
        else:
            print(f"{Fore.RED}[-] failed url (status code: {response.status_code}): {url}{Style.RESET_ALL}")
            with open("failed.txt", "a") as f:
                f.write(url + "\n")
    except requests.RequestException as e:
        # 捕捉所有异常并认为URL访问失败
        print(f"{Fore.YELLOW}[-] failed url: {url}{Style.RESET_ALL}")
        with open("failed.txt", "a") as f:
            f.write(url + "\n")


# 读取URL并进行多线程处理
def main():
    with open('url.txt', 'r') as f:
        urls = [line.strip() for line in f if line.strip()]

    # 使用多线程执行URL检测
    with ThreadPoolExecutor(max_workers=10) as executor:
        executor.map(check_url, urls)


if __name__ == "__main__":
    main()
