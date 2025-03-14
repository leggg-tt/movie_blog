// Add smooth scrolling effect for anchor links
document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();

            const targetElement = document.querySelector(this.getAttribute('href'));
            if (targetElement) {
                targetElement.scrollIntoView({
                    behavior: 'smooth'
                });
            }
        });
    });

    // Add animation to blog cards when they come into view
    const blogCards = document.querySelectorAll('.blog-card');

    if ('IntersectionObserver' in window) {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('animated');
                    observer.unobserve(entry.target);
                }
            });
        }, { threshold: 0.1 });

        blogCards.forEach(card => {
            observer.observe(card);
        });
    } else {
        // Fallback for browsers without IntersectionObserver
        blogCards.forEach(card => {
            card.classList.add('animated');
        });
    }
});