(function () {
    // Логгер
    function log(msg, data = null) {
        console.warn('[SECURITY LOG]', msg, data || '');
    }

    // Отслеживание внешних скриптов
    const originalScript = document.createElement;
    document.createElement = function (tag) {
        const el = originalScript.call(document, tag);
        if (tag.toLowerCase() === 'script') {
            const setSrc = Object.getOwnPropertyDescriptor(HTMLScriptElement.prototype, 'src').set;
            Object.defineProperty(el, 'src', {
                set(value) {
                    log('Внешний скрипт добавлен:', value);
                    setSrc.call(this, value);
                },
                get() {
                    return this.getAttribute('src');
                },
                configurable: true
            });
        }
        return el;
    };

    // Отслеживание eval / Function
    window.eval = new Proxy(eval, {
        apply(target, thisArg, args) {
            log('Вызов eval:', args[0]);
            return target.apply(thisArg, args);
        }
    });

    window.Function = new Proxy(Function, {
        construct(target, args) {
            log('Вызов new Function:', args.join(' '));
            return new target(...args);
        }
    });

    // Элементы audio/video/iframe
    const tagsToWatch = ['audio', 'video', 'iframe'];
    const observer = new MutationObserver(mutations => {
        for (const m of mutations) {
            m.addedNodes.forEach(node => {
                if (node.tagName && tagsToWatch.includes(node.tagName.toLowerCase())) {
                    log(`Добавлен <${node.tagName.toLowerCase()}>:`, node.src || node.outerHTML);
                }
            });
        }
    });
    observer.observe(document.documentElement, {childList: true, subtree: true});

    // Перехват редиректов
    const originalLocationAssign = window.location.assign;
    window.location.assign = function (url) {
        log('Переход через location.assign:', url);
        return originalLocationAssign.call(this, url);
    };

    // Клики на подозрительные ссылки
    document.addEventListener('click', e => {
        const a = e.target.closest('a');
        if (a && a.href && !a.href.startsWith(location.origin)) {
            log('Клик по внешней ссылке:', a.href);
        }
    });

})();