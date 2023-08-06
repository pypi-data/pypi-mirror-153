[GitHub Pages](https://jameskabbes.github.io/imessage)<br>
[PyPI](https://pypi.org/project/kabbes-imessage)

# imessage
Python tools for sending iMessage/SMS message from a Mac

<br> 

# Installation
`pip install kabbes_imessage`

<br>

# Running main

```
python -m kabbes_imessage
```

<br>

# Usage
For more in-depth documentation, read the information provided on the Pages. Or better yet, read the source code.

```python
import kabbes_imessage
```

```python
message_obj = kabbes_imessage.Message( 'This is a test message' ) 
message_obj.PhoneNumbers.make_PhoneNumber( '123-555-5555', medium = 'SMS' )
message_obj.PhoneNumbers.make_PhoneNumber( '234-555-5555', medium = 'iMessage' )

message_obj.send()
```

```
>>> Sending SMS message This is a test message to type:	PhoneNumber,	formatted:	+11235555555...
Sending iMessage message This is a test message to type:	PhoneNumber,	formatted:	+12345555555...
```


<br>

# Author
James Kabbes

