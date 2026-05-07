(() => {
    const btn = document.getElementById('backToTop');
    if (!btn) return;

    btn.addEventListener('click', () => {
        window.scrollTo({ top: 0, behavior: 'smooth' });
    });

    const update = () => {
        btn.classList.toggle('show', window.scrollY > 600);
    };

    window.addEventListener('scroll', update, { passive: true });
    update();
})();

