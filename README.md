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

# Language reference

## Plain text or HTML

You can include arbitrary text inside `[` and `]`,
given that it doesn't contain any `[`.

```
[ Hello ]
```

```
[ <div id="hello"></div> ]
```

However, you can't just include a tag inside plain text:
```
[ Wrong: ]
[ hello, it[world]! ]
```

But you can put a sequence of tags inside the brackets.

```
[ [hello,] it[world] [!] ]
```

In general, you can put either plain text or a sequence
of tags inside the brackets.

You can communicate structure by using brackets.

## Arbitrary plain tags

You can create any tag you want using `!`:
```
[ !kbd[Ctrl + C] ]
```
```html
<kbd>Ctrl + C</kbd>
```

## Predefined tags

Some tags are defined as language builtins.

```
[
    p [
        This is a paragraph
    ]
]
```

Currently supported tags: `p`, `pre`, `it`, `bf`, `^` (superscript), `_` (subscript)


The purpose of this group of language constructs is to allow rendering to different targets: LaTeX, an abstract syntax tree etc. in the future.

## Raw text

```
[:raw
    This text preserves original
        Indentation
            And can [use]
                [square] ]]]brackets[
rrr:]
```

**rawrrr**

## Comments

```
[
    comment[Comment]
    todo[Comment]
    bug[Comment]
    doc[Comment]
]
```
```html
    <!--comment:Comment-->
    <!--todo:Comment-->
    <!--bug:Comment-->
    <!--doc:Comment-->
```

## Links

```
[
    a[https://my-site.com][My site!]
]
```

## ID and class specifiers

```
    #myDiv [
        hello
    ]
    .some of my classes [
        world
    ]
```

```html
    <div id="myDiv">hello</div>
    <div class="some of my classes">hello</div>
```

## Headers

```
[
    header(1)[Lorem ipsum]
    header(2)[Dolor sit amet]
]
```

```html
    <h1>Lorem ipsum</h1>
    <h2>Dolor sit amet</h2>
```

## Python expressions

```
[
    $["foo" + "!"*3 + "bar"]
    $[:raw
        [1, 2, 3][1]
    rrr:]
]
```

```html
foo!!!bar
2
```

## Parse the result of a python expression

```
[   
    $xmu[:raw "[ p[Paragraph] ]" rrr:]
]
```

```html
<p>Paragraph</p>
```

```
[   
    $xmu[:raw "[ $xmu['p[Paragraph]'] ]" rrr:]
]
```

```html
<p>Paragraph</p>
```

## Tables

```
[
    table(3, 2)[
        [ Lorem ] [ Ipsum ] [ Dolor ]
        [ Sit   ] [ Amet  ] [       ]
    ]
]
```

```html
   <table>
        <tr>
            <td> Lorem </td>
            <td> Ipsum </td>
            <td> Dolor </td>
        </tr>
        <tr>
            <td> Sit   </td>
            <td> Amet  </td>
            <td>       </td>
        </tr>
    </table>
```

## Constants

To see the list of all constants, take a look at
`/xmu/extensions/text_formatting.py`

A constant begins with a `?`.

```
[
    [XMU] ?-- [an extensible markup language]
]
```

```html
XMU &emdash; an extensible markup language
```

## Styling

Anonymous styles are now very powerful!
XMU uses SCSS (a flavour of SASS) to compile
inline styles.

```
style [:raw
    color: red;
    font-family: 'Comic Sans MS';
rrr:][
    header(1)[
        Solving FizzBuzz by the means of a DSL
    ]
]
```

Basically, XMU creates a random ID and creates
a standalone style for it.

```html
<style>#aspefpsnfglktjgu {
    color: red;
    font-family: 'Comic Sans MS'; }
</style>
<emu-styled id=aspefpsnfglktjgu>
    <h1>Solving FizzBuzz by the means of a DSL</h1>
</emu-styled>
```

The advantage of using SASS is that you can define a nested style:

```
style [:raw
    color: red;
    font-family: 'Comic Sans MS';
    b {
        color: blue;
    }
rrr:][
    header(1)[
        Solving FizzBuzz by the means of a DSL
    ]
    bf[ This text will be blue]
]
```

```html
<style>
    #jghejijhvudjuhvg {
        color: red;
        font-family: 'Comic Sans MS'; }
        #jghejijhvudjuhvg b {
            color: blue;}
</style>
<emu-styled id=jghejijhvudjuhvg>
    <h1>Solving FizzBuzz by the means of a DSL</h1>
    <b> This text will be blue </b>
</emu-styled>
```

## Jinja2

```
%[ user.name ]
```

```html
{{ user.name }}
```

---
```
%extends[website.com]
```

```html
{% extends "website.com" %}
```
---
```
%block(footer)[ header(2)[All lefts reserved] ]
```

```
{% block footer %}
<h2>All lefts reserved</h2>
{% endblock %}
```

## FontAwesome

```
fas[home]
```
```html
<i class="fas fas-home"></i>
```

# Extending the language

Tutorial coming soon