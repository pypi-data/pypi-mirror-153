/*
 * jQuery Autocomplete plugin 1.1
 *
 * Copyright (c) 2009 Jörn Zaefferer
 *
 * Dual licensed under the MIT and GPL licenses:
 *   http://www.opensource.org/licenses/mit-license.php
 *   http://www.gnu.org/licenses/gpl.html
 *
 * Revision: $Id: jquery.autocomplete.js 15 2009-08-22 10:30:27Z joern.zaefferer $
 */

;(function($) {

var constants = {
    WINDOW_PADDING: 20,
    LR_POSITION: {},
    CR_POSITION: {},
    TB_POSITION: {}
};

$.fn.extend({
    autocomplete: function(urlOrData, options) {

        var isUrl = typeof urlOrData == "string";

        options = $.extend({}, $.Autocompleter.defaults, {
            url: isUrl ? urlOrData : null,
            delay: isUrl ? $.Autocompleter.defaults.delay : 10,
            data: isUrl ? null : urlOrData,
            scroll: options && (options.scroll || options.flexible),
            max: (options && options.flexible) ? 0 :
                 (options && options.scroll) ? 10 : 150
        }, options);

        // if highlight is set to false, replace it with a do-nothing function
        options.highlight = options.highlight || function(value) { return value; };

        // if the formatMatch option is not specified, then use formatItem for backwards compatibility
        options.formatMatch = options.formatMatch || options.formatItem;

        return this.each(function() {
            new $.Autocompleter(this, options);
        });

    },
    result: function(handler) {
        return this.bind("result", handler);
    },
    search: function(handler) {
        return this.trigger("search", [handler]);
    },
    flushCache: function() {
        return this.trigger("flushCache");
    },
    setOptions: function(options){
        return this.trigger("setOptions", [options]);
    },
    unautocomplete: function() {
        return this.trigger("unautocomplete");
    }
});

$.Autocompleter = function(input, options) {

    var

        KEY = {
            UP: 38,
            DOWN: 40,
            DEL: 46,
            TAB: 9,
            RETURN: 13,
            ESC: 27,
            COMMA: 188,
            PAGEUP: 33,
            PAGEDOWN: 34,
            BACKSPACE: 8
        },

        // Create $ object for input element
        $input = $(input).attr("autocomplete", "off").addClass(options.inputClass),

        jqxhr,

        prevTrans = {},

        curTerm,

        timeout,

        selectedResult = $input.val(),

        previousResult = selectedResult,

        cache = $.Autocompleter.Cache(options),

        lastKeyPressCode,

        config = {
            mouseDownOnSelect: false,
            hasFocus: 0
        },

        select = $.Autocompleter.Select(options, input, selectCurrent, config),

        blockSubmit,

        isKbNavEnabled = options.isKbNavEnabled,

        $button;

    if (options.button) {

        $button = $('<div class="ac_button" />');

        $button.insertAfter($input);

        $button.bind('mousedown', function() {
            return false;
        });

        $button.bind('click', function() {
            if (select.visible()) {
                hideResultsNow();
            } else {
                $input.trigger('showList');
            }
            return false;
        });

    }

    // only opera doesn't trigger keydown multiple times while pressed, others don't work with keypress at all
    $input.bind("keydown.autocomplete", function(event) {
        // a keypress means the input has focus
        // avoids issue where input had focus before the autocomplete was applied
        config.hasFocus = 1;
        // track last key pressed
        lastKeyPressCode = event.keyCode;
        switch(event.keyCode) {

            case KEY.UP:
                if (isKbNavEnabled) {
                    event.preventDefault();
                    if ( select.visible() ) {
                        select.prev();
                    } else {
                        onChange(0, true);
                    }
                }
                break;

            case KEY.DOWN:
                if (isKbNavEnabled) {
                    event.preventDefault();
                    if ( select.visible() ) {
                        select.next();
                    } else {
                        onChange(0, true);
                    }
                }
                break;

            case KEY.PAGEUP:
                if (isKbNavEnabled) {
                    event.preventDefault();
                    if ( select.visible() ) {
                        select.pageUp();
                    } else {
                        onChange(0, true);
                    }
                }
                break;

            case KEY.PAGEDOWN:
                if (isKbNavEnabled) {
                    event.preventDefault();
                    if ( select.visible() ) {
                        select.pageDown();
                    } else {
                        onChange(0, true);
                    }
                }
                break;

            // matches also semicolon
            case KEY.TAB:
            case KEY.RETURN:
                if ( isKbNavEnabled && selectCurrent() ) {
                    // stop default to prevent a form submit, Opera needs special handling
                    event.preventDefault();
                    blockSubmit = true;
                    return false;
                }
                break;

            case KEY.ESC:
                select.hide();
                break;

            default:
                clearTimeout(timeout);
                timeout = setTimeout(onChange, options.delay);
                break;
        }
    }).bind('focus', function(){
        // track whether the field has focus, we shouldn't process any
        // results if the field no longer has focus
        config.hasFocus++;

    }).bind('blur', function() {

        config.hasFocus = 0;
        lastKeyPressCode = undefined;

        if (!config.mouseDownOnSelect) {

            clearTimeout(timeout);

            timeout = setTimeout(function() {

                var currentResult = $input.val();

                hideResultsNow();

                if ((options.mustMatch || options.autoFill ||
                        options.autoSelect) && !config.hasFocus &&
                        selectedResult != currentResult) {
                    // call search and run callback
                    $input.search(function(result) {
                        if (result) {
                            autoFill(currentResult, result);
                        } else if (options.mustMatch) {
                            $input.val("");
                            selectedResult = '';
                            $input.trigger("change");
                            $input.trigger("result", null);
                        }
                    });
                }

            }, 200);

        }
    }).bind('click', function() {
        // show select when clicking in a focused field
        if ((options.dropDownOnClick || config.hasFocus++ > 1) &&
                !select.visible() ) {
            onChange(0, true);
        }
    }).bind("search", function() {

        // TODO why not just specifying both arguments?

        var fn = (arguments.length > 1) ? arguments[1] : null;

        function findValueCallback(q, data) {

            var result,
                normalizedQ = $.trim(q.toLowerCase());

            for (var i = 0; data && i < data.length; i++) {
                if ($.trim(data[i].result.toLowerCase()) === normalizedQ) {
                    result = data[i];
                    break;
                }
            }

            fn(result);

        }

        request($.trim($input.val()), findValueCallback, findValueCallback);

    }).bind("flushCache", function() {
        cache.flush();
    }).bind("setOptions", function() {
        $.extend(options, arguments[1]);
        // if we've updated the data, repopulate
        if ( "data" in arguments[1] ) {
            cache.populate();
            if (select.visible()) {
                select.emptyList();
                select.addItems(cache.load(curTerm));
            }
        }
    }).bind("unautocomplete", function() {

        if (options.button) {
            $button.remove();
        }

        select.unbind();
        $input.unbind();

        $(input.form).unbind(".autocomplete");

        $(window).unbind('resize', hideIfVisible);

    }).bind("showList", function() {

        clearTimeout(timeout);

        timeout = setTimeout(function() {
            $input.focus();
            $input.scrollLeft(0);
            request('', receiveData, hideResultsNow);
        }, 1);

    }).bind("endReached", function() {
        if (options.flexible) {
            getNextItems();
        }
    }).bind("scrollToOption", function(event, optionValue) {
        select.scrollToOption(optionValue);
    });

    $(window).bind('resize', hideIfVisible);

    function hideIfVisible() {
        if(select.visible()) {
            hideResultsNow();
        }
    }

    function abortAjax() {
        if (jqxhr) {
            jqxhr.abort();
            jqxhr = null;
        }
    }

    function getNextItems() {

        var handler = options.queryGenerator,
            query = prevTrans.query ? handler(prevTrans.response, curTerm) : undefined;

        if (!query) {
            return ;
        }

        abortAjax();

        select.splash(true);
        splash(true);

        $.extend(prevTrans, {
            response: undefined,
            query: query
        });

        jqxhr = $.ajax({
            cache: false,
            traditional: options.traditional,
            dataType: options.dataType,
            url: options.url,
            data: query,
            success: function(data) {
                var parsed = options.parse && options.parse(data) || parse(data);
                prevTrans.response = data;
                select.addItems(parsed);
            },
            complete: function() {
                jqxhr = null;
                select.splash(false);
                splash(false);
            }
        });

    }

    function selectCurrent() {

        var selected = select.selected();

        if( !selected ) {
            return false;
        }

        previousResult = selectedResult = selected.result;

        $input.val(selected.result);

        hideResultsNow();

        $input.trigger("change");
        $input.trigger("result", [selected.data, selected.value]);

        return true;

    }

    function onChange(crap, skipPrevCheck) {

        if( lastKeyPressCode == KEY.DEL ) {
            select.hide();
            return;
        }

        var currentResult = $input.val();

        if (!skipPrevCheck && currentResult == previousResult) {
            return;
        }

        previousResult = currentResult;

        if (skipPrevCheck && options.data) {
            request('', receiveData, hideResultsNow);
        } else {
            if (currentResult.length >= options.minChars) {
                if (!options.matchCase) {
                    currentResult = currentResult.toLowerCase();
                }
                request(currentResult, receiveData, hideResultsNow);
            } else {
                select.hide();
            }
        }

    };

    // fills in the input box w/the first match (assumed to be the best match)
    // q: the term entered
    // firstRresult: the first matching result
    function autoFill(q, firstMatch){
        // autofill in the complete box w/the first match as long as the user hasn't entered in more data
        // if the last user key pressed was backspace, don't autofill
        var fResult = firstMatch.result;
        if (($input.val().toLowerCase() == q.toLowerCase()) &&
                lastKeyPressCode != KEY.BACKSPACE) {
            // fill in the value (keep the case the user has typed)
            if (options.keepUserCase) {
                $input.val($input.val() + fResult.substring(previousResult.length));
            } else {
                $input.val(fResult);
            }
            // select the portion of the value not typed by the user (so the next character will erase)
            if (config.hasFocus) {
                $input.selection(previousResult.length, previousResult.length + fResult.length);
            }
            selectedResult = previousResult = $input.val();
            $input.trigger("change");
            $input.trigger("result", [firstMatch.data, fResult]);
        }
    };

    function hideResultsNow() {
        select.hide();
        clearTimeout(timeout);
        abortAjax();
    };

    function receiveData(q, data) {
        if ( data && data.length && config.hasFocus ) {
            select.hide();
            select.display(data, q);
            if (options.autoFill) {
                autoFill(q, data[0]);
            }
            select.show();
        } else {
            hideResultsNow();
        }
    };

    function request(term, success, failure) {

        prevTrans = {};
        curTerm = term;

        if (!options.matchCase)
            term = term.toLowerCase();

        var data = cache.load(term),
            responseParser = function(data) {
                return options.parse && options.parse(data) || parse(data);
            },
            query;

        // receive the cached data
        if (data && data.length) {
            success(term, data);
        } else if (typeof options.data == "function") {
            splash(true);
            options.data(term, function(data) {
                // cache.add(term, data);
                success(term, data);
                splash(false);
            });
        // if an AJAX url has been supplied, try loading the data now
        } else if( (typeof options.url == "string") && (options.url.length > 0) ){

            query = {};

            if (options.queryGenerator) {
                $.extend(query, options.queryGenerator(undefined, term));
            } else {
                $.each(options.extraParams, function(key, param) {
                    query[key] = typeof param == "function" ? param() : param;
                });
                $.extend(query, {
                    query: term,
                    limit: options.max
                });
            }

            if (prevTrans && prevTrans.response &&
                $.param(prevTrans.query) === $.param(query)) {
                success(term, responseParser(prevTrans.response));
            } else {

                abortAjax();

                splash(true);

                prevTrans.query = query;

                jqxhr = $.ajax({
                    cache: false,
                    traditional: options.traditional,
                    dataType: options.dataType,
                    url: options.url,
                    data: query,
                    success: function(data) {
                        var parsed = responseParser(data);
                        prevTrans.response = data;
                        // cache.add(term, parsed);
                        success(term, parsed);
                    },
                    complete: function() {
                        jqxhr = null;
                        splash(false);
                    }
                });

            }

        } else {
            // if we have a failure, we need to empty the list -- this prevents the the [TAB] key from selecting the last successful match
            select.emptyList();
            failure(term);
        }
    };

    function parse(data) {
        var parsed = [];
        var rows = data.split("\n");
        for (var i=0; i < rows.length; i++) {
            var row = $.trim(rows[i]);
            if (row) {
                row = row.split("|");
                parsed[parsed.length] = {
                    data: row,
                    value: row[0],
                    result: options.formatResult && options.formatResult(row, row[0]) || row[0]
                };
            }
        }
        return parsed;
    };

    function splash(isVisible) {
        $input[ isVisible ? 'addClass' : 'removeClass' ](options.loadingClass);
    };

};

$.extend($.Autocompleter, constants, {

    defaults: {
        fixed: false,
        isKbNavEnabled: true,
        traditional: false,
        position: constants.TB_POSITION,
        inputClass: "ac_input",
        resultsClass: "ac_results",
        loadingClass: "ac_loading",
        keepUserCase: true,
        minChars: 1,
        delay: 400,
        matchCase: false,
        matchSubset: true,
        matchContains: false,
        cacheLength: 10,
        max: 100,
        mustMatch: false,
        extraParams: {},
        queryGenerator: null,
        formatItem: function(row) { return row[0]; },
        formatMatch: null,
        autoFill: false,
        autoSelect: false,
        width: 0,
        flexible: false,
        multipleSeparator: ", ",
        highlight: function(value, term) {
            return value.replace(new RegExp("(?![^&;]+;)(?!<[^<>]*)(" + term.replace(/([\^\$\(\)\[\]\{\}\*\.\+\?\|\\])/gi, "\\$1") + ")(?![^<>]*>)(?![^&;]+;)", "gi"), "<strong>$1</strong>");
        },
        scroll: true,
        scrollHeight: 180,
        offsetLeft: 0,
        offsetTop: 0,
        button: false,
        dropDownOnClick: false,
        emptyItem: null
    },

    Cache: function(options) {

        var data = {};
        var length = 0;

        function matchSubset(s, sub) {
            if (!options.matchCase)
                s = s.toLowerCase();
            var i = s.indexOf(sub);
            if (options.matchContains == "word"){
                i = s.toLowerCase().search("\\b" + sub.toLowerCase());
            }
            if (i == -1) return false;
            return i == 0 || options.matchContains;
        };

        function add(q, value) {
            if (length > options.cacheLength){
                flush();
            }
            if (!data[q]){
                length++;
            }
            data[q] = value;
        }

        function populate(){
            if( !options.data ) return false;
            // track the matches
            var stMatchSets = {},
                nullData = 0;

            // no url was specified, we need to adjust the cache length to make sure it fits the local data store
            if( !options.url ) options.cacheLength = 1;

            // track all options for minChars = 0
            stMatchSets[""] = [];

            // loop through the array and create a lookup structure
            for ( var i = 0, ol = options.data.length; i < ol; i++ ) {
                var rawValue = options.data[i];
                // if rawValue is a string, make an array otherwise just reference the array
                rawValue = (typeof rawValue == "string") ? [rawValue] : rawValue;

                var value = options.formatMatch(rawValue, i+1, options.data.length);
                if ( value === false )
                    continue;

                var firstChar = value.charAt(0).toLowerCase();
                // if no lookup array for this character exists, look it up now
                if( !stMatchSets[firstChar] )
                    stMatchSets[firstChar] = [];

                // if the match is a string
                var row = {
                    value: value,
                    data: rawValue,
                    result: options.formatResult && options.formatResult(rawValue) || value
                };

                // push the current match into the set list
                stMatchSets[firstChar].push(row);

                // keep track of minChars zero items
                if ( nullData++ < options.max ) {
                    stMatchSets[""].push(row);
                }
            };

            // add the data items to the cache
            $.each(stMatchSets, function(i, value) {
                // increase the cache size
                options.cacheLength++;
                // add to the cache
                add(i, value);
            });
        }

        // populate any existing data
        setTimeout(populate, 25);

        function flush(){
            data = {};
            length = 0;
        }

        return {
            flush: flush,
            add: add,
            populate: populate,
            load: function(q) {
                if (!options.cacheLength || !length)
                    return null;
                /*
                 * if dealing w/local data and matchContains than we must make sure
                 * to loop through all the data collections looking for matches
                 */
                if( !options.url && options.matchContains ){
                    // track all matches
                    var csub = [];
                    // loop through all the data grids for matches
                    for( var k in data ){
                        // don't search through the stMatchSets[""] (minChars: 0) cache
                        // this prevents duplicates
                        if( k.length > 0 ){
                            var c = data[k];
                            $.each(c, function(i, x) {
                                // if we've got a match, add it to the array
                                if (matchSubset(x.value, q)) {
                                    csub.push(x);
                                }
                            });
                        }
                    }
                    return csub;
                } else
                // if the exact item exists, use it
                if (data[q]){
                    return data[q];
                } else
                if (options.matchSubset) {
                    for (var i = q.length - 1; i >= options.minChars; i--) {
                        var c = data[q.substr(0, i)];
                        if (c) {
                            var csub = [];
                            $.each(c, function(i, x) {
                                if (matchSubset(x.value, q)) {
                                    csub[csub.length] = x;
                                }
                            });
                            return csub;
                        }
                    }
                }
                return null;
            }
        };
    },

    Select: function (options, input, select, config) {

        var CLASSES = {
            ACTIVE: "ac_over"
        };

        var

            $listItems,
            listHeight = 0,
            active = -1,
            term = "",
            isEndReached = false,
            needsInit = true,
            curMenuHeight = 0,
            curMenuWidth = 0,
            curMenuOffset = 0,

            $element,
            $splash,
            $list,
            $window = $(window),
            $input = $(input);

        // Create results
        function init() {

            if (!needsInit) {
                return;
            }

            needsInit = false;

            $element = $("<div/>");
            $element
                .hide()
                .css("position", options.fixed ? "fixed": "absolute")
                .addClass(options.resultsClass)
                .appendTo(document.body);

            $list = $("<ul/>").appendTo($element).mouseover( function(event) {

                var targetEl = target(event),
                    $target = $(targetEl);

                if(targetEl.nodeName && targetEl.nodeName.toUpperCase() == 'LI' &&
                   $target.attr('class') != 'splash') {
                    active = $("li", $list).removeClass(CLASSES.ACTIVE).index(targetEl);
                    $target.addClass(CLASSES.ACTIVE);
                }

            }).click(function(event) {
                $(target(event)).addClass(CLASSES.ACTIVE);
                select();
                // TODO provide option to avoid setting focus again after selection? useful for cleanup-on-focus
                input.focus();
                return false;
            }).mousedown(function() {
                config.mouseDownOnSelect = true;
                setTimeout(function() {
                    config.mouseDownOnSelect = false;
                    if (config.hasFocus == 0) {
                        input.focus();
                    }
                }, 1);
                return false;
            });

            if (options.flexible) {
                $list.scroll(function() {
                    if (!isEndReached && $list.scrollTop() > getItemsBottom()) {
                        onListEndReached();
                    }
                });
            }

            if( options.width > 0 ) {
                $element.css("width", options.width);
            }

        }

        function getMenuWidth() {
            return typeof options.width == "string" || options.width > 0 ?
                   options.width : $input.outerWidth();
        }

        function getItemsBottom() {
            return $list[0].scrollHeight - curMenuHeight -
                   $listItems.last().outerHeight(true);
        }

        function visible() {
            return $element && $element.is(":visible");
        }

        function onListEndReached() {
            isEndReached = true;
            $input.trigger('endReached');
        }

        function target(event) {
            var element = event.target;
            while(element && element.tagName != "LI")
                element = element.parentNode;
            // more fun with IE, sometimes event.target is empty, just ignore it then
            if(!element)
                return [];
            return element;
        }

        function moveSelect(step) {
            $listItems.slice(active, active + 1).removeClass(CLASSES.ACTIVE);
            movePosition(step);
            var activeItem = $listItems.slice(active, active + 1).addClass(CLASSES.ACTIVE);
            if(options.scroll) {
                var offset = 0;
                $listItems.slice(0, active).each(function() {
                    offset += this.offsetHeight;
                });
                if((offset + activeItem[0].offsetHeight - $list.scrollTop()) > $list[0].clientHeight) {
                    $list.scrollTop(offset + activeItem[0].offsetHeight - $list.innerHeight());
                } else if(offset < $list.scrollTop()) {
                    $list.scrollTop(offset);
                }
            }
        };

        function movePosition(step) {
            active += step;
            if (active < 0) {
                active = 0;
            } else if (active >= $listItems.size()) {
                active = $listItems.size() - 1;
            }
        }

        function limitNumberOfItems(available) {
            return options.max && options.max < available ? options.max : available;
        }

        function splash(isVisible) {

            var padding = 30;

            if (!$list) {
                return ;
            }

            if (isVisible) {
                if (!$splash) {
                    $list.css({'overflow': 'auto'});
                    $splash = $('<li></li>');
                    $splash.addClass('splash');
                    $list.append($splash);
                }
            } else {
                $splash.remove();
                $splash = null;
            }

        }

        function addItems(data) {

            var max = limitNumberOfItems(data.length),
                offset = $list.find("li.ac_even, li.ac_odd").length,
                inputVal = $input.val(),
                formatted;

            isEndReached = false;

            for (var i = 0; i < max; i++) {

                if (!data[i]) {
                    continue;
                }

                formatted = options.formatItem(data[i].data, i+1, max,
                                               data[i].value, term);
                if ( formatted === false ) {
                    continue;
                }

                addFormattedItem(
                    options.highlight(formatted, inputVal), data[i],
                    (offset++ % 2 == 0 ? "ac_even" : "ac_odd"));

            }

            $listItems = $list.find("li");

            // apply bgiframe if available
            if ( $.fn.bgiframe ) {
                $list.bgiframe();
            }

        }

        function addEmptyItem() {

            var emptyItem = options.emptyItem;

            if (emptyItem === true) {
                emptyItem = '\u2014';
            }

            addFormattedItem(
                emptyItem,
                {
                    data: null,
                    value: '',
                    result: ''
                },
                'ac_even'
            );
        }

        function addFormattedItem(formattedItem, itemData, cssClass) {
            $("<li/>").html(formattedItem)
                      .addClass(cssClass)
                      .data("ac_data", itemData)
                      .appendTo($list);
        }

        function resizeMenu() {

            var left,
                top,
                wScrollLeft = $window.scrollLeft(),
                wScrollTop = $window.scrollTop() + constants.WINDOW_PADDING / 2,
                wWidth = $window.width(),
                wHeight = $window.height() - constants.WINDOW_PADDING,
                lastWindowX = wScrollLeft + wWidth,
                lastWindowY = wScrollTop + wHeight,
                maxHeight,
                offset = $input.offset(),
                position;

            if (options.flexible) {
                if (options.position == constants.LR_POSITION) {
                    maxHeight = wHeight;
                } else {
                    maxHeight = Math.max(
                        offset.top - wScrollTop,
                        wScrollTop + wHeight -
                        offset.top -
                        (
                            options.position == constants.TB_POSITION ?
                            $input.outerHeight() : 0
                        )
                    );
                }
                curMenuHeight = Math.min(listHeight, maxHeight);
            } else {
                curMenuHeight = Math.min(listHeight, options.scrollHeight);
            }

            curMenuWidth = getMenuWidth();

            $element.css({ 'min-width': getMenuWidth() + 'px' });
            $list.css({ 'max-height': curMenuHeight + 'px' });

            if(options.scroll && curMenuHeight < listHeight) {

                $list.css({ 'overflow': 'auto' });

            } else {

                $list.css({ 'overflow': 'visible' });
                if (options.flexible && !isEndReached) {
                    onListEndReached();
                }
            }

            if (options.position == constants.LR_POSITION) {

                left = offset.left + input.offsetWidth;
                top = offset.top + Math.floor($input.outerHeight() / 2);
                top -= Math.floor(curMenuHeight / 2);

                if (top < wScrollTop) {
                    top = wScrollTop;
                } else if (top + curMenuHeight > wScrollTop + wHeight) {
                    top = wScrollTop + wHeight - curMenuHeight;
                }

                if (left + curMenuWidth > lastWindowX &&
                    lastWindowX - left < offset.left - wScrollLeft) {
                    left = offset.left - curMenuWidth;
                }

            } else if (options.position == constants.TB_POSITION) {

                top = offset.top + input.offsetHeight;
                left = offset.left;

                if (top + curMenuHeight > lastWindowY &&
                    lastWindowY - top < offset.top - wScrollTop) {
                    top = offset.top - curMenuHeight;
                }

            } else if (options.position == constants.CR_POSITION) {
                top = offset.top + $input.getCaretPosition().top + 20;
                left = offset.left;
            } else {
                throw new Error("Unknown position type: " + options.position);
            }

            if (options.fixed) {
                top -= wScrollTop;
                left -= wScrollLeft;
            }

            top += options.offsetTop;
            left += options.offsetLeft;

            $element.css({ left: left, top: top });
            curMenuOffset = { left: left - offset.left,
                              top: top - offset.top };

        }

        return {

            splash: splash,

            display: function(d, q) {

                term = q;
                init();
                $list.empty();

                if (options.emptyItem != null) {
                    addEmptyItem();
                }

                addItems(d);

            },

            addItems: function(d) {
                addItems(d);
            },

            next: function() {
                moveSelect(1);
            },
            prev: function() {
                moveSelect(-1);
            },
            pageUp: function() {
                if (active != 0 && active - 8 < 0) {
                    moveSelect( -active );
                } else {
                    moveSelect(-8);
                }
            },
            pageDown: function() {
                if (active != $listItems.size() - 1 && active + 8 > $listItems.size()) {
                    moveSelect( $listItems.size() - 1 - active );
                } else {
                    moveSelect(8);
                }
            },
            hide: function() {
                $element && $element.hide();
                $listItems && $listItems.removeClass(CLASSES.ACTIVE);
                active = -1;
            },
            visible: visible,
            show: function() {

                $element.css({ 'min-width': getMenuWidth(),
                               'top': '-10000px',
                               'left': '-10000px' });
                $list.css({ 'max-height': 'none',
                            'overflow': 'visible'  });
                $element.show();

                listHeight = $element.outerHeight(true);
                $element.hide();

                isEndReached = false;
                $list.scrollTop(0);

                resizeMenu();

                $element.show();

                $input.trigger('listShown');

            },
            selected: function() {
                var selected = $listItems && $listItems.filter("." + CLASSES.ACTIVE).removeClass(CLASSES.ACTIVE);
                return selected && selected.length && $.data(selected[0], "ac_data");
            },
            scrollToOption: function(optionValue) {
                $list.scrollTo(
                    $list.find('li').filter(function () {
                        return $(this).data('ac_data').value == optionValue;
                    })
                );
            },
            emptyList: function (){
                $list && $list.empty();
            },
            unbind: function() {
                if(!needsInit) {
                    $element.remove();
                }
            }
        };
    }

});

$.fn.selection = function(start, end) {
    if (start !== undefined) {
        return this.each(function() {
            if( this.createTextRange ){
                var selRange = this.createTextRange();
                if (end === undefined || start == end) {
                    selRange.move("character", start);
                    selRange.select();
                } else {
                    selRange.collapse(true);
                    selRange.moveStart("character", start);
                    selRange.moveEnd("character", end);
                    selRange.select();
                }
            } else if( this.setSelectionRange ){
                this.setSelectionRange(start, end);
            } else if( this.selectionStart ){
                this.selectionStart = start;
                this.selectionEnd = end;
            }
        });
    }
    var field = this[0];
    if ( field.createTextRange ) {
        var range = document.selection.createRange(),
            orig = field.value,
            teststring = "<->",
            textLength = range.text.length;
        range.text = teststring;
        var caretAt = field.value.indexOf(teststring);
        field.value = orig;
        this.selection(caretAt, caretAt + textLength);
        return {
            start: caretAt,
            end: caretAt + textLength
        }
    } else if( field.selectionStart !== undefined ){
        return {
            start: field.selectionStart,
            end: field.selectionEnd
        }
    }
};

})(jQuery);
