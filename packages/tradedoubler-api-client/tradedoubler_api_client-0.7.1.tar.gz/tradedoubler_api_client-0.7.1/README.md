# tradedoubler_api_client
Unofficial simple python wrapper for Tradedoubler API

## instalation
`pip install tradedoubler-api-client`

## example of usage
```python
from tradedoubler_api_client import Tradedoubler

td = Tradedoubler('relative_path_to_credentials.json')

pending_sales = td.pending_sales()
list_pendint_sales = td.pending_sales().get_all()
list_pendint_sales.csv(path='csv')
list_pendint_sales.json(path='json')
```
[more examples...](https://github.com/adamczarnecki/tradedoubler_api_client/tree/master/examples)

### credentials.json schema:

```json
{
    "td_secret": "[secret]",
    "td_id": "[id of application]",
    "td_user_name": "[email@domain.com]",
    "td_userpassword": "[passToAcount]"
}
```
visit [solutions.tradedoubler.com/tools/api-client/index.php](http://solutions.tradedoubler.com/tools/api-client/index.php) to get app id and secret.

## List of reasons to deny transaction
| code | reason                                                                     |
|:----:|----------------------------------------------------------------------------|
|   6  | Application/Credit Check Denied                                            |
|   7  | Fraudulent Order/Application                                               |
|   8  | Duplication / Sale Accredited to Another Source                            |
|   9  | Order Yet To Be Fulfilled                                                  |
|  10  | Returned goods                                                             |
|  13  | Invalid Lead                                                               |
|  14  | Order Cancelled                                                            |
|  16  | Insuffient Information (Applicable only for untracked sales)               |
|  17  | Order not found (Applicable only for untracked sales)                      |
|  18  | Sale Already Accredited to Publisher (Applicable only for untracked sales) |
|  19  | Voucher incorrectly used                                                   |
