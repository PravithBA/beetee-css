# BeeTee Css
A css pre processor which has features such as ranges, variables, etc to make your css experience better

# Syntax
## Ranges
```

    /* Declaration of a range */
    color = | black, white |;

    .c-$color {
        color: $color;
    }

```
Result:
```css

    .c-black {

        color: black;

    }

    .c-white {

        color: white;

    }

```
There can also be multiple ranges in a single block, for example:
```

bg_color_range = | black, white |;
color_range = | red, pink |;

.bc-$bg_color_range-$color_range{
    background-color : $bg_color_range;
    color : $color_range
}

```
Result:
```css

.bc-black-red {

    background-color: black;
    color: red;

}

.bc-black-pink {

    background-color: black;
    color: pink;

}

.bc-white-red {

    background-color: white;
    color: red;

}

.bc-white-pink {

    background-color: white;
    color: pink;

}

```

More features comming soon