# `xmu`

# API Tutorial

The basic API is very simple. It consists of one function.

```python
>>> import xmu
>>> xmu_string = """
... [   
...     p[ This is a paragraph. ]
...     p[ [Hello, ] $[name] [!] ]
... ]
... """
>>> html = xmu.parse(xmu_string, context={"name": "John"})
>>> print(html)
```
```html
<p> This is a paragraph. </p>
<p>Hello, 
John
!</p>
```


# Feature example

#### Input
```xmu
[
    header(1)[
        Hello, world!
    ]
    style[
        $text-color: red;
        color: $text-color;
        border-color: darken($text-color, 10%);
    ][
        table(3, 2)[
            [ Lorem ] [ Ipsum ] [ Dolor ]
            [ Sit   ] [ Amet  ] [:raw \_/__^[.]w[.]^__\_/ rrr:]
        ]
     ]
]
```

#### Output
```
<h1> Hello, world! </h1>
<style>#lwunnaxwqbgasdhs {
    color: red;
    border-color: #cc0000; }
</style>
<emu-styled id=lwunnaxwqbgasdhs>
    <table>
        <tr>
            <td> Lorem </td>
            <td> Ipsum </td>
            <td> Dolor </td>
        </tr>
        <tr>
            <td> Sit </td>
            <td> Amet </td>
            <td> \_/__^[.]w[.]^__\_/ </td>
        </tr>
    </table>
</emu-styled>
```