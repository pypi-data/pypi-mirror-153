# Pigeonly Address

For standardizing addresses.

For more information on USPS API keys and terms, see [here](https://www.usps.com/business/web-tools-apis/)
### Installation

`pip install pigeonly-address`

#### Example Usage

```python

from pigeonly_address import AddressService, StandardizeAddressError

# Example usage
try:
    address = {
        "name": "aj patel",
        "line_one": "5 reynolds",
        "line_two": "#3",
        "city": "New bedford",
        "governing_district": "MA",
        "postal_code": "02744",
        "country": "USA"
    }
    standardized_addr = AddressService("USPS_API_KEY").standardize_address(**address)
    print(standardized_addr)
    # Example success
    # {   
    #     "name": "AJ PATEL",
    #     "line_one": "5 REYNOLDS ST",
    #     "line_two": "APT 3",
    #     "city": "NEW BEDFORD",
    #     "governing_district": "MA",
    #     "postal_code": "02740",
    #     "country": "US",
    #     "meta": None
    # }
    # ------------------------------------------
    # A `meta` field is also returned.
    # Usually meta is None.
    # But sometimes, like if an address is correct,
    # but the address apt # is not verified,
    # a message returns => meta["message"]
    meta = standardized_addr.pop("meta")
    if meta and meta.get("message"):
        print(meta["message"])
    

except StandardizeAddressError as e:
    # Example str(e) == "Address Not Found"
    print(e)
```

# USPS Docs

For US Addresses, it uses the USPS API when possible.

- [USPS Address Docs](https://www.usps.com/business/web-tools-apis/address-information-api.htm#)
- [USPS Docs HOME](https://www.usps.com/business/web-tools-apis/documentation-updates.htm)
