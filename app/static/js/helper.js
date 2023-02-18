export const initSelectInput = (element, options, values, defaultValue) => {
  if (!values) values = options;

  console.log(options, values);

  if (options.length !== values.length) return;

  for (let i = 0, n = options.length; i < n; i++) {
    let option = document.createElement('option');
    option.value = values[i];
    option.innerHTML = options[i];
    element.appendChild(option);
  }

  element.value = defaultValue || values[0];
}