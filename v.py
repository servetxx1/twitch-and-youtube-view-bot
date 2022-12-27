from selenium import webdriver

# Proxylist.txt dosyasını okuyun ve proxy adreslerini bir listeye alın
with open("proxies.txt") as f:
    proxy_addresses = f.readlines()
proxy_addresses = [x.strip() for x in proxy_addresses]

# Her bir proxy adresi için bir tarayıcı açın
drivers = []
for proxy_address in proxy_addresses:
    # Firefox tarayıcısını açın ve proxy ayarlarını ekleyin
    firefox_profile = webdriver.FirefoxProfile()
    firefox_profile.set_preference("network.proxy.type", 1)
    firefox_profile.set_preference("network.proxy.http", proxy_address.split(":")[0])
    firefox_profile.set_preference("network.proxy.http_port", int(proxy_address.split(":")[1]))
    firefox_profile.set_preference("network.proxy.ssl", proxy_address.split(":")[0])
    firefox_profile.set_preference("network.proxy.ssl_port", int(proxy_address.split(":")[1]))

    driver = webdriver.Firefox(firefox_profile=firefox_profile)
    drivers.append(driver)
# İstediğiniz web sayfalarını açın
for driver in drivers:
    driver.get("https://ifconfig.co")
