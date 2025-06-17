// Animation on scroll function
document.addEventListener('DOMContentLoaded', function() {
  const animatedElements = document.querySelectorAll('[data-aos]');
  
  // Configuration de l'Intersection Observer
  const options = {
    root: null, // viewport
    threshold: 0.1, // 10% de l'élément visible
    rootMargin: '0px 0px -10% 0px' // déclencher un peu avant que l'élément soit complètement visible
  };
  
  // Callback exécuté lorsqu'un élément entre dans le viewport
  const handleIntersection = (entries, observer) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('aos-animate');
        observer.unobserve(entry.target); // arrêter d'observer une fois l'animation déclenchée
      }
    });
  };
  
  // Créer l'observer
  const observer = new IntersectionObserver(handleIntersection, options);
  
  // Observer chaque élément avec l'attribut data-aos
  animatedElements.forEach(element => {
    observer.observe(element);
  });
  
  // Appliquer l'animation immédiatement pour les éléments déjà visibles
  setTimeout(() => {
    // Animer tous les éléments visibles dans le viewport
    animatedElements.forEach(el => {
      const rect = el.getBoundingClientRect();
      const isVisible = (
        rect.top <= (window.innerHeight || document.documentElement.clientHeight) &&
        rect.bottom >= 0
      );
      
      if (isVisible) {
        el.classList.add('aos-animate');
      }
    });
  }, 200); // un délai légèrement plus long pour garantir que le DOM est prêt
});
