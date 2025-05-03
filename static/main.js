const cards = document.querySelectorAll('.card')
const cardObserver = new IntersectionObserver(entries => {
	entries.forEach(entry => {
		if (entry.isIntersecting) {
    		entry.target.style.transition = 'all 1s ease-out';
            entry.target.style.opacity = '1';
            entry.target.style.transform = 'translateY(0)';
        }
	})
})

cards.forEach(card => {
    card.style.opacity = '0';
    card.style.transform = 'translateY(20em)';
    cardObserver.observe(card);
});

const tbody = document.querySelector('tbody')

Array.from(tbody.children).forEach(item => {
	item.style.transformOrigin = 'center center';
	item.style.transform = 'rotateX(180deg)';
	item.style.setProperty('opacity', '0');
})

setTimeout(() => {
	Array.from(tbody.children).forEach((item, i) => {
		item.style.transition = 'all 0.5s ease-out';
		item.style.transitionDelay = `${i * 100}ms`;
		item.style.setProperty('opacity', '1')
    	item.style.setProperty('transform', 'rotateX(0deg)');
	})
}, 100);
