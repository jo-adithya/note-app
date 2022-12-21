const mainColor = '#536DFE';
const grey = '#CCC';

$('.form-group input').focus(function (e) {
  let group = $(this).parent().parent();
  let placeholder = $(this).parent().children().first();

  group.css('border-color', mainColor);
  group.children().first().css({ color: mainColor });

  placeholder.css({
    fontSize: '0.7rem',
    color: mainColor,
    transform: 'translate(5px, -15px)',
  });
});

$('.form-group input').blur(function (e) {
  let group = $(this).parent().parent();
  let placeholder = $(this).parent().children().first();

  group.css('border-color', grey);
  group.children().first().css('color', grey);

  let style = { color: grey };
  if (!$(this).val())
    style = { ...style, fontSize: '1rem', transform: 'translate(5px, 8px)' };

  placeholder.css(style);
});
