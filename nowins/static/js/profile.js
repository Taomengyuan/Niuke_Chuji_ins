$(function () {
    var oExports = {
        initialize: fInitialize,
        // 渲染更多数据
        renderMore: fRenderMore,
        // 请求数据
        requestData: fRequestData,
        // 简单的模板替换
        tpl: fTpl
    };
    // 初始化页面脚本
    oExports.initialize();

    function fInitialize() {
        var that = this;
        // 常用元素
        that.listEl = $('div.js-image-list');
        // 初始化数据
        that.uid = window.uid;
        that.page = 1;
        <!-- 添加js 如果修改成2，则每次点击更多增加显示2个图片-->
        <!-- 添加js 修改成3 每次点击更多增加显示3个图片-->
        that.pageSize = 3;
        that.listHasNext = true;
        // 绑定事件
        $('.js-load-more').on('click', function (oEvent) {
            var oEl = $(oEvent.currentTarget);
            var sAttName = 'data-load';
            // 正在请求数据中，忽略点击事件
            if (oEl.attr(sAttName) === '1') {
                return;
            }
            // 增加标记，避免请求过程中的频繁点击
            oEl.attr(sAttName, '1');
            that.renderMore(function () {
                // 取消点击标记位，可以进行下一次加载
                oEl.removeAttr(sAttName);
                // 没有数据隐藏加载更多按钮
                !that.listHasNext && oEl.hide();
            });
        });
    }

    function fRenderMore(fCb) {
        var that = this;
        // 没有更多数据，不处理
        if (!that.listHasNext) {
            return;
        }
        that.requestData({
            uid: that.uid,
            page: that.page + 1,
            pageSize: that.pageSize,
            call: function (oResult) {
                // 是否有更多数据
                that.listHasNext = !!oResult.has_next && (oResult.images || []).length > 0;
                // 更新当前页面
                that.page++;
                // 渲染数据
                var sHtml = '';
                $.each(oResult.images, function (nIndex, oImage) {
                    sHtml += that.tpl([
                    //点击“更多”按钮之后，显示的框架格式
                    // 将profile.html的其中一个单括号改成井号,并把image.去掉即可
                    //     '<a class="item" href="/image/{{ image.id }}">', // 将其中一个单括号改成井号
                    //         '<div class="img-box">',
                    //             '<img src="{{ image.url }}">',
                    //         '</div>',
                    //         '<div class="img-mask"></div>',
                    //         '<div class="interaction-wrap">',
                    //             <!--评论的长度-->
                    //             '<div class="interaction-item"><i class="icon-comment"></i> {{ image.comments|length  }}</div>',
                    //         '</div>',
                    //     '</a>'].join(''), oImage);



                        '<a class="item" href="/image/#{id}">',
                            '<div class="img-box">',
                                '<img src="#{url}">',
                            '</div>',
                            '<div class="img-mask"></div>',
                            '<div class="interaction-wrap">',
                                '<div class="interaction-item"><i class="icon-comment"></i>#{comment_count}</div>',
                            '</div>',
                        '</a>'].join(''), oImage);
                });
                sHtml && that.listEl.append(sHtml);
            },
            error: function () {
                alert('出现错误，请稍后重试');
            },
            always: fCb
        });
    }

    function fRequestData(oConf) {
        var that = this;
        var sUrl = '/profile/images/' + oConf.uid + '/' + oConf.page + '/' + oConf.pageSize + '/';
        $.ajax({url: sUrl, dataType: 'json'}).done(oConf.call).fail(oConf.error).always(oConf.always);
    }

    function fTpl(sTpl, oData) {
        var that = this;
        sTpl = $.trim(sTpl);
        return sTpl.replace(/#{(.*?)}/g, function (sStr, sName) {
            return oData[sName] === undefined || oData[sName] === null ? '' : oData[sName];
        });
    }
});