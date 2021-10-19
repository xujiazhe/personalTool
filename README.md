# chrome script


## read
```css

::selection {
    color: blue;
    background-color: #FAF9DE;
    /*background-color:#fff7f7;*/
    outline: darkblue;
    font-family: 'Sarasa Term Slab HC Light','iosevka Light' !important;
    outline-style: dashed;
    outline-width: 2px;
}

p > ::selection  {
   /*color: darkblue;*/
}

```

## flee
```javascript

// @include    *://*.zhihu.com/*
// @include    *://*.youtube.com/*
// @include    *://*.bilibili.com/*
// ==/UserScript==

(function() {
    'use strict';
    let table = {
        "zhihu.com/":"https://zhuanlan.zhihu.com/p/25516905",
        "youtube.com/":"https://www.youtube.com/feed/channels",
        "bilibili.com/":"https://space.bilibili.com/20259914",
        "weibo.com":"https://weibo.com/mygroups?gid=110001571368870"
    }
    let href = location.href;
    if(location.pathname !== "/"){
        return;
    }
    for(let pattern in table){
        if(href.indexOf(pattern) !== -1){
            let url = table[pattern]
            location.href = url;
            break;
        }
    }
    // Your code here...
})();
```
