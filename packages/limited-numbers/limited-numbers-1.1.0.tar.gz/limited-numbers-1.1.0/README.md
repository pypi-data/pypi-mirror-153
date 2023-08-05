# Limited Numbers

A simple library made with Python

## Installation

### Windows

```sh
pip3 install limited-numbers
```

### Linux

```sh
python3 -m pip install limited-numbers
```

## Usage

You can use to simulate number overflows (useful if you wanna simulate x-bit numbers)

```py
from limited_numbers import Int

#let's simulate a 8-bit number
number = Int(255) 
'''Int takes 1 positional and 2 keyword arguments. The positional parameter is the number limit after which overflows. The other 2 are to set the number to else than 0 and the other is the lower limit (begin_from)'''

#increase by 1
number += 1

#loop until it overflows
while number!=0:
    print('Number: {}').format(number.get()) #or number.number 
    #PS. Used .format above so that the code is highlighted in Markdown
    number+=1
```

You can also subtract from the number