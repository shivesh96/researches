import time
import tkinter as tk
import threading
import requests

threads = []
timeout = 5

proxy_timeout = 5000
proxy_type = "http" # "http", "socks4", "socks5"
proxy_country = "IN" # "IN"
proxy_ssl = "IN" # "IN"
proxy_anonymity = "IN" # "IN"
proxyListUrl = f"https://api.proxyscrape.com/v2/?request=getproxies&protocol={proxy_type}&timeout={proxy_timeout}&country={proxy_country}&ssl={proxy_ssl}&anonymity={proxy_anonymity}"
testOnUrl = "https://www.qrail.in"
# testOnUrl = "https://www.irctc.co.in/nget"

counter = 1
def get_proxies():
    # set status 
    status_label.configure(text="Status: Getting Proxies...")
    # Set up requests with the proxy
    response = requests.get(proxyListUrl)
    print(response.text)
    response.raise_for_status()
    proxies = response.text.strip().split("\r\n")
    # print(proxies)
    return proxies

def check_proxy(proxy):
    try:
        # start time
        start_time = time.time()
        # print("checking proxy... - " + proxy)
        response = requests.get(testOnUrl, proxies={'http': proxy, 'https': proxy}, timeout=timeout)
        if response.status_code == 200:
            print_report(proxy, True, time.time() - start_time)
            return True
        else:
            print_report(proxy, False, time.time() - start_time)
            return False
    except requests.exceptions.RequestException:
        print_report(proxy, False, time.time() - start_time)
        pass
    return False

def check_proxies():
    status_label.configure(text="Status: Initiating Check...")
    global threads
    proxies = proxy_text.get('1.0', 'end-1c').split('\n')
    result_text.delete('1.0', 'end')
    
    for proxy in proxies:
        t = threading.Thread(target=check_proxy, args=(proxy,))
        t.start()
        threads.append(t)

    status_label.configure(text="Status: Check Initiated")

def check_threads():
    global threads
    if all(not t.is_alive() for t in threads):
        status_label.configure(text="Status: Ready")
        threads = []  # Clear the list of threads

    # Call this function again after 1000ms
    root.after(1000, check_threads)

def print_report(proxy, is_working, time_taken):
    global counter
    time_taken = round(time_taken, 2)
    status_label.configure(text=f"Status:  {proxy} - {'Working' if is_working else 'Not Working'} - {time_taken}")
    # result_text.insert('end', f'{counter}{"-Working - " if is_working else "Working Not -"} : {proxy}\n')
    if(is_working):
        result_text.insert('end', f'{counter}{"-Working"}: {proxy} - {time_taken}\n')
        counter += 1

# Create the GUI
root = tk.Tk()
root.title("Proxy Checker")

# Status label
status_label = tk.Label(root, text="Status: Waiting for input...")
status_label.pack()

# Proxy input
proxy_label = tk.Label(root, text="Enter Proxies (one per line):")
proxy_label.pack()

proxy_text = tk.Text(root, height=10, width=50)
proxy_text.pack()

proxies = get_proxies()
# print(proxies)
status_label.configure(text="Status: Got Proxies")
proxy_text.insert('1.0', '\n'.join(proxies))
status_label.configure(text="Status: Proxies Loaded")

# Check button
check_button = tk.Button(root, text="Check Proxies", command=check_proxies)
check_button.pack()

# Result output
result_label = tk.Label(root, text="Results:")
result_label.pack()

result_text = tk.Text(root, height=10, width=50)
result_text.pack()

# Call the check_threads function after 1000ms
root.after(1000, check_threads)

# Start the GUI event loop
root.mainloop()