var TelMaskBehavior = function (val) {
  return val.replace(/\D/g, '').length === 11 ? '(00) 00000-0000' : '(00) 0000-00009';
},
spOptions = {
  onKeyPress: function(val, e, field, options) {
      field.mask(TelMaskBehavior.apply({}, arguments), options);
    }
};


$(document).ready(function(){
            $('.datemask').mask('00/00/0000');
            $('.moneymask').mask("#.##0,00", {reverse: true});
            $('.cnpjmask').mask('00.000.000/0000-00');
            $('.cpfmask').mask('000.000.000-00');
            $('.cepmask').mask('00000-000');
            $('.contrmask').mask('0000/0000');
            $('.telmask').mask(TelMaskBehavior, spOptions);
        });

