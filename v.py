from selenium import webdriver

# Proxy adreslerinizi bir liste olarak tanımlayın
proxy_addresses = ["35.236.145.25:8090","35.236.145.25:8090","1.255.134.136:3128","103.154.237.110:8080","103.48.68.35:82"]

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


    driver.get("https://www.twitch.tv/ggeinn")
