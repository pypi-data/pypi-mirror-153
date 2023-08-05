var locale

function setLocale() {
  var locale_name = $(document.body).data('locale')
  locale = 'BABEL_TO_LOAD_'+locale_name
}

function t(word) {
  if ( window[locale] != undefined) {
    var translation = window[locale].messages[word]
    if (translation == undefined)
      translation = word;
  } else
    translation = word;
  return translation
}
