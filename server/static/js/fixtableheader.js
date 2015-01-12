/*
* Auther:Mike.Jiang
* Email: dataadapter@hotmail.com
* Date: 2012-09-05
*/
/*
主要思想：
1>将原有的TABLE中的THEAD元素复制一份放在一个新的DIV(fixedheadwrap)中
2>设置这个fixedheadwrap为绝对位于原来的TABLE的THEAD位置
*/
(function ($) {
    $.fn.extend({
        FixedHead: function (options) {
            var op = $.extend({ tableLayout: "auto" }, options);
            return this.each(function () {
                var $this = $(this); //指向当前的table
                var $thisParentDiv = $(this).parent(); //指向当前table的父级DIV，这个DIV要自己手动加上去
                $thisParentDiv.wrap("<div class='fixedtablewrap'></div>").parent().css({ "position": "relative" }); //在当前table的父级DIV上，再加一个DIV
                var x = $thisParentDiv.position();

                var fixedDiv = $("<div class='fixedheadwrap' style='clear:both;overflow:hidden;z-index:2;position:absolute;' ></div>")
                    .insertBefore($thisParentDiv)//在当前table的父级DIV的前面加一个DIV，此DIV用来包装tabelr的表头
                    .css({ "width": $thisParentDiv[0].clientWidth, "left": x.left, "top": x.top });

                var $thisClone = $this.clone(true);
                $thisClone.find("tbody").remove(); //复制一份table，并将tbody中的内容删除，这样就仅余thead，所以要求表格的表头要放在thead中
                $thisClone.appendTo(fixedDiv); //将表头添加到fixedDiv中

                $this.css({ "marginTop": 0, "table-layout": op.tableLayout });
                //当前TABLE的父级DIV有水平滚动条，并水平滚动时，同时滚动包装thead的DIV
                $thisParentDiv.scroll(function () {
                    fixedDiv[0].scrollLeft = $(this)[0].scrollLeft;
                });

                //因为固定后的表头与原来的表格分离开了，难免会有一些宽度问题
                //下面的代码是将原来表格中每一个TD的宽度赋给新的固定表头
                var $fixHeadTrs = $thisClone.find("thead tr");
                var $orginalHeadTrs = $this.find("thead");
                $fixHeadTrs.each(function (indexTr) {
                    var $curFixTds = $(this).find("td");
                    var $curOrgTr = $orginalHeadTrs.find("tr:eq(" + indexTr + ")");
                    $curFixTds.each(function (indexTd) {
                        $(this).css("width", $curOrgTr.find("td:eq(" + indexTd + ")").width());
                    });
                });
            });
        }
    });
})(jQuery);