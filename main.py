import time

import requests

# TODO: should I just pull all gladiators and then just sort out Mojave in Dataframes?
#


def main():
    callAPI(
        "roseville",
        "https://www.autonationchryslerdodgejeepramroseville.com/apis/widget/INVENTORY_LISTING_DEFAULT_AUTO_NEW:inventory-data-bus1/getInventory?bodyStyle=Truck%20Crew%20Cab&compositeType=new&make=Jeep&model=Gladiator&year=2024&pageSize=50",
    )
    callAPI(
        "sacramento",
        "https://www.sacsuperstore.com/apis/widget/INVENTORY_LISTING_DEFAULT_AUTO_NEW:inventory-data-bus1/getInventory?make=Jeep&model=Gladiator&year=2024&pageSize=50",
    )
    callAPI(
        "folsom",
        "https://www.folsomcdjr.com/apis/widget/INVENTORY_LISTING_DEFAULT_AUTO_ALL:inventory-data-bus1/getInventory?make=Jeep&model=Gladiator&year=2024&pageSize=50",
    )
    callAPI(
        "elkgrove",
        "https://equ6hxb6wg-dsn.algolia.net/1/indexes/*/queries?x-algolia-agent=Algolia%20for%20JavaScript%20(4.9.1)%3B%20Browser%20(lite)%3B%20JS%20Helper%20(3.4.4)&x-algolia-api-key=da97ef494552f47ecc6f47068888d120&x-algolia-application-id=EQU6HXB6WG",
        "elkgrove-request.json",
    )
    callAPI(
        "reno",
        "https://www.lithiajeepreno.com/apis/widget/INVENTORY_LISTING_DEFAULT_AUTO_NEW:inventory-data-bus1/getInventory?year=2024&gvBodyStyle=Truck&model=Gladiator&make=Jeep&pageSize=50",
    )
    callAPI(
        "placerville",
        "https://2591j46p8g-dsn.algolia.net/1/indexes/*/queries?x-algolia-agent=Algolia for JavaScript (4.9.1); Browser (lite); JS Helper (3.4.4)&x-algolia-api-key=78311e75e16dd6273d6b00cd6c21db3c&x-algolia-application-id=2591J46P8G",
        "placerville-request.json",
    )


def callAPI(location, url, payloadLocation=None):
    if payloadLocation:
        payload = ""
        with open("/home/ksiler/msrfree/requests/" + payloadLocation, "r") as f:
            payload = f.read()
        response = requests.post(url, data=payload)
    else:
        response = requests.get(url)

    now = time.strftime("%Y%m%d")
    filename = location + "-" + now + ".json"
    with open("/home/ksiler/msrfree/data/" + filename, "wb") as f:
        f.write(response.content)


if __name__ == "__main__":
    main()
