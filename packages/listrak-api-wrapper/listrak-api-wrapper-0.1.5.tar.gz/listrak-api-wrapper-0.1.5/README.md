# listrak-api-wrapper
This is a wrapper for the [Listrak API](https://api.listrak.com/email). This wrapper is meant to be used with the Listrak /email API

Note: This is a work in progress, not all endpoints are functional at the moment. Please see bottom of page for details.

# Installation Instructions
## Install Requirements (If Necessary)
* The "requests" library is required to use this package.

```
pip install requests
```

## Install Library
```
pip install listrak-api-wrapper
```

# Usage Instructions
## Create a Client
Note: This example assumes the LISTRAK_CLIENT_ID and LISTRAK_CLIENT_SECRET API credentials are saved as environment variables.
```
import os
from listrak import listrak


# Create listrak_api obj that will be used to authenticate with Listrak API
client_id = os.getenv("LISTRAK_CLIENT_ID")
client_secret = os.getenv("LISTRAK_CLIENT_SECRET")

listrak_api = listrak.Listrak(client_id, client_secret)
```
Example showing how to get all lists associated with your account.
```
lists = listrak_api.uri_list.get_all_lists()
```

### Working
- CONTACT
- LIST
- LISTIMPORT
- SEGMENTATIONFIELD
- SEGMENTATIONFIELDGROUP

### Planned
- CAMPAIGN (N/A)
- CONVERSATION (N/A)
- CONVERSATIONMESSAGE (N/A)
- CONVERSATIONMESSAGEACTIVITY (N/A)
- CONVERSATIONMESSAGELINK (N/A)
- CONVERSATIONMESSAGELINKCLICKER (N/A)
- CONVERSATIONMESSAGESUMMARY (N/A)
- CONVERSATIONSUMMARY (N/A)
- EVENT (N/A)
- EVENTGROUP (N/A)
- FOLDER (N/A)
- IPPOOL (N/A)
- LISTIMPORTCONTACT (N/A)
- LISTIMPORTSTATUS (N/A)
- LISTIMPORTSUMMARY (N/A)
- MESSAGE (N/A)
- MESSAGEACTIVITY (N/A)
- MESSAGELINK (N/A)
- MESSAGELINKCLICKER (N/A)
- MESSAGESTATUS (N/A)
- MESSAGESUMMARY (N/A)
- SAVEDAUDIENCE (N/A)
- SAVEDMESSAGE (N/A)
- TRANSACTIONALMESSAGE (N/A)
- TRANSACTIONALMESSAGEACTIVITY (N/A)
- TRANSACTIONALMESSAGERESEND (N/A)