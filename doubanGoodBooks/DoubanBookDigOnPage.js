/**
 * Created by xujiazhe on 2019/3/12.
 * 豆瓣书
 *  页面好书过滤
 *  本地有没有
 *    有
 *      打开预览
 *    没有
 *      网上搜索 下载/网络标记  微盘 爱问 谷歌图书 百度图书 网络信息
 *      一键转存到 Git库里
 *
 *  保存热门tag 或者 搜索
 *
 * 本地书籍chrome 浏览
 *      豆瓣评分 样式展示. 打开.
 *
 * 书籍并库
 *
 * 专业目录
 *  选择 专业课表
 *
 *  书籍阅读器
 *      高亮与朗读
 */

RATE_SCORE_LIMIT = 9.5;
RATE_COUNT_LIMIT = 200;
PAGE_LOAD_COUNT = 10;

//let $$ = document.querySelectorAll;
//let $ = document.querySelector;

class DoubanBook {
    constructor(bookDomEle) {
        if (bookDomEle.dealed) {
            return null;
        }
        this.bookDomEle = bookDomEle;

        try {
            this.parse(bookDomEle);
        } catch (e) {
            this.bookDomEle.style['background-color'] = 'yellow';
            return null;
        }
        bookDomEle.dealed = true;
    }

    get isGoodEnough() {
        return RATE_SCORE_LIMIT > 0 ?
            this.rate >= RATE_SCORE_LIMIT :
            this.rate <= -RATE_SCORE_LIMIT;
    }

    get isVoteCntEnough() {
        return this.rat_cnt >= RATE_COUNT_LIMIT;
    }

    selfCheck(toggle) {
        if (this.isGoodEnough && this.isVoteCntEnough) {
            return true;
        } else {
            if (toggle) this.bookDomEle.style.display = "none";
            else this.bookDomEle.remove();
            return false;
        }
    }

    // 本地书库 检查
    viewLocal() {

    }

    addSearch() {
        let pdf_link = "https://www.google.com/search?q=" +
            encodeURIComponent("百度网盘  " + this.name + " ") + "pdf";
        this.cover.href = pdf_link;
        // 微盘搜索
    }
}

class SearchBook extends DoubanBook {
    constructor(bookDomEle) {
        super(bookDomEle);
    }

    parse(ele) {
        const rate_ele = $('.rating-info .rating_nums', ele)[0];
        this.rate = rate_ele.textContent;
        this.name = $$('.title a', ele)[0].textContent;
        this.link = "" + ($('.title a', ele)[0].href);
        this.cover = $$('.pic .nbg', ele)[0];
        this.rat_cnt = /\((\d+)人评价\)/.exec(rate_ele.nextElementSibling.textContent)[1];
        this.rat_cnt = parseInt(this.rat_cnt);
    }
}

class TagBook extends DoubanBook {
    constructor(bookDomEle) {
        super(bookDomEle);
    }

    parse(ele) {
        this.rate = $('.rating_nums', ele)[0].textContent;
        this.name = $('a.title', ele)[0].textContent;
        this.link = "" + ($('a.title', ele)[0].href);
        this.cover = $('dt a', ele)[0];

        this.rat_cnt = RATE_COUNT_LIMIT;

        this.rate = parseFloat(this.rate);
    }
}

const PageConfig = {
    BookSearch: {
        urlReg: /search\?cat=1001&q=([\w\u4e00-\u9fa5\%]+)/,
        BookSelector: '.search-result > div.result-list > div.result',
        BookClass: SearchBook,
        buttonSelector: ".j.a_search_more"
    },
    TagList: {
        urlReg: /tag\/([\w\u4e00-\u9fa5\%]+)/,
        BookSelector: '#book > dl',
        BookClass: TagBook,
        buttonSelector: ".load-more"
    }
};

class DigBookOnPage {
    static dom = document;
    static BookContainer = {}
    static GOOD_BOOK_LIST = []; //objects


    static pageConfig = {
        urlReg: /url匹配/,
        BookSelector: '页面选择器',
        BookClass: "书解析类",
        buttonSelector: "加载按钮选择器"
    };

    constructor(dom) {
        DigBookOnPage.dom = document;
        DigBookOnPage.BookContainer = $(DigBookOnPage.selector, DigBookOnPage.dom).parentNode;
    }

    static loadConfigByPage() {
        // 不同的页面, 不同的 书列表项 解析方式
        let onDoubanSite = /www.douban\.com/.test(window.location.host);
        if (!onDoubanSite) {
            return;
        }
        const subUrl = window.location.pathname + window.location.search;

        for (const pageType in PageConfig) {
            let config = PageConfig[pageType];
            const res = config.urlReg.exec(subUrl);
            if (res === null) continue;
            this.pageConfig = config;
            this.BookContainer = $(DigBookOnPage.selector, DigBookOnPage.dom).parentNode; //dom
            if (!this.domFormatTest()) {
                console.error("也许格式不对")
            }

            return pageType;
        }
    }

    static domFormatTest() {
        try {
            let bookEle = $(this.pageConfig.BookSelector, this.dom);

            new this.pageConfig.BookClass(bookEle);
            return true;
        } catch (e) {
            return false;
        }
    }


    static loadGoodBook(conf) {
        // 如果 以前 有结果, 直接加载

        // const subUrl = window.location.pathname + window.location.search;
        // let bookids = localStorage.getItem(subUrl);

        let pageCnt = conf && conf.pageCnt;
        if (typeof  pageCnt !== undefined) {
            this.pageCnt = pageCnt;
        }
        let bookList = document.querySelectorAll(this.pageConfig.BookSelector);
        bookList = Array.prototype.map.call(bookList,
            (ele) => {
                let book = new this.pageConfig.BookClass(ele);
                if (book !== null && book.selfCheck()) {
                    return book;
                } else {
                    return null;
                }
            }).filter(
            (book) => book !== null
        );

        this.GOOD_BOOK_LIST = this.GOOD_BOOK_LIST.concat(bookList);

        //let button = document.querySelector(this.pageConfig.buttonSelector);
        //let event = new Event('click');
        //button.dispatchEvent(event);
        jQuery(this.pageConfig.buttonSelector).trigger('click');


        // 定时滚页
        if (this.pageCnt > 0) {
            console.error(" this.pageCnt = ", this.pageCnt)
            setTimeout(this.loadGoodBook.bind(this), 1500);
            this.pageCnt -= 1;
        }
    }

    static sort(onPage) {
        this.GOOD_BOOK_LIST.sort((a, b) => {
                let ba = a.rate;
                let bb = b.rate;
                return ba < bb ? 1 : (ba > bb ? -1 : 0);
            }
        );

        if (onPage) {
            let bookDomList = this.GOOD_BOOK_LIST.map((book) => book.bookDomEle);
            this.BookContainer.removeAll(); //??
            this.BookContainer.appendChild(bookDomList);
        }
    };

    static save() {
        let bookids = this.GOOD_BOOK_LIST.map((book) => {
            let bookDomEle = book.bookDomEle;
            switch (this.PageType) {
                case 'BookSearch':
                    // "moreurl(this,{i: '8', query: 'python', from: 'dou_search_book', sid: 26709315, qcat: '1001'})" 词法解析
                    const a = $(".title a", ele)[0];
                    return /sid: (\d+),/.exec(bookDomEle.getAttribute("onclick"))[1];

                case 'TagList':
                    // https://book.douban.com/subject/30293801/?from=tag
                    const a = $("dd a.title", ele)[0];
                    return /subject\/(\d+)\/\?from=tag/.exec(a.href)[1];
            }
        });

        const subUrl = window.location.pathname + window.location.search;
        localStorage.setItem(subUrl, bookids);

        return {
            subUrl: subUrl,
            bookids: bookids,
            // 页数
        };
        //  /tag/计算机  ["30293801", "30139217", "1148282", "26912767", "5333562", "30259573", "30329536", "1230413", "26197294", "2061116", "26899701", "21323941", "3707841", "21706191", "5387403"]
    }
}

DigBookOnPage.loadConfigByPage();
DigBookOnPage.loadGoodBook({
    pageCnt: 10
});
