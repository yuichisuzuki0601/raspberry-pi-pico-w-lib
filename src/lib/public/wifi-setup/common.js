const $ = (q) => document.querySelector(`${q}`);
const getValue = (q) => $(`${q}`).value;
const setValue = (q, value) => ($(`${q}`).value = value);
