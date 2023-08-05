
RangeSlider = function (params) {
    var $inputFrom = params.$inputFrom,
        $inputTo = params.$inputTo,
        $rangeInput = params.$rangeInput,
        min = parseFloat(params.$inputFrom.prop('min')),
        max = parseFloat(params.$inputTo.prop('max')),
        lastVal = [min, max];

    function handleRangeInputChange () {
        var val = $rangeInput.slider('getValue');

        if (val[0] !== lastVal[0]) {
            $inputFrom.val(val[0]);
        }

        if (val[1] !== lastVal[1]) {
            $inputTo.val(val[1]);
        }

        lastVal = val;
    }

    function handleTextInputChange() {
        $rangeInput.slider('setValue', [
            Number($inputFrom.val()),
            Number($inputTo.val())
        ]);
    }
    
    $rangeInput.slider({
        range: true,
        tooltip: 'hide',
        min: min,
        max: max,
        step: params.step || 10
    });

    $rangeInput.change(handleRangeInputChange);

    $inputFrom.keyup(handleTextInputChange);

    $inputTo.keyup(handleTextInputChange);
    
    handleTextInputChange();
};
