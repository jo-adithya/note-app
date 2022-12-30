import { initSelectInput } from './helper.js';

const actionButtons = jQuery.makeArray($('.btn-action'));
const advanceButtons = jQuery.makeArray($('.btn-advance'));
const fontFamilySelector = $('#fontName')[0];
const fontSizeSelector = $('#fontSize')[0];

const fontFamilies = [
  'Poppins',
  'Verdana',
  'Georgia',
  'Courier New',
  'cursive',
];

const fontSizes = [10, 13, 16, 18, 24, 32, 48];

const init = (() => {
  initSelectInput(fontFamilySelector, fontFamilies);
  initSelectInput(
    fontSizeSelector,
    fontSizes,
    Array.from({ length: 7 }, (v, k) => k + 1),
    3
  );
})();

actionButtons.forEach((button) => {
  $(button).click(() => {
    document.execCommand(button.id, false, null);
  });
});

advanceButtons.forEach((button) => {
  $(button).change(() => {
    console.log(button.id, false, button.value);
    document.execCommand(button.id, false, button.value);
  });
});
