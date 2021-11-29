$('.form-group input').focus(function(e) {
    let group = $(this).parent().parent();
    let placeholder = $(this).parent().children().first();

    group.css({borderBottom: "1px solid #536DFE"});
    group.children().first().css('color', '#536DFE');

    placeholder.css("color", "#536DFE").animate({fontSize: "0.7rem", translateY: "-120%"}, "fast");
})

$('.form-group input').blur(function(e) {
    let group = $(this).parent().parent();
    group.css("border-color", "#ccc");
    group.children().first().css('color', '#ccc');
})
