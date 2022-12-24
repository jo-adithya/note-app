const mainColor = '#536DFE';
const grey = '#999';

$('.form-group input').focus(function (e) {
  let group = $(this).parent().parent();
  let placeholder = $(this).parent().children().first();

  group.css('border-color', mainColor);
  group.children().first().css({ color: mainColor });

  placeholder.css({
    fontSize: '0.7rem',
    color: mainColor,
    transform: 'translate(5px, -12px)',
  });
});

$('.form-group input').blur(function (e) {
  let group = $(this).parent().parent();
  let placeholder = $(this).parent().children().first();

  group.css('border-color', grey);
  group.children().first().css('color', grey);

  let style = { color: grey };
  if (!$(this).val())
    style = { ...style, fontSize: 'inherit', transform: 'translate(5px, 8px)' };

  placeholder.css(style);
});

$('.alert > .btn-close').click((e) => {
  let alert = $('.alert');
  alert.fadeOut();
})
