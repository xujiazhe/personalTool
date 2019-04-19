// 打出大约8.5分的搜索链接
// tag_book(-8.5); // 在不到8.5分的书中 挑挑捡捡

// console.table(tuples, [0, 1 ,2])

function tag_ele_parser(ele) {
    var rate = $('.rating_nums', ele)[0].textContent;
    var name = $('a.title', ele)[0].textContent;
    var link = "" + ($('a.title', ele)[0].href);
    var a = $('dt a', ele)[0];
    var rat_cnt = 200;
    var search_link = "https://www.google.com/search?q=" +
        encodeURIComponent("百度网盘  " + name + " ") + "pdf";


    return [rate, name, search_link, rat_cnt, a]
}

function cat_ele_parser(ele) {
    var rate_ele = $('.rating-info .rating_nums', ele)[0];
    var rate = rate_ele.textContent;
    var name = $$('.title a', ele)[0].textContent;
    var link = "" + ($('.title a', ele)[0].href);
    var a = $$('.pic .nbg', ele)[0];
    var rat_cnt = /\((\d+)人评价\)/.exec(rate_ele.nextElementSibling.textContent)[1];
    rat_cnt = parseInt(rat_cnt);

    var search_link = "https://www.google.com/search?q=" +
        encodeURIComponent("百度网盘  " + name + " ") + "pdf";

    return [rate, name, search_link, rat_cnt, a]
}

var tuples = [];

var filters = {
    'tag': {
        func: tag_ele_parser,
        selector: '#book > dl'
    },
    'cat': {
        func: cat_ele_parser,
        selector: '.search-result > div.result-list > div.result'
    }
};

function book_filter(rat, type) {
    tuples = [];
    var match = function (rat) {
        return rat > 0 ?
            function (rate) {
                return rate >= rat;
            } : function (rate) {
                return rate < -rat;
            }
    }(rat);
    var selector_str = filters[type].selector;
    var parser_func = filters[type].func;

    $$(selector_str).forEach(function (ele) {
        ele.style.display = "";
        try {
            var ret = parser_func(ele);
            if (ret === undefined) return;
            var [rate, name, search_link, rat_cnt, a] = ret;
            var link = a.href;
            var rate = parseFloat(rate);
            a.href = search_link;
            if (!match(rate) || rat_cnt < 200) {
                ele.style.display = "none";
                return;
            }

        } catch (e) {
            rat > 0 ? ele.style.display = 'none' : '';
            return;
        }
        //console.log(name, "   ", rate);
        tuples.push([rate, name, search_link, link]);
    });

    tuples.sort(function (a, b) {
        a = a[0];
        b = b[0];

        return a < b ? 1 : (a > b ? -1 : 0);
    });

    rat > 0 ? tuples.forEach(function (tuple) {
        var rate = tuple[0];
        var name = tuple[1];
        var link = tuple[2];
        var url = tuple[3];
        //console.log(name, "  ", rate, link);
    }) : 0;
    FinalResult = tuples;
    console.table(FinalResult);
}

// book_filter(8.5, 'cat'); // 打出大约8.5分的搜索链接
// book_filter(-8.5); // 在不到8.5分的书中 挑挑捡捡

function douban_book(rate){
    if(! /www.douban\.com/.test(window.location.host) ){
        return ;
    }

    var sub_url = window.location.pathname + window.location.search;

    var cat_reg = /search\?cat=1001&q=([\w\u4e00-\u9fa5\%]+)/;
    var tag_reg = /tag\/([\w\u4e00-\u9fa5\%]+)/;

    var re_array = {
        cat: cat_reg,
        tag: tag_reg
    };
    for(var type in re_array){
        var res = re_array[type].exec(sub_url);
        if( res === null ) continue;
        book_filter(rate, type);
        break;
    }
};


douban_book(8.9);

// console.table(tuples, [0, 1 ,2])
