
try {
    new Function("import('/reactfiles/frontend/main-4b1ba1ae.js')")();
} catch (err) {
    var el = document.createElement('script');
    el.src = '/reactfiles/frontend/main-4b1ba1ae.js';
    el.type = 'module';
    document.body.appendChild(el);
}
