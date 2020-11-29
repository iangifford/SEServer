### Endpoints
# Account Creation
`/accountcreate`
__Args:__
- `is_owner`
  - type: Boolean
- `is_sitter`
  - type: Boolean
- `is_admin`
  - type: Boolean
- `is_shelter`
  - type: Boolean
- `first_name`
  - type: String
- `last_name`
  - type: String
- `email`
  - type: String
- `password`
  - type: String

__Returns:__
- "400 - Bad account parameters."
- "201 - {'id':'`(uuid4: String)`'}"

# Account Info Retrieval
`/accountinfo`
__Args:__
- `uuid`
  - type: String

__Returns:__
- "400 - Invalid Account id."
- "{'is_owner':`(is_owner: Boolean)`,
    'is_sitter':`(is_sitter: Boolean)`,
    'is_shelter':`(is_shelter: Boolean)`,
    'is_admin':`(is_admin: Boolean)`, 
    'first_name':`(first_name: String)`,
    'last_name':`(last_name: String)`,
    'email':`(email: String)`}